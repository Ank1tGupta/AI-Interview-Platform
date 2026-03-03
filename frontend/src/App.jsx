import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Interview from "./pages/Interview";
import Welcome from "./pages/Welcome";
import Report from "./pages/Report";
import ThankYou from "./pages/ThankYou";
import RecruiterReport from "./pages/RecruiterReport";
import Register from "./pages/Register";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/interview/:token" element={<Welcome />} />
        <Route path="/interview/:token/start" element={<Interview />} />
        <Route path="/report/:id" element={<Report />} />
        <Route path="/thank-you" element={<ThankYou />} />
        <Route path="/recruiter/report/:id" element={<RecruiterReport />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;