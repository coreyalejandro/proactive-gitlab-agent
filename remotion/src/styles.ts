import type { CSSProperties } from "react";

export const COLORS = {
  bg: "#1e1e2e",
  surface: "#262637",
  accent: "#7c3aed",
  accentLight: "#a78bfa",
  red: "#ef4444",
  green: "#22c55e",
  yellow: "#eab308",
  text: "#e2e8f0",
  textMuted: "#94a3b8",
  code: "#0d1117",
  border: "#334155",
} as const;

export const fullScreen: CSSProperties = {
  width: "100%",
  height: "100%",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  backgroundColor: COLORS.bg,
  fontFamily: "'Inter', 'SF Pro Display', system-ui, sans-serif",
  color: COLORS.text,
};

export const codeBlock: CSSProperties = {
  backgroundColor: COLORS.code,
  borderRadius: 12,
  padding: "24px 32px",
  fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  fontSize: 22,
  lineHeight: 1.6,
  color: COLORS.text,
  border: `1px solid ${COLORS.border}`,
  textAlign: "left" as const,
  whiteSpace: "pre" as const,
  maxWidth: "85%",
};
