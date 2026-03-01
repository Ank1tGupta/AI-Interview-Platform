import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../services/api";

export default function RecruiterReport() {
  const { id } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      const res = await API.get(
        `/recruiter/report/${id}/`
      );
      setReport(res.data);
    };

    fetchReport();
  }, [id]);

  if (!report) return <div className="p-6">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow">

        <h1 className="text-2xl font-bold mb-4">
          Candidate Interview Report
        </h1>

        <p><strong>Overall Score:</strong> {report.overall_score}</p>

        <hr className="my-4" />

        {report.questions.map((q, index) => (
          <div key={q.id} className="mb-6 p-4 border rounded">
            <h3 className="font-semibold">
              Question {index + 1}
            </h3>

            <p className="mb-2">{q.question}</p>

            <p>
              <strong>Answer:</strong>{" "}
              {q.answer || "No answer submitted"}
            </p>

            {q.score !== null && (
              <p>
                <strong>Score:</strong> {q.score}
              </p>
            )}

            {q.feedback && (
              <p>
                <strong>Feedback:</strong> {q.feedback}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}