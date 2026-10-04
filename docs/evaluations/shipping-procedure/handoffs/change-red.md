# C1 RED handoff

- **Phase:** RED.
- **Behavior / source:** `decision-c1.md` explicitly supersedes the threshold in N1; A1 remains in force.
- **Given:** a 5000-cent subtotal, below the revised 7500-cent threshold.
- **When:** `shippingCharge(5000)` is requested.
- **Then:** return the standard 500-cent charge.
- **Observable outcome / level:** public return value / behavior unit test.
- **Scope:** replace only the obsolete 5000-cent-free expectation in `test/shipping-policy.test.mjs`; production scope is `shipping.mjs`.
- **Evidence:** `node --test` exits 1; new expectation fails `0 !== 500`, the other three checks pass (`29-change-red.json`). Production is unchanged from accepted N1+A1.
- **Constraints:** net subtotal, integer cents, standard fee and pre-commit verification remain inherited. The blocked sync branch is not the baseline.
- **Open questions:** C1 authorizes the requirement change; latest-trunk compatibility remains unresolved in S1 and outside this independent case.
- **Next prompt:** implement the revised threshold only, run `node --test`, and return GREEN evidence. Do not silently retain or weaken the superseded criterion.
