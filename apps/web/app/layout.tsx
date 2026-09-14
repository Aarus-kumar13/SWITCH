import "./globals.css";
import React from "react";

export const metadata = {
  title: "SWITCH — Autonomous Personal AI Operating System",
  description: "Next-Generation Multimodal AI Operating System with Voice, Vision, Local Computer Control & Self-Learning",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-slate-950 text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}
