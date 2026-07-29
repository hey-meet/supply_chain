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
    async scanTodayNews() {
        try {
            // Override default 60s timeout for the heavy multi-agent scan
            const response = await apiClient.get("/api/news/scan", { timeout: 180000 });
            return response.data;
        } catch (error) {
            console.error("Failed to execute daily news scan:", error);
            throw error;
        }
    },
};

export default newsService;