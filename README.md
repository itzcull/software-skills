# Software Skills

A curated collection of tech-stack agnostic software engineering skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Each skill encodes industry best practices as structured reference material that AI coding agents can apply during development.

## Why

Coding agents work better when they have access to well-organized domain knowledge. These skills provide that knowledge -- from TDD phase orchestration to system design tradeoffs to domain-driven design tactics -- in a format Claude Code can load on demand.

Skills are not libraries or frameworks. They are structured reference documents that shape how an agent approaches a problem.

## Skills

| Skill | Description |
|-------|-------------|
| **Test-Driven Development** (`test-driven-development`) | Complete TDD skill -- RED-GREEN-REFACTOR cycle orchestration, phase execution, handoff contracts, and guided TDD pairing |
| **Code Review** (`code-review`) | Structured taxonomy-guided review with two-pass detection across 16 error categories |
| **Design Patterns** (`design-patterns`) | GoF and modern patterns -- creational, structural, behavioural, and architectural with trade-offs (22 reference files) |
| **Domain-Driven Design** (`domain-driven-design`) | Strategic and tactical DDD -- bounded contexts, aggregates, entities, value objects, context mapping, EventStorming (17 reference files) |
| **DiffDive** (`diffdive`) | Branch analysis and context loading for getting up to speed on unfamiliar branches |
| **Git Conventions** (`git-conventions`) | Commit message format, TDD commit rhythm, conventional commit types, PR standards |
| **Refactorings** (`refactorings`) | Refactoring catalog based on Fowler's work -- method composition, feature moving, data organisation, conditional simplification (57 reference files) |
| **Test Design** (`test-design`) | Authoritative resource on writing great tests -- behavior-focused design, test levels, test doubles, integration testing, and E2E/browser testing |
| **System Design** (`system-design`) | Distributed systems patterns -- CAP theorem, caching, load balancing, message queues, consistency models, architectural patterns (61 reference files) |
| **Twelve-Factor** (`twelve-factor`) | Twelve-Factor App methodology for building deployable SaaS applications |

## Installation

### Plugin marketplace (recommended)

```bash
/plugin marketplace add itzcull/software-skills
/plugin install software-skills@software-skills
/reload-plugins
```

You can also browse and install from the `/plugin` Discover tab.

### Local testing

If you've cloned the repo and want to test changes locally:

```bash
claude --plugin-dir ./software-skills
```

### Manual

```bash
git clone https://github.com/itzcull/software-skills.git

# Copy all skills
cp -r software-skills/skills/* ~/.claude/skills/

# Or symlink for easier updates
ln -sf "$(pwd)/software-skills/skills/"* ~/.claude/skills/
```

Skills are loaded on demand by Claude Code based on the task context.

## Skill Structure

Each skill is a directory containing a `SKILL.md` file and an optional `references/` directory:

```
my-skill/
  SKILL.md              # Main skill definition
  references/           # Optional supporting documents
    concept-a.md
    concept-b.md
```

### SKILL.md format

```yaml
---
name: my-skill
description: One-line description of what this skill covers and when to use it.
license: MIT
metadata:
  author: your-name
---

## Purpose
What problem this skill solves and why it exists.

## When to use
Specific scenarios where this skill applies.

## Reference files
Links to documents in the references/ directory.
```

The `description` field in frontmatter is what Claude Code uses to decide whether to load the skill, so make it specific about the skill's scope and trigger conditions.

## Contributing

### Adding a new skill

1. Create a directory under `skills/` with a kebab-case name
2. Write a `SKILL.md` following the format above
3. Add reference files in `references/` if the skill covers a broad domain
4. Open a PR with a clear description of what the skill teaches

### Quality expectations

- **Tech-stack agnostic** -- skills should encode principles and practices, not framework-specific recipes
- **Authoritative sources** -- reference established literature, standards, or widely-accepted practices
- **Actionable** -- include enough detail that an agent can apply the knowledge, not just recite it
- **Focused** -- one coherent domain per skill; split broad topics into separate skills

### Modifying an existing skill

- Keep changes focused on accuracy or coverage gaps
- Preserve the existing structure and conventions
- Reference files should be self-contained -- each should be understandable on its own

## License

[MIT](LICENSE)
