import apiClient from "./apiClient";

const incidentService = {
    async getIncidentCenter(query = null) {
        try {
            const url = query ? `/incident?query=${encodeURIComponent(query)}` : "/incident";
            // Override 60s timeout for heavy dynamic simulations
            const response = await apiClient.get(url, query ? { timeout: 180000 } : undefined);
            return response.data;
        } catch (error) {
            console.error("Failed to fetch incident data:", error);
            throw error;
        }
    },
};

export default incidentService;