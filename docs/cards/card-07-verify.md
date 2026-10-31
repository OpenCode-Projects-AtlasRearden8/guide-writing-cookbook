# Recipe Card 7: Verify Every Claim

**Use when:** a chapter says something the reader could spend real time or money on.

## Sort the claim, then verify it the matching way

| Claim type | Verify by |
|---|---|
| Fact ("free tier = 25/day") | Test it; write in today's date |
| Procedure ("click this, then this") | Run it **fresh** on a clean state, following only the written steps |
| Implication ("won't affect existing files") | Test the normal path *and* the path that goes wrong |
| Comparison ("A faster than B") | Numbers from your hardware; no numbers, no claim |
| Forecast ("prices will stay near X") | Mark as a prediction, dated like milk |

## The verification loop

1. [ ] Write the steps.
2. [ ] Reset: fresh profile, clean folder, new account if needed.
3. [ ] Follow only the written steps — no memory assists. Any intuitive deviation = a hole in the steps: rewrite.
4. [ ] Log what actually happens, including the awkward prompts and pauses.
5. [ ] Fix, then rerun the **entire** procedure — not the changed step.
6. [ ] Can't reset? Note it: "verified 2026-10-__ on version ___."

## Sources

- Vendor docs are primary; forums only for errors you personally hit.
- Two independent sources for facts you didn't test yourself.
- Release-notes pages, not forum threads *about* release notes.

## Guardrails

- [ ] Health/money/law topics stay educational: no dosages, diagnostics, triage, or financial instructions; boundary sentence stated where the topic brushes the line ("this is education about tools, not medical advice").
- [ ] Every volatile claim exists in `claims.md` with: where it appears, date checked, risk, next check.
- [ ] Ship gate: procedures run fresh twice; every fact tested, dated, or marked; recovery paths tested by deliberately going wrong.
