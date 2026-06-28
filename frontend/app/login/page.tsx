"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "../../lib/api";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("judge@hackathon.com");
  const [password, setPassword] = useState("securepassword123");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    try {
      const res = await api.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", res.data.access_token);
      router.push("/dashboard");
    } catch (error) {
      alert("Login failed. Please check backend login route or credentials.");
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-black text-white">
      <form onSubmit={handleLogin} className="flex flex-col gap-4 w-80">
        <h1 className="text-3xl font-bold text-center">RecruitIQ Login</h1>

        <input
          type="email"
          placeholder="Email"
          className="border p-2 rounded text-black"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="border p-2 rounded text-black"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="bg-blue-600 text-white p-2 rounded">
          Login
        </button>
      </form>
    </main>
  );
}