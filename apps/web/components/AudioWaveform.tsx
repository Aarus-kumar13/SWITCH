"use client";

import React from "react";

interface AudioWaveformProps {
  active: boolean;
}

export const AudioWaveform: React.FC<AudioWaveformProps> = ({ active }) => {
  const bars = [12, 24, 40, 18, 32, 48, 20, 36, 14, 28, 44, 22];

  return (
    <div className="flex items-center justify-center gap-1.5 h-12 my-2">
      {bars.map((height, i) => (
        <div
          key={i}
          className={`w-1 rounded-full bg-gradient-to-t from-blue-500 to-cyan-400 transition-all duration-300 ${
            active ? "animate-pulse" : "opacity-30 h-3"
          }`}
          style={{
            height: active ? `${height}px` : "12px",
            animationDelay: `${i * 80}ms`,
          }}
        />
      ))}
    </div>
  );
};
