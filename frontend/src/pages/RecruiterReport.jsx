import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../services/api";

export default function RecruiterReport() {
  const { id } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      const res = await API.get(`/recruiter/report/${id}/`);
      setReport(res.data);
    };

    fetchReport();
  }, [id]);

  if (!report)
    return (
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-50 to-purple-50">
        <div className="text-gray-600 text-lg animate-pulse">
          Generating AI Report...
        </div>
      </div>
    );

  return (
    <div className="min-h-screen bg-linear-to-br from-indigo-50 via-white to-purple-50 p-10">

      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="bg-white p-8 rounded-3xl shadow-xl mb-10">

          <h1 className="text-3xl font-bold mb-6 text-gray-800">
            AI Interview Report
          </h1>

          <div className="flex items-center justify-between">

            <div>
              <p className="text-gray-500">Candidate</p>
              <p className="text-xl font-semibold">
                {report.candidate_name || report.candidate_email}
              </p>
            </div>

            <div>
              <p className="text-gray-500">Role</p>
              <p className="text-xl font-semibold">
                {report.role}
              </p>
            </div>

            <div>
              <p className="text-gray-500">Difficulty</p>
              <p className="text-xl font-semibold">
                {report.difficulty}
              </p>
            </div>

            {/* Big Score Circle */}
            <div className="flex flex-col items-center">
              <div className="w-24 h-24 rounded-full bg-linear-to-r from-indigo-600 to-purple-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                {report.overall_score ?? 0}
              </div>
              <p className="mt-2 text-gray-500 text-sm">
                Overall Score
              </p>
            </div>

          </div>

        </div>

        {/* Question Breakdown */}
        <div className="space-y-8">

          {report.questions.map((q, index) => (
            <div
              key={q.id}
              className="bg-white p-8 rounded-3xl shadow-md hover:shadow-xl transition"
            >
              <h2 className="text-lg font-semibold mb-4 text-gray-800">
                Question {index + 1}
              </h2>

              <p className="text-gray-700 mb-4">
                {q.question}
              </p>

              <div className="mb-4">
                <p className="text-sm text-gray-500 mb-1">
                  Candidate Answer
                </p>
                <div className="bg-gray-50 p-4 rounded-xl text-gray-700">
                  {q.answer || "No answer submitted"}
                </div>
              </div>

              {/* Score Bar */}
              {q.score !== null && (
                <div className="mb-4">
                  <div className="flex justify-between text-sm text-gray-500 mb-1">
                    <span>AI Score</span>
                    <span>{q.score}/10</span>
                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-linear-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${(q.score / 10) * 100}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {/* AI Feedback */}
              {q.feedback && (
                <div>
                  <p className="text-sm text-gray-500 mb-1">
                    AI Feedback
                  </p>
                  <div className="bg-indigo-50 border border-indigo-100 p-4 rounded-xl text-gray-700">
                    {q.feedback}
                  </div>
                </div>
              )}

            </div>
          ))}

        </div>

      </div>

    </div>
  );
}