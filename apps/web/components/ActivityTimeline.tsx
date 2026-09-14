"use client";

import React from "react";
import { ShieldAlert, CheckCircle2, Clock, Terminal } from "lucide-react";

export interface ActivityItem {
  id: string;
  user_command: string;
  agent_selected: string;
  reasoning_summary: string;
  tool_used: string;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  execution_result: string;
  timestamp: string;
}

interface ActivityTimelineProps {
  activities: ActivityItem[];
}

export const ActivityTimeline: React.FC<ActivityTimelineProps> = ({ activities }) => {
  return (
    <div className="glass-panel p-4 rounded-xl space-y-3">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <h3 className="text-sm font-medium text-slate-300 flex items-center gap-2">
          <Terminal className="w-4 h-4 text-purple-400" />
          Transparent Activity Audit Trail
        </h3>
        <span className="text-xs text-slate-500 font-mono">{activities.length} Events</span>
      </div>

      <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
        {activities.length === 0 ? (
          <p className="text-xs text-slate-500 italic py-4 text-center">No audit activity recorded yet.</p>
        ) : (
          activities.map((act) => (
            <div key={act.id} className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 text-xs space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-200 capitalize font-mono">{act.agent_selected} Agent</span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    act.risk_level === "HIGH"
                      ? "bg-red-500/20 text-red-400 border border-red-500/30"
                      : act.risk_level === "MEDIUM"
                      ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                      : "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                  }`}
                >
                  {act.risk_level} RISK
                </span>
              </div>
              <p className="text-slate-400 font-mono text-[11px] truncate">Tool: {act.tool_used}</p>
              <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-slate-800/50">
                <span className="flex items-center gap-1 text-slate-400">
                  <CheckCircle2 className="w-3 h-3 text-green-400 inline" />
                  {act.execution_result}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-slate-600" />
                  {new Date(act.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
