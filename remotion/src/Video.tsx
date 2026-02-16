/**
 * PROACTIVE Demo Video
 * 3 minutes (5400 frames @ 30fps)
 *
 * Timeline:
 *   [0:00 - 0:30]  Problem    (frames 0-899)
 *   [0:30 - 1:00]  Origin     (frames 900-1799)
 *   [1:00 - 2:15]  Demo       (frames 1800-4049)
 *   [2:15 - 2:45]  Evidence   (frames 4050-4949)
 *   [2:45 - 3:00]  Vision     (frames 4950-5399)
 */
import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { ProblemScene } from "./scenes/ProblemScene";
import { OriginScene } from "./scenes/OriginScene";
import { DemoScene } from "./scenes/DemoScene";
import { EvidenceScene } from "./scenes/EvidenceScene";
import { VisionScene } from "./scenes/VisionScene";
import { COLORS } from "./styles";

export const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      {/* 0:00 - 0:30 */}
      <Sequence from={0} durationInFrames={900}>
        <ProblemScene />
      </Sequence>

      {/* 0:30 - 1:00 */}
      <Sequence from={900} durationInFrames={900}>
        <OriginScene />
      </Sequence>

      {/* 1:00 - 2:15 */}
      <Sequence from={1800} durationInFrames={2250}>
        <DemoScene />
      </Sequence>

      {/* 2:15 - 2:45 */}
      <Sequence from={4050} durationInFrames={900}>
        <EvidenceScene />
      </Sequence>

      {/* 2:45 - 3:00 */}
      <Sequence from={4950} durationInFrames={450}>
        <VisionScene />
      </Sequence>
    </AbsoluteFill>
  );
};
