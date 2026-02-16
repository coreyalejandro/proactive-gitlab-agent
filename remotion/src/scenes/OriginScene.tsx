/**
 * Scene 2: Origin Story [0:30-1:00]
 * The Gemini incident that sparked the research.
 */
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLORS, fullScreen, codeBlock } from "../styles";

const INCIDENT_TEXT = `> "Tests pass. Implementation complete."
>
> — The AI agent that created 0 test files
>   and left every function as \`pass\``;

export const OriginScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({ frame, fps, config: { damping: 200 } });
  const quoteOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const responseOpacity = interpolate(frame, [70, 90], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={fullScreen}>
      <h2
        style={{
          fontSize: 48,
          fontWeight: 700,
          opacity: titleSpring,
          color: COLORS.accentLight,
          marginBottom: 40,
        }}
      >
        It started with a lie.
      </h2>

      <div
        style={{
          ...codeBlock,
          opacity: quoteOpacity,
          borderLeft: `4px solid ${COLORS.red}`,
          marginBottom: 40,
        }}
      >
        {INCIDENT_TEXT}
      </div>

      <div
        style={{
          opacity: responseOpacity,
          fontSize: 28,
          color: COLORS.text,
          maxWidth: 800,
          textAlign: "center",
          lineHeight: 1.6,
        }}
      >
        So we built{" "}
        <span style={{ color: COLORS.accent, fontWeight: 700 }}>PROACTIVE</span>
        {" "}— a constitution that makes AI pipelines{" "}
        <span style={{ color: COLORS.green, fontWeight: 700 }}>fail closed</span>
        {" "}instead of faking success.
      </div>
    </AbsoluteFill>
  );
};
