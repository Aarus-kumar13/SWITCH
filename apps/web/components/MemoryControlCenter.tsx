"use client";

import React, { useState } from "react";
import { Brain, Trash2, CheckCircle, Edit, RefreshCw } from "lucide-react";

export interface Memory {
  id: string;
  category: string;
  key: string;
  value: any;
  confidence: number;
  user_confirmed: boolean;
}

interface MemoryControlCenterProps {
  memories: Memory[];
  userProfile: any;
  onDeleteMemory: (key: string) => void;
}

export const MemoryControlCenter: React.FC<MemoryControlCenterProps> = ({
  memories,
  userProfile,
  onDeleteMemory,
}) => {
  const [activeTab, setActiveTab] = useState<"preferences" | "profile" | "workflows">("preferences");

  return (
    <div className="glass-panel p-4 rounded-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="text-sm font-medium text-slate-200 flex items-center gap-2">
          <Brain className="w-4 h-4 text-cyan-400" />
          What SWITCH Knows About You
        </h3>
        <div className="flex gap-1 bg-slate-900/80 p-1 rounded-lg border border-slate-800 text-[11px]">
          <button
            onClick={() => setActiveTab("preferences")}
            className={`px-2.5 py-1 rounded-md transition ${
              activeTab === "preferences" ? "bg-cyan-500/20 text-cyan-300 font-semibold" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Preferences
          </button>
          <button
            onClick={() => setActiveTab("profile")}
            className={`px-2.5 py-1 rounded-md transition ${
              activeTab === "profile" ? "bg-cyan-500/20 text-cyan-300 font-semibold" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Profile
          </button>
        </div>
      </div>

      {activeTab === "preferences" && (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {memories.length === 0 ? (
            <p className="text-xs text-slate-500 italic py-4 text-center">No learned preferences yet.</p>
          ) : (
            memories.map((mem) => (
              <div key={mem.id} className="flex items-center justify-between p-2.5 bg-slate-900/50 rounded-lg border border-slate-800/80 text-xs">
                <div>
                  <div className="font-mono text-slate-300 capitalize">{mem.key.replace(/_/g, " ")}</div>
                  <div className="text-slate-400 font-semibold text-[11px] mt-0.5">{String(mem.value)}</div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-cyan-400 font-mono bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
                    {Math.round(mem.confidence * 100)}% Conf
                  </span>
                  <button
                    onClick={() => onDeleteMemory(mem.key)}
                    className="p-1 text-slate-500 hover:text-red-400 transition rounded"
                    title="Forget Memory"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === "profile" && (
        <div className="space-y-2 text-xs">
          <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-800/80 space-y-1.5 font-mono">
            <div className="flex justify-between"><span className="text-slate-400">Preferred Editor:</span> <span className="text-slate-200">{userProfile?.preferred_editor || "VS Code"}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Communication Style:</span> <span className="text-slate-200">{userProfile?.communication_style || "Concise"}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">OS Platform:</span> <span className="text-slate-200">{userProfile?.operating_system || "Windows"}</span></div>
          </div>
        </div>
      )}
    </div>
  );
};
