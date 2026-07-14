from backend.prompts.prompt_loader import PromptLoader


class PromptManager:
    """Handles loading and rendering prompt templates."""

    def __init__(self, template_dir: str):
        self.loader = PromptLoader(template_dir)
        self._cache: dict[str, str] = {}

    def get_prompt(self, template_name: str) -> str:
        """Return a cached prompt template."""

        if template_name not in self._cache:
            self._cache[template_name] = self.loader.load(
                template_name
            )

        return self._cache[template_name]

    def render(
        self,
        template_name: str,
        variables: dict | None = None,
    ) -> str:
        """Render a prompt template."""

        prompt = self.get_prompt(template_name)

        if not variables:
            return prompt

        for key, value in variables.items():
            prompt = prompt.replace(
                f"{{{{{key}}}}}",
                str(value),
            )

        return prompt


# Singleton instance used across the application
prompt_manager = PromptManager(
    template_dir="backend/prompts/templates"
)