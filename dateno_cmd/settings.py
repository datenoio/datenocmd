from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Dict

import yaml
from pydantic import Field
from dateno_cmd.utils.errors import UserInputError
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_CONFIGFILE = ".dateno_cmd.yaml"


class Settings(BaseSettings):
    """
    Centralized configuration for the Dateno CLI.

    Priority order:
      1) CLI flags (later, in Typer command handlers)
      2) Environment variables (recommended for CI/CD)
      3) .env file (developer convenience; MUST NOT contain API keys)
      4) Legacy YAML config (~/..dateno_cmd.yaml or ./.dateno_cmd.yaml) for user API key
      5) Defaults
    """

    # API key must NOT be loaded from .env; user provides it via ENV or YAML.
    apikey: Optional[str] = Field(default=None, alias="DATENO_APIKEY")

    # Non-secret defaults can come from .env
    server_url: str = Field(default="https://api.dateno.io", alias="DATENO_SERVER_URL")
    timeout_ms: int = Field(default=30_000, alias="DATENO_TIMEOUT_MS")
    retries: int = Field(default=2, alias="DATENO_RETRIES")

    output_format: str = Field(default="yaml", alias="DATENO_OUTPUT_FORMAT")  # yaml|json
    debug: bool = Field(default=False, alias="DATENO_DEBUG")

    # Optional explicit YAML config path override (legacy support)
    config_yaml: Optional[str] = Field(default=None, alias="DATENO_CONFIG_YAML")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def load_user_yaml_if_needed(self) -> "Settings":
        """
        Load user configuration from YAML if fields are not provided via env/.env.

        Supported locations:
          - DATENO_CONFIG_YAML (explicit path)
          - ./.dateno_cmd.yaml (current working directory)
          - ~/..dateno_cmd.yaml (user home)
        """
        cfg = self._read_yaml_config()
        if isinstance(cfg, dict):
            fields_set = getattr(self, "__pydantic_fields_set__", set())

            def _set_if_missing(field: str, value: Any) -> None:
                if field in fields_set or value is None:
                    return
                if field == "timeout_ms" or field == "retries":
                    try:
                        setattr(self, field, int(value))
                    except (TypeError, ValueError):
                        return
                elif field == "debug":
                    if isinstance(value, bool):
                        setattr(self, field, value)
                    elif isinstance(value, (int, float)):
                        setattr(self, field, bool(value))
                    elif isinstance(value, str):
                        setattr(self, field, value.strip().lower() in {"1", "true", "yes", "y", "on"})
                else:
                    setattr(self, field, str(value))

            _set_if_missing("apikey", cfg.get("apikey"))
            _set_if_missing("server_url", cfg.get("server_url"))
            _set_if_missing("timeout_ms", cfg.get("timeout_ms"))
            _set_if_missing("retries", cfg.get("retries"))
            _set_if_missing("output_format", cfg.get("output_format"))
            _set_if_missing("debug", cfg.get("debug"))

        return self

    def require_apikey(self) -> "Settings":
        """
        Ensure an API key is available for API calls.
        """
        if not self.apikey:
            raise UserInputError(
                "API key is missing. Provide it via environment variable DATENO_APIKEY "
                "or in ~/..dateno_cmd.yaml as 'apikey: ...'."
            )
        return self

    def _read_yaml_config(self) -> Optional[Dict[str, Any]]:
        """
        Read YAML config from one of supported locations.
        """
        candidates: list[Path] = []

        if self.config_yaml:
            candidates.append(Path(self.config_yaml))

        candidates.append(Path.cwd() / DEFAULT_CONFIGFILE)
        candidates.append(Path.home() / DEFAULT_CONFIGFILE)

        for p in candidates:
            try:
                if p.exists() and p.is_file():
                    with p.open("r", encoding="utf-8") as f:
                        return yaml.safe_load(f)
            except Exception:
                # Ignore broken configs at this stage; the caller can enforce require_apikey()
                continue

        return None


def get_settings() -> Settings:
    """
    Build Settings instance and apply YAML fallback for user-level API key.
    """
    s = Settings()
    return s.load_user_yaml_if_needed()
