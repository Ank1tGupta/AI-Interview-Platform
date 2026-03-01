import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiRefreshCw } from "react-icons/fi";
import API from "../services/api";

export default function Dashboard() {
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState([]);
  const [view, setView] = useState("dashboard");

  const [role, setRole] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [questionCount, setQuestionCount] = useState(5);
  const [candidateEmail, setCandidateEmail] = useState("");
  const [candidateName, setCandidateName] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  const [pendingDelete, setPendingDelete] = useState(null);
  const [loading, setLoading] = useState(false); // NEW: loading state for refresh

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/");
      return;
    }
    fetchInterviews();
  }, [view]);

  const fetchInterviews = async () => {
    const start = Date.now();
    try {
      setLoading(true); // start spin
      const res = await API.get("/recruiter/interviews/");
      setInterviews(res.data || []);
    } catch (err) {
      console.error("fetch interviews error", err);
      setInterviews([]);
    } finally {
      const diff = Date.now() - start;
      const min = 500;
      if (diff < min) {
        setTimeout(() => setLoading(false), min - diff);
      } else {
        setLoading(false);
      }
    }
  };

  const createInterview = async () => {
    await API.post("/recruiter/create-interview/", {
      role,
      difficulty,
      question_count: questionCount,
      candidate_email: candidateEmail,
      candidate_name: candidateName,
    });

    setRole("");
    setCandidateEmail("");
    setCandidateName("");
    fetchInterviews();
  };

  const deleteInterview = async (id) => {
    try {
      await API.delete(`/recruiter/interviews/${id}/`);
      fetchInterviews();
    } catch (err) {
      alert("Failed to delete interview");
    }
  };

  const completed = interviews.filter(i => i.status === "Completed").length;

  const avgScore =
    interviews.length > 0
      ? (
          interviews
            .filter(i => i.score !== null)
            .reduce((acc, i) => acc + i.score, 0) /
          (interviews.filter(i => i.score !== null).length || 1)
        ).toFixed(2)
      : 0;

  return (
    <div className="min-h-screen flex bg-linear-to-br from-indigo-50 via-white to-purple-50">

      {/* Sidebar */}
      <div className="w-64 bg-white shadow-xl p-6 hidden md:block">
        <h2 className="text-2xl font-bold text-indigo-600 mb-8">
          AI Interview
        </h2>

        <nav className="space-y-4">
          <p
            className={`cursor-pointer ${view === "dashboard" ? "text-gray-600 font-medium" : "text-gray-400"}`}
            onClick={() => setView("dashboard")}
          >
            Dashboard
          </p>
          <p
            className={`cursor-pointer ${view === "interviews" ? "text-gray-600 font-medium" : "text-gray-400"}`}
            onClick={() => setView("interviews")}
          >
            Interviews
          </p>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">

        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">
            Recruiter Dashboard
          </h1>

          <div className="bg-white px-4 py-2 rounded-full shadow text-sm text-gray-600">
            AI Powered Evaluation
          </div>
        </div>

        {view === "dashboard" && (
          <>
            <div className="grid grid-cols-3 gap-6 mb-10">
              <div className="bg-white p-6 rounded-2xl shadow-md hover:shadow-xl transition">
                <p className="text-gray-500">Total Interviews</p>
                <h2 className="text-3xl font-bold text-indigo-600">
                  {interviews.length}
                </h2>
              </div>

              <div className="bg-white p-6 rounded-2xl shadow-md hover:shadow-xl transition">
                <p className="text-gray-500">Completed</p>
                <h2 className="text-3xl font-bold text-green-600">
                  {completed}
                </h2>
              </div>

              <div className="bg-white p-6 rounded-2xl shadow-md hover:shadow-xl transition">
                <p className="text-gray-500">Average Score</p>
                <h2 className="text-3xl font-bold text-purple-600">
                  {avgScore}
                </h2>
              </div>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-md mb-10">
              <h2 className="text-xl font-semibold mb-6 text-gray-800">
                Create New Interview
              </h2>

              <div className="grid grid-cols-5 gap-4">
                <input
                  className="border rounded-lg p-3 focus:ring-2 focus:ring-indigo-400 outline-none"
                  placeholder="Role"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                />

                <select
                  className="border rounded-lg p-3 focus:ring-2 focus:ring-indigo-400 outline-none"
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>

                <input
                  type="number"
                  className="border rounded-lg p-3 focus:ring-2 focus:ring-indigo-400 outline-none"
                  value={questionCount}
                  onChange={(e) => setQuestionCount(e.target.value)}
                />

                <input
                  className="border rounded-lg p-3 focus:ring-2 focus:ring-indigo-400 outline-none"
                  placeholder="Candidate Name"
                  value={candidateName}
                  onChange={(e) => setCandidateName(e.target.value)}
                />

                <input
                  className="border rounded-lg p-3 focus:ring-2 focus:ring-indigo-400 outline-none"
                  placeholder="Candidate Email"
                  value={candidateEmail}
                  onChange={(e) => setCandidateEmail(e.target.value)}
                />
              </div>

              <button
                onClick={createInterview}
                className="mt-6 bg-linear-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl shadow-lg hover:opacity-90 transition"
              >
                Create & Send Interview
              </button>
            </div>
          </>
        )}

        {view === "interviews" && (
          <div className="bg-white p-8 rounded-2xl shadow-md">

            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-800">
                Interview Sessions
              </h2>

              {/* Refresh Button with Spin */}
              <button
                onClick={fetchInterviews}
                disabled={loading}
                className="p-2 rounded-full hover:bg-indigo-100 text-indigo-600 transition disabled:opacity-50"
              >
                <FiRefreshCw
                  size={18}
                  className={loading ? "animate-spin" : ""}
                />
              </button>
            </div>

            <table className="w-full text-left">
              <thead>
                <tr className="border-b text-gray-500">
                  <th className="py-3">Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Score</th>
                  <th></th>
                </tr>
              </thead>

              <tbody>
                {interviews.map((i) => (
                  <tr key={i.id} className="border-b hover:bg-gray-50 transition">
                    <td className="py-3">{i.name || "-"}</td>
                    <td className="py-3">{i.email}</td>
                    <td>{i.role}</td>

                    <td>
                      <span
                        className={`px-3 py-1 rounded-full text-sm ${
                          i.status === "Completed"
                            ? "bg-green-100 text-green-700"
                            : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {i.status}
                      </span>
                    </td>

                    <td className="font-semibold">
                      {i.score ?? "-"}
                    </td>

                    <td className="space-x-2">
                      {i.status === "Completed" && (
                        <button
                          onClick={() => navigate(`/recruiter/report/${i.id}`)}
                          className="px-3 py-1 rounded-full text-sm bg-indigo-100 text-indigo-700 hover:bg-indigo-200 transition"
                        >
                          View Report
                        </button>
                      )}

                      <button
                        onClick={() => setPendingDelete(i.id)}
                        className="px-3 py-1 rounded-full text-sm bg-red-100 text-red-700 hover:bg-red-200 transition"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Modal */}
        {pendingDelete !== null && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center">
            <div className="bg-white p-8 rounded-2xl shadow-lg max-w-sm text-center">
              <p className="mb-6">
                Are you sure you want to delete this interview?
              </p>

              <div className="space-x-4">
                <button
                  onClick={() => {
                    deleteInterview(pendingDelete);
                    setPendingDelete(null);
                  }}
                  className="px-6 py-2 bg-red-600 text-white rounded-full hover:opacity-90"
                >
                  Yes, delete
                </button>

                <button
                  onClick={() => setPendingDelete(null)}
                  className="px-6 py-2 bg-gray-200 rounded-full hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}