"use client";

import React from "react";
import { Activity, Clock, CheckCircle2, AlertTriangle, RefreshCw } from "lucide-react";

export interface ActiveTaskItem {
  id: string;
  name: string;
  agent: string;
  status: string;
  progress: number;
}

interface ActiveTasksCardProps {
  tasks: ActiveTaskItem[];
}

export const ActiveTasksCard: React.FC<ActiveTasksCardProps> = ({ tasks }) => {
  const defaultTasks: ActiveTaskItem[] = [
    { id: "t1", name: "Monitoring deployment & server status", agent: "Computer Control", status: "MONITORING", progress: 100 },
    { id: "t2", name: "Battery & telemetry event watcher", agent: "System Telemetry", status: "ACTIVE", progress: 95 },
    { id: "t3", name: "Researching project optimization techniques", agent: "Research", status: "IN_PROGRESS", progress: 75 },
  ];

  const displayTasks = tasks.length > 0 ? tasks : defaultTasks;

  return (
    <div className="glass-panel p-4 rounded-xl border border-cyan-500/20 bg-slate-950/70 space-y-3">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <h3 className="text-sm font-mono font-bold text-cyan-300 flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
          ACTIVE TASKS & MONITORING
        </h3>
        <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/30 font-bold">
          {displayTasks.length} RUNNING
        </span>
      </div>

      <div className="space-y-2.5 max-h-56 overflow-y-auto pr-1">
        {displayTasks.map((t) => (
          <div key={t.id} className="p-3 bg-slate-900/80 rounded-lg border border-slate-800/90 text-xs space-y-2 font-mono">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-200 truncate">{t.name}</span>
              <span className="text-[10px] font-bold text-cyan-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                {t.agent}
              </span>
            </div>
            <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden border border-slate-800">
              <div
                className="bg-gradient-to-r from-blue-500 to-cyan-400 h-1.5 rounded-full transition-all duration-500"
                style={{ width: `${t.progress}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
