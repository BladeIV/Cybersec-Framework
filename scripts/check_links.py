#!/usr/bin/env python3
"""Check that every URL in the NetGuardian catalog is reachable.

Run locally or in CI:

    python scripts/check_links.py

Exit code is non-zero if any link looks dead. Hosts that answer with an
access-control status (401/403/429) are reported as warnings, not failures,
because some project sites block automated requests.

Because this job also runs on pull requests, where a contributor controls the
catalog URLs, it refuses non-http(s) schemes and never requests a URL (or a
redirect target) that resolves to a private, loopback, link-local or otherwise
non-public address. That keeps a malicious catalog entry from pointing the CI
runner at an internal service (SSRF). Transient network errors are retried a
couple of times so a blip doesn't fail the whole job.
"""
from __future__ import annotations

import ipaddress
import socket
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from netguardian.loader import load_catalog  # noqa: E402

TIMEOUT = 20
RETRIES = 2  # extra attempts after the first, for transient errors
UA = "Mozilla/5.0 (compatible; NetGuardian-linkcheck/1.0)"
# Statuses that mean "reachable but bot-blocked" — warn, don't fail.
SOFT = {401, 403, 429}
ALLOWED_SCHEMES = {"http", "https"}


def _host_is_public(host: str) -> bool:
    """True only if every address the host resolves to is globally routable."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = info[4][0]
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        if not addr.is_global or addr.is_multicast:
            return False
    return True


def _url_is_safe(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname:
        return False
    return _host_is_public(parsed.hostname)


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects to non-public destinations (SSRF guard)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _url_is_safe(newurl):
            raise urllib.error.URLError(f"blocked redirect to {newurl!r}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_GuardedRedirectHandler())


def check(url: str) -> tuple[str, int | None, str]:
    if not _url_is_safe(url):
        return url, None, "blocked (non-public or bad scheme)"

    last: tuple[str, int | None, str] = (url, None, "error: unknown")
    for attempt in range(RETRIES + 1):
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
        try:
            with _opener.open(req, timeout=TIMEOUT) as resp:
                return url, resp.status, "ok"
        except urllib.error.HTTPError as e:
            if e.code in SOFT:
                return url, e.code, "soft"
            if 500 <= e.code < 600:  # server error — may be transient
                last = (url, e.code, "fail")
            else:
                return url, e.code, "fail"
        except Exception as e:  # noqa: BLE001 - any network error
            last = (url, None, f"error: {e.__class__.__name__}")
        if attempt < RETRIES:
            time.sleep(2 * (attempt + 1))
    return last


def main() -> int:
    catalog = load_catalog()
    urls = sorted({t.url for t in catalog.iter_tools()})
    print(f"Checking {len(urls)} catalog links...\n")

    failures, warnings = [], []
    with ThreadPoolExecutor(max_workers=12) as pool:
        for url, status, kind in pool.map(check, urls):
            if kind == "ok":
                print(f"  OK   {status} {url}")
            elif kind == "soft":
                print(f"  WARN {status} {url} (blocks bots?)")
                warnings.append((url, status))
            else:
                print(f"  FAIL {status} {url} ({kind})")
                failures.append((url, status, kind))

    print(f"\n{len(urls)} checked · {len(failures)} failed · {len(warnings)} warnings")
    if failures:
        print("\nDead links:")
        for url, status, kind in failures:
            print(f"  - {url} ({status or kind})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
