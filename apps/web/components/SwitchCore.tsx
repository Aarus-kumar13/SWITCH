"use client";

import React from "react";
import { Mic, MicOff, Sparkles, AlertCircle, CheckCircle, Cpu, Radio, PhoneCall } from "lucide-react";
import { AssistantState } from "./StateIndicator";

interface SwitchCoreProps {
  state: AssistantState;
  currentAction?: string;
  isListening: boolean;
  onToggleListen: () => void;
  onTriggerCall: () => void;
}

export const SwitchCore: React.FC<SwitchCoreProps> = ({
  state,
  currentAction,
  isListening,
  onToggleListen,
  onTriggerCall,
}) => {
  const getCoreGlow = () => {
    switch (state) {
      case "LISTENING":
        return "from-cyan-500 via-teal-400 to-blue-600 shadow-[0_0_80px_rgba(6,182,212,0.6)] animate-pulse";
      case "THINKING":
      case "PLANNING":
        return "from-purple-600 via-indigo-500 to-cyan-500 shadow-[0_0_80px_rgba(168,85,247,0.6)] animate-spin-slow";
      case "EXECUTING":
        return "from-blue-600 via-cyan-400 to-emerald-500 shadow-[0_0_80px_rgba(59,130,246,0.6)]";
      case "CALLING":
        return "from-emerald-500 via-teal-400 to-cyan-500 shadow-[0_0_80px_rgba(16,185,129,0.6)] animate-pulse";
      case "WAITING":
        return "from-amber-500 via-yellow-400 to-orange-600 shadow-[0_0_80px_rgba(245,158,11,0.6)]";
      case "SUCCESS":
        return "from-green-500 via-emerald-400 to-cyan-500 shadow-[0_0_60px_rgba(34,197,94,0.5)]";
      case "ERROR":
        return "from-red-600 via-rose-500 to-orange-600 shadow-[0_0_70px_rgba(239,68,68,0.6)]";
      default:
        return "from-cyan-600/60 via-blue-700/50 to-indigo-900/60 shadow-[0_0_40px_rgba(6,182,212,0.3)]";
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center p-8 text-center my-4 select-none">
      {/* Outer Rotating HUD Rings */}
      <div className="relative flex items-center justify-center w-64 h-64 md:w-80 md:h-80 rounded-full border border-cyan-500/20 bg-slate-950/80 backdrop-blur-xl">
        {/* Ring 1 - Outer dashed rotation */}
        <div className="absolute inset-0 rounded-full border-2 border-dashed border-cyan-500/30 animate-[spin_20s_linear_infinite]" />
        
        {/* Ring 2 - Counter rotating segment */}
        <div className="absolute inset-4 rounded-full border border-cyan-400/40 border-t-transparent border-b-transparent animate-[spin_12s_linear_infinite_reverse]" />

        {/* Ring 3 - Glowing Core Orbit */}
        <div className="absolute inset-8 rounded-full border border-blue-500/20" />

        {/* Central SWITCH Core */}
        <button
          onClick={onToggleListen}
          className={`relative flex items-center justify-center w-36 h-36 md:w-44 md:h-44 rounded-full bg-gradient-to-tr ${getCoreGlow()} transition-all duration-700 cursor-pointer group hover:scale-105 active:scale-95`}
        >
          {/* Core Inner Glass Orb */}
          <div className="absolute inset-2 rounded-full bg-slate-950/80 backdrop-blur-md flex flex-col items-center justify-center text-cyan-300 border border-cyan-500/40 group-hover:border-cyan-300 transition">
            <Mic className={`w-10 h-10 md:w-12 md:h-12 transition-transform duration-300 ${isListening ? "scale-125 text-cyan-300 animate-pulse" : "group-hover:scale-110 text-cyan-400/80"}`} />
            <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400/90 mt-1 uppercase">
              {isListening ? "LISTENING" : "TOUCH TO TALK"}
            </span>
          </div>

          {/* Pulse Ripple Effect */}
          {isListening && (
            <div className="absolute inset-0 rounded-full border-2 border-cyan-400 animate-ping opacity-75" />
          )}
        </button>
      </div>

      {/* Voice Core Status Display */}
      <div className="mt-6 space-y-1.5 max-w-lg">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-semibold tracking-wider uppercase">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          {state}
        </div>
        <h2 className="text-xl md:text-2xl font-bold tracking-tight text-slate-100">
          {state === "LISTENING" ? "I am listening to you..." : state === "THINKING" ? "Processing query & context..." : "How can I help you?"}
        </h2>
        {currentAction && (
          <p className="text-xs text-cyan-300/80 font-mono bg-slate-900/90 border border-cyan-500/20 px-4 py-1.5 rounded-lg shadow-inner">
            ⚡ {currentAction}
          </p>
        )}
      </div>
    </div>
  );
};
