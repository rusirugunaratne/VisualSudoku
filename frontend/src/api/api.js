import axios from "axios";

const API_URL = 'http://localhost:8000/'

export const ENDPOINTS = {
    readBoard: "read_board",
    solveBoard: 'solve_board'
};

export const createAPIEndpoint = (endpoint) => {
    let url = API_URL + "api/" + endpoint + "/";
    return {
        fetch: () => axios.get(url),
        fetchById: (id) => axios.get(url + id),
        post: (newRecord) => axios.post(url, newRecord),
        put: (id, updatedRecord) => axios.put(url + id, updatedRecord),
        delete: (id) => axios.delete(url + id),
    };
};