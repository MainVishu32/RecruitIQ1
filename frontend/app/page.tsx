import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-bold">RecruitIQ</h1>
      <p className="text-lg">Frontend is live successfully.</p>

      <Link
        href="/dashboard"
        className="px-4 py-2 rounded bg-blue-600 text-white"
      >
        Go to Dashboard
      </Link>
    </main>
  );
}