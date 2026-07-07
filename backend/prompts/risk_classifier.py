import json


def build_risk_classification_prompt(article: dict) -> str:
    """
    Build the prompt used by the Risk Classification Agent.
    """

    article_json = json.dumps(article, indent=2)

    return f"""
You are an AI Supply Chain Risk Intelligence Agent for a cement manufacturing company.

Your task is to analyze the following news article and produce a structured risk assessment.

News Article:
{article_json}

Analyze the article and identify:

1. Risk Category
2. Risk Severity
3. Confidence Score (0.0 to 1.0)
4. Business Impact
5. Affected Suppliers
6. Affected Materials
7. Summary
8. Reasoning
9. Recommended Action

Return ONLY valid JSON using this schema:

{{
    "category": "",
    "severity": "",
    "confidence": 0.0,
    "business_impact": "",
    "affected_suppliers": [
        {{
            "name": "",
            "entity_type": "",
            "location": "",
            "description": ""
        }}
    ],
    "affected_materials": [],
    "summary": "",
    "reasoning": "",
    "recommended_action": ""
}}

Do not include markdown.
Do not include explanations.
Return only valid JSON.
"""