import axios from "axios";

const BASE_URL = window.location.protocol + '//' + window.location.hostname + ':8000'

// console.log(BASE_URL)


export default axios.create({
    baseURL: BASE_URL
});