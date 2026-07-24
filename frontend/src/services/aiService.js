import apiClient from "./apiClient";

const aiService = {
    async getAIDecisionCenter() {
        try {
            const response = await apiClient.get("/decision-center");
            return response.data;
        } catch (error) {
            console.error("Failed to fetch AI Decision Center data:", error);
            throw error;
        }
    },
};

export default aiService;