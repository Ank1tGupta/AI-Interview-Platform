import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../services/api";

export default function Report() {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await API.get(`/recruiter/report/${id}/`);
        setReport(res.data);
        setLoading(false);
      } catch (err) {
        alert("Failed to load report");
      }
    };

    fetchReport();
  }, [id]);

  if (loading) {
    return <div className="p-6">Loading report...</div>;
  }

  if (!report) {
    return <div className="p-6">No report found.</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow-lg">

        <h1 className="text-2xl font-bold mb-4">
          Interview Report
        </h1>

        <div className="mb-6">
          <p><strong>Candidate:</strong> {report.candidate_name || report.candidate_email}</p>
          <p><strong>Role:</strong> {report.role}</p>
          <p><strong>Difficulty:</strong> {report.difficulty}</p>
          <p>
            <strong>Overall Score:</strong>{" "}
            <span className="text-blue-600 font-bold">
              {report.overall_score}
            </span>
          </p>
        </div>

        <hr className="mb-6" />

        {report.questions.map((q, index) => (
          <div key={q.id} className="mb-6 p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">
              Question {index + 1}
            </h3>

            <p className="mb-3 text-gray-700">
              {q.question}
            </p>

            <div className="mb-2">
              <strong>Your Answer:</strong>
              <p className="text-gray-600">
                {q.answer || "No answer submitted"}
              </p>
            </div>

            {q.score !== null && (
              <div className="mb-2">
                <strong>Score:</strong>{" "}
                <span className="text-green-600 font-semibold">
                  {q.score}/10
                </span>
              </div>
            )}

            {q.feedback && (
              <div>
                <strong>Feedback:</strong>
                <p className="text-gray-600">
                  {q.feedback}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}