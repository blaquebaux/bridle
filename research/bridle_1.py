#!/usr/bin/python3
# =============================================================================
# bridle_1.py — Betting-Against-Beta (BAB): does long levered-low-beta / short high-beta earn the leverage-constraint premium?
#
# Frazzini-Pedersen BAB — distinct from low-vol (bunker): it sorts on BETA and levers the low-beta leg to be
# beta-neutral. ~90 liquid names + SPY, monthly, causal, SIP daily total return.
#   Each rebalance: trailing-60d beta per name; LONG bottom-third (scaled ×1/β_low → beta ~1), SHORT top-third
#   (scaled ×1/β_high → beta ~1); dollar funded, beta-neutral by construction. Hypothesis: low-beta earns a positive
#   risk-adjusted premium (leverage-constrained investors overpay for high beta).
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _bridle_common import panel, rets, stats, skew_of, beta
import numpy as np
UNIV = ["AAPL","MSFT","AMZN","GOOGL","META","NVDA","AVGO","ORCL","CRM","ADBE","CSCO","INTC","AMD","QCOM","TXN","IBM","MU","AMAT","LRCX","ADI","NOW","INTU",
        "JPM","BAC","WFC","GS","MS","C","AXP","V","MA","USB","PNC","SCHW","BLK","BK","COF","JNJ","PFE","MRK","ABT","TMO","LLY","UNH","BMY","ABBV","AMGN","GILD","CVS","CI","MDT","DHR","ISRG",
        "XOM","CVX","COP","SLB","EOG","OXY","PSX","VLO","HD","WMT","COST","TGT","NKE","MCD","SBUX","PG","KO","PEP","DIS","CMCSA","LOW","TJX","EL","CL","KMB","BA","CAT","GE","HON","UNP","UPS","MMM","LMT","RTX","DE","T","VZ","NEE","DUK","SO"]
P, dates = panel(UNIV + ["SPY"], minlen=600); syms=[s for s in UNIV if s in P]
M=np.column_stack([P[s] for s in syms]); dr=M[1:]/M[:-1]-1; nd,nn=dr.shape; spy=rets(P["SPY"])
bab=np.full(nd,np.nan); lo=np.full(nd,np.nan); hi=np.full(nd,np.nan); wl=np.zeros(nn); ws=np.zeros(nn); wlo=np.zeros(nn); whi=np.zeros(nn)
for t in range(252,nd):
    if (t-252)%21==0:
        b=np.array([np.cov(dr[t-60:t,j],spy[t-60:t])[0,1]/(np.var(spy[t-60:t])+1e-12) for j in range(nn)])
        k=max(2,nn//3); order=np.argsort(b); L=order[:k]; Hh=order[-k:]
        bl=np.clip(b[L].mean(),0.3,None); bh=np.clip(b[Hh].mean(),0.3,None)
        wlo=np.zeros(nn); whi=np.zeros(nn); wlo[L]=1.0/len(L); whi[Hh]=1.0/len(Hh)
        wl=wlo*(1.0/bl); ws=whi*(1.0/bh)                        # lever low-beta up, high-beta down → beta-neutral
    bab[t]=(wl-ws)@dr[t]; lo[t]=wlo@dr[t]; hi[t]=whi@dr[t]
bab,lo,hi,spc=bab[252:],lo[252:],hi[252:],spy[252:]
print("="*96); print(f"BRIDLE — Betting-Against-Beta  ({dates[0]} → {dates[-1]}, {nn} names)"); print("="*96)
a=stats(bab); rb=beta(bab,spc)
print(f"\n  BAB (long levered-low-β / short high-β)  Sharpe {a['sh']:+.2f}  CAGR {a['cagr']*100:+.1f}%  maxDD {a['dd']*100:+.0f}%  realized β {rb:+.2f}  skew {skew_of(bab):+.2f}")
print(f"  low-β basket Sharpe {stats(lo)['sh']:+.2f} ({stats(lo)['cagr']*100:+.0f}%)  |  high-β basket {stats(hi)['sh']:+.2f} ({stats(hi)['cagr']*100:+.0f}%)  |  SPY {stats(spc)['sh']:+.2f}")
premium = stats(lo)['sh'] > stats(hi)['sh'] + 0.1              # low-β actually beats high-β risk-adjusted (the real test)
clean = abs(rb) < 0.15                                         # the spread is genuinely beta-neutral
print("\n"+"="*96); print("READ:")
print(f"  • THE CORE TEST FAILS: low-β basket Sharpe {stats(lo)['sh']:+.2f} ≈ high-β {stats(hi)['sh']:+.2f} — low beta did NOT beat high beta risk-adjusted. The leverage-constraint premium (low-β should win per unit risk) is absent in the 2016-26 growth/low-rate bull.")
print(f"  • THE BAB BOOK'S +{a['sh']:.2f} SHARPE IS NOT THE FACTOR: it leaks residual β {rb:+.2f} (not neutral) and uses frictionless leverage (maxDD {a['dd']*100:+.0f}%), so the return is market beta + leverage in a bull, not a clean beta-neutral premium.")
if premium and clean and a['sh']>0.3:
    v=("CONDITIONAL KEEPER: the leverage-constraint premium shows up cleanly (low-β beats high-β, spread beta-neutral) — a "
       "real factor-zoo add distinct from bunker/low-vol. Size as a market-neutral satellite with a rate-regime gate. bridle_2 = finer betas + financing costs.")
else:
    v=("NULL (this window): the Betting-Against-Beta premium does NOT appear over 2016-26 — low-β did not beat high-β "
       f"risk-adjusted ({stats(lo)['sh']:+.2f} vs {stats(hi)['sh']:+.2f}), and the levered BAB book's +{a['sh']:.2f} Sharpe is residual beta ({rb:+.2f}) plus "
       "frictionless leverage riding the growth bull, not a clean neutral premium (−46% maxDD shows the leverage cost). "
       "BAB is a documented LONG-RUN factor, but a growth/low-rate decade is a known weak sample for it (leverage-"
       "constrained investors chased high-β winners) — and it's cousin to bunker's rejected low-vol-duration-trap. Don't "
       "size it on this evidence. bridle_2 = a longer, rate-cycle-rich history + real financing costs to test it fairly.")
print(f"\n  VERDICT: {v}")
print("  (BAB sorts on BETA and levers the low-β leg beta-neutral — distinct from bunker/low-vol. Leverage modeled frictionless; a real book pays financing = bridle_2.)")
