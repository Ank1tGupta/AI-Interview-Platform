import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";

export default function Interview() {
  const { token } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchInterview = async () => {
      try {
        const res = await API.get(`/public/interview/${token}/`);
        setQuestions(res.data.questions);
        setLoading(false);
      } catch (err) {
        alert("Invalid or expired interview link");
      }
    };

    fetchInterview();
  }, [token]);

  const handleSubmit = async () => {
    try {
      setSubmitting(true);

      const currentQuestion = questions[currentIndex];

      await API.post(`/public/interview/${token}/answer/`, {
        question_id: currentQuestion.id,
        answer_text: answer,
        time_taken_seconds: 60,
      });

      setAnswer("");

      if (currentIndex < questions.length - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        await API.post(`/public/interview/${token}/complete/`);
        navigate("/thank-you");
      }

      setSubmitting(false);
    } catch (err) {
      alert("Failed to submit answer");
      setSubmitting(false);
    }
  };

  if (loading)
    return (
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-50 to-purple-50">
        <div className="text-gray-600 text-lg animate-pulse">
          Preparing your AI interview...
        </div>
      </div>
    );

  if (questions.length === 0)
    return (
      <div className="min-h-screen flex items-center justify-center">
        No questions available.
      </div>
    );

  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-linear-to-br from-indigo-50 via-white to-purple-50 p-10">

      <div className="max-w-3xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800">
            AI Interview Session
          </h1>

          <p className="text-gray-500 mt-2">
            Question {currentIndex + 1} of {questions.length}
          </p>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-3 mt-4">
            <div
              className="bg-linear-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white p-8 rounded-3xl shadow-lg mb-6">

          <h2 className="text-lg font-semibold mb-4 text-gray-800">
            {currentQuestion.text}
          </h2>

          <textarea
            className="w-full border rounded-xl p-4 focus:ring-2 focus:ring-indigo-400 outline-none min-h-40"
            placeholder="Type your answer here..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

        </div>

        {/* Actions */}
        <div className="flex justify-between">

          <button
            disabled={currentIndex === 0}
            onClick={() => setCurrentIndex(currentIndex - 1)}
            className="px-6 py-2 rounded-xl border border-gray-300 text-gray-600 hover:bg-gray-100 disabled:opacity-40"
          >
            Previous
          </button>

          <button
            onClick={handleSubmit}
            disabled={!answer || submitting}
            className="bg-linear-to-r from-indigo-600 to-purple-600 text-white px-6 py-2 rounded-xl shadow-lg hover:opacity-90 transition disabled:opacity-40"
          >
            {currentIndex === questions.length - 1
              ? "Finish Interview"
              : "Submit & Next"}
          </button>

        </div>

      </div>

    </div>
  );
}