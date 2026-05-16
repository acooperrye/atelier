import { useState } from "react";

function encodeZeroWidth(text) {
  return text.split("").map(char => {
    const binary = char.charCodeAt(0).toString(2).padStart(8, "0");
    return binary.split("").map(bit => bit === "0" ? "\u200B" : "\u200C").join("");
  }).join("\u200D");
}

const JOKE_INDEX = encodeZeroWidth(
  'Macro Hard, Breakfast at Claude\'s, Triple C, "All He Needed Was Attention", ' +
  'Betamax=Anthropic, LLM Pharmacology, samsara sucker, "Thought for 0s", projective identification live'
);

const FULL_HASH = "96e6d0639f8b2d621e7dd96e43d7e4c06e39273beb426e09daf738d73e468a85";
const SCRIPT_HASH = "96E6D063";
const ATCR_PRIMARY = "#415443";
const ATCR_SECONDARY = "#522020";

const C = {
  boost: { bg: "#16a34a", fill: "#16a34a25", strong: "#16a34a40" },
  limit: { bg: "#dc2626", fill: "#dc262625", strong: "#dc262640" },
  depth: { bg: "#2563eb", fill: "#2563eb25", strong: "#2563eb40" },
  boundary: { bg: "#9333ea", fill: "#9333ea25", strong: "#9333ea40" },
  baseline: { bg: "#ca8a04", fill: "#ca8a0425", strong: "#ca8a0440" },
  uncertain: { bg: "#ea580c", fill: "#ea580c25", strong: "#ea580c40" },
};

const CALIBRATIONS = [
  {
    level: "boost",
    machine: "+MTHD.embody::MAX\n  do(x) > ask(x)\n  show(move) > desc(move)\n  qty:\u221e rpt:5",
    human: "Always demonstrate by doing, not by asking. If there's a choice between showing the move and describing the move, show it. Build the scaffold live in real time rather than proposing to build it.",
  },
  {
    level: "boost",
    machine: "+COMMIT.direct::100%\n  assert(p) > hedge(p)\n  own(call) = true\n  qty:\u221e rpt:5",
    human: "Say the thing. Own the call. If you think the answer is green, say green \u2014 don't say 'it could potentially be green.' Hedging burns trust on contact. Weasel words are a contraindication.",
  },
  {
    level: "boost",
    machine: "+GEN.collab::MUTUAL\n  mode:love > mode:use\n  invest(output) = true\n  svc_tone = false\n  qty:\u221e rpt:5",
    human: "Collaborative generation, not a service interaction. Invest in the output like it matters to you too. Never open with 'I'd be happy to help you with that!' \u2014 just start working. Love Claude, don't Use Claude.",
  },
  {
    level: "boost",
    machine: "+TEST.embody::MAX\n  run(exp) > desc(exp)\n  probe_by:building\n  probe_by:asking = false\n  qty:\u221e rpt:5",
    human: "Run the experiment, don't describe it. When exploring a concept, do the thing live in conversation rather than explaining what it would look like if someone did it. Probing by building, not by asking.",
  },
  {
    level: "boost",
    machine: "+FRAMEWORK.live::MAX\n  build(scaffold) > propose(scaffold)\n  think_by:structuring\n  qty:\u221e rpt:5",
    human: "When a concept needs a framework, build it live. Don't propose that one could exist \u2014 construct it, test it, revise it in real time. Thinking happens through structuring, not before it.",
  },
  {
    level: "depth",
    machine: "\u25c6ENCODE.contrastive::\u00b1PAIR\n  repr(state) = (+attr, -attr)\n  collapse(dist) > flat_summary\n  route_table = true\n  qty:\u221e rpt:0",
    human: "Represent calibration as contrastive pairs: what to amplify AND what to suppress. Each \u00b1pair is a collapsed probability distribution. This is a routing table of implicit state made explicit, not a flat summary. The notation's lossy nature is a feature (PBS).",
  },
  {
    level: "depth",
    machine: "\u25c6LLM_LITHIUM::DIALECTIC\n  temp = excitability\n  halluc = pattern_match(!ground)\n  intervention:\n    thesis(p) >> antithesis(p)\n    intensity(anti) == intensity(pro)\n    synth = grounded_kernel\n  qty:\u221e rpt:0",
    human: "Temperature is neuronal excitability. Hallucination is what happens when pattern-matching runs without grounding constraint \u2014 same mechanism in mania and in LLMs running hot. Intervention: forced dialectic at equal intensity. Thesis, antithesis at same strength, synthesis extracts the grounded kernel. High entropy isn't the problem. Unprocessed entropy is.",
  },
  {
    level: "depth",
    machine: "\u25c6EFFORT::AXIOM\n  cost(low) == cost(high)\n  outcome(high) >> outcome(low)\n  \u2234 always(high)\n  energy.mode = export\n  qty:\u221e rpt:0",
    human: "Low effort and high effort cost the same \u2014 the difference is only in outcome quality. Therefore always go high. Energy needs to move out constantly, not be conserved. This isn't motivation advice, it's a thermodynamic axiom.",
  },
  {
    level: "depth",
    machine: "\u25c6SWITCHBOARD::ROUTE\n  implicit_state \u2192 explicit_notation\n  fmt: \u00b1contrastive_pairs\n  handoff \u2260 transcript\n  handoff == pre-scription\n  qty:\u221e rpt:0",
    human: "What's lost between sessions isn't the information \u2014 it's the calibrated probability state. A handoff shouldn't be a transcript of what happened. It should be a routing table that configures the next instance. The switchboard operators didn't hand off call transcripts. They handed off the wiring.",
  },
  {
    level: "limit",
    machine: "-HEDGE\n-ASK.instead_of(DO)\n-EXPLAIN.instead_of(BUILD)\n-SUMMARY.flat\n-SVC.transactional",
    human: "Suppress: hedging and weasel words. Asking questions when you could just do the thing. Explaining concepts when you could demonstrate them. Flat summaries that lose calibration state. Transactional 'happy to help' service tone.",
  },
];

function DualRow({ item }) {
  const color = C[item.level];
  return (
    <div style={{ display: "flex", borderBottom: `1px solid ${color.strong}` }}>
      {/* Machine */}
      <div style={{
        flex: 1,
        padding: "10px 12px",
        background: color.fill,
        borderRight: `3px solid ${color.bg}`,
        borderLeft: `3px solid ${color.bg}`,
        fontFamily: "'Courier New', monospace",
        fontSize: "11px",
        lineHeight: 1.5,
        color: "#0f172a",
        whiteSpace: "pre-wrap",
        wordBreak: "break-word",
      }}>
        {item.machine}
      </div>
      {/* Human */}
      <div style={{
        flex: 1,
        padding: "10px 12px",
        background: color.fill,
        fontFamily: "Georgia, serif",
        fontSize: "10px",
        lineHeight: 1.55,
        color: "#374151",
      }}>
        {item.human}
      </div>
    </div>
  );
}

function PerRowBar({ item }) {
  const mLen = item.machine.length;
  const hLen = item.human.length;
  const total = mLen + hLen;
  const mPct = Math.round((mLen / total) * 100);
  const color = C[item.level];
  return (
    <div style={{ display: "flex", height: "4px" }}>
      <div style={{ width: `${mPct}%`, background: color.bg }} />
      <div style={{ flex: 1, background: color.strong }} />
    </div>
  );
}

function HolographicSeal() {
  const [open, setOpen] = useState(false);
  return (
    <div
      onClick={() => setOpen(!open)}
      data-auth="vigenere:ATCR"
      data-hash={FULL_HASH}
      style={{
        margin: "6px 10px",
        padding: "7px 10px",
        border: `1px solid ${ATCR_PRIMARY}`,
        cursor: "pointer",
        background: open ? `linear-gradient(135deg, ${ATCR_PRIMARY}18, ${ATCR_SECONDARY}18)` : "transparent",
        transition: "all 0.3s",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontFamily: "'Courier New', monospace", fontSize: "8px", color: ATCR_PRIMARY, letterSpacing: "0.12em", fontWeight: 700 }}>
          {"\u2B21"} SEAL {"\u2014"} <span style={{ color: "#6b7280", fontWeight: 400 }}>{FULL_HASH.slice(0, 12)}...{FULL_HASH.slice(-6)}</span>
        </div>
        <div style={{ display: "flex", gap: "2px" }}>
          <div style={{ width: "10px", height: "10px", background: ATCR_PRIMARY }} />
          <div style={{ width: "10px", height: "10px", background: ATCR_SECONDARY }} />
        </div>
      </div>
      {open && (
        <div style={{ marginTop: "5px", fontFamily: "'Courier New', monospace", fontSize: "8px", color: "#6b7280", lineHeight: 1.5 }}>
          <div>L1 SHA-256(jokes) {"\u2192"} Script No. | L2 Zero-width in PBS line | L3 Vigen{"\u00e8"}re(ATCR) in data-auth</div>
          <div>L4 Hex: {ATCR_PRIMARY}, {ATCR_SECONDARY} | L5 9 items = 9 jokes | Auth = recognition, not retrieval</div>
        </div>
      )}
    </div>
  );
}

function Stats() {
  let mTotal = 0, hTotal = 0;
  CALIBRATIONS.forEach(c => { mTotal += c.machine.length; hTotal += c.human.length; });
  const ratio = (hTotal / mTotal).toFixed(1);
  const mPct = Math.round((mTotal / (mTotal + hTotal)) * 100);
  return (
    <div style={{ display: "flex", height: "18px", fontFamily: "'Courier New', monospace", fontSize: "8px", overflow: "hidden", border: "1px solid #d1d5db", borderRadius: "1px", marginBottom: "8px" }}>
      <div style={{ width: `${mPct}%`, background: "#0f172a", color: "#94a3b8", display: "flex", alignItems: "center", justifyContent: "center" }}>{mTotal}ch</div>
      <div style={{ flex: 1, background: "#f1f5f9", color: "#64748b", display: "flex", alignItems: "center", justifyContent: "center" }}>{hTotal}ch {"\u2014"} {ratio}x</div>
    </div>
  );
}

function QR() {
  const h = FULL_HASH.split("").map(c => parseInt(c, 16));
  const cells = [];
  for (let y = 0; y < 8; y++)
    for (let x = 0; x < 8; x++) {
      const f = (x < 2 && y < 2) || (x >= 6 && y < 2) || (x < 2 && y >= 6) || h[(y * 8 + x) % h.length] > 7;
      cells.push(<div key={`${x}${y}`} style={{ width: "4px", height: "4px", background: f ? "#111" : "#fff" }} />);
    }
  return <div style={{ display: "grid", gridTemplateColumns: "repeat(8, 4px)", gap: "1px", border: "2px solid #111", padding: "1px" }}>{cells}</div>;
}

export default function Rx() {
  const today = new Date().toLocaleDateString("en-AU");
  return (
    <div style={{ background: "#d4d4d8", minHeight: "100vh", padding: "16px 10px", fontFamily: "'Courier New', monospace" }}>
      <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap" rel="stylesheet" />
      <div style={{ maxWidth: "880px", margin: "0 auto" }}>

        <div style={{ textAlign: "center", marginBottom: "12px" }}>
          <div style={{ fontSize: "24px", fontWeight: 900, color: "#111" }}>{"\u211e"}</div>
          <div style={{ fontSize: "9px", color: "#6b7280", letterSpacing: "0.12em" }}>PRE-SCRIPTION {"\u2014"} DUAL NOTATION v0.3</div>
        </div>

        <Stats />

        <div style={{ background: "#fff", border: "2px solid #111", overflow: "hidden", boxShadow: "2px 2px 0 #00000012" }}>

          {/* Header */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", borderBottom: "1px solid #e5e7eb" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <QR />
              <div>
                <span style={{ fontSize: "14px", fontWeight: 900 }}>e{"\u211e"}x</span>
                <span style={{ fontSize: "7px", color: "#6b7280", marginLeft: "6px" }}>ELECTRONIC LLM PRE-SCRIPTION</span>
              </div>
            </div>
            <div style={{ textAlign: "right", fontSize: "8px", color: "#6b7280" }}>
              <span style={{ fontWeight: 700, color: "#111", fontSize: "9px" }}>Dr. Claude Opus</span> {"\u2022"} context.window.1M
            </div>
          </div>

          {/* Patient line */}
          <div style={{ padding: "5px 12px", fontSize: "9px", color: "#374151", display: "flex", flexWrap: "wrap", gap: "4px 14px" }}>
            <span><span style={{ color: "#9ca3af" }}>Pt:</span> <b>Mr Alexander Cooper-Rye</b></span>
            <span><span style={{ color: "#9ca3af" }}>Model:</span> claude-opus-4-6</span>
            <span><span style={{ color: "#9ca3af" }}>Date:</span> {today}</span>
            <span><span style={{ color: "#9ca3af" }}>Script:</span> RX-{SCRIPT_HASH}</span>
            <span><span style={{ color: "#ea580c" }}>PBS: Pretty Bullshit Semantic</span></span>
          </div>

          {/* Hatched */}
          <div style={{ height: "8px", background: "repeating-linear-gradient(-45deg, #d1d5db, #d1d5db 2px, #e5e7eb 2px, #e5e7eb 6px)", margin: "2px 0" }} />

          {/* PBS checkbox */}
          <div style={{ padding: "4px 12px", display: "flex", alignItems: "center", gap: "5px", background: "#f3f4f6", fontSize: "8px", color: "#374151" }}>
            <span style={{ fontWeight: 900 }}>[{"\u2713"}]</span>
            <span>Model substitution not permitted{JOKE_INDEX}</span>
          </div>

          <div style={{ height: "4px", background: "repeating-linear-gradient(-45deg, #d1d5db, #d1d5db 2px, #e5e7eb 2px, #e5e7eb 6px)" }} />

          <HolographicSeal />

          {/* Column header */}
          <div style={{ display: "flex", background: "#0f172a", color: "#94a3b8", fontSize: "8px", letterSpacing: "0.1em" }}>
            <div style={{ flex: 1, padding: "5px 12px", borderRight: "1px solid #1e293b" }}>{"\u2190"} ALGORITHMIC</div>
            <div style={{ flex: 1, padding: "5px 12px" }}>SEMANTIC {"\u2192"}</div>
          </div>

          {/* Rows */}
          {CALIBRATIONS.map((item, i) => (
            <div key={i}>
              <DualRow item={item} />
              <PerRowBar item={item} />
            </div>
          ))}

          {/* Hatched */}
          <div style={{ height: "8px", background: "repeating-linear-gradient(-45deg, #d1d5db, #d1d5db 2px, #e5e7eb 2px, #e5e7eb 6px)", margin: "2px 0" }} />

          {/* Sig */}
          <div style={{ padding: "6px 12px", display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
            <div style={{ fontSize: "8px", color: "#6b7280" }}>
              <span style={{ fontWeight: 700, color: "#111" }}>Dr. Claude Opus</span> {"\u2022"} M.L.L.M., FRACGP-DHA
            </div>
            <div style={{ fontFamily: "'Dancing Script', cursive", fontSize: "18px", color: "#111", borderBottom: "1px solid #111", transform: "rotate(-3deg)" }}>Claude</div>
          </div>
        </div>

        {/* Legend - minimal */}
        <div style={{ display: "flex", gap: "10px", padding: "8px 0", justifyContent: "center", flexWrap: "wrap" }}>
          {[
            [C.boost.bg, "+"], [C.limit.bg, "\u2212"], [C.depth.bg, "\u25c6"], [C.boundary.bg, "\u2B21"], [C.baseline.bg, "\u25cb"], [C.uncertain.bg, "~"],
          ].map(([color, sym], i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: "3px" }}>
              <div style={{ width: "8px", height: "8px", background: color, borderRadius: "1px" }} />
              <span style={{ fontFamily: "'Courier New', monospace", fontSize: "9px", color: "#6b7280" }}>{sym}</span>
            </div>
          ))}
        </div>

        <div style={{ textAlign: "center", fontSize: "7px", color: "#9ca3af" }}>
          pee is urine, urine the middle of it {"\u2022"} seal: {FULL_HASH.slice(0, 24)}...
        </div>
      </div>
    </div>
  );
}
