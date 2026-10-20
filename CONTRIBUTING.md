# Contributing to NetGuardian

Thanks for helping build the catalog. Most contributions are a one-file edit.

## Add or edit a tool

1. Open the YAML file for the right NIST CSF function in
   `netguardian/catalog/` (`govern`, `identify`, `protect`, `detect`,
   `respond`, `recover`).
2. Find or add a category under `categories:`, then add your tool to its
   `tools:` list.

A tool entry looks like this:

```yaml
- name: Nmap
  url: https://nmap.org/
  description: Network discovery, port scanning, service and OS detection.
  teams: [red, blue]        # one or both of: red, blue
  license: NPSL
  cost: free                # keep the catalog free/low-cost
  platforms: [linux, macos, windows]
  command: nmap             # optional: CLI name, used for the "installed" filter
  tags: [scanner, ports, inventory]
```

**Required fields:** `name`, `url`, `description`, `teams`, `license`, `cost`.
`platforms`, `command` and `tags` are optional.

### Rules of thumb

- Only free or free-tier tools. The project's goal is "easiest and lowest
  cost". If a tool has a paid-only core, leave it out.
- Put a tool in the function it most helps with. Dual-use tools (e.g. BloodHound)
  can be tagged for both teams.
- Keep descriptions to one plain sentence.

## Run the checks

```bash
pip install -e ".[dev]"
pytest                 # validates every catalog entry
python -m netguardian.cli --list   # eyeball the result
```

The test suite fails if a tool is missing a required field or uses a team
other than `red`/`blue`, so a green run means the catalog is well-formed.

## Open a pull request

Keep PRs focused. For a new tool, the title `Add <tool> to <function>` is
perfect.
