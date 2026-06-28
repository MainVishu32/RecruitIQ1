import axios from "axios";

export const api = axios.create({
  baseURL: "https://recruitiq1.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});