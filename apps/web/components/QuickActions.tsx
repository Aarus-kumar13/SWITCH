"use client";

import React from "react";
import { Mic, Monitor, Search, CheckSquare, Brain, Settings } from "lucide-react";

interface QuickActionsProps {
  onActionClick: (command: string) => void;
}

export const QuickActions: React.FC<QuickActionsProps> = ({ onActionClick }) => {
  const actions = [
    { label: "Talk", icon: Mic, command: "SWITCH, let's talk.", color: "text-cyan-400 border-cyan-500/40 hover:bg-cyan-500/20" },
    { label: "Computer", icon: Monitor, command: "Check my computer system telemetry and running processes.", color: "text-blue-400 border-blue-500/40 hover:bg-blue-500/20" },
    { label: "Research", icon: Search, command: "Research modern React performance optimization techniques.", color: "text-purple-400 border-purple-500/40 hover:bg-purple-500/20" },
    { label: "Tasks", icon: CheckSquare, command: "List my active background tasks and monitoring jobs.", color: "text-emerald-400 border-emerald-500/40 hover:bg-emerald-500/20" },
    { label: "Memory", icon: Brain, command: "Show what you remember about me and my preferences.", color: "text-amber-400 border-amber-500/40 hover:bg-amber-500/20" },
    { label: "Settings", icon: Settings, command: "Show current risk security policy and permission settings.", color: "text-slate-300 border-slate-700 hover:bg-slate-800" },
  ];

  return (
    <div className="w-full grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5 my-4">
      {actions.map((act, i) => {
        const Icon = act.icon;
        return (
          <button
            key={i}
            onClick={() => onActionClick(act.command)}
            className={`flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-slate-950/80 border text-xs font-mono font-bold transition duration-200 shadow-md ${act.color}`}
          >
            <Icon className="w-4 h-4" />
            <span>[ {act.label} ]</span>
          </button>
        );
      })}
    </div>
  );
};
