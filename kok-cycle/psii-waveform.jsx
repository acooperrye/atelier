import { useState, useEffect, useRef, useCallback } from "react";

const COLORS = {
  bg: "#0a0a0a",
  grid: "#1a1a1a",
  gridAccent: "#222",
  s0: "#4a9eff",
  s1: "#22d68a",
  s2: "#ffb84a",
  s3: "#ff4a6a",
  o2burst: "#ffffff",
  photon: "rgba(255,200,100,0.6)",
  text: "#888",
  textBright: "#ccc",
  fluorescence: "#7c3aed",
  envelope: "rgba(255,255,255,0.05)",
};

const S_STATES = [
  { label: "S₀", color: COLORS.s0, desc: "Resting", charge: 0 },
  { label: "S₁", color: COLORS.s1, desc: "One electron removed", charge: 1 },
  { label: "S₂", color: COLORS.s2, desc: "Two electrons removed", charge: 2 },
  { label: "S₃", color: COLORS.s3, desc: "Three electrons removed", charge: 3 },
];

export default function PSIIWaveform() {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const timeRef = useRef(0);
  const [speed, setSpeed] = useState(1);
  const [showPhotons, setShowPhotons] = useState(true);
  const [showFluorescence, setShowFluorescence] = useState(true);
  const [paused, setPaused] = useState(false);
  const pausedRef = useRef(false);
  const [hoveredState, setHoveredState] = useState(null);
  const [dims, setDims] = useState({ w: 800, h: 500 });

  useEffect(() => {
    pausedRef.current = paused;
  }, [paused]);

  useEffect(() => {
    const handleResize = () => {
      const w = Math.min(window.innerWidth - 32, 900);
      const h = Math.min(window.innerHeight - 280, 520);
      setDims({ w, h: Math.max(h, 300) });
    };
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const { w, h } = dims;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.scale(dpr, dpr);

    if (!pausedRef.current) {
      timeRef.current += 0.008 * speed;
    }
    const t = timeRef.current;

    // Background
    ctx.fillStyle = COLORS.bg;
    ctx.fillRect(0, 0, w, h);

    const margin = { top: 60, bottom: 50, left: 60, right: 30 };
    const plotW = w - margin.left - margin.right;
    const plotH = h - margin.top - margin.bottom;
    const centerY = margin.top + plotH * 0.5;

    // Grid
    ctx.strokeStyle = COLORS.grid;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 8; i++) {
      const y = margin.top + (plotH / 8) * i;
      ctx.beginPath();
      ctx.moveTo(margin.left, y);
      ctx.lineTo(margin.left + plotW, y);
      ctx.stroke();
    }
    for (let i = 0; i <= 16; i++) {
      const x = margin.left + (plotW / 16) * i;
      ctx.strokeStyle = i % 4 === 0 ? COLORS.gridAccent : COLORS.grid;
      ctx.beginPath();
      ctx.moveTo(x, margin.top);
      ctx.lineTo(x, margin.top + plotH);
      ctx.stroke();
    }

    // Zero line
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(margin.left, centerY);
    ctx.lineTo(margin.left + plotW, centerY);
    ctx.stroke();

    // Number of complete cycles visible
    const cyclesVisible = 4;
    const samplesPerCycle = 4; // 4 S-states per cycle
    const totalSteps = cyclesVisible * samplesPerCycle;

    // Draw the S-state waveform as a stepped phase signal
    const stepWidth = plotW / totalSteps;
    const amplitude = plotH * 0.35;

    // S-state voltage-like waveform (charge accumulation then release)
    const getYForState = (stateIndex) => {
      const charges = [0, 0.33, 0.66, 1.0];
      return centerY - charges[stateIndex] * amplitude;
    };

    // Phase offset from time
    const phaseOffset = (t * 2) % 1;

    // Draw photon arrival markers
    if (showPhotons) {
      ctx.globalAlpha = 0.15;
      for (let i = 0; i < totalSteps; i++) {
        const x = margin.left + i * stepWidth + stepWidth * 0.05;
        const stateIdx = i % 4;
        ctx.fillStyle = COLORS.photon;
        const flashX = x + phaseOffset * stepWidth;
        if (flashX < margin.left + plotW) {
          ctx.beginPath();
          ctx.moveTo(flashX, margin.top);
          ctx.lineTo(flashX, margin.top + plotH);
          ctx.lineWidth = 2;
          ctx.strokeStyle = COLORS.photon;
          ctx.stroke();

          // Small photon symbol
          ctx.globalAlpha = 0.5;
          ctx.fillStyle = COLORS.photon;
          ctx.font = "10px monospace";
          ctx.fillText("hν", flashX - 6, margin.top - 5);
          ctx.globalAlpha = 0.15;
        }
      }
      ctx.globalAlpha = 1;
    }

    // Draw the main S-state waveform
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";

    for (let i = 0; i < totalSteps; i++) {
      const stateIdx = i % 4;
      const x1 = margin.left + i * stepWidth;
      const x2 = x1 + stepWidth;
      const y = getYForState(stateIdx);
      const nextStateIdx = (i + 1) % 4;
      const yNext = getYForState(nextStateIdx);

      // Horizontal line for this state
      ctx.strokeStyle = S_STATES[stateIdx].color;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(x1, y);
      ctx.lineTo(x2, y);
      ctx.stroke();

      // Transition line to next state
      if (i < totalSteps - 1) {
        ctx.strokeStyle =
          stateIdx === 3
            ? COLORS.o2burst
            : S_STATES[(stateIdx + 1) % 4].color;
        ctx.lineWidth = stateIdx === 3 ? 3 : 1.5;
        ctx.globalAlpha = stateIdx === 3 ? 1 : 0.5;
        ctx.beginPath();
        ctx.moveTo(x2, y);
        ctx.lineTo(x2, yNext);
        ctx.stroke();
        ctx.globalAlpha = 1;

        // O2 burst marker
        if (stateIdx === 3) {
          ctx.fillStyle = COLORS.o2burst;
          ctx.font = "bold 11px monospace";
          ctx.fillText("O₂↑", x2 - 12, yNext + amplitude + 20);

          // Burst glow
          const grad = ctx.createRadialGradient(x2, yNext, 0, x2, yNext, 20);
          grad.addColorStop(0, "rgba(255,255,255,0.2)");
          grad.addColorStop(1, "rgba(255,255,255,0)");
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(x2, yNext, 20, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // State label at midpoint
      const midX = (x1 + x2) / 2;
      ctx.fillStyle = S_STATES[stateIdx].color;
      ctx.font = "bold 11px monospace";
      ctx.textAlign = "center";
      ctx.fillText(S_STATES[stateIdx].label, midX, y - 10);
      ctx.textAlign = "left";
    }

    // Draw fluorescence yield oscillation (period-4 with decay and modulation)
    if (showFluorescence) {
      ctx.strokeStyle = COLORS.fluorescence;
      ctx.lineWidth = 1.5;
      ctx.globalAlpha = 0.8;
      ctx.beginPath();

      const fluoAmplitude = plotH * 0.12;
      // The fluorescence yield shows period-4 oscillation
      // Higher on S2/S3 transitions, lower on S0/S1
      const fluoYields = [0.6, 0.75, 1.0, 0.85]; // relative yields per S-state

      for (let px = 0; px < plotW; px++) {
        const frac = px / plotW;
        const statePos = frac * totalSteps;
        const stateIdx = Math.floor(statePos) % 4;
        const nextIdx = (stateIdx + 1) % 4;
        const within = statePos - Math.floor(statePos);

        // Smooth interpolation
        const yield1 = fluoYields[stateIdx];
        const yield2 = fluoYields[nextIdx];
        const smoothT = within * within * (3 - 2 * within);
        const currentYield = yield1 + (yield2 - yield1) * smoothT;

        const fluoY =
          margin.top + plotH * 0.82 - currentYield * fluoAmplitude;
        const x = margin.left + px;

        if (px === 0) ctx.moveTo(x, fluoY);
        else ctx.lineTo(x, fluoY);
      }
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Label
      ctx.fillStyle = COLORS.fluorescence;
      ctx.font = "10px monospace";
      ctx.fillText("fluorescence yield", margin.left + plotW - 120, margin.top + plotH * 0.72);
    }

    // Animated scan line
    const scanX = margin.left + (phaseOffset * plotW * 4) % plotW;
    ctx.strokeStyle = "rgba(255,255,255,0.08)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(scanX, margin.top);
    ctx.lineTo(scanX, margin.top + plotH);
    ctx.stroke();

    // Axes labels
    ctx.fillStyle = COLORS.text;
    ctx.font = "10px monospace";
    ctx.save();
    ctx.translate(15, centerY);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = "center";
    ctx.fillText("charge accumulation →", 0, 0);
    ctx.restore();

    ctx.textAlign = "center";
    ctx.fillText("flash number →", margin.left + plotW / 2, h - 10);

    // Title
    ctx.fillStyle = COLORS.textBright;
    ctx.font = "13px monospace";
    ctx.textAlign = "left";
    ctx.fillText("Photosystem II — Kok Cycle Phase Waveform", margin.left, 25);
    ctx.fillStyle = COLORS.text;
    ctx.font = "10px monospace";
    ctx.fillText(
      "~4,930 turnovers/sec · 4 S-states per O₂ · period-4 oscillation",
      margin.left,
      42
    );

    // Turnover rate indicator
    ctx.fillStyle = COLORS.textBright;
    ctx.font = "10px monospace";
    ctx.textAlign = "right";
    ctx.fillText(`~${Math.round(4930 * speed)} Hz`, margin.left + plotW, 25);
    ctx.fillStyle = COLORS.text;
    ctx.fillText("effective turnover", margin.left + plotW, 42);
    ctx.textAlign = "left";

    animRef.current = requestAnimationFrame(draw);
  }, [dims, speed, showPhotons, showFluorescence]);

  useEffect(() => {
    animRef.current = requestAnimationFrame(draw);
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, [draw]);

  return (
    <div
      style={{
        background: COLORS.bg,
        minHeight: "100vh",
        color: COLORS.textBright,
        fontFamily: "monospace",
        padding: "16px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "12px",
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          width: dims.w,
          height: dims.h,
          borderRadius: "4px",
          border: "1px solid #1a1a1a",
        }}
      />

      {/* S-state legend */}
      <div
        style={{
          display: "flex",
          gap: "16px",
          flexWrap: "wrap",
          justifyContent: "center",
          fontSize: "11px",
        }}
      >
        {S_STATES.map((s, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              opacity: hoveredState === null || hoveredState === i ? 1 : 0.3,
              cursor: "pointer",
              transition: "opacity 0.2s",
            }}
            onMouseEnter={() => setHoveredState(i)}
            onMouseLeave={() => setHoveredState(null)}
          >
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                background: s.color,
                boxShadow: `0 0 6px ${s.color}44`,
              }}
            />
            <span style={{ color: s.color }}>{s.label}</span>
            <span style={{ color: COLORS.text }}>{s.desc}</span>
            {i === 3 && (
              <span style={{ color: COLORS.o2burst, marginLeft: 4 }}>
                → O₂ release + reset
              </span>
            )}
          </div>
        ))}
      </div>

      {/* Controls */}
      <div
        style={{
          display: "flex",
          gap: "20px",
          alignItems: "center",
          flexWrap: "wrap",
          justifyContent: "center",
          fontSize: "11px",
        }}
      >
        <button
          onClick={() => setPaused(!paused)}
          style={{
            background: "none",
            border: "1px solid #333",
            color: COLORS.textBright,
            padding: "4px 12px",
            cursor: "pointer",
            fontFamily: "monospace",
            fontSize: "11px",
            borderRadius: "2px",
          }}
        >
          {paused ? "▶ play" : "▮▮ pause"}
        </button>

        <label style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ color: COLORS.text }}>speed</span>
          <input
            type="range"
            min="0.1"
            max="3"
            step="0.1"
            value={speed}
            onChange={(e) => setSpeed(parseFloat(e.target.value))}
            style={{ width: 80, accentColor: COLORS.s1 }}
          />
          <span>{speed.toFixed(1)}×</span>
        </label>

        <label
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            cursor: "pointer",
          }}
        >
          <input
            type="checkbox"
            checked={showPhotons}
            onChange={(e) => setShowPhotons(e.target.checked)}
            style={{ accentColor: COLORS.photon }}
          />
          <span style={{ color: COLORS.text }}>photon flashes</span>
        </label>

        <label
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            cursor: "pointer",
          }}
        >
          <input
            type="checkbox"
            checked={showFluorescence}
            onChange={(e) => setShowFluorescence(e.target.checked)}
            style={{ accentColor: COLORS.fluorescence }}
          />
          <span style={{ color: COLORS.text }}>fluorescence</span>
        </label>
      </div>

      {/* Annotation */}
      <div
        style={{
          maxWidth: 600,
          textAlign: "center",
          color: COLORS.text,
          fontSize: "10px",
          lineHeight: 1.6,
          padding: "8px 16px",
          borderTop: "1px solid #1a1a1a",
        }}
      >
        Four photon hits accumulate charge through S₀→S₁→S₂→S₃.
        On the fourth, the water-oxidising complex releases O₂ and resets.
        The fluorescence yield oscillates with this rhythm — proof the system has phase.
        Your convolution experiment would match an input waveform to this clock.
      </div>
    </div>
  );
}
