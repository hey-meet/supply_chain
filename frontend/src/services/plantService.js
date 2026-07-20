import apiClient from "./apiClient";

const plantService = {
    async getPlantsInventory() {
        try {
            const response = await apiClient.get("/inventory");
            return response.data;
        } catch (error) {
            console.error("Failed to fetch Plants & Inventory data:", error);
            throw error;
        }
    },
};

export default plantService;