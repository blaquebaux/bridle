# Blaque Baux Bridle

**Betting-Against-Beta (BAB) — the leverage-constraint premium, or just a levered bet on a growth bull?**

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/bridle_1.py   # needs Alpaca data keys in the environment
```

Frazzini-Pedersen BAB: long *levered* low-beta / short high-beta, beta-neutral by construction — distinct from `bunker`/low-vol (that sorts on realized vol; this sorts on **beta** and levers).

## Finding (null, this window)
- **The core test fails:** low-β basket Sharpe **+0.95 ≈** high-β **+0.99** — low beta did *not* beat high beta risk-adjusted over the 2016-26 growth/low-rate bull.
- **The BAB book's +0.44 Sharpe isn't the factor:** it leaks residual β **+0.22** (not neutral) and rides frictionless leverage (maxDD **−46%**) — market beta + leverage in a bull, not a clean premium.

## Verdict
**NULL (this window).** BAB is a documented *long-run* factor, but a growth/low-rate decade is a known weak sample (leverage-constrained investors chased high-β winners) — cousin to `bunker`'s rejected low-vol-duration trap. Don't size it on this evidence. `bridle_2` = a longer, rate-cycle-rich history with real financing costs.

## Status
**Research.** Honest white-space study — verdict falls where it falls, proxy limits named, `bridle_2` path noted. Fat-tail scorecard, causal, Alpaca SIP daily total return. No live capital.
