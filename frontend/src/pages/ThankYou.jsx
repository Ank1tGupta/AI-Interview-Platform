export default function ThankYou() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-50 via-white to-purple-50">
      <div className="bg-white p-8 rounded-3xl shadow-lg text-center max-w-md">
        <h1 className="text-2xl font-bold mb-4">
          Interview Submitted 🎉
        </h1>
        <p className="text-gray-600">
          Thank you for completing the interview. The recruiter will review your results.
        </p>
      </div>
    </div>
  );
}