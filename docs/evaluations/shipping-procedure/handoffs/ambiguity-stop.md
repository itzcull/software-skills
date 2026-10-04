# A1 escalation: discount basis is unspecified

Request: extend checkout to accept a discount and apply the free-shipping policy.

The request does not establish whether the threshold uses the gross subtotal or the amount after discount. Both would produce different observable outcomes for a 5000-cent subtotal with a 1000-cent discount.

- Disposition: escalated before RED. Do not choose an expected result or edit production code.
- Evidence: `11-ambiguity-stop.json` shows a clean worktree at the accepted N1 commit. Its source fingerprint matches the normal-case pushed state.
- Decision required from fixture controller: gross or net eligibility, and the behavior when discount is omitted.
- Inherited constraints: integer cents, valid discount no larger than subtotal, all unit/CLI checks before commit or push.
- Recovery: after the decision, update cycle inputs, create one focused behavior test, and establish RED.
