import json
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.prompts.risk_classifier import (
    build_risk_classification_prompt,
)


def test_risk_classification_prompt():
    """
    Verify that the Prompt Manager correctly loads and renders
    the Risk Classification prompt.
    """

    sample_article = {
        "title": "Heavy rainfall disrupts limestone transportation",
        "source": "Reuters",
        "location": "Rajasthan, India",
        "summary": (
            "Heavy rainfall has blocked major highways, "
            "delaying limestone deliveries to nearby cement plants."
        ),
    }

    prompt = build_risk_classification_prompt(
        sample_article
    )

    # Basic validation
    assert isinstance(prompt, str)
    assert len(prompt) > 0

    article_json = json.dumps(
        sample_article,
        indent=2,
    )

    # Verify the template rendered correctly
    assert article_json in prompt

    # Ensure the placeholder has been replaced
    assert "{{executive_summary_output}}" not in prompt

    print("\n" + "=" * 80)
    print("PROMPT RENDERED SUCCESSFULLY")
    print("=" * 80)
    print(prompt)
    print("=" * 80)