#!/usr/bin/env python3
"""Check that every URL in the NetGuardian catalog is reachable.

Run locally or in CI:

    python scripts/check_links.py

Exit code is non-zero if any link looks dead. Hosts that answer with an
access-control status (401/403/429) are reported as warnings, not failures,
because some project sites block automated requests.
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from netguardian.loader import load_catalog  # noqa: E402

TIMEOUT = 20
UA = "Mozilla/5.0 (compatible; NetGuardian-linkcheck/1.0)"
# Statuses that mean "reachable but bot-blocked" — warn, don't fail.
SOFT = {401, 403, 429}


def check(url: str) -> tuple[str, int | None, str]:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return url, resp.status, "ok"
    except urllib.error.HTTPError as e:
        return url, e.code, "soft" if e.code in SOFT else "fail"
    except Exception as e:  # noqa: BLE001 - network errors of any kind
        return url, None, f"error: {e.__class__.__name__}"


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
