import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

export default function Dashboard() {
  const navigate = useNavigate();

  const [interviews, setInterviews] = useState([]);

  const [role, setRole] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [questionCount, setQuestionCount] = useState(5);
  const [candidateEmail, setCandidateEmail] = useState("");

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    const res = await API.get("/recruiter/interviews/");
    setInterviews(res.data);
  };

  const createInterview = async () => {
    await API.post("/recruiter/create-interview/", {
      role,
      difficulty,
      question_count: questionCount,
      candidate_email: candidateEmail
    });

    setRole("");
    setCandidateEmail("");
    fetchInterviews();
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-6">
        Recruiter Dashboard
      </h1>

      {/* Create Interview */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="font-semibold mb-4">
          Create Interview
        </h2>

        <input
          className="border p-2 w-full mb-2"
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />

        <select
          className="border p-2 w-full mb-2"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        <input
          type="number"
          className="border p-2 w-full mb-2"
          value={questionCount}
          onChange={(e) => setQuestionCount(e.target.value)}
        />

        <input
          className="border p-2 w-full mb-4"
          placeholder="Candidate Email"
          value={candidateEmail}
          onChange={(e) => setCandidateEmail(e.target.value)}
        />

        <button
          onClick={createInterview}
          className="bg-blue-600 text-white px-4 py-2 rounded w-full"
        >
          Create & Send Interview
        </button>
      </div>

      {/* Interview List */}
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-4">
          Candidate Interviews
        </h2>

        {interviews.map((i) => (
          <div key={i.id} className="border p-3 rounded mb-2">
            <p><strong>{i.email}</strong></p>
            <p>Role: {i.role}</p>
            <p>Status: {i.status}</p>

            {i.score && <p>Score: {i.score}</p>}

            {i.status === "Completed" && (
              <button
                onClick={() => navigate(`/recruiter/report/${i.id}`)}
                className="mt-2 bg-green-600 text-white px-3 py-1 rounded"
              >
                View Report
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}