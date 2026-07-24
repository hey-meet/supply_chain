import apiClient from "./apiClient";

const networkService = {
    async getSupplyChainNetwork() {
        try {
            const response = await apiClient.get("/supply-chain");
            return response.data;
        } catch (error) {
            console.error("Failed to fetch Supply Chain Network data:", error);
            throw error;
        }
    },
};

export default networkService;