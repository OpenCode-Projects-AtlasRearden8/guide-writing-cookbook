# Chapter 7: Verify Every Claim

## The idea

A manual's currency is trust. Readers follow your steps with real files, real
money, and real evenings. One wrong claim costs the reader an evening and costs
you the only thing you traded them for their trust. Verification is not
perfectionism; it is contract fulfillment.

## The claim taxonomy

Sort every claim before you trust it, by what kind of being-true it even means:

- **A fact:** "The free tier allows 25 messages a day." Verify by testing it
  yourself and noting the date. Update, or mark with the date checked.
- **A procedure:** "Click this, then this." Verify by doing it *fresh* — wipe
  your state, follow your own steps exactly as written, on a clean account or a
  clean folder. Never verify a procedure from memory.
- **An implication:** "This won't affect your existing files." Verify by
  testing both branches: the normal path *and* the path that goes wrong.
- **A comparison:** "Option A is faster than B." Verify on your hardware, with
  your numbers, and write the numbers. "Faster" without numbers is somebody
  else's opinion you borrowed.
- **A forecast:** "Prices will stay near $20." Label it a prediction, dated.
  Predictions in manuals decay fastest; date them like milk.

## The verification loop, done as a human

1. **Write the steps.**
2. **Reset.** Fresh browser profile, clean folder, new account if warranted.
3. **Follow your steps only.** No memory-assists. If you deviate intuitively,
   the steps were incomplete — rewrite, don't cheat.
4. **Log what actually happens,** including the awkward pauses and unexpected
   prompts. Your reader will see exactly what you saw.
5. **Log every discrepancy** immediately: step numbers, the actual wording on
   screen, durations, file sizes.
6. **Fix and rerun the full procedure** after fixes, because step 7 leaking
   into step 8 fixes nothing about step 3.

If you cannot reset (free trial spent, state created), add a dated note: "verified
2026-10-15 on version 3.2." Version-and-date beats nothing.

## Cross-checking without the internet's noise

- Uses vendor help pages primary, forums secondary; forums for the errors you
  had, primary docs for setup defaults.
- Two independent sources for any fact you didn't test yourself.
- For version claims, check the release notes page, not the forum thread about it.
- Careful with blog posts describing versions of software whose screens change
  per platform: what's true on Android may be false on desktop.

## Verifying harmlessness

For topics touching health, money, law, or safety: the claim you verify is not
the advice itself (you are not giving medical advice anyway); the claim is that
**your book stays educational**. Check:

- No dosages, no diagnostics, no triage instructions.
- Boundaries stated plainly where the topic walks near the line ("For anything
  medical, ask your care provider; this page is education about tools, and it
  isn't medical advice.").
- Tax, legal, and financial figures marked as *"example only, in your country
  the numbers differ."*

## The fragile-claim ledger

Keep a one-file inventory (`claims.md`) of anything volatile:

| Claim | Where in book | Verified on | Risk | Next check |
|---|---|---|---|---|
| Free tier allows 25 msgs/day | Ch. 3, step 2 | 2026-10-14 | high | 2026-11 quarterly |
| Steps 1–6 run clean on version 3.2 | Ch. 4 | 2026-10-15 | medium | next version bump |
| MP3 export ~1 MB/minute | Ch. 4 note | 2026-10-15 | low | yearly |

Anything with risk *high* and no *next check* is a trust leak waiting to open.

## The shipping gate

Manual ships only when:

- Every procedure has been run fresh end-to-end, twice.
- Every fact has either your own test result, a dated reliable source, or an
  in-text date-of-check mark.
- Every volatile claim appears in `claims.md`.
- Every place the reader could go wrong has a recovery path that you tested by
  actually going wrong on purpose.

The double-check that takes an hour buys trust that lasts years. That trade is
the whole business model of beginner-friendly writing.
