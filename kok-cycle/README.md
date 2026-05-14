# kok-cycle

**The Action Cycling Hypothesis** — photosynthetic quantum yield as a mechanical duty cycle constraint, not a thermodynamic inefficiency.

→ Brief: [atcooper.net/tools/kok-cycle](https://atcooper.net/tools/kok-cycle)
→ Preprint: [atcooper.net/tools/kok-cycle/action-cycling-hypothesis.pdf](https://atcooper.net/tools/kok-cycle/action-cycling-hypothesis.pdf)

## The claim

The measured maximum quantum yield of C3 photosynthesis (~0.093) sits ~25.6% below the stoichiometric theoretical maximum (1/8 = 0.125). The conventional account attributes the gap to a list of leaks — photorespiration, non-photosynthetic pigment absorption, photosystem excitation imbalance. This preprint proposes the gap is mechanical: the Kok cycle of water oxidation is a four-stroke engine with three productive strokes and one reset stroke (S₃→S₀), during which the reaction centre cannot accept new photochemistry. The productive duty cycle is 3/4.

```
φ = φ_max × D × (1 − 4ε) = 0.125 × 0.75 × 0.992 = 0.0930
```

Three multiplicative terms — stoichiometry, mechanics, stochastic pair-coupling noise — all derivable from the architecture of the Kok cycle. No free parameters, no curve fitting. The product matches the observed value.

## Contents

- `action_cycling_hypothesis.pdf` — the preprint (v1.0, 15 March 2026). Main paper plus three appendices: (A) computational sensitivity analysis, (B) the photon-pair derivation, (C) a clearly-flagged speculative thought experiment, not part of the core hypothesis.
- `build_paper.py` — ReportLab script that generates the preprint PDF.
- `kok_duty_cycle.py` — the sensitivity-analysis script. Sweeps all four S-state transition times across their published ranges (625 combinations), computes the reset-overhead fraction and predicted quantum yield for each, and reports the closest matches to the observed 0.093. Run it: `python3 kok_duty_cycle.py`.
- `psii-waveform.jsx` — React/Canvas visualisation of the PSII Kok cycle phase waveform: stepped charge accumulation through S₀→S₁→S₂→S₃, photon flashes, O₂ bursts, and the period-4 fluorescence oscillation. The site hosts a vanilla-HTML port of this at `/tools/kok-cycle/waveform.html`.

## Falsifiability

The model's central prediction is that the S₃→S₀ reset occupies ~25% of total Kok cycle time under saturating illumination. This is directly testable against measured OEC cycle timing. Published S-state transition kinetics are consistent with it — a combinatorial sweep of the reported ranges returns 56 of 625 parameter combinations within 0.003 of the observed quantum yield, with the closest matches clustering in a 25.3–25.9% reset-fraction band.

## Status

Preprint v1.0. The biological mechanism (the Kok cycle, the S-state transitions) is settled science; the duty-cycle interpretation of the quantum yield gap is the contribution and is offered for falsification.
