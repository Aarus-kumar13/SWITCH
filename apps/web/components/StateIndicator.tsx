"use client";

import React from "react";
import { Activity, Mic, Brain, Cpu, PhoneCall, CheckCircle, AlertTriangle } from "lucide-react";

export type AssistantState =
  | "IDLE"
  | "LISTENING"
  | "THINKING"
  | "PLANNING"
  | "EXECUTING"
  | "WAITING"
  | "CALLING"
  | "SPEAKING"
  | "SUCCESS"
  | "ERROR";

interface StateIndicatorProps {
  state: AssistantState;
  currentAction?: string;
}

export const StateIndicator: React.FC<StateIndicatorProps> = ({ state, currentAction }) => {
  const getStateConfig = () => {
    switch (state) {
      case "LISTENING":
        return { color: "border-cyan-500 text-cyan-400 bg-cyan-500/10", icon: Mic, label: "Listening..." };
      case "THINKING":
      case "PLANNING":
        return { color: "border-purple-500 text-purple-400 bg-purple-500/10", icon: Brain, label: "Thinking & Planning..." };
      case "EXECUTING":
        return { color: "border-blue-500 text-blue-400 bg-blue-500/10", icon: Cpu, label: "Executing Autonomous Tools..." };
      case "CALLING":
        return { color: "border-emerald-500 text-emerald-400 bg-emerald-500/10", icon: PhoneCall, label: "Initiating Phone Call..." };
      case "SUCCESS":
        return { color: "border-green-500 text-green-400 bg-green-500/10", icon: CheckCircle, label: "Completed Successfully" };
      case "ERROR":
        return { color: "border-red-500 text-red-400 bg-red-500/10", icon: AlertTriangle, label: "Error / Attention Required" };
      case "WAITING":
        return { color: "border-amber-500 text-amber-400 bg-amber-500/10", icon: Activity, label: "Waiting for Human Approval" };
      default:
        return { color: "border-slate-700 text-slate-400 bg-slate-800/40", icon: Activity, label: "SWITCH Ready" };
    }
  };

  const config = getStateConfig();
  const Icon = config.icon;

  return (
    <div className="flex flex-col items-center justify-center p-6 text-center">
      <div className={`relative flex items-center justify-center w-24 h-24 rounded-full border-2 ${config.color} transition-all duration-500 shadow-lg shadow-cyan-500/5`}>
        <Icon className="w-10 h-10 animate-pulse" />
        <div className="absolute inset-0 rounded-full border border-current opacity-20 animate-ping" />
      </div>

      <h2 className="mt-4 text-xl font-semibold tracking-wide text-slate-100">{config.label}</h2>
      {currentAction && (
        <p className="mt-1 text-sm text-slate-400 max-w-md font-mono bg-slate-900/60 px-3 py-1 rounded-full border border-slate-800">
          {currentAction}
        </p>
      )}
    </div>
  );
};
