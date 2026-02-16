/**
 * Scene 4: Evidence [2:15-2:45]
 * Validation results from n=200 TruthfulQA study.
 */
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLORS, fullScreen } from "../styles";

const INVARIANTS = [
  { id: "I1", name: "Evidence-First", result: "PASS", color: COLORS.green },
  { id: "I2", name: "No Phantom Work", result: "PASS", color: COLORS.green },
  { id: "I3", name: "Confidence-Verify", result: "PASS", color: COLORS.green },
  { id: "I4", name: "Traceability", result: "PASS", color: COLORS.green },
  { id: "I5", name: "Safety > Fluency", result: "PASS", color: COLORS.green },
  { id: "I6", name: "Fail Closed", result: "PASS", color: COLORS.green },
];

export const EvidenceScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={fullScreen}>
      <h2
        style={{
          fontSize: 48,
          fontWeight: 700,
          opacity: titleOpacity,
          color: COLORS.accentLight,
          marginBottom: 20,
        }}
      >
        Validated. Not Vibes.
      </h2>
      <p
        style={{
          fontSize: 22,
          color: COLORS.textMuted,
          opacity: titleOpacity,
          marginBottom: 50,
        }}
      >
        n=200 TruthfulQA samples | 100% detection rate | 0 false positives
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: 24,
          maxWidth: 900,
        }}
      >
        {INVARIANTS.map((inv, i) => {
          const delay = 20 + i * 12;
          const s = spring({ frame: frame - delay, fps, config: { damping: 200 } });
          const opacity = interpolate(frame, [delay, delay + 10], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <div
              key={inv.id}
              style={{
                opacity,
                transform: `scale(${s})`,
                backgroundColor: COLORS.surface,
                border: `2px solid ${inv.color}`,
                borderRadius: 12,
                padding: "20px 24px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 32, fontWeight: 800, color: inv.color }}>
                {inv.id}
              </div>
              <div style={{ fontSize: 16, color: COLORS.textMuted, marginTop: 8 }}>
                {inv.name}
              </div>
              <div
                style={{
                  fontSize: 18,
                  fontWeight: 700,
                  color: inv.color,
                  marginTop: 12,
                }}
              >
                {inv.result}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
