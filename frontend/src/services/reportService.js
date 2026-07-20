import apiClient from "./apiClient";

const reportService = {
    async getExecutiveReports() {
        try {
            const response = await apiClient.get("/reports");
            return response.data;
        } catch (error) {
            console.error("Failed to fetch Executive Reports data:", error);
            throw error;
        }
    },
};

export default reportService;