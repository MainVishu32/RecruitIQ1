"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "../../../lib/api";
import { BarChart, Activity, Users, Target, Zap } from "lucide-react";
import { motion } from "framer-motion";

export default function AnalyticsPage() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const res = await api.get('/analytics/');
      return res.data;
    }
  });

  if (isLoading) return <div className="p-10 text-muted">Loading metrics...</div>;

  const cards = [
    { title: "Total Job Profiles", value: metrics?.total_jobs_posted, icon: Target, color: "text-blue-400" },
    { title: "Candidate Pool Size", value: metrics?.total_candidates_pooled, icon: Users, color: "text-emerald-400" },
    { title: "Avg. Match Score", value: `${metrics?.average_match_score}%`, icon: Activity, color: "text-purple-400" },
    { title: "AI Computations", value: metrics?.total_computations_run, icon: Zap, color: "text-amber-400" },
  ];

  return (
    <div className="max-w-7xl mx-auto p-6 h-screen pt-12">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold flex items-center gap-2">
          <BarChart className="text-accent" /> Platform Intelligence
        </h1>
        <p className="text-muted text-sm mt-1">Macro-level recruitment metrics and AI performance.</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-surface border border-white/10 rounded-xl p-6 relative overflow-hidden group hover:border-white/20 transition-colors"
          >
            <div className={`absolute -right-6 -top-6 opacity-5 group-hover:opacity-10 transition-opacity ${card.color}`}>
              <card.icon size={100} />
            </div>
            <div className="relative z-10">
              <h3 className="text-sm font-medium text-muted mb-2">{card.title}</h3>
              <div className="text-4xl font-bold tracking-tight text-white">{card.value}</div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Placeholder for future Recharts integration */}
      <div className="mt-8 bg-surface border border-white/10 rounded-xl p-6 h-64 flex items-center justify-center text-muted border-dashed">
        Detailed Matching Distribution Chart (Recharts) goes here.
      </div>
    </div>
  );
}