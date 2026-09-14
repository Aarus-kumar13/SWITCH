"use client";

import React, { useEffect, useState } from "react";
import { Battery, Cpu, HardDrive, Monitor, Zap } from "lucide-react";

export const TelemetryWidget: React.FC = () => {
  const [telemetry, setTelemetry] = useState<any>({
    battery_percentage: 94,
    is_charging: true,
    cpu_usage_percent: 15,
    ram_usage_percent: 42,
    disk_free_gb: 120,
    active_window_title: "VS Code - SWITCH-OS",
  });

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/system/status");
        if (res.ok) {
          const data = await res.json();
          if (data.telemetry) {
            setTelemetry(data.telemetry);
          }
        }
      } catch (e) {
        // Keep default telemetry state if server offline
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-panel p-4 rounded-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <h3 className="text-sm font-medium text-slate-300 flex items-center gap-2">
          <Monitor className="w-4 h-4 text-cyan-400" />
          System Telemetry
        </h3>
        <span className="text-xs text-green-400 flex items-center gap-1 font-mono">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          MONITORING
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
          <div className="text-slate-400 flex items-center gap-1.5 mb-1">
            <Battery className="w-3.5 h-3.5 text-blue-400" />
            Battery
          </div>
          <div className="text-sm font-semibold text-slate-100 flex items-center justify-between">
            {telemetry.battery_percentage}%
            {telemetry.is_charging && <Zap className="w-3.5 h-3.5 text-amber-400 inline" />}
          </div>
        </div>

        <div className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
          <div className="text-slate-400 flex items-center gap-1.5 mb-1">
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            CPU Load
          </div>
          <div className="text-sm font-semibold text-slate-100">{telemetry.cpu_usage_percent}%</div>
        </div>

        <div className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
          <div className="text-slate-400 flex items-center gap-1.5 mb-1">
            <HardDrive className="w-3.5 h-3.5 text-emerald-400" />
            RAM Usage
          </div>
          <div className="text-sm font-semibold text-slate-100">{telemetry.ram_usage_percent}%</div>
        </div>

        <div className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
          <div className="text-slate-400 flex items-center gap-1.5 mb-1">
            <HardDrive className="w-3.5 h-3.5 text-cyan-400" />
            Free Disk
          </div>
          <div className="text-sm font-semibold text-slate-100">{telemetry.disk_free_gb} GB</div>
        </div>
      </div>

      <div className="text-[11px] font-mono text-slate-400 truncate bg-slate-950/80 px-2.5 py-1.5 rounded border border-slate-900">
        Active Window: <span className="text-slate-200">{telemetry.active_window_title}</span>
      </div>
    </div>
  );
};
