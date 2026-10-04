# A1 RED handoff

- **Phase:** RED.
- **Behavior / source:** net-subtotal eligibility from `decision-a1.md`.
- **Given:** 5000-cent subtotal and 1000-cent discount.
- **When:** the consumer runs `node checkout.mjs 5000 1000`.
- **Then:** exit successfully and print shipping charge `500`.
- **Observable outcome / test level:** CLI output / integration through the actual public checkout and quote implementation, without mocks.
- **Scope:** `test/checkout-contract.test.mjs`, test `discounts reduce the subtotal used for free-shipping eligibility`; production `checkout.mjs`.
- **Evidence:** `node --test`, exit 1, 3 existing tests pass and the new test fails because checkout prints `0`; `12-discount-red.json`. No production edit in RED.
- **Constraints:** inherited N1 threshold, cent units, no-discount compatibility and complete pre-commit gate.
- **Open questions:** resolved by scripted A1; no live user approval claimed.
- **Next prompt:** implement only the approved discount behavior in checkout; run `node --test`; return GREEN evidence.
