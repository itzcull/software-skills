# Software Skills

A cohesive collection of software engineering skills designed to serve a user's structured-development procedure. Skills follow the [Agent Skills specification](https://agentskills.io/specification).

## How the skills fit together

The goal is not a single prescribed methodology or a collection of unrelated practices. Every skill should provide a capability that a user can compose into their own development procedure.

- **The shared contract:** [Structured development](skills/structured-development/SKILL.md) defines the methodology-independent responsibilities and conformance requirements. That skill is authoritative for the contract; this README explains the repository's organising purpose.
- **The user's implementation:** a concrete procedure determines how those obligations are fulfilled, including its development loops, progression conditions, decision authority, and placement of cross-cutting concerns.
- **The supporting skills:** reusable capabilities supply protocols, decision support, or evidence within that procedure. Each skill owns its detailed guidance.

Not every procedure needs every skill, and not every skill must independently fulfil the entire contract. A skill can support several responsibilities or operate across multiple loops; composition does not require a fixed hierarchy or one skill per stage.

For example:

- [Test-driven development](skills/test-driven-development/SKILL.md) supplies a behaviour-level implementation and design-feedback protocol.
- [Architecture decision records](skills/architecture-decision-record/SKILL.md) support recording decisions and their rationale.
- [Code review](skills/code-review/SKILL.md) produces evidence-backed findings for the enclosing procedure to act on.

Completing a skill's activity does not automatically establish feature acceptance or release readiness. The enclosing procedure determines how its results contribute to broader decisions.

## What each skill should make clear

To support reliable composition, each skill should explain:

- **Purpose:** the development responsibility or concern it helps fulfil.
- **Applicability:** when the enclosing procedure should invoke it.
- **Inputs:** the intent, constraints, decisions, or evidence it needs.
- **Results:** what it produces and what those results establish.
- **Boundaries:** what it does not decide or prove, and what must return to the enclosing procedure.

These are design expectations, not a mandatory document template or a claim that every existing skill has already been assessed. Cohesion comes from compatible concepts and explicit handoffs, not identical workflows or duplicated contract requirements.

Each installable skill is a direct child of `skills/`. A skill contains `SKILL.md` and only the support files that its instructions use.

## Install

### Pi

Clone the repository and add `~/skills/software/skills` to the `skills` array in `~/.pi/agent/settings.json`.

### Codex

```bash
mkdir -p ~/.agents/skills
for skill in ~/skills/software/skills/*; do
  [ -f "$skill/SKILL.md" ] && ln -s "$skill" ~/.agents/skills/"${skill##*/}"
done
```

### Gemini CLI

```bash
gemini skills install https://github.com/itzcull/software-skills --path skills --scope user
```

Use `gemini skills link ~/skills/software/skills --scope user` to use a local checkout without copying it.

### Claude Code

```bash
claude plugin marketplace add itzcull/software-skills
claude plugin install software-skills@software-skills
```

For local use:

```bash
claude --plugin-dir ~/skills/software
```

## License

[MIT](LICENSE)
