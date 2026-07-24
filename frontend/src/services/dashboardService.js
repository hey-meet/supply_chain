import apiClient from "./apiClient";

export const getDashboardData = async () => {
    try {
        const response = await apiClient.get("/dashboard");
        return response.data;
    } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
        throw error;
    }
};