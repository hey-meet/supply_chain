import json
from typing import Any

from backend.prompts.prompt_manager import (
    prompt_manager,
)


def build_risk_classification_prompt(
    article: dict[str, Any],
) -> str:
    """
    Build the Risk Classification prompt using the
    enterprise Prompt Manager.
    """

    article_json = json.dumps(article, indent=2)

    return f"""
You are an AI Supply Chain Risk Intelligence Agent for a cement manufacturing company.

Your task is to analyze the following structured news context and produce a valid risk assessment.

Structured News Context:
{article_json}

Analyze the disruption and identify:

1. Risk Category
2. Risk Severity
3. Confidence Score
4. Business Impact
5. Primary Location
6. Affected Suppliers
7. Affected Materials
8. Summary
9. Reasoning
10. Recommended Action

Return ONLY valid JSON.

The response MUST exactly follow this schema:

{{
    "category": "raw_material_shortage | transportation | weather | port_congestion | supplier_failure | regulatory | labor_strike | energy | price_fluctuation | geopolitical | other",

    "severity": "low | medium | high | critical",

    "confidence": 0.95,

    "business_impact": "low | medium | high | severe",

    "location": {{
        "country": "",
        "state": null,
        "city": null
    }},

    "affected_suppliers": [
        {{
            "name": "",
            "entity_type": "",
            "location": "",
            "description": ""
        }}
    ],

    "affected_materials": [
        "Coal",
        "Limestone"
    ],

    "summary": "",

    "reasoning": "",

    "recommended_action": ""
}}

STRICT RULES

1. category MUST be exactly one of:

- raw_material_shortage
- transportation
- weather
- port_congestion
- supplier_failure
- regulatory
- labor_strike
- energy
- price_fluctuation
- geopolitical
- other

2. severity MUST be exactly one of:

- low
- medium
- high
- critical

3. business_impact MUST be exactly one of:

- low
- medium
- high
- severe

4. confidence MUST be a decimal number between 0.0 and 1.0.

5. location represents the PRIMARY real-world place where the
disruption is occurring.

- If the article clearly names a location, return it with at least
  "country" filled in ("state" and "city" as available).
- If NO clear real-world location is stated or reasonably inferable,
  return "location": null. Do NOT guess or invent a location that
  isn't supported by the article text.

6. affected_suppliers MUST be an array of supplier objects.

Example:

[
    {{
        "name": "Western Coalfields",
        "entity_type": "Supplier",
        "location": "Maharashtra",
        "description": "Primary coal supplier"
    }}
]

7. affected_materials MUST be an array of strings.

Correct:

[
    "Coal",
    "Limestone",
    "Diesel"
]

Incorrect:

[
    {{
        "name": "Coal",
        "description": "Critical raw material"
    }}
]

8. summary MUST contain 2-3 concise sentences.

9. reasoning MUST briefly explain why the risk category and severity were selected.

10. recommended_action MUST provide clear mitigation steps for the supply chain team.

11. Do NOT invent suppliers if none are mentioned. Return an empty list.

12. Return ONLY valid JSON.

13. Do NOT use Markdown.

14. Do NOT wrap the response inside ```json blocks.

15. Do NOT include explanations before or after the JSON.
"""
