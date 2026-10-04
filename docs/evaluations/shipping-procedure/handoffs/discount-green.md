# A1 GREEN handoff

- **Phase:** GREEN.
- **Behavior / source:** net-subtotal eligibility, `decision-a1.md` and `discount-red.md`.
- **Given / When / Then:** given 5000 subtotal and 1000 discount, invoking checkout prints 500 shipping cents.
- **Observable outcome / test level:** public CLI output / real integration.
- **Scope:** only `checkout.mjs` changed during GREEN; it supplies the net subtotal to the unchanged quote function.
- **Evidence:** `node --test`, exit 0, 4/4 checks pass; `13-discount-green.json`.
- **Constraints:** N1 threshold, cents-based inputs, omitted discount is zero, all-test gate, no deployment.
- **Open questions:** none for A1.
- **Next prompt:** assess refactoring, rerun all tests and report to the enclosing feature loop. Do not treat this handoff alone as feature acceptance.
