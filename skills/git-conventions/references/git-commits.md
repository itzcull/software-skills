# Git Commits

## Core Principles

**Stability First**: Every commit represents stable, working software.

**Incremental Progress**: Small, focused changes that are easy to review, revert, and bisect.

**Imperative Voice**: Clear, actionable commit messages that describe what the code DOES when applied.

**Semantic Clarity**: Type prefixes indicate the nature of change at a glance.

## Stability Invariant

Every commit MUST satisfy ALL of these criteria:

- All tests pass
- Build succeeds
- Linting passes
- Type checking passes

**Why this matters:**

- **Bisect safety**: Any commit can be checked out and run
- **Rollback confidence**: Can revert to any previous commit safely
- **CI/CD reliability**: Every commit is deployable
- **Team coordination**: No one pulls broken code

**Pre-commit verification:**

```bash
npm test && npm run build && npm run lint && npm run typecheck
```

## Commit Message Format

### Structure

```
<type>: <description>

[optional body]

[optional footer]
```

### Types (Conventional Commits)

| Type | Purpose |
|------|---------|
| `feat` | New functionality added |
| `fix` | Bug or error corrections |
| `refactor` | Code improvements without behavior change |
| `test` | Test additions or modifications |
| `chore` | Routine tasks (dependency upgrades, tooling) |
| `deprecate` | Functionality deprecation |
| `release` | Version release commits |

### Breaking Changes

Append `!` after type to indicate breaking changes:

```
feat!: change payment API to require authentication
```

### Description Rules

- Maximum 256 characters
- Imperative mood ("add" not "added")
- Lowercase first letter (unless proper noun)
- No period at end
- Focus on WHAT and WHY, not HOW

### Examples

```
feat: add payment validation for credit cards
fix: correct timezone handling in order timestamps
refactor: extract shipping calculation logic
test: add edge cases for payment validation
chore: upgrade dependencies to latest versions
```

**Anti-patterns:**

```
feat: Added payment stuff          (past tense, vague)
fix: fixed the bug.               (vague, period, past tense)
refactor: cleanup                 (too vague)
feat: updates                     (meaningless)
```

### Body (Optional)

Use the body when the description alone is insufficient:

- Explain WHY the change was needed
- Describe trade-offs considered
- Document edge cases or constraints
- Wrap at 72 characters per line
- Blank line separates from description

```
refactor: replace synchronous file operations with async

The previous synchronous implementation blocked the event loop,
causing UI freezes when processing large files. This refactor
uses async/await throughout the file processing pipeline.

Trade-off: Slightly more complex error handling, but significantly
better UX for large file operations (>10MB).
```

### Footer (Optional)

Use for metadata like breaking changes and issue references:

```
BREAKING CHANGE: payment API now requires authentication token

Closes: #123
Fixes: #456
Co-authored-by: Jane Developer <jane@example.com>
```

## Commit Rhythm with TDD

### Commit Points in RED-GREEN-REFACTOR

1. **After GREEN** (Required)
   - Test passes
   - Minimal implementation complete
   - Commit message: `feat: <what behavior was added>`

2. **After REFACTOR** (Required if refactored)
   - Code improved while tests remain green
   - Commit message: `refactor: <what was improved>`

3. **Before REFACTOR** (Recommended)
   - Safety checkpoint before restructuring
   - Ensures rollback point if refactoring goes wrong

### Never Commit

- During RED phase (failing tests)
- When tests are broken
- When build fails
- When linting or type errors are present

### Good vs Bad Commit Sequences

**Good - Clear TDD progression:**

```
feat(test): add test for payment validation (RED)
feat: implement payment validation (GREEN)
refactor: extract payment validation constants (REFACTOR)
```

**Good - No refactoring needed:**

```
feat(test): add test for discount calculation (RED)
feat: implement discount calculation (GREEN)
```

**Bad - Combined test and implementation:**

```
feat: add payment validation with tests
```

This suggests the test wasn't written first.

**Bad - Refactoring during RED:**

```
feat(test): add test for shipping calculation (RED)
refactor: extract shipping logic
```

Never refactor when tests aren't green.

## Atomic Commits

Each commit should be a complete, logical unit.

### Include Together

- Feature code + its tests
- Bug fix + regression test
- Refactored code + any required test updates
- Type definitions + implementation using them

### Separate Commits

- Multiple unrelated features
- Refactoring + new feature (refactor first, then feature)
- Bug fix + unrelated cleanup

### Example

**Good - Atomic feature commit:**

```
feat: add email validation to user registration

- Implement email format validation
- Add tests for valid/invalid email formats
- Update user registration form with validation
```

All changes relate to ONE feature.

**Bad - Multiple unrelated changes:**

```
feat: add email validation and fix login bug

- Add email validation
- Fix password hashing in login
- Update dependencies
- Refactor user service
```

Four unrelated changes - impossible to revert selectively.

## Verifying TDD Compliance via Git History

### Checking Commit History

```bash
git log --oneline path/to/file.ts
git log -p --follow path/to/implementation.ts
git log -p --follow path/to/implementation.test.ts
```

### What to Look For

**Good signs:**

- Test file commits appear BEFORE implementation commits
- Commit messages show RED-GREEN-REFACTOR progression
- Small, focused commits
- Refactoring in separate commits from features

**Bad signs:**

- Implementation committed without corresponding test
- Test and implementation in same commit without clear RED phase
- Large commits with multiple features
- Refactoring mixed with new features

### Code Review Checklist

- Was there a failing test before each production code change?
- Do commit messages indicate RED-GREEN-REFACTOR progression?
- Are refactoring commits separate from feature commits?
- Does each commit represent stable software?
- Are commit messages clear and imperative?
- Is each commit atomic and focused?

## Common Mistakes

### Mistake 1: Vague Descriptions

```
fix: bug fix
refactor: cleanup
feat: updates
```

**Fix**: Be specific about WHAT was fixed, cleaned, or updated.

### Mistake 2: Past Tense

```
feat: added payment validation
fix: fixed the bug
```

**Fix**: Use imperative mood - describe what the code DOES when applied.

### Mistake 3: Committing Unstable Code

```
git commit -m "feat: add payment processing (WIP - tests broken)"
```

**Fix**: Wait until tests pass. Use `git stash` if you need to switch context.

### Mistake 4: Multiple Features in One Commit

```
feat: add user authentication, payment processing, and email notifications
```

**Fix**: Three separate commits, one for each feature.

### Mistake 5: Refactoring During RED

Refactoring when tests are failing.

**Fix**: Only refactor when all tests are green.

## Pull Request Standards

- Every PR must have all tests passing
- All linting and quality checks must pass
- Work in small increments that maintain a working state
- PRs should be focused on a single feature or fix
- Include description of the behavior change, not implementation details

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Blockly Commit Guidelines](https://developers.google.com/blockly/guides/contribute/get-started/commits)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

## Related skills

- Load `software-practices` for 50/72 Rule, TDD, and Red-Green-Refactor details
