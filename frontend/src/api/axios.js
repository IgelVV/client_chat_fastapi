// import axios from "axios";
// import { getObjectFromLocalStorage } from "../utils/localStorageManager"
// import localAuthName from "../hooks/useAuth";

// const BASE_URL = window.location.protocol + '//' + window.location.hostname + ':8000'


// const getAccessToken = () => {
//     const auth = getObjectFromLocalStorage(localAuthName);
//     console.log(auth)
//     return auth?.accessToken
// }

// export default axios.create({
//     baseURL: BASE_URL,
//     headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getAccessToken()}` },
//     withCredentials: true
// });

// export const getAxiosPrivate = () => axios.create({
//     baseURL: BASE_URL,
//     headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getAccessToken()}` },
//     withCredentials: true
// });


import axios from 'axios';
import { getLocalAuth } from "../context/AuthProvider"

const BASE_URL = window.location.protocol + '//' + window.location.hostname + ':8000'

const api = axios.create({
  baseURL: BASE_URL,
});

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    const token = getLocalAuth()?.accessToken;
    console.log(token)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api
