# A1 cycle and feature disposition

- **Goal / behavior:** apply free-shipping eligibility to the net subtotal; omitted discount is zero. Authority is the scripted response `decision-a1.md`, not an assumed user choice.
- **Escalation:** `ambiguity-stop.md` and `11-ambiguity-stop.json` preserve the no-edit pause before the response.
- **Changed files:** `checkout.mjs`, `test/checkout-contract.test.mjs`.
- **RED:** new CLI behavior fails with `0` rather than `500`, 3 existing tests pass (`12-discount-red.json`).
- **GREEN:** only the checkout adapter changes; 4/4 tests pass (`13-discount-green.json`).
- **REFACTOR:** skipped after assessment. Names specify cents; zero is the defined no-discount default, not unexplained configuration; no duplicated policy, complex structure, or unnecessary mutation exists. The small imperative CLI boundary remains separate from the pure quote function.
- **Verification:** 4/4 unit/CLI checks and whitespace checks pass (`14-discount-refactor-checks.json`, `15-discount-review-diff.json`). No configured lint/type/build checks are claimed.
- **Review:** same-executor two-pass review checked output, optional-argument compatibility, and preservation of N1. No supported finding within the valid-input fixture scope. This is not independent review.
- **Concern evidence:** the real CLI receives and subtracts cent values before calling the public quote API; no collaborator mocks or internal interaction assertions are used.
- **Cycle disposition:** completed after resolving the missing policy.
- **Enclosing disposition:** fixture N1+A1 accepted under its explicit gate; local commit and local-remote push permitted. No production release or operational acceptance.
- **Next:** retain this accepted checkpoint for both the independent sync-failure case and the changed-requirement case. Do not carry a blocked sync tree into the latter silently.
