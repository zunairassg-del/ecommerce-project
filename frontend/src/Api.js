import axios from "axios";

const api = axios.create({
    baseURL: "http://10.168.157.208:8000/api"
});

export default api;