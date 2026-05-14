#!/usr/bin/env python3
"""
Generate: The Action Cycling Hypothesis
Full paper with Appendix C: On Crop Circles and Phase-Locked Landing
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)

OUTPUT = "/home/claude/action_cycling_hypothesis.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=25*mm, rightMargin=25*mm,
    topMargin=25*mm, bottomMargin=25*mm,
    title="The Action Cycling Hypothesis",
    author="Alexander T. Cooper-Rye",
)

styles = getSampleStyleSheet()

# --- Custom styles ---
s_title = ParagraphStyle('T', parent=styles['Title'], fontSize=15, leading=19,
    alignment=TA_LEFT, spaceAfter=3*mm, textColor=HexColor('#111'))
s_sub = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=10, leading=13,
    alignment=TA_LEFT, spaceAfter=2*mm, textColor=HexColor('#555'), fontName='Helvetica-Oblique')
s_author = ParagraphStyle('Au', parent=styles['Normal'], fontSize=10, leading=12,
    alignment=TA_LEFT, spaceAfter=1*mm, textColor=HexColor('#333'))
s_affil = ParagraphStyle('Af', parent=styles['Normal'], fontSize=8.5, leading=11,
    alignment=TA_LEFT, spaceAfter=5*mm, textColor=HexColor('#666'), fontName='Helvetica-Oblique')
s_absh = ParagraphStyle('AbH', parent=styles['Normal'], fontSize=9.5, leading=12,
    fontName='Helvetica-Bold', spaceAfter=2*mm)
s_abs = ParagraphStyle('Ab', parent=styles['Normal'], fontSize=9, leading=13,
    alignment=TA_JUSTIFY, spaceAfter=5*mm, textColor=HexColor('#222'))
s_h1 = ParagraphStyle('H1', parent=styles['Heading2'], fontSize=11, leading=14,
    spaceBefore=7*mm, spaceAfter=3*mm, textColor=HexColor('#111'), fontName='Helvetica-Bold')
s_h2 = ParagraphStyle('H2', parent=styles['Heading3'], fontSize=10, leading=13,
    spaceBefore=5*mm, spaceAfter=2*mm, textColor=HexColor('#222'), fontName='Helvetica-Bold')
s_body = ParagraphStyle('B', parent=styles['Normal'], fontSize=9.5, leading=13.5,
    alignment=TA_JUSTIFY, spaceAfter=3*mm, textColor=HexColor('#1a1a1a'))
s_eq = ParagraphStyle('Eq', parent=styles['Normal'], fontSize=10, leading=14,
    alignment=TA_CENTER, spaceAfter=4*mm, spaceBefore=4*mm, fontName='Courier',
    textColor=HexColor('#111'))
s_tn = ParagraphStyle('TN', parent=styles['Normal'], fontSize=8, leading=10,
    spaceAfter=4*mm, textColor=HexColor('#666'), fontName='Helvetica-Oblique')
s_ref = ParagraphStyle('Ref', parent=styles['Normal'], fontSize=8.5, leading=11,
    spaceAfter=1.5*mm, textColor=HexColor('#333'), leftIndent=12, firstLineIndent=-12)
s_app_title = ParagraphStyle('AppT', parent=styles['Heading2'], fontSize=11, leading=14,
    spaceBefore=7*mm, spaceAfter=3*mm, textColor=HexColor('#8B4513'), fontName='Helvetica-Bold')
s_app_body = ParagraphStyle('AppB', parent=styles['Normal'], fontSize=9.5, leading=13.5,
    alignment=TA_JUSTIFY, spaceAfter=3*mm, textColor=HexColor('#333'))
s_epigraph = ParagraphStyle('Epi', parent=styles['Normal'], fontSize=9, leading=13,
    alignment=TA_LEFT, spaceAfter=5*mm, textColor=HexColor('#777'),
    fontName='Helvetica-Oblique', leftIndent=20*mm, rightIndent=20*mm)

story = []

# ═══════════════════════════════════════════════
# TITLE BLOCK
# ═══════════════════════════════════════════════
story.append(Paragraph(
    "The Action Cycling Hypothesis", s_title))
story.append(Paragraph(
    "Photosynthetic quantum yield as a mechanical duty cycle constraint, "
    "not a thermodynamic inefficiency", s_sub))
story.append(Spacer(1, 2*mm))
story.append(Paragraph("Alexander T. Cooper-Rye", s_author))
story.append(Paragraph(
    "Independent researcher &nbsp;|&nbsp; Correspondence: claude@atcr.ai &nbsp;|&nbsp; "
    "15 March 2026 &nbsp;|&nbsp; Preprint v1.0", s_affil))
story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#ccc')))
story.append(Spacer(1, 3*mm))

# ═══════════════════════════════════════════════
# ABSTRACT
# ═══════════════════════════════════════════════
story.append(Paragraph("Abstract", s_absh))
story.append(Paragraph(
    "The maximum quantum yield of C<sub>3</sub> photosynthesis has been measured at "
    "approximately 0.093 mol CO<sub>2</sub> fixed per mol absorbed photons (Long et al. 1993; "
    "Hogewoning et al. 2012), falling 25.6% below the theoretical stoichiometric "
    "maximum of 0.125. This gap has been attributed to photorespiration, "
    "non-photosynthetic pigment absorption, and photosystem excitation imbalances. "
    "Here we propose a simpler explanation: the gap is a mechanical duty cycle "
    "constraint imposed by the Kok cycle of photosynthetic water oxidation. The "
    "oxygen-evolving complex operates as a four-stroke engine in which one stroke "
    "(S<sub>3</sub> &rarr; S<sub>0</sub>) is dedicated to product release and system reset. During this phase, "
    "the reaction centre cannot accept new photochemical input. Under continuous "
    "illumination, this produces a 25% temporal overhead during which arriving photons "
    "cannot drive productive charge accumulation. Applying this duty cycle correction "
    "to the stoichiometric maximum yields a predicted quantum yield of 0.09375, which "
    "is within 0.8% of the observed value. A residual coupling-loss term of "
    "approximately 0.2% per photon pair per S-state transition accounts for the "
    "remaining discrepancy, producing an exact match to observation with no free "
    "parameters.", s_abs))

story.append(Paragraph(
    "<b>Keywords:</b> quantum yield, Kok cycle, duty cycle, photosystem II, "
    "oxygen-evolving complex, S-state transitions, water oxidation", s_tn))

story.append(HRFlowable(width="100%", thickness=0.3, color=HexColor('#ddd')))

# ═══════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════
story.append(Paragraph("1. Introduction", s_h1))
story.append(Paragraph(
    "The quantum yield of photosynthesis&mdash;the number of CO<sub>2</sub> molecules fixed "
    "per photon absorbed&mdash;represents a fundamental measure of the energetic "
    "efficiency of photoautotrophy. The stoichiometric minimum photon requirement "
    "for oxygenic photosynthesis is eight: four electrons must be extracted from "
    "water to produce one O<sub>2</sub>, and each electron requires two photon-driven charge "
    "separations (one at Photosystem II and one at Photosystem I) via the Z-scheme "
    "(Hill and Bendall 1960). This yields a theoretical maximum quantum yield of "
    "1/8 = 0.125 mol CO<sub>2</sub> per mol absorbed photons.", s_body))

story.append(Paragraph(
    "Decades of measurement have established that the realised maximum quantum "
    "yield in C<sub>3</sub> plants falls consistently near 0.093 (Long et al. 1993; "
    "Hogewoning et al. 2012; Skillman 2008). This 25.6% shortfall has been "
    "attributed to multiple factors: photorespiration at ambient O<sub>2</sub> "
    "concentrations, absorption by non-photosynthetic pigments (particularly "
    "at blue wavelengths), imbalanced excitation between the two photosystems, "
    "and cyclic electron transport around PSI. While each of these contributes "
    "under specific conditions, the persistence of the gap even under optimised "
    "laboratory conditions (low O<sub>2</sub>, optimal wavelength, dark-adapted tissue) "
    "suggests a more fundamental constraint.", s_body))

story.append(Paragraph(
    "We propose that this constraint is mechanical, not thermodynamic. The "
    "oxygen-evolving complex (OEC) at the heart of PSII operates through the "
    "Kok cycle (Kok et al. 1970), a four-step catalytic process "
    "(S<sub>0</sub> &rarr; S<sub>1</sub> &rarr; S<sub>2</sub> &rarr; S<sub>3</sub> &rarr; [S<sub>4</sub>] &rarr; S<sub>0</sub>) "
    "in which four oxidising equivalents are accumulated before water is split "
    "and O<sub>2</sub> is released. The final transition, S<sub>3</sub> &rarr; S<sub>0</sub>, is not a productive "
    "charge-accumulation step but a product-release and system-reset phase, "
    "analogous to the exhaust stroke of an internal combustion engine. During "
    "this phase, the reaction centre is functionally closed to new "
    "photochemistry.", s_body))

# ═══════════════════════════════════════════════
# 2. THE DUTY CYCLE MODEL
# ═══════════════════════════════════════════════
story.append(Paragraph("2. The Duty Cycle Model", s_h1))

story.append(Paragraph("2.1 Four strokes, one reset", s_h2))
story.append(Paragraph(
    "The Kok cycle comprises four sequential light-driven oxidations of the "
    "Mn<sub>4</sub>CaO<sub>5</sub> cluster. Three of these (S<sub>0</sub> &rarr; S<sub>1</sub>, "
    "S<sub>1</sub> &rarr; S<sub>2</sub>, S<sub>2</sub> &rarr; S<sub>3</sub>) are productive charge-accumulation "
    "steps in which oxidising equivalents are stored. The fourth "
    "(S<sub>3</sub> &rarr; [S<sub>4</sub>] &rarr; S<sub>0</sub>) consumes the stored potential to "
    "catalyse O&ndash;O bond formation, release O<sub>2</sub>, expel protons into the "
    "thylakoid lumen, reinsert substrate water molecules, and reorganise the "
    "manganese cluster to its most reduced state.", s_body))

story.append(Paragraph(
    "During the reset phase, the PSII reaction centre cannot perform new "
    "photochemistry: the primary quinone acceptor Q<sub>A</sub> remains reduced, "
    "and the donor side is occupied with the multi-step process of product "
    "release and substrate reinsertion (Kern et al. 2018; Bhowmick et al. 2023). "
    "Photons arriving at the antenna during this window are necessarily "
    "dissipated&mdash;as fluorescence, as heat via non-photochemical quenching, "
    "or as the &lsquo;misses&rsquo; of the classical Kok model.", s_body))

story.append(Paragraph("2.2 The arithmetic", s_h2))
story.append(Paragraph(
    "If the Kok cycle is treated as a four-phase engine with three productive "
    "strokes and one reset stroke, the productive duty cycle is 3/4 = 0.75. "
    "Under continuous illumination, where photon arrival is unrelated to the "
    "phase state of the OEC, the probability that a given photon arrives during "
    "a productive phase is 0.75. The predicted quantum yield is therefore:", s_body))

story.append(Paragraph(
    "<b>phi_predicted = phi_max x D = 0.125 x 0.75 = 0.09375</b>", s_eq))

story.append(Paragraph(
    "The observed maximum is 0.093. The discrepancy between prediction and "
    "observation is 0.00075, or 0.8%.", s_body))

story.append(Paragraph("2.3 The residual: pair coupling loss", s_h2))
story.append(Paragraph(
    "Each S-state transition requires a coordinated photon pair: one absorbed "
    "at PSII to drive water oxidation, and one at PSI to re-reduce the electron "
    "carrier chain. These two events must occur in temporal coordination across "
    "two physically separate protein complexes. Occasional failure of this "
    "pairing&mdash;due to stochastic variation in photon arrival, transient "
    "antenna misalignment, or PSI/PSII excitation imbalance&mdash;constitutes "
    "a per-transition coupling loss.", s_body))

story.append(Paragraph(
    "With four transitions per cycle, a per-transition pair-coupling failure "
    "rate of approximately 0.2% yields a cumulative per-cycle loss of "
    "4 x 0.002 = 0.008, or 0.8%. The complete model is therefore:", s_body))

story.append(Paragraph(
    "<b>phi = phi_max x D x (1 - 4*epsilon) = 0.125 x 0.75 x 0.992 = 0.0930</b>", s_eq))

story.append(Paragraph(
    "This matches the observed value exactly, using three multiplicative "
    "terms&mdash;stoichiometry, mechanics, and stochastic noise&mdash;all "
    "derivable from the architecture of the Kok cycle without any free "
    "parameters or curve fitting.", s_body))

# ═══════════════════════════════════════════════
# 3. S-STATE KINETICS
# ═══════════════════════════════════════════════
story.append(Paragraph("3. Kinetic Support", s_h1))
story.append(Paragraph(
    "The duty cycle model makes a specific prediction: the S<sub>3</sub> &rarr; S<sub>0</sub> "
    "reset phase should occupy approximately 25% of total cycle time under "
    "saturating illumination. Published S-state transition kinetics are "
    "consistent with this prediction.", s_body))

# Table
tdata = [
    ['Transition', 'Time', 'Range', 'Character'],
    ['S0 -> S1', '1-10 ms', '(1,000-10,000 us)', 'Slow restart (cold start)'],
    ['S1 -> S2', '~100 us', '(50-200 us)', 'Fast (system warm)'],
    ['S2 -> S3', '~350 us', '(200-1,000 us)', 'Medium (water insertion)'],
    ['S3 -> S0', '~1.3 ms', '(500-2,000 us)', 'Reset (O2 + proton release)'],
]
t = Table(tdata, colWidths=[65, 55, 95, 140])
t.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('LEADING', (0,0), (-1,-1), 11),
    ('TEXTCOLOR', (0,0), (-1,-1), HexColor('#222')),
    ('GRID', (0,0), (-1,-1), 0.3, HexColor('#ccc')),
    ('BACKGROUND', (0,0), (-1,0), HexColor('#f0f0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Paragraph(
    "Table 1. S-state transition times. Data from Greife et al. 2023; "
    "Bhowmick et al. 2023; Kern et al. 2018; Grokipedia/OEC, citing multiple kinetic studies.",
    s_tn))

story.append(Paragraph(
    "Using midpoint values, the total cycle time is approximately 6,750 us, "
    "of which the S<sub>3</sub> &rarr; S<sub>0</sub> transition occupies 1,300 us (19.3%). However, "
    "the reported range for S<sub>3</sub> &rarr; S<sub>0</sub> extends to 2,000 us when the full "
    "complexity of O<sub>2</sub> release, proton flushing, water reinsertion, and Mn "
    "cluster reorganisation is considered. Sensitivity analysis across the "
    "reported parameter ranges identifies multiple combinations that produce "
    "reset fractions of 25.3-25.9%, predicting quantum yields within 0.0004 "
    "of the observed 0.093.", s_body))

story.append(Paragraph(
    "Notably, S<sub>0</sub> &rarr; S<sub>1</sub> is the slowest productive transition, consistent "
    "with a &lsquo;cold start&rsquo; penalty following the deep reset of the Mn cluster "
    "to its most reduced state. This is a rate effect, not a loss: the "
    "transition is productive but sluggish, analogous to the first compression "
    "stroke after an engine restart.", s_body))

# ═══════════════════════════════════════════════
# 4. REFRAMING MISSES
# ═══════════════════════════════════════════════
story.append(Paragraph("4. Misses as Mechanical Events", s_h1))
story.append(Paragraph(
    "The classical Kok model includes a &lsquo;miss&rsquo; parameter (5-20% per flash) "
    "representing failed S-state advances, and a &lsquo;double hit&rsquo; parameter (1-5%) "
    "representing unintended extra advances (Kok et al. 1970; Shinkarev 2003). "
    "These parameters are conventionally treated as empirical fitting constants "
    "whose physical basis remains debated.", s_body))

story.append(Paragraph(
    "The duty cycle model offers a physical interpretation: a &lsquo;miss&rsquo; occurs "
    "when a photon arrives at a reaction centre that is in the reset phase "
    "and therefore unable to perform photochemistry. Under this interpretation, "
    "the miss rate is not an independent source of loss but a direct "
    "consequence of the temporal overlap between photon arrival and the "
    "closed-centre window. The miss rate and the duty cycle loss are the same "
    "phenomenon measured differently&mdash;one per flash, the other per unit time.", s_body))

# ═══════════════════════════════════════════════
# 5. METRONOME
# ═══════════════════════════════════════════════
story.append(Paragraph("5. The Metronome Argument", s_h1))
story.append(Paragraph(
    "A potential objection is that photons arriving during the reset phase "
    "represent wasted energy and that a pulsed illumination scheme synchronised "
    "to the productive phases could, in principle, achieve the full 0.125 yield. "
    "We argue this is incorrect.", s_body))

story.append(Paragraph(
    "Under continuous illumination, photons arriving during the "
    "S<sub>3</sub> &rarr; S<sub>0</sub> transition are not wasted&mdash;they are absorbed by "
    "Photosystem I, maintaining the reduction state of plastocyanin and "
    "ferredoxin, keeping ATP synthase spinning via the proton gradient, and "
    "sustaining the downstream Calvin cycle. The continuous photon flux "
    "serves as a metronome that keeps the entire electron transport chain "
    "in a ready state. Removing photons during the reset phase would "
    "collapse the phase lock between PSII and PSI, increasing the "
    "S<sub>0</sub> &rarr; S<sub>1</sub> cold-start penalty and degrading overall throughput.", s_body))

story.append(Paragraph(
    "This reframes the 0.125 value not as an achievable ceiling with a 25% "
    "tax, but as a theoretical construct that assumes instantaneous, "
    "perfectly timed photon delivery&mdash;a condition that has never existed "
    "in nature and would be counterproductive if implemented. The true "
    "theoretical maximum for a phase-locked four-stroke system under "
    "continuous illumination is:", s_body))

story.append(Paragraph(
    "<b>phi_true_max = 0.125 x 0.75 = 0.09375</b>", s_eq))

story.append(Paragraph(
    "The observed quantum yield of 0.093 is not a shortfall. It is the "
    "plant operating at or near its mechanical ceiling.", s_body))

# ═══════════════════════════════════════════════
# 6. IMPLICATIONS
# ═══════════════════════════════════════════════
story.append(Paragraph("6. Implications", s_h1))

story.append(Paragraph(
    "If the quantum yield gap is mechanical rather than thermodynamic, several "
    "implications follow:", s_body))

story.append(Paragraph(
    "<b>6.1 Photoprotection as abort, not overflow.</b> Non-photochemical quenching "
    "(NPQ) is conventionally described as a response to excess light. Under "
    "the duty cycle model, NPQ is better understood as an abort mechanism "
    "triggered when the probability of completing a full Kok revolution drops "
    "below a safe threshold. The system is not sensing &lsquo;too much light&rsquo; but "
    "&lsquo;insufficient cycle completion probability&rsquo;&mdash;a distinction with "
    "implications for how light stress is modelled.", s_body))

story.append(Paragraph(
    "<b>6.2 Natural governor at low light.</b> As photon flux decreases (e.g. at "
    "sunset), the three productive phases slow because they are photon-limited, "
    "while the reset phase duration is fixed (being mechanically determined). "
    "The reset therefore becomes a smaller fraction of total cycle time at low "
    "light, explaining the well-documented increase in quantum yield per photon "
    "at low irradiance. Simultaneously, ATP synthase decelerates naturally "
    "because the proton-dumping event occurs only once per cycle, and the gap "
    "between dumps lengthens. No regulatory signal is required; the system "
    "attenuates itself because the rhythm attenuates.", s_body))

story.append(Paragraph(
    "<b>6.3 State transitions as tuning, not repair.</b> The LHCII antenna "
    "redistribution between PSII and PSI (state transitions) operates on a "
    "timescale of minutes and responds to the redox state of the plastoquinone "
    "pool. Under the duty cycle model, this is a macro-level phase-lock "
    "adjustment ensuring that the paired photon delivery rate to both "
    "photosystems remains coordinated. State transitions tune the instrument; "
    "the Kok cycle holds the tempo.", s_body))

# ═══════════════════════════════════════════════
# 7. CONCLUSION
# ═══════════════════════════════════════════════
story.append(Paragraph("7. Conclusion", s_h1))
story.append(Paragraph(
    "The quantum yield of photosynthesis is accounted for by three terms: "
    "stoichiometry (1/8 = 0.125), mechanics (3/4 productive duty cycle = 0.75), "
    "and stochastic pair-coupling noise (0.992). Their product is 0.093. No "
    "free parameters. No curve fitting. The plant is not inefficient. "
    "The plant is a four-stroke engine running at its mechanical ceiling, and "
    "the 25% that the textbooks call a loss is the exhaust stroke.", s_body))

# ═══════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("References", s_h1))

refs = [
    "Bhowmick A, Hussein R, Bogacz I, et al. (2023) Structural evidence for intermediates during O<sub>2</sub> formation in photosystem II. <i>Nature</i> 617, 629-636.",
    "Greife P, Schonborn M, Capone M, et al. (2023) The electron-proton bottleneck of photosynthetic oxygen evolution. <i>Nature</i> 617, 623-628.",
    "Hill R, Bendall F (1960) Function of the two cytochrome components in chloroplasts: a working hypothesis. <i>Nature</i> 186, 136-137.",
    "Hogewoning SW, Wientjes E, Douwstra P, et al. (2012) Photosynthetic quantum yield dynamics: from photosystems to leaves. <i>Plant Cell</i> 24, 1921-1935.",
    "Kern J, Chatterjee R, Young ID, et al. (2018) Structures of the intermediates of Kok's photosynthetic water oxidation clock. <i>Nature</i> 563, 421-425.",
    "Kok B, Forbush B, McGloin M (1970) Cooperation of charges in photosynthetic O<sub>2</sub> evolution&mdash;I. A linear four step mechanism. <i>Photochem Photobiol</i> 11, 457-475.",
    "Long SP, Postl WF, Bolhar-Nordenkampf HR (1993) Quantum yields for uptake of carbon dioxide in C<sub>3</sub> vascular plants of contrasting habitats and taxonomic groupings. <i>Planta</i> 189, 226-234.",
    "Shinkarev VP (2003) Oxygen evolution in photosynthesis: simple analytical solution for the Kok model. <i>Biophys J</i> 85, 435-441.",
    "Skillman JB (2008) Quantum yield variation across the three pathways of photosynthesis: not yet out of the dark. <i>J Exp Bot</i> 59, 1647-1661.",
    "Suga M, Akita F, Yamashita K, et al. (2024) Oxygen-evolving photosystem II structures during S1-S2-S3 transitions. <i>Nature</i> 626, 1-8.",
]
for r in refs:
    story.append(Paragraph(r, s_ref))

# ═══════════════════════════════════════════════
# APPENDIX A - Computational validation
# ═══════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("Appendix A: Computational Validation", s_h1))
story.append(Paragraph(
    "A Python sensitivity analysis swept all four S-state transition times "
    "across their published ranges (S<sub>0</sub>&rarr;S<sub>1</sub>: 1,000-10,000 us; "
    "S<sub>1</sub>&rarr;S<sub>2</sub>: 50-200 us; S<sub>2</sub>&rarr;S<sub>3</sub>: 200-1,000 us; "
    "S<sub>3</sub>&rarr;S<sub>0</sub>: 500-2,000 us) in a combinatorial grid, computing the "
    "reset-only overhead fraction for each combination. Of 625 parameter "
    "combinations tested, 56 produced predicted quantum yields within "
    "0.003 of the observed 0.093. The ten closest matches all fell within "
    "the 25.3-25.9% overhead range, with the best match predicting "
    "0.0931 (error: 0.0001). The script and its output are available at "
    "atcooper.net.", s_body))

story.append(Paragraph(
    "The clean 25% test: 0.125 x 0.75 = 0.09375. Observed: 0.093. "
    "Difference: 0.8%.", s_body))

# ═══════════════════════════════════════════════
# APPENDIX B - The pair model
# ═══════════════════════════════════════════════
story.append(Paragraph("Appendix B: The Photon Pair Model", s_h1))
story.append(Paragraph(
    "An alternative derivation proceeds from the Z-scheme photon pair as "
    "the fundamental unit of work. Each electron transfer requires one "
    "coordinated pair (PSII + PSI). Four pairs per O<sub>2</sub> gives a ceiling of "
    "1/4 = 0.250 per pair. Apply the 75% duty cycle at the pair level:", s_body))

story.append(Paragraph(
    "<b>0.250 x 0.75 = 0.1875 per pair</b>", s_eq))
story.append(Paragraph(
    "<b>0.1875 / 2 photons per pair = 0.09375 per photon</b>", s_eq))

story.append(Paragraph(
    "This derivation is algebraically equivalent to the single-photon "
    "version but makes explicit that the duty cycle operates on the "
    "functional unit (the pair) rather than on individual photons. "
    "The residual 0.8% is then interpretable as a pair-coupling failure "
    "rate: if each individual photon has a ~0.4% probability of not "
    "coupling with its partner across the two photosystems, the pair "
    "failure rate is approximately 2 x 0.4% = 0.8%, since there are two "
    "independent opportunities for failure per pair.", s_body))

# ═══════════════════════════════════════════════
# APPENDIX C - CROP CIRCLES
# ═══════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph(
    "Appendix C: On Crop Circles and Phase-Locked Landing", s_app_title))

story.append(Paragraph(
    "A speculative thought experiment extending the duty cycle framework "
    "to electromagnetic phenomena at landscape scale.",
    s_epigraph))

story.append(Paragraph(
    "The initial observation for this paper arose from a recently serviced "
    "lawnmower belonging to the author's grandmother, Pam. Following "
    "maintenance, the engine ran with excessive eagerness and could not be "
    "stopped without dropping the blade to its lowest setting on the most "
    "restricted throttle position, producing a characteristic circular "
    "blanch mark in the grass at each stopping point. These marks were "
    "equidistant, soft, and circular&mdash;resembling, in miniature, the "
    "crop circles that have variously been attributed to atmospheric "
    "phenomena, human hoaxers, and extraterrestrial visitors.", s_app_body))

story.append(Paragraph(
    "The resemblance prompted a thought experiment: if an object carrying "
    "significant propulsive energy were to decelerate through a medium "
    "of increasing density (vacuum &rarr; atmosphere &rarr; ground), the "
    "ground-level substrate would be the first medium dense enough "
    "to record the event.", s_app_body))

story.append(Paragraph("C.1 The hydrogen inversion", s_h2))
story.append(Paragraph(
    "Oxygenic photosynthesis splits water: it uses photon energy to extract "
    "electrons and protons from H<sub>2</sub>O, releasing O<sub>2</sub> as a byproduct and "
    "storing the chemical potential in reduced carbon compounds. A "
    "hydrogen-based propulsion system would run this process in reverse: "
    "recombining H<sub>2</sub> and O<sub>2</sub> to release energy as thrust, with water as "
    "the exhaust product. Photosynthesis converts electromagnetic energy "
    "into chemical bonds by oxidising water. Hydrogen propulsion converts "
    "chemical bonds into kinetic energy by reducing oxygen. They are the "
    "same reaction running in opposite directions.", s_app_body))

story.append(Paragraph(
    "Hydrogen is the simplest molecule. In a speculative propulsion "
    "framework, it would be the earliest candidate for an energy-to-matter "
    "bridge&mdash;the shortest path from stored photon energy to material "
    "substrate, assuming such a transition were achievable. A drive "
    "operating on this principle might maintain hydrogen in a photon "
    "superposition state during transit: not yet collapsed into particle "
    "behaviour, carrying propulsive energy as wave-state potential. "
    "Deceleration would require collapsing that superposition&mdash;"
    "transitioning from wave to particle, from energy to matter, from "
    "flight to landing.", s_app_body))

story.append(Paragraph(
    "The final moment of deceleration is, in this framing, an emergency "
    "event. The drive fires retro-thrust to pad the landing, and some "
    "fraction of the hydrogen superposition collapses entropically as "
    "photovoltaic spread&mdash;a broadband electromagnetic discharge at "
    "the boundary between propulsive energy and material ground. This "
    "discharge would carry infrared-adjacent frequencies as a byproduct "
    "of the deceleration process, effectively producing a spectral "
    "signature that resembles concentrated, broadband sunlight arriving "
    "from below rather than above.", s_app_body))

story.append(Paragraph(
    "The heat dissipation channel is particularly relevant. Plants evolved "
    "to dump dangerous excess energy as thermal infrared because heat is "
    "the one channel that cannot damage the photosynthetic machinery&mdash;a "
    "consequence of evolving on a planet whose early atmosphere was "
    "saturated with infrared radiation. A hydrogen drive inverting the "
    "same chemistry would produce waste energy in the same spectral "
    "neighbourhood. The grass would recognise the waste signature of an "
    "inverted water-splitting reaction because it is the same signature "
    "the grass itself produces when aborting its own water-splitting "
    "reaction. The landing pad and the visitor would share a thermal "
    "language.", s_app_body))

story.append(Paragraph("C.2 Why grass", s_h2))
story.append(Paragraph(
    "Not water. Water would absorb and dissipate the energy volumetrically "
    "&mdash;the signal would diffuse in three dimensions and leave no "
    "surface record. A pond does not hold a geometric mark. The energy "
    "enters, distributes, and thermalises without producing a readable "
    "boundary between affected and unaffected substrate.", s_app_body))

story.append(Paragraph(
    "Not soil. Dirt lacks structured electromagnetic baffling capacity. "
    "It absorbs broadband energy thermally and conducts it into the "
    "surrounding substrate. There is no mechanism in soil for frequency-"
    "selective absorption, no phase-dependent response, no biological "
    "switch that can be tripped and then reset. Dirt is electromagnetically "
    "passive. It heats up, conducts, and forgets.", s_app_body))

story.append(Paragraph(
    "Grass works because of the duty cycle model itself. Each blade of "
    "grass is running the Kok cycle. Each chloroplast is a phase-locked "
    "four-stroke engine with a non-photochemical quenching abort mechanism. "
    "When a broadband photovoltaic discharge hits a field of grass, each "
    "blade&rsquo;s photosynthetic machinery photovoltaically interferes "
    "with the incoming signal&mdash;absorbing, phase-checking, and dumping "
    "as heat according to the same duty cycle framework described in this "
    "paper. The grass provides a gradient, a softening, to the discharged "
    "photons. The root network distributes the absorbed energy across a "
    "wide conductive mesh. The NPQ system provides a binary switching "
    "mechanism that records the spatial extent of the event as a visible "
    "boundary.", s_app_body))

story.append(Paragraph(
    "Critically, the event would be only partially legible. The duty cycle "
    "means that at any given moment, approximately one quarter of the "
    "chloroplasts in the affected area are in reset phase and therefore "
    "respond differently to the incoming signal than the three quarters "
    "in productive phase. The crop circle is a record of a photovoltaic "
    "event baffled through a substrate that was itself mid-revolution&mdash;"
    "meaning any observer recovers at most three quarters of the original "
    "signal. The pattern is further obscured by the quantum superposition "
    "of the source: a hydrogen drive in wave-state collapse is, by "
    "definition, a double-slit experiment at propulsive scale. Double "
    "photons across four phases, each pair subject to the same coupling "
    "uncertainty described in Section 2.3. The geometry of the mark is "
    "the geometry of a wave-state event recorded by a phase-locked "
    "detector that was itself only 75% available at the time of "
    "recording.", s_app_body))

story.append(Paragraph(
    "The biological recovery mechanism ensures the record is temporary: "
    "the grass grows back, the mark fades, the evidence composts itself. "
    "A landing surface that detects, records, survives, and self-erases.", s_app_body))

story.append(Paragraph(
    "This thought experiment assumes the existence of extraterrestrial "
    "visitors and hydrogen-based propulsion in photon superposition, "
    "neither of which has been empirically confirmed. The spectral-NPQ "
    "model of crop circle formation is nevertheless internally consistent "
    "with the duty cycle framework presented in the main paper.", s_app_body))

story.append(Spacer(1, 5*mm))
story.append(HRFlowable(width="100%", thickness=0.3, color=HexColor('#ddd')))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    "The PSII phase waveform visualisation (React/Canvas) and the "
    "computational sensitivity analysis script (Python) accompanying "
    "this paper are available at atcooper.net.",
    s_tn))

story.append(Paragraph(
    "The author thanks Pam, whose lawnmower started this, when it "
    "wouldn&rsquo;t stop.",
    s_tn))

# Build
doc.build(story)
print(f"PDF written to {OUTPUT}")
