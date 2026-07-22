import apiClient from "./apiClient";

const incidentService = {
    async getIncidentCenter() {
        const response = await apiClient.get("/incident");
        return response.data;
    },
};

export default incidentService;