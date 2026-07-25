import apiClient from "./apiClient";

const incidentService = {
    async getIncidentCenter(query = null) {
        try {
            const url = query ? `/incident?query=${encodeURIComponent(query)}` : "/incident";
            const response = await apiClient.get(url);
            return response.data;
        } catch (error) {
            console.error("Failed to fetch incident data:", error);
            throw error;
        }
    },
};

export default incidentService;