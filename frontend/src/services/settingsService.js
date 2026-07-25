import apiClient from "./apiClient";

export const getSettingsData = async () => {
    try {
        const response = await apiClient.get("/settings");
        return response.data;
    } catch (error) {
        console.error("Failed to fetch settings data:", error);
        throw error;
    }
};

export const saveSettingsData = async (settings) => {
    try {
        const response = await apiClient.post("/settings", settings);
        return response.data;
    } catch (error) {
        console.error("Failed to save settings data:", error);
        throw error;
    }
};