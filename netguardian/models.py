"""Data models for the NetGuardian tool catalog.

The catalog is stored as YAML, one file per NIST CSF 2.0 function. These
dataclasses give the rest of the app a typed, validated view of that data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

# NIST CSF 2.0 functions, in their canonical order.
CSF_FUNCTIONS = {
    "GV": "Govern",
    "ID": "Identify",
    "PR": "Protect",
    "DE": "Detect",
    "RS": "Respond",
    "RC": "Recover",
}

VALID_TEAMS = {"red", "blue"}


@dataclass(frozen=True)
class Tool:
    name: str
    url: str
    description: str
    teams: tuple[str, ...]
    license: str
    cost: str
    platforms: tuple[str, ...] = ()
    command: str | None = None
    tags: tuple[str, ...] = ()
    # Back-references, filled in by the loader.
    function: str = ""
    category: str = ""

    @property
    def is_installed(self) -> bool:
        """True if the tool's CLI command is on PATH."""
        import shutil

        return bool(self.command) and shutil.which(self.command) is not None


@dataclass
class Category:
    name: str
    tools: list[Tool] = field(default_factory=list)


@dataclass
class Function:
    code: str
    name: str
    summary: str
    categories: list[Category] = field(default_factory=list)

    def iter_tools(self) -> Iterator[Tool]:
        for category in self.categories:
            yield from category.tools


@dataclass
class Catalog:
    functions: list[Function] = field(default_factory=list)

    def iter_tools(self) -> Iterator[Tool]:
        for function in self.functions:
            yield from function.iter_tools()

    def all_tags(self) -> list[str]:
        return sorted({tag for tool in self.iter_tools() for tag in tool.tags})

    def filter(
        self,
        *,
        team: str | None = None,
        query: str | None = None,
        free_only: bool = False,
        installed_only: bool = False,
    ) -> "Catalog":
        """Return a new catalog keeping only tools that match every filter.

        Empty functions and categories are dropped so the tree stays tidy.
        """
        q = (query or "").strip().lower()

        def keep(tool: Tool) -> bool:
            if team and team not in tool.teams:
                return False
            if free_only and tool.cost != "free":
                return False
            if installed_only and not tool.is_installed:
                return False
            if q:
                haystack = " ".join(
                    [
                        tool.name,
                        tool.description,
                        " ".join(tool.tags),
                        tool.category,
                        CSF_FUNCTIONS.get(tool.function, ""),
                    ]
                ).lower()
                if q not in haystack:
                    return False
            return True

        out: list[Function] = []
        for fn in self.functions:
            cats = []
            for cat in fn.categories:
                tools = [t for t in cat.tools if keep(t)]
                if tools:
                    cats.append(Category(name=cat.name, tools=tools))
            if cats:
                out.append(
                    Function(
                        code=fn.code, name=fn.name, summary=fn.summary, categories=cats
                    )
                )
        return Catalog(functions=out)
