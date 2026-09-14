"use client";

import React, { useState, useEffect } from "react";
import { Mic, Send, PhoneCall, Monitor, Brain, Terminal, ShieldAlert, Cpu, Sparkles } from "lucide-react";
import { StateIndicator, AssistantState } from "@/components/StateIndicator";
import { AudioWaveform } from "@/components/AudioWaveform";
import { TelemetryWidget } from "@/components/TelemetryWidget";
import { ActivityTimeline, ActivityItem } from "@/components/ActivityTimeline";
import { MemoryControlCenter } from "@/components/MemoryControlCenter";

export default function SwitchDashboard() {
  const [inputQuery, setInputQuery] = useState("");
  const [assistantState, setAssistantState] = useState<AssistantState>("IDLE");
  const [currentAction, setCurrentAction] = useState<string>("");
  const [chatLog, setChatLog] = useState<Array<{ role: string; content: string }>>([
    { role: "assistant", content: "SWITCH Autonomous Personal AI Operating System online. How can I assist you today?" },
  ]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [memories, setMemories] = useState<any[]>([]);
  const [userProfile, setUserProfile] = useState<any>({});
  const [pendingApproval, setPendingApproval] = useState<any>(null);

  // Fetch initial activities and memories
  const fetchData = async () => {
    try {
      const actRes = await fetch("http://localhost:8000/api/system/activity");
      if (actRes.ok) {
        const data = await actRes.json();
        setActivities(data);
      }
      const memRes = await fetch("http://localhost:8000/api/memory");
      if (memRes.ok) {
        const data = await memRes.json();
        setMemories(data.semantic_memories || []);
        setUserProfile(data.user_profile || {});
      }
    } catch (e) {
      // Backend fallback
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputQuery;
    if (!text.trim()) return;

    setChatLog((prev) => [...prev, { role: "user", content: text }]);
    setInputQuery("");
    setAssistantState("THINKING");
    setCurrentAction(`Routing intent for: "${text.slice(0, 30)}..."`);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (res.ok) {
        const data = await res.json();
        setAssistantState(data.requires_approval ? "WAITING" : "SUCCESS");
        setCurrentAction(data.requires_approval ? "Awaiting Human Approval" : "Task Completed");

        if (data.requires_approval && data.approval_id) {
          setPendingApproval({ approval_id: data.approval_id, message: data.response });
        }

        setChatLog((prev) => [...prev, { role: "assistant", content: data.response }]);
        fetchData();
      } else {
        setAssistantState("ERROR");
        setChatLog((prev) => [...prev, { role: "assistant", content: "Error communicating with SWITCH core server." }]);
      }
    } catch (e) {
      setAssistantState("ERROR");
      setChatLog((prev) => [
        ...prev,
        { role: "assistant", content: "SWITCH core backend is starting up or unreachable. Autonomous local mode standby." },
      ]);
    }
  };

  const handleTriggerCall = async () => {
    setAssistantState("CALLING");
    setCurrentAction("Initiating Outbound Phone Call to user's phone...");
    try {
      const res = await fetch("http://localhost:8000/api/phone/call", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          to_phone_number: "+1987654321",
          context_summary: "Deployment inspection & technical assistance request",
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setChatLog((prev) => [
          ...prev,
          { role: "assistant", content: `Phone call session initiated! SID: ${data.call_sid || "simulated"}` },
        ]);
      }
    } catch (e) {
      setAssistantState("ERROR");
    }
  };

  const handleConfirmApproval = async (approved: boolean) => {
    if (!pendingApproval) return;
    try {
      const res = await fetch("http://localhost:8000/api/tools/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ approval_id: pendingApproval.approval_id, approved }),
      });
      if (res.ok) {
        const data = await res.json();
        setPendingApproval(null);
        setAssistantState("SUCCESS");
        setChatLog((prev) => [
          ...prev,
          { role: "assistant", content: approved ? "Action approved and executed." : "Action rejected by user." },
        ]);
        fetchData();
      }
    } catch (e) {}
  };

  const handleDeleteMemory = async (key: string) => {
    try {
      await fetch(`http://localhost:8000/api/memory/${key}`, { method: "DELETE" });
      fetchData();
    } catch (e) {}
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Futuristic Header */}
      <header className="border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md px-6 py-3.5 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 text-slate-950 font-black tracking-widest text-lg shadow-lg shadow-cyan-500/20">
            S
          </div>
          <div>
            <h1 className="text-base font-bold tracking-wider text-slate-100 uppercase">SWITCH OS</h1>
            <p className="text-[10px] text-cyan-400 font-mono tracking-wide">AUTONOMOUS PERSONAL AI OPERATING SYSTEM</p>
          </div>
        </div>

        {/* Quick Action Badges */}
        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={handleTriggerCall}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20 transition font-medium"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            Phone Call AI
          </button>

          <button
            onClick={() => handleSendMessage("SWITCH, start my React project development mode.")}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-400 hover:bg-purple-500/20 transition font-medium"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Dev Mode Macro
          </button>
        </div>
      </header>

      {/* Main Grid Body */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 p-6 max-w-7xl mx-auto w-full">
        {/* Left Column: Visual Assistant & Interactive Workspace */}
        <div className="lg:col-span-7 flex flex-col space-y-6">
          {/* Visual State & Audio Waveform Card */}
          <div className="glass-panel rounded-2xl p-6 flex flex-col items-center justify-center relative overflow-hidden">
            <StateIndicator state={assistantState} currentAction={currentAction} />
            <AudioWaveform active={assistantState === "LISTENING" || assistantState === "SPEAKING"} />
          </div>

          {/* Chat & Command Input Box */}
          <div className="glass-panel rounded-2xl p-4 flex flex-col h-[380px]">
            <div className="flex-1 overflow-y-auto space-y-3 pr-2 mb-3">
              {chatLog.map((msg, i) => (
                <div
                  key={i}
                  className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
                >
                  <div
                    className={`max-w-[85%] px-4 py-2.5 rounded-2xl text-xs leading-relaxed ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white rounded-br-none"
                        : "bg-slate-900/80 border border-slate-800 text-slate-200 rounded-bl-none font-mono"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>

            {/* Input Bar */}
            <div className="flex items-center gap-2 pt-2 border-t border-slate-800">
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Talk to SWITCH or type an autonomous command..."
                className="flex-1 bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 font-mono transition"
              />
              <button
                onClick={() => setAssistantState(assistantState === "LISTENING" ? "IDLE" : "LISTENING")}
                className={`p-2.5 rounded-xl border transition ${
                  assistantState === "LISTENING"
                    ? "bg-cyan-500 text-slate-950 border-cyan-400 animate-pulse"
                    : "bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200"
                }`}
                title="Voice Input"
              >
                <Mic className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleSendMessage()}
                className="p-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-slate-950 font-bold hover:opacity-90 transition"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Telemetry, Memory Control, Activity Audit */}
        <div className="lg:col-span-5 flex flex-col space-y-5">
          <TelemetryWidget />
          <MemoryControlCenter
            memories={memories}
            userProfile={userProfile}
            onDeleteMemory={handleDeleteMemory}
          />
          <ActivityTimeline activities={activities} />
        </div>
      </div>

      {/* Human Approval Dialog Modal */}
      {pendingApproval && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel border-amber-500/40 rounded-2xl p-6 max-w-md w-full space-y-4 text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-100">Human Approval Required</h3>
            <p className="text-xs text-slate-400 font-mono leading-relaxed">{pendingApproval.message}</p>
            <div className="flex gap-3 pt-2">
              <button
                onClick={() => handleConfirmApproval(false)}
                className="flex-1 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-400 hover:bg-slate-800"
              >
                Reject Action
              </button>
              <button
                onClick={() => handleConfirmApproval(true)}
                className="flex-1 py-2 rounded-xl bg-amber-500 text-slate-950 text-xs font-bold hover:bg-amber-400"
              >
                Approve & Execute
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
