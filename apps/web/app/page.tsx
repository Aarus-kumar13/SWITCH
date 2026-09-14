"use client";

import React, { useState, useEffect } from "react";
import { Mic, Send, PhoneCall, ShieldAlert, Sparkles, Terminal, Activity, Brain } from "lucide-react";
import { JarvisCore } from "@/components/JarvisCore";
import { HudHeader } from "@/components/HudHeader";
import { QuickActions } from "@/components/QuickActions";
import { ActiveTasksCard } from "@/components/ActiveTasksCard";
import { TelemetryWidget } from "@/components/TelemetryWidget";
import { ActivityTimeline, ActivityItem } from "@/components/ActivityTimeline";
import { MemoryControlCenter } from "@/components/MemoryControlCenter";
import { AssistantState } from "@/components/StateIndicator";

export default function JarvisDashboard() {
  const [inputQuery, setInputQuery] = useState("");
  const [assistantState, setAssistantState] = useState<AssistantState>("IDLE");
  const [currentAction, setCurrentAction] = useState<string>("");
  const [isListening, setIsListening] = useState<boolean>(false);
  const [chatLog, setChatLog] = useState<Array<{ role: string; content: string }>>([
    { role: "assistant", content: "SWITCH OS JARVIS Core online. All 14 specialized agents initialized. How can I help you?" },
  ]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [memories, setMemories] = useState<any[]>([]);
  const [userProfile, setUserProfile] = useState<any>({});
  const [pendingApproval, setPendingApproval] = useState<any>(null);

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
    } catch (e) {}
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
    setIsListening(false);
    setAssistantState("THINKING");
    setCurrentAction(`Analyzing request & context for: "${text.slice(0, 35)}..."`);

    // Simulated multi-step progress feedback as specified in Section 36
    setTimeout(() => {
      setAssistantState("PLANNING");
      setCurrentAction("Formulating multi-step execution plan...");
    }, 800);

    setTimeout(() => {
      setAssistantState("EXECUTING");
      setCurrentAction("Executing authorized tools & computer agents...");
    }, 1600);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (res.ok) {
        const data = await res.json();
        setAssistantState(data.requires_approval ? "WAITING" : "SUCCESS");
        setCurrentAction(data.requires_approval ? "Requires Human Approval Checkpoint" : "Verified successfully.");

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
        { role: "assistant", content: "SWITCH backend is starting up or unreachable. Standby mode active." },
      ]);
    }
  };

  const handleToggleListen = () => {
    if (isListening) {
      setIsListening(false);
      setAssistantState("IDLE");
      setCurrentAction("");
    } else {
      setIsListening(true);
      setAssistantState("LISTENING");
      setCurrentAction("Listening to voice input...");
      // Auto-simulate voice input capture after 3.5s
      setTimeout(() => {
        if (isListening) {
          handleSendMessage("SWITCH, inspect my project and check server telemetry.");
        }
      }, 3500);
    }
  };

  const handleTriggerCall = async () => {
    setAssistantState("CALLING");
    setCurrentAction("Initiating Outbound Phone Call to registered phone number...");
    try {
      const res = await fetch("http://localhost:8000/api/phone/call", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          to_phone_number: "+1987654321",
          context_summary: "Deployment inspection & technical problem discussion",
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
    <main className="min-h-screen bg-[#030712] text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* JARVIS HUD Header */}
      <HudHeader
        onTriggerCall={handleTriggerCall}
        onOpenMacro={() => handleSendMessage("SWITCH, start my React project development environment.")}
      />

      {/* Main Grid Content */}
      <div className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        {/* Quick Action HUD Bar (Section 35 Spec) */}
        <QuickActions onActionClick={(cmd) => handleSendMessage(cmd)} />

        {/* Central Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: JARVIS Core & Command Console */}
          <div className="lg:col-span-7 flex flex-col space-y-6">
            {/* Glowing JARVIS Reactor Core Visualizer */}
            <div className="glass-panel border-cyan-500/20 bg-slate-950/80 rounded-2xl relative overflow-hidden shadow-[0_0_50px_rgba(6,182,212,0.1)]">
              <JarvisCore
                state={assistantState}
                currentAction={currentAction}
                isListening={isListening}
                onToggleListen={handleToggleListen}
                onTriggerCall={handleTriggerCall}
              />
            </div>

            {/* High-Tech Terminal Command Console */}
            <div className="glass-panel border-cyan-500/20 bg-slate-950/90 rounded-2xl p-4 flex flex-col h-[380px] shadow-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
                <span className="text-xs font-mono text-cyan-400 flex items-center gap-2 font-bold">
                  <Terminal className="w-4 h-4 text-cyan-400" />
                  JARVIS MULTIMODAL CONSOLE
                </span>
                <span className="text-[10px] font-mono text-slate-500">VOICE & TEXT ONLINE</span>
              </div>

              {/* Chat Log Stream */}
              <div className="flex-1 overflow-y-auto space-y-3 pr-2 mb-3">
                {chatLog.map((msg, i) => (
                  <div key={i} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
                    <div
                      className={`max-w-[85%] px-4 py-2.5 rounded-2xl text-xs leading-relaxed ${
                        msg.role === "user"
                          ? "bg-gradient-to-r from-blue-600 to-cyan-500 text-slate-950 font-bold rounded-br-none shadow-[0_0_15px_rgba(6,182,212,0.3)]"
                          : "bg-slate-900/90 border border-cyan-500/20 text-cyan-100 rounded-bl-none font-mono shadow-inner"
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
              </div>

              {/* Command Input Bar */}
              <div className="flex items-center gap-2 pt-2 border-t border-slate-800">
                <input
                  type="text"
                  value={inputQuery}
                  onChange={(e) => setInputQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder='Say "SWITCH, look at this..." or type a command...'
                  className="flex-1 bg-slate-950 border border-cyan-500/30 rounded-xl px-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-400 font-mono transition shadow-inner"
                />
                <button
                  onClick={handleToggleListen}
                  className={`p-2.5 rounded-xl border transition ${
                    isListening
                      ? "bg-cyan-400 text-slate-950 border-cyan-300 animate-pulse shadow-[0_0_20px_rgba(6,182,212,0.8)]"
                      : "bg-slate-900 border-cyan-500/30 text-cyan-400 hover:bg-slate-800"
                  }`}
                  title="Voice Command"
                >
                  <Mic className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleSendMessage()}
                  className="p-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-400 text-slate-950 font-bold hover:brightness-110 transition shadow-[0_0_15px_rgba(6,182,212,0.4)]"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: HUD Widgets & Telemetry */}
          <div className="lg:col-span-5 flex flex-col space-y-5">
            <TelemetryWidget />
            <ActiveTasksCard tasks={[]} />
            <MemoryControlCenter memories={memories} userProfile={userProfile} onDeleteMemory={handleDeleteMemory} />
            <ActivityTimeline activities={activities} />
          </div>
        </div>
      </div>

      {/* Human Approval Dialog Modal */}
      {pendingApproval && (
        <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 z-50">
          <div className="glass-panel border-amber-500/50 bg-slate-950/95 rounded-2xl p-6 max-w-md w-full space-y-4 text-center shadow-[0_0_50px_rgba(245,158,11,0.3)]">
            <div className="mx-auto w-12 h-12 rounded-full bg-amber-500/10 border border-amber-500/40 flex items-center justify-center text-amber-400">
              <ShieldAlert className="w-6 h-6 animate-pulse" />
            </div>
            <h3 className="text-base font-mono font-bold text-slate-100 uppercase tracking-wider">HUMAN APPROVAL REQUIRED</h3>
            <p className="text-xs text-slate-300 font-mono leading-relaxed bg-slate-900/90 p-3 rounded-lg border border-slate-800">
              {pendingApproval.message}
            </p>
            <div className="flex gap-3 pt-2">
              <button
                onClick={() => handleConfirmApproval(false)}
                className="flex-1 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono font-semibold text-slate-400 hover:bg-slate-800"
              >
                REJECT
              </button>
              <button
                onClick={() => handleConfirmApproval(true)}
                className="flex-1 py-2.5 rounded-xl bg-amber-500 text-slate-950 font-mono text-xs font-bold hover:bg-amber-400 shadow-[0_0_15px_rgba(245,158,11,0.4)]"
              >
                APPROVE & EXECUTE
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
