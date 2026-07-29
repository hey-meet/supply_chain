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
    async executeAction(actionKey, pageContext = "incident_center", entityId = null) {
        try {
            // Override 60s timeout for complex AI reasoning actions
            const response = await apiClient.post("/decision-center/action", {
                action: actionKey,
                page_context: pageContext,
                entity_id: entityId
            }, { timeout: 180000 });
            return response.data;
        } catch (error) {
            console.error(`Failed to execute AI action ${actionKey}:`, error);
            throw error;
        }
    },
};

export default aiService;