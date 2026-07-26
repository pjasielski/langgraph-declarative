"""Create LangChain chat model instances from YAML ``llm:`` config sections.

Provider packages (langchain-openai, langchain-anthropic) are optional
dependencies — they are imported lazily and a clear install hint is raised
when missing.
"""

from __future__ import annotations

from langgraph_declarative.errors import ConfigValidationError, DeclarativeError
from langgraph_declarative.schema import LLMConfig


def _missing_provider_package(provider: str, package: str) -> DeclarativeError:
    return DeclarativeError(
        f"LLM provider '{provider}' requires the '{package}' package. "
        f"Install it with: pip install {package}  (or: uv add {package})"
    )


def _create_openai(config: LLMConfig):
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise _missing_provider_package("openai", "langchain-openai") from None
    return ChatOpenAI(**_model_kwargs(config))


def _create_anthropic(config: LLMConfig):
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError:
        raise _missing_provider_package("anthropic", "langchain-anthropic") from None
    return ChatAnthropic(**_model_kwargs(config))


def _model_kwargs(config: LLMConfig) -> dict:
    kwargs = {"model": config.model}
    if config.temperature is not None:
        kwargs["temperature"] = config.temperature
    if config.max_tokens is not None:
        kwargs["max_tokens"] = config.max_tokens
    return kwargs


# Provider name → factory. Tests may monkeypatch this to inject fakes.
_PROVIDERS = {
    "openai": _create_openai,
    "anthropic": _create_anthropic,
}


def merge_llm_config(
    base: LLMConfig | None, override: LLMConfig | None
) -> LLMConfig | None:
    """Merge a graph-level default with a per-node override (override wins)."""
    if base is None:
        return override
    if override is None:
        return base
    data = base.model_dump(exclude_none=True)
    data.update(override.model_dump(exclude_none=True))
    return LLMConfig(**data)


def create_llm(config: LLMConfig):
    """Instantiate a chat model from a (merged) LLM config.

    Raises ``ConfigValidationError`` for missing/unknown provider or missing
    model, and ``DeclarativeError`` when the provider package is not installed.
    """
    if config.provider is None:
        raise ConfigValidationError(
            "llm config is missing 'provider' — "
            f"supported providers: {', '.join(sorted(_PROVIDERS))}"
        )
    if config.model is None:
        raise ConfigValidationError("llm config is missing 'model'")
    factory = _PROVIDERS.get(config.provider)
    if factory is None:
        supported = ", ".join(f"'{p}'" for p in sorted(_PROVIDERS))
        raise ConfigValidationError(
            f"Unknown llm provider '{config.provider}'. Supported: {supported}."
        )
    return factory(config)
