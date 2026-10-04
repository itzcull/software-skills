# Normal case: RED handoff

- **Phase:** RED
- **Behavior / source:** N1, orders of at least 5000 cents qualify for free shipping (`procedure.md`).
- **Given:** a 5000-cent subtotal.
- **When:** the caller requests `shippingCharge(5000)`.
- **Then:** the returned charge is 0 cents.
- **Observable outcome type:** return value.
- **Test level:** behavior unit test through the exported public function; existing CLI regression tests remain applicable.
- **Scope:** `test/shipping-policy.test.mjs`, test `orders at the free-shipping threshold ship free`; production API `shippingCharge` in `shipping.mjs`.
- **Evidence:** `node --test`, exit 1; 2 existing tests pass and the new test fails with `500 !== 0`. Full output and source snapshot: `evidence/05-normal-red.json`. No production file was changed for RED.
- **Constraints:** preserve the 500-cent charge below the threshold and cents-based CLI; all tests are required before commit or push. Valid integer inputs only; no additional features.
- **Open questions:** none for N1.
- **Next prompt:** execute GREEN for N1 in `shipping.mjs`, using this handoff; run `node --test` and return the result without refactoring or widening scope.
