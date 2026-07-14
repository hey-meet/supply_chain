from pathlib import Path


class PromptLoader:
    """Loads prompt templates from the templates directory."""

    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)

    def load(self, template_name: str) -> str:
        """Load a prompt template from disk."""

        template_path = self.template_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: {template_path}"
            )

        return template_path.read_text(
            encoding="utf-8"
        )