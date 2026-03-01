import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// redirect to login on 401 to keep UX smooth
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response &&
      error.response.status === 401 &&
      !window.location.pathname.startsWith("/register")
    ) {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      window.location.href = "/"; // login page
    }
    return Promise.reject(error);
  }
);

export default API;