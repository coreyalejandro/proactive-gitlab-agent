import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";

// 3 minutes at 30fps = 5400 frames
const DURATION_FRAMES = 5400;
const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ProactiveDemo"
      component={Video}
      durationInFrames={DURATION_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
