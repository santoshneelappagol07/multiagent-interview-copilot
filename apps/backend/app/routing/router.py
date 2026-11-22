from app.routing.strategy import AnswerMode, RoutingStrategy
from app.llm.factory import llm_factory
from app.llm.base import BaseLLMProvider
from typing import Tuple
import logging

logger = logging.getLogger("ai_voice_copilot.routing")

class ModelRouter:
    def __init__(self):
        self.strategy = RoutingStrategy()

    def select_provider_and_model(self, mode: AnswerMode) -> Tuple[BaseLLMProvider, str, str]:
        """
        Returns (provider_instance, provider_name, model_name)
        Automatically evaluates availability and executes seamless fallback if the primary provider is unconfigured or rate-limited.
        """
        chain = self.strategy.get_chain(mode)

        for provider_name, model in chain:
            try:
                provider = llm_factory.get_provider(provider_name)
                if provider.is_available():
                    logger.info(f"Routing query in [{mode}] mode to provider: {provider_name} ({model})")
                    return provider, provider_name, model
            except Exception as e:
                logger.warning(f"Provider {provider_name} check failed: {e}")

        # Fallback to local Ollama if all cloud keys are exhausted
        logger.warning(f"All primary providers unavailable for mode [{mode}], falling back to local Ollama")
        return llm_factory.get_provider("ollama"), "ollama", "llama3.1"

model_router = ModelRouter()
