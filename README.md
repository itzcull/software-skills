# Software Skills

Software engineering skills that follow the [Agent Skills specification](https://agentskills.io/specification).

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
