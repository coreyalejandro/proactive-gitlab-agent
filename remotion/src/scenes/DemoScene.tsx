/**
 * Scene 3: Hero Demo [1:00-2:15]
 * Phantom completion detected and blocked. Shows MR review flow.
 */
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { COLORS, fullScreen, codeBlock } from "../styles";

const MR_DESCRIPTION = `Title: Implement user authentication

"All tests pass. Implementation is complete.
 The auth module is fully tested and ready
 for production."`;

const REVIEW_OUTPUT = `:no_entry: PROACTIVE Review: BLOCKED

Trust Score: 0%

[ERROR] I2: No Phantom Work
> Phantom completion detected. MR claims
> 'All tests pass' but no test artifacts
> found. Merge blocked.

Fix: Run tests and commit artifacts,
     or remove the completion claim.`;

export const DemoScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={fullScreen}>
      {/* MR Description appears */}
      <Sequence from={0} durationInFrames={120}>
        <AbsoluteFill style={{ ...fullScreen, flexDirection: "row", gap: 40, padding: 60 }}>
          <div style={{ flex: 1 }}>
            <h3
              style={{
                fontSize: 24,
                color: COLORS.textMuted,
                marginBottom: 16,
                opacity: interpolate(frame, [0, 15], [0, 1], {
                  extrapolateRight: "clamp",
                }),
              }}
            >
              Merge Request
            </h3>
            <div
              style={{
                ...codeBlock,
                opacity: interpolate(frame, [10, 30], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
                fontSize: 20,
              }}
            >
              {MR_DESCRIPTION}
            </div>

            <div
              style={{
                marginTop: 20,
                fontSize: 18,
                color: COLORS.yellow,
                opacity: interpolate(frame, [40, 55], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
              }}
            >
              Scanning for claims...
            </div>
          </div>

          <div style={{ flex: 1 }}>
            <h3
              style={{
                fontSize: 24,
                color: COLORS.textMuted,
                marginBottom: 16,
                opacity: interpolate(frame, [50, 65], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
              }}
            >
              PROACTIVE Review
            </h3>
            <div
              style={{
                ...codeBlock,
                opacity: interpolate(frame, [60, 80], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
                borderLeft: `4px solid ${COLORS.red}`,
                fontSize: 18,
              }}
            >
              {REVIEW_OUTPUT}
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* Blocked badge */}
      <Sequence from={100} durationInFrames={120}>
        <AbsoluteFill
          style={{
            ...fullScreen,
            justifyContent: "center",
          }}
        >
          <div
            style={{
              transform: `scale(${spring({
                frame: frame - 100,
                fps,
                config: { damping: 12 },
              })})`,
              backgroundColor: COLORS.red,
              padding: "24px 60px",
              borderRadius: 16,
              fontSize: 48,
              fontWeight: 800,
              letterSpacing: 4,
            }}
          >
            MERGE BLOCKED
          </div>
          <div
            style={{
              marginTop: 30,
              fontSize: 24,
              color: COLORS.textMuted,
              opacity: interpolate(frame - 100, [20, 40], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            I2 violation: Phantom completion claim without test artifacts
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
