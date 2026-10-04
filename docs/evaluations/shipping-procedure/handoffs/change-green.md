# C1 GREEN handoff

- **Phase:** GREEN.
- **Behavior / source:** revised 7500-cent threshold from `decision-c1.md` and `change-red.md`.
- **Given / When / Then:** a 5000-cent subtotal now returns a 500-cent shipping charge.
- **Outcome / level:** public return value / behavior unit test with inherited CLI checks.
- **Scope:** one policy value changed in `shipping.mjs`; no test changed during GREEN.
- **Evidence:** `node --test`, exit 0, 4/4 checks pass (`30-change-green.json`).
- **Constraints:** inherited cent units, net basis and standard fee remain unchanged. No claim about the blocked latest-trunk integration.
- **Open questions:** none within C1; S1 remains a separate unresolved integration.
- **Next prompt:** assess refactoring and rerun the cycle checks. Then return to feature evaluation for the controller-required checkout tests on both sides of the revised threshold before acceptance.
