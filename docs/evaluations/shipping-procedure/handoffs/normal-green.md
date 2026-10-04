# Normal case: GREEN handoff

- **Phase:** GREEN
- **Behavior / source:** N1, free shipping at a subtotal of at least 5000 cents, inherited from `normal-red.md`.
- **Given / When / Then:** given 5000 cents, when `shippingCharge` is called, return 0 cents.
- **Observable outcome type / test level:** return value / behavior unit test, with CLI regression checks.
- **Scope:** `shipping.mjs` now implements the threshold; `test/shipping-policy.test.mjs` remains the RED test. No test changed during GREEN.
- **Evidence:** `node --test`, exit 0, 3/3 tests pass; `evidence/06-normal-green.json` contains the output and exact source.
- **Constraints:** inherited 500-cent below-threshold fee, cents-based checkout, and all-test pre-commit gate still apply. No release authorization.
- **Open questions:** none.
- **Next prompt:** perform the REFACTOR assessment for N1; preserve behavior, rerun tests, and report whether changes are warranted before the enclosing feature review.
