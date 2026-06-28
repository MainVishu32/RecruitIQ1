"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload,
  Play,
  CheckCircle2,
  BrainCircuit,
  FileText,
} from "lucide-react";
import { api } from "../../lib/api";

export default function DashboardPage() {
  const queryClient = useQueryClient();

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null);
  const [csvFile, setCsvFile] = useState<File | null>(null);

  // Job Form State
  const [jobTitle, setJobTitle] = useState("");
  const [jobDesc, setJobDesc] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  function handleEnterDashboard() {
    localStorage.setItem("access_token", "demo-token");
    setIsAuthenticated(true);
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
  }

  // Queries
  const { data: jobs } = useQuery({
    queryKey: ["jobs"],
    queryFn: async () => {
      const res = await api.get("/jobs/");
      return res.data;
    },
    enabled: isAuthenticated,
  });

  const { data: results, isLoading: isLoadingResults } = useQuery({
    queryKey: ["results", selectedJobId],
    queryFn: async () => {
      if (!selectedJobId) return null;
      const res = await api.get(`/analysis/results/${selectedJobId}`);
      return res.data;
    },
    enabled: isAuthenticated && !!selectedJobId,
  });

  // Mutations
  const createJob = useMutation({
    mutationFn: async () =>
      await api.post("/jobs/upload", {
        title: jobTitle,
        description: jobDesc,
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
      setSelectedJobId(data.data.id);
      setJobTitle("");
      setJobDesc("");
    },
  });

  const uploadCsv = useMutation({
    mutationFn: async () => {
      if (!csvFile) return;

      const formData = new FormData();
      formData.append("file", csvFile);

      await api.post("/candidates/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },
    onSuccess: () => alert("Candidates uploaded successfully."),
  });

  const runAnalysis = useMutation({
    mutationFn: async () => await api.post(`/analysis/run/${selectedJobId}`),
    onSuccess: () =>
      queryClient.invalidateQueries({
        queryKey: ["results", selectedJobId],
      }),
    onError: () => {
      alert(
        "Analysis route is currently disabled on backend for deployment. UI is working."
      );
    },
  });

  if (!isAuthenticated) {
    return (
      <main className="min-h-screen bg-black text-white grid grid-cols-1 md:grid-cols-2">
        <section className="flex flex-col justify-center px-10 md:px-20 bg-gradient-to-br from-black via-[#0b1120] to-black">
          <div className="flex items-center gap-3 mb-6">
            <BrainCircuit className="text-blue-500" size={36} />
            <h1 className="text-4xl font-bold">RecruitIQ</h1>
          </div>

          <h2 className="text-5xl font-bold leading-tight mb-4">
            Semantic Hiring Intelligence
          </h2>

          <p className="text-gray-400 text-lg max-w-md">
            Upload job descriptions, ingest candidate datasets, and discover
            best-fit profiles using intelligent matching.
          </p>
        </section>

        <section className="flex items-center justify-center p-8">
          <div className="w-full max-w-md bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl">
            <h2 className="text-3xl font-bold mb-2">Welcome back</h2>
            <p className="text-gray-400 mb-8">
              Continue to your RecruitIQ workspace.
            </p>

            <button
              onClick={handleEnterDashboard}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg transition"
            >
              Enter Dashboard
            </button>

            <p className="text-xs text-gray-500 mt-4 text-center">
              Prototype demo login enabled.
            </p>
          </div>
        </section>
      </main>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 grid grid-cols-12 gap-8 h-screen pt-12">
      {/* Sidebar: Data Ingestion */}
      <div className="col-span-4 space-y-8">
        <div>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2 text-xl font-medium tracking-tight">
              <BrainCircuit className="text-accent" />
              RecruitIQ
            </div>

            <button
              onClick={handleLogout}
              className="text-xs text-muted hover:text-white border border-white/10 px-3 py-1 rounded"
            >
              Logout
            </button>
          </div>

          <p className="text-sm text-muted">Semantic Discovery Engine</p>
        </div>

        {/* Job Creation Panel */}
        <div className="bg-surface border border-white/10 rounded-xl p-5 shadow-2xl bg-glass-gradient">
          <h3 className="text-sm font-semibold mb-4 flex items-center gap-2">
            <FileText size={16} /> Define Job Blueprint
          </h3>

          <input
            className="w-full bg-black/50 border border-white/10 rounded-md p-2 text-sm mb-3 focus:outline-none focus:border-accent transition-colors"
            placeholder="Job Title (e.g. Senior Frontend Engineer)"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
          />

          <textarea
            className="w-full bg-black/50 border border-white/10 rounded-md p-2 text-sm h-32 focus:outline-none focus:border-accent transition-colors resize-none"
            placeholder="Paste detailed job description here..."
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          />

          <button
            onClick={() => createJob.mutate()}
            disabled={createJob.isPending || !jobTitle || !jobDesc}
            className="w-full mt-2 bg-white text-black font-medium py-2 rounded-md text-sm hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            {createJob.isPending ? "Saving..." : "Save Job Profile"}
          </button>
        </div>

        {/* Candidate Upload Panel */}
        <div className="bg-surface border border-white/10 rounded-xl p-5 bg-glass-gradient">
          <h3 className="text-sm font-semibold mb-4 flex items-center gap-2">
            <Upload size={16} /> Ingest Candidates (CSV)
          </h3>

          <input
            type="file"
            accept=".csv"
            onChange={(e) => setCsvFile(e.target.files?.[0] || null)}
            className="text-sm text-muted file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-white/10 file:text-white hover:file:bg-white/20 mb-3 w-full"
          />

          <button
            onClick={() => uploadCsv.mutate()}
            disabled={uploadCsv.isPending || !csvFile}
            className="w-full bg-surfaceHighlight border border-white/10 text-white font-medium py-2 rounded-md text-sm hover:bg-white/10 transition-colors disabled:opacity-50"
          >
            {uploadCsv.isPending ? "Uploading..." : "Upload Dataset"}
          </button>
        </div>
      </div>

      {/* Main Content: Discovery & Results */}
      <div className="col-span-8 flex flex-col">
        {/* Job Selector & Trigger */}
        <div className="flex justify-between items-center mb-6 bg-surface border border-white/10 rounded-xl p-4">
          <select
            className="bg-black/50 border border-white/10 rounded-md p-2 text-sm focus:outline-none min-w-[300px]"
            onChange={(e) => setSelectedJobId(Number(e.target.value))}
            value={selectedJobId || ""}
          >
            <option value="" disabled>
              Select a Job Profile to Analyze
            </option>

            {jobs?.map((job: any) => (
              <option key={job.id} value={job.id}>
                {job.title}
              </option>
            ))}
          </select>

          <button
            onClick={() => runAnalysis.mutate()}
            disabled={runAnalysis.isPending || !selectedJobId}
            className="flex items-center gap-2 bg-accent text-white font-medium px-6 py-2 rounded-md text-sm hover:bg-blue-600 transition-colors disabled:opacity-50 shadow-[0_0_15px_rgba(59,130,246,0.3)]"
          >
            <Play size={16} />
            {runAnalysis.isPending ? "Running AI Pipeline..." : "Run Semantic Search"}
          </button>
        </div>

        {/* Results Stream */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
          {isLoadingResults && (
            <div className="text-muted text-sm animate-pulse">
              Computing vector distances...
            </div>
          )}

          <AnimatePresence>
            {results?.map((res: any, index: number) => (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                key={res.result_id}
                className="bg-surface border border-white/10 rounded-xl p-5 hover:border-accent/50 transition-colors group relative overflow-hidden"
              >
                {/* Score Gradient Background */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-accent/10 rounded-bl-full blur-3xl pointer-events-none" />

                <div className="flex justify-between items-start mb-4 relative z-10">
                  <div>
                    <h2 className="text-lg font-semibold flex items-center gap-2">
                      {res.candidate.full_name}
                      {res.overall_score > 80 && (
                        <CheckCircle2 size={16} className="text-success" />
                      )}
                    </h2>
                    <p className="text-sm text-muted">
                      {res.candidate.experience_years} years exp •{" "}
                      {res.candidate.email}
                    </p>
                  </div>

                  <div className="text-right">
                    <div className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
                      {res.overall_score}%
                    </div>
                    <div className="text-xs text-muted">Match Score</div>
                  </div>
                </div>

                {/* XAI Report */}
                <div className="bg-black/40 border border-white/5 rounded-lg p-4 mb-4">
                  <p className="text-sm leading-relaxed text-gray-300">
                    <span className="font-semibold text-white">
                      AI Reasoning:{" "}
                    </span>
                    {res.xai_report}
                  </p>
                </div>

                {/* Skill Badges */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-xs font-semibold text-muted mb-2 uppercase tracking-wider">
                      Matched Context
                    </h4>

                    <div className="flex flex-wrap gap-2">
                      {res.matched_skills.map((skill: string, i: number) => (
                        <span
                          key={i}
                          className="px-2 py-1 bg-success/10 text-success border border-success/20 rounded text-xs"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-xs font-semibold text-muted mb-2 uppercase tracking-wider">
                      Missing Context
                    </h4>

                    <div className="flex flex-wrap gap-2">
                      {res.missing_skills.map((skill: string, i: number) => (
                        <span
                          key={i}
                          className="px-2 py-1 bg-danger/10 text-danger border border-danger/20 rounded text-xs"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {!isLoadingResults && results?.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-muted border border-dashed border-white/10 rounded-xl p-10">
              <BrainCircuit size={48} className="mb-4 opacity-20" />
              <p>No analysis results found. Select a job and run the pipeline.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}