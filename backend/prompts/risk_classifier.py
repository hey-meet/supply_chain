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

    serialized_article = json.dumps(
        article,
        indent=2,
    )

    return prompt_manager.render(
        template_name="risk_classification.txt",
        variables={
            "executive_summary_output": serialized_article,
        },
    )