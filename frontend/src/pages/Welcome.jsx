import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";

export default function Welcome() {
  const { token } = useParams();
  const navigate = useNavigate();
  const [interview, setInterview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInterview = async () => {
      try {
        const res = await API.get(`/public/interview/${token}/`);
        setInterview(res.data);
      } catch (err) {
        alert("Invalid or expired interview link");
      } finally {
        setLoading(false);
      }
    };

    fetchInterview();
  }, [token]);

  const start = () => {
    navigate(`/interview/${token}/start`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-50 to-purple-50">
        <div className="text-gray-600 text-lg animate-pulse">
          Preparing your interview…
        </div>
      </div>
    );
  }

  if (!interview) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-50 to-purple-50">
        <div className="text-gray-600">Interview not found.</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-50 via-white to-purple-50">
      <div className="max-w-lg bg-white p-8 rounded-3xl shadow-lg text-center">
        <h1 className="text-2xl font-bold mb-4">
          Welcome{interview.candidate_name ? `, ${interview.candidate_name}` : ''}!
        </h1>
        <p className="text-gray-600 mb-6">
          You're about to begin an AI-generated interview for the role of <strong>{interview.role}</strong> ({interview.difficulty}).
        </p>
        <button
          onClick={start}
          className="bg-linear-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl shadow-lg hover:opacity-90 transition"
        >
          Start Interview
        </button>
      </div>
    </div>
  );
}
