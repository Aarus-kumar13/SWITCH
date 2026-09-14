"use client";

import React, { useState, useEffect } from "react";
import { Shield, Zap, Cpu, Activity, PhoneCall, Radio, Terminal, Settings } from "lucide-react";

interface HudHeaderProps {
  onTriggerCall: () => void;
  onOpenMacro: () => void;
}

export const HudHeader: React.FC<HudHeaderProps> = ({ onTriggerCall, onOpenMacro }) => {
  const [timeStr, setTimeStr] = useState<string>("");

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString("en-US", { hour12: false }));
    };
    updateClock();
    const interval = setInterval(updateClock, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="w-full border-b border-cyan-500/20 bg-slate-950/80 backdrop-blur-xl px-6 py-3 flex items-center justify-between sticky top-0 z-50">
      {/* JARVIS Brand Logo & System Status */}
      <div className="flex items-center gap-4">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-lg bg-slate-900 border border-cyan-500/40 text-cyan-400 font-mono font-black text-xl shadow-[0_0_15px_rgba(6,182,212,0.3)]">
          S
          <div className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-base font-extrabold tracking-widest text-slate-100 uppercase font-mono">SWITCH OS</h1>
            <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono border border-cyan-500/40 font-bold">
              JARVIS CORE v2.5
            </span>
          </div>
          <p className="text-[10px] text-cyan-400/80 font-mono tracking-wider">AUTONOMOUS PERSONAL AI OPERATING SYSTEM</p>
        </div>
      </div>

      {/* Center HUD System Clock */}
      <div className="hidden md:flex items-center gap-3 font-mono text-xs bg-slate-900/80 px-4 py-1.5 rounded-full border border-cyan-500/30 text-cyan-300 shadow-inner">
        <Activity className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
        <span>SYS TIME:</span>
        <span className="font-bold text-slate-100 tracking-wider">{timeStr || "21:24:00"}</span>
        <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-ping" />
        <span className="text-[10px] text-green-400 font-bold">ONLINE</span>
      </div>

      {/* Right HUD Action Controls */}
      <div className="flex items-center gap-2 text-xs">
        <button
          onClick={onTriggerCall}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/20 transition font-mono font-semibold shadow-[0_0_15px_rgba(16,185,129,0.2)]"
        >
          <PhoneCall className="w-3.5 h-3.5" />
          <span>PHONE AI</span>
        </button>

        <button
          onClick={onOpenMacro}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/40 text-purple-300 hover:bg-purple-500/20 transition font-mono font-semibold shadow-[0_0_15px_rgba(168,85,247,0.2)]"
        >
          <Zap className="w-3.5 h-3.5 text-purple-400" />
          <span>DEV MACRO</span>
        </button>
      </div>
    </header>
  );
};
