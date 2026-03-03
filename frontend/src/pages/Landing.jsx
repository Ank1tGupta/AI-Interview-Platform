import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-linear-to-br from-indigo-50 via-white to-purple-50 relative overflow-hidden">

      {/* Decorative Glow */}
      <div className="absolute -top-40 -right-40 w-96 h-96 bg-purple-300 opacity-20 rounded-full blur-3xl"></div>
      <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-300 opacity-20 rounded-full blur-3xl"></div>

      {/* Navbar */}
      <div className="flex justify-between items-center px-10 py-6">
        <h1 className="text-2xl font-bold bg-linear-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          AI Interview
        </h1>

        <div className="space-x-4">
          <button
            onClick={() => navigate("/login")}
            className="text-gray-600 hover:text-indigo-600"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/register")}
            className="bg-linear-to-r from-indigo-600 to-purple-600 text-white px-5 py-2 rounded-xl shadow-md hover:opacity-90 transition"
          >
            Get Started
          </button>
        </div>
      </div>

      {/* Hero Section */}
      <div className="text-center mt-24 px-6">
        <h2 className="text-5xl font-extrabold text-gray-800 leading-tight">
          AI-Powered Interviews <br />
          <span className="bg-linear-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            That Evaluate Smarter
          </span>
        </h2>

        <p className="mt-6 text-gray-600 max-w-2xl mx-auto text-lg">
          Automate candidate screening with AI-generated questions,
          intelligent evaluation, and detailed performance insights —
          all in one seamless platform.
        </p>

        <div className="mt-10 space-x-4">
          <button
            onClick={() => navigate("/register")}
            className="bg-linear-to-r from-indigo-600 to-purple-600 text-white px-8 py-3 rounded-2xl shadow-lg hover:opacity-90 transition"
          >
            Start Free Trial
          </button>

          <button
            onClick={() => navigate("/login")}
            className="border border-gray-300 px-8 py-3 rounded-2xl hover:bg-gray-100 transition"
          >
            Recruiter Login
          </button>
        </div>
      </div>

      {/* Features Section */}
      <div className="mt-32 px-10 grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">

        <div className="bg-white/70 backdrop-blur-xl border border-gray-100 p-8 rounded-3xl shadow-md hover:shadow-xl transition">
          <h3 className="text-xl font-semibold mb-4 text-indigo-600">
            AI Question Generation
          </h3>
          <p className="text-gray-600">
            Generate role-specific interview questions instantly using advanced AI models.
          </p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl border border-gray-100 p-8 rounded-3xl shadow-md hover:shadow-xl transition">
          <h3 className="text-xl font-semibold mb-4 text-purple-600">
            Automated Evaluation
          </h3>
          <p className="text-gray-600">
            Get intelligent scoring, feedback, and improvement suggestions in seconds.
          </p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl border border-gray-100 p-8 rounded-3xl shadow-md hover:shadow-xl transition">
          <h3 className="text-xl font-semibold mb-4 text-indigo-600">
            Secure Token Access
          </h3>
          <p className="text-gray-600">
            Send candidates secure interview links with zero login friction.
          </p>
        </div>

      </div>

      {/* Final CTA */}
      <div className="text-center mt-32 pb-20">
        <h3 className="text-3xl font-bold text-gray-800">
          Ready to Transform Your Hiring Process?
        </h3>

        <button
          onClick={() => navigate("/register")}
          className="mt-8 bg-linear-to-r from-indigo-600 to-purple-600 text-white px-10 py-4 rounded-2xl shadow-lg hover:opacity-90 transition"
        >
          Create Your First Interview
        </button>
      </div>

    </div>
  );
}