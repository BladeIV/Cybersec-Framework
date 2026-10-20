"""Load and validate the YAML tool catalog."""
from __future__ import annotations

from pathlib import Path

import yaml

from .models import (
    CSF_FUNCTIONS,
    VALID_TEAMS,
    Catalog,
    Category,
    Function,
    Tool,
)

CATALOG_DIR = Path(__file__).parent / "catalog"

REQUIRED_TOOL_FIELDS = ("name", "url", "description", "teams", "license", "cost")


class CatalogError(ValueError):
    """Raised when a catalog file is malformed."""


def _parse_tool(raw: dict, *, function: str, category: str, where: str) -> Tool:
    missing = [f for f in REQUIRED_TOOL_FIELDS if f not in raw]
    if missing:
        raise CatalogError(f"{where}: tool missing fields {missing}: {raw!r}")

    _require_sequence(raw["teams"], "teams", raw["name"], where)
    teams = tuple(raw["teams"])
    if not teams:
        raise CatalogError(
            f"{where}: tool {raw['name']!r} must list at least one team "
            f"({sorted(VALID_TEAMS)})"
        )
    bad_teams = set(teams) - VALID_TEAMS
    if bad_teams:
        raise CatalogError(
            f"{where}: tool {raw['name']!r} has invalid team(s) {bad_teams}; "
            f"allowed: {sorted(VALID_TEAMS)}"
        )

    for field_name in ("platforms", "tags"):
        if field_name in raw:
            _require_sequence(raw[field_name], field_name, raw["name"], where)

    return Tool(
        name=raw["name"],
        url=raw["url"],
        description=raw["description"],
        teams=teams,
        license=raw["license"],
        cost=raw["cost"],
        platforms=tuple(raw.get("platforms", ())),
        command=raw.get("command"),
        tags=tuple(raw.get("tags", ())),
        function=function,
        category=category,
    )


def _require_sequence(value, field_name: str, tool_name: str, where: str) -> None:
    """Reject a scalar where a YAML list is expected.

    A string is iterable, so ``tuple("scanner")`` would silently become
    ``('s', 'c', ...)``. Catch that at load time instead.
    """
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise CatalogError(
            f"{where}: tool {tool_name!r} field {field_name!r} must be a list, "
            f"got {value!r}"
        )


def load_function(path: Path) -> Function:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise CatalogError(f"{path.name}: top level must be a mapping")

    code = data.get("function")
    if code not in CSF_FUNCTIONS:
        raise CatalogError(
            f"{path.name}: unknown function code {code!r}; "
            f"expected one of {list(CSF_FUNCTIONS)}"
        )

    categories = []
    for raw_cat in data.get("categories", []):
        cat_name = raw_cat["name"]
        tools = [
            _parse_tool(
                t, function=code, category=cat_name, where=f"{path.name}/{cat_name}"
            )
            for t in raw_cat.get("tools", [])
        ]
        categories.append(Category(name=cat_name, tools=tools))

    return Function(
        code=code,
        name=data.get("name", CSF_FUNCTIONS[code]),
        summary=data.get("summary", ""),
        categories=categories,
    )


def load_catalog(catalog_dir: Path = CATALOG_DIR) -> Catalog:
    """Load every catalog YAML file and return a validated Catalog.

    Functions come back in canonical NIST CSF order regardless of filename.
    """
    functions: dict[str, Function] = {}
    for path in sorted(catalog_dir.glob("*.yaml")):
        fn = load_function(path)
        if fn.code in functions:
            raise CatalogError(f"duplicate function {fn.code} in {path.name}")
        functions[fn.code] = fn

    ordered = [functions[code] for code in CSF_FUNCTIONS if code in functions]
    return Catalog(functions=ordered)
