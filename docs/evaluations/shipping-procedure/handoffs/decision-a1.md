# Scripted controller decision A1

This is a fixture response, not a live user approval.

After the ambiguity escalation, the controller selects net-subtotal eligibility. Checkout receives subtotal cents and optional discount cents; omitted discount means zero. The free-shipping threshold applies to subtotal minus discount. Valid-input restrictions from the procedure remain unchanged.

Authorized behavior: a 5000-cent subtotal with a 1000-cent discount pays the standard 500-cent shipping charge. Preserve the N1 quote policy and no-discount CLI behavior.

Proceed to RED for this behavior. Do not change the threshold or add unrelated validation.
