"""Triage cases: a lightweight incident / engagement workspace.

A case bundles together the kind of work a blue- or red-team analyst does
during triage: a checklist mapped to the NIST CSF functions, free-form
notes, and a Markdown report export. Cases are stored as plain JSON files
so they are easy to diff, share and keep in version control.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .models import CSF_FUNCTIONS

# Default home for saved cases. Override with NETGUARDIAN_HOME.
import os

CASES_DIR = Path(os.environ.get("NETGUARDIAN_HOME", Path.home() / ".netguardian")) / "cases"

# Starter checklists keyed by case kind, each item tagged with a CSF function.
# These are deliberately short; teams are expected to adapt them.
CHECKLIST_TEMPLATES: dict[str, list[tuple[str, str]]] = {
    "incident": [
        ("GV", "Confirm scope and assign an incident owner"),
        ("ID", "Identify affected assets, accounts and data"),
        ("DE", "Collect and preserve logs and relevant artifacts"),
        ("RS", "Contain the threat (isolate hosts, disable accounts)"),
        ("RS", "Investigate root cause and map to MITRE ATT&CK"),
        ("RS", "Eradicate: remove persistence and malicious artifacts"),
        ("RC", "Recover and validate affected systems"),
        ("GV", "Write up timeline and lessons learned"),
    ],
    "pentest": [
        ("GV", "Confirm rules of engagement and written authorisation"),
        ("ID", "Passive reconnaissance and OSINT"),
        ("ID", "Active discovery: hosts, services, attack surface"),
        ("ID", "Vulnerability analysis"),
        ("ID", "Exploitation of in-scope findings"),
        ("ID", "Post-exploitation and impact assessment"),
        ("GV", "Document findings with severity and evidence"),
        ("GV", "Deliver report and remediation advice"),
    ],
}


@dataclass
class ChecklistItem:
    function: str
    text: str
    done: bool = False


@dataclass
class Note:
    timestamp: str
    text: str


@dataclass
class Case:
    name: str
    kind: str  # "incident" or "pentest"
    created: str = field(default_factory=lambda: _now())
    checklist: list[ChecklistItem] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)

    @classmethod
    def new(cls, name: str, kind: str) -> "Case":
        if kind not in CHECKLIST_TEMPLATES:
            raise ValueError(
                f"unknown case kind {kind!r}; expected one of "
                f"{list(CHECKLIST_TEMPLATES)}"
            )
        checklist = [
            ChecklistItem(function=fn, text=text)
            for fn, text in CHECKLIST_TEMPLATES[kind]
        ]
        return cls(name=name, kind=kind, checklist=checklist)

    def add_note(self, text: str) -> None:
        self.notes.append(Note(timestamp=_now(), text=text))

    @property
    def progress(self) -> tuple[int, int]:
        done = sum(1 for i in self.checklist if i.done)
        return done, len(self.checklist)

    # --- persistence ---------------------------------------------------
    @property
    def slug(self) -> str:
        return "".join(c if c.isalnum() else "-" for c in self.name.lower()).strip("-")

    def path(self, cases_dir: Path = CASES_DIR) -> Path:
        return cases_dir / f"{self.slug}.json"

    def save(self, cases_dir: Path = CASES_DIR) -> Path:
        cases_dir.mkdir(parents=True, exist_ok=True)
        p = self.path(cases_dir)
        p.write_text(json.dumps(asdict(self), indent=2))
        return p

    @classmethod
    def load(cls, path: Path) -> "Case":
        data = json.loads(Path(path).read_text())
        return cls(
            name=data["name"],
            kind=data["kind"],
            created=data.get("created", _now()),
            checklist=[ChecklistItem(**i) for i in data.get("checklist", [])],
            notes=[Note(**n) for n in data.get("notes", [])],
        )

    # --- export --------------------------------------------------------
    def to_markdown(self) -> str:
        done, total = self.progress
        lines = [
            f"# {self.name}",
            "",
            f"- **Type:** {self.kind}",
            f"- **Created:** {self.created}",
            f"- **Progress:** {done}/{total} steps complete",
            "",
            "## Checklist",
            "",
        ]
        for fn in CSF_FUNCTIONS:
            items = [i for i in self.checklist if i.function == fn]
            if not items:
                continue
            lines.append(f"### {fn} — {CSF_FUNCTIONS[fn]}")
            for item in items:
                box = "x" if item.done else " "
                lines.append(f"- [{box}] {item.text}")
            lines.append("")
        if self.notes:
            lines += ["## Notes", ""]
            for note in self.notes:
                lines.append(f"- **{note.timestamp}** — {note.text}")
            lines.append("")
        return "\n".join(lines)


def list_cases(cases_dir: Path = CASES_DIR) -> list[Path]:
    if not cases_dir.exists():
        return []
    return sorted(cases_dir.glob("*.json"))


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
