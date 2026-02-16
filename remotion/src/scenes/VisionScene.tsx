/**
 * Scene 5: Vision [2:45-3:00]
 * Tagline and call to action.
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

export const VisionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({ frame, fps, config: { damping: 15 } });
  const taglineOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ctaOpacity = interpolate(frame, [60, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={fullScreen}>
      <div
        style={{
          transform: `scale(${logoScale})`,
          fontSize: 96,
          fontWeight: 900,
          letterSpacing: 8,
          background: `linear-gradient(135deg, ${COLORS.accent}, ${COLORS.accentLight})`,
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          marginBottom: 30,
        }}
      >
        PROACTIVE
      </div>

      <div
        style={{
          opacity: taglineOpacity,
          fontSize: 36,
          color: COLORS.text,
          marginBottom: 50,
          fontWeight: 300,
        }}
      >
        Constitutional AI for your pipeline.
      </div>

      <div
        style={{
          opacity: ctaOpacity,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div
          style={{
            fontSize: 22,
            color: COLORS.textMuted,
          }}
        >
          Every claim verified. Every merge earned.
        </div>
        <div
          style={{
            marginTop: 20,
            padding: "16px 40px",
            borderRadius: 12,
            border: `2px solid ${COLORS.accent}`,
            fontSize: 20,
            color: COLORS.accentLight,
            fontWeight: 600,
          }}
        >
          gitlab.com/proactive
        </div>
      </div>
    </AbsoluteFill>
  );
};
