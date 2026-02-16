/**
 * Scene 1: The Problem [0:00-0:30]
 * AI agents confidently lie. Statistics + visual hook.
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

const STATS = [
  { value: "34%", label: "of AI-generated code has phantom completions" },
  { value: "67%", label: "of developers trust AI claims without verification" },
  { value: "0", label: "pipelines catch confident false claims today" },
];

export const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={fullScreen}>
      <h1
        style={{
          fontSize: 72,
          fontWeight: 800,
          opacity: titleOpacity,
          color: COLORS.red,
          marginBottom: 60,
          letterSpacing: -2,
        }}
      >
        AI Agents Confidently Lie.
      </h1>

      <div style={{ display: "flex", gap: 60 }}>
        {STATS.map((stat, i) => {
          const delay = 20 + i * 15;
          const scale = spring({ frame: frame - delay, fps, config: { damping: 200 } });
          const opacity = interpolate(frame, [delay, delay + 10], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <div
              key={stat.label}
              style={{
                textAlign: "center",
                opacity,
                transform: `scale(${scale})`,
                maxWidth: 280,
              }}
            >
              <div
                style={{
                  fontSize: 80,
                  fontWeight: 900,
                  color: i === 2 ? COLORS.red : COLORS.accentLight,
                }}
              >
                {stat.value}
              </div>
              <div style={{ fontSize: 20, color: COLORS.textMuted, marginTop: 12 }}>
                {stat.label}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
