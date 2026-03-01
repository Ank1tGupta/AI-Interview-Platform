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
      const currentQuestion = questions[currentIndex];

      await API.post(
        `/public/interview/${token}/answer/`,
        {
          question_id: currentQuestion.id,
          answer_text: answer,
          time_taken_seconds: 60
        }
      );

      setAnswer("");

      if (currentIndex < questions.length - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        await API.post(`/public/interview/${token}/complete/`);
        navigate(`/thank-you`);
      }

    } catch (err) {
      alert("Failed to submit answer");
    }
  };

  if (loading) {
    return <div className="p-6">Loading interview...</div>;
  }

  if (questions.length === 0) {
    return <div className="p-6">No questions available.</div>;
  }

  const currentQuestion = questions[currentIndex];

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-lg font-semibold mb-4">
          Question {currentIndex + 1} of {questions.length}
        </h2>

        <p className="mb-6 text-gray-700">
          {currentQuestion.text}
        </p>

        <textarea
          className="w-full p-3 border rounded mb-4"
          rows="5"
          placeholder="Type your answer here..."
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />

        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {currentIndex === questions.length - 1
            ? "Finish Interview"
            : "Next Question"}
        </button>
      </div>
    </div>
  );
}