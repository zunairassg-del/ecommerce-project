import axios from 'axios';

const API = axios.create({
    baseURL: 'https://ecom-zunatech.duckdns.org',
    withCredentials: true,
});

export default API;