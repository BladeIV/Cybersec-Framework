"""NetGuardian Textual app.

Shows the tool catalog as a searchable, filterable tree with a details
panel. The same app runs in the terminal (`netguardian`) and in the
browser (`netguardian --web`, served by `textual-serve`).
"""
from __future__ import annotations

import webbrowser

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Footer,
    Header,
    Input,
    Markdown,
    Select,
    Static,
    Tree,
)
from textual.widgets.tree import TreeNode

from .loader import load_catalog
from .models import Catalog, Tool


class NetGuardianApp(App):
    CSS = """
    #body { height: 1fr; }
    #sidebar { width: 42%; min-width: 34; border-right: solid $panel; }
    #filters { height: auto; padding: 0 1; }
    #search { margin: 1 0; }
    Select { margin-bottom: 1; }
    #detail { padding: 1 2; }
    #count { color: $text-muted; padding: 0 1; }
    Tree { height: 1fr; }
    """

    BINDINGS = [
        ("/", "focus_search", "Search"),
        ("o", "open_url", "Open site"),
        ("r", "reset", "Reset filters"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, catalog: Catalog | None = None) -> None:
        super().__init__()
        self.catalog = catalog or load_catalog()
        self._team: str | None = None
        self._free_only = False
        self._installed_only = False
        self._selected_tool: Tool | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Horizontal(id="body"):
            with Vertical(id="sidebar"):
                with Vertical(id="filters"):
                    yield Input(placeholder="Search tools…", id="search")
                    yield Select(
                        [("All teams", "all"), ("Red team", "red"), ("Blue team", "blue")],
                        value="all",
                        id="team",
                        allow_blank=False,
                    )
                    yield Select(
                        [
                            ("Any cost", "any"),
                            ("Free only", "free"),
                            ("Installed only", "installed"),
                        ],
                        value="any",
                        id="avail",
                        allow_blank=False,
                    )
                yield Static("", id="count")
                yield Tree("NIST CSF 2.0", id="tree")
            yield Markdown(_WELCOME, id="detail")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "NetGuardian"
        self.sub_title = "Security tool catalog & triage"
        self._rebuild_tree()

    # --- filtering & tree ---------------------------------------------
    def _current(self) -> Catalog:
        search = self.query_one("#search", Input).value
        return self.catalog.filter(
            team=self._team,
            query=search,
            free_only=self._free_only,
            installed_only=self._installed_only,
        )

    def _rebuild_tree(self) -> None:
        tree = self.query_one("#tree", Tree)
        tree.clear()
        view = self._current()
        total = 0
        visible: set[tuple[str, str]] = set()
        for fn in view.functions:
            fn_node = tree.root.add(f"{fn.code} · {fn.name}", expand=True)
            for cat in fn.categories:
                cat_node = fn_node.add(cat.name, expand=True)
                for tool in cat.tools:
                    total += 1
                    visible.add((tool.name, tool.url))
                    label = tool.name
                    if tool.is_installed:
                        label += " ✓"
                    cat_node.add_leaf(label, data=tool)
        tree.root.expand()
        self.query_one("#count", Static).update(f"{total} tools shown")

        # If the selected tool was filtered out, drop the stale selection so
        # the details panel and the "open" action don't point at a hidden tool.
        if self._selected_tool is not None and (
            self._selected_tool.name,
            self._selected_tool.url,
        ) not in visible:
            self._selected_tool = None
            self.query_one("#detail", Markdown).update(_WELCOME)

    # --- events --------------------------------------------------------
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search":
            self._rebuild_tree()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "team":
            self._team = None if event.value == "all" else str(event.value)
        elif event.select.id == "avail":
            self._free_only = event.value == "free"
            self._installed_only = event.value == "installed"
        self._rebuild_tree()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node: TreeNode = event.node
        if isinstance(node.data, Tool):
            self._selected_tool = node.data
            self.query_one("#detail", Markdown).update(_tool_markdown(node.data))

    # --- actions -------------------------------------------------------
    def action_focus_search(self) -> None:
        self.query_one("#search", Input).focus()

    def action_open_url(self) -> None:
        if self._selected_tool:
            webbrowser.open(self._selected_tool.url)
            self.notify(f"Opening {self._selected_tool.url}")

    def action_reset(self) -> None:
        self.query_one("#search", Input).value = ""
        self.query_one("#team", Select).value = "all"
        self.query_one("#avail", Select).value = "any"
        self._team = None
        self._free_only = self._installed_only = False
        self._rebuild_tree()


_WELCOME = """\
# NetGuardian

Browse 50+ free, open-source security tools organised by the six
**NIST CSF 2.0** functions and tagged for **red** and **blue** teams.

- Type in the search box, or press **/**
- Filter by team and availability on the left
- Select a tool to see details here
- Press **o** to open the selected tool's website

Everything here is free to use. Pick a tool on the left to begin.
"""


def _tool_markdown(tool: Tool) -> str:
    teams = ", ".join(tool.teams) or "—"
    platforms = ", ".join(tool.platforms) or "—"
    tags = ", ".join(f"`{t}`" for t in tool.tags) or "—"
    installed = "yes ✓" if tool.is_installed else ("no" if tool.command else "n/a")
    parts = [
        f"# {tool.name}",
        "",
        tool.description,
        "",
        f"- **Teams:** {teams}",
        f"- **License:** {tool.license}",
        f"- **Cost:** {tool.cost}",
        f"- **Platforms:** {platforms}",
        f"- **Tags:** {tags}",
    ]
    if tool.command:
        parts.append(f"- **Command:** `{tool.command}` (installed: {installed})")
    parts += ["", f"**Website:** {tool.url}", "", "_Press **o** to open in a browser._"]
    return "\n".join(parts)


def run() -> None:
    NetGuardianApp().run()


if __name__ == "__main__":
    run()
