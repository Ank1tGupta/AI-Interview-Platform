import axios from "axios";

// All request paths below are relative to the backend's /api prefix, so
// normalise whether or not VITE_API_URL already includes it.
const root = (import.meta.env.VITE_API_URL || "http://localhost:8000")
  .replace(/\/+$/, "")
  .replace(/\/api$/, "");

const API = axios.create({
  baseURL: `${root}/api`,
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Public interview pages are unauthenticated - a 401 there is a real error,
// not an expired session, so only bounce recruiters back to login.
const PUBLIC_PATHS = ["/login", "/register", "/interview", "/thank-you"];

API.interceptors.response.use(
  (response) => response,
  (error) => {
    const onPublicPage = PUBLIC_PATHS.some((p) =>
      window.location.pathname.startsWith(p)
    );

    if (error.response?.status === 401 && !onPublicPage) {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default API;
