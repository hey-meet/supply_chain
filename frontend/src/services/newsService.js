import apiClient from "./apiClient";

const newsService = {
    async getNewsIntelligence() {
        try {
            const response = await apiClient.get("/api/news");
            return response.data;
        } catch (error) {
            console.error("Failed to fetch News Intelligence data:", error);
            throw error;
        }
    },
};

export default newsService;