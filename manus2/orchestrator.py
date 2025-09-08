import asyncio
from typing import Any

from manus2.adapters.telegram_bot import send_message
from manus2.adapters.ollama_client import generate
from manus2.adapters.github_actions import trigger_workflow
from manus2.adapters.n8n_client import call_flow
from manus2.config import settings
from manus2.utils.logger import get_logger

log = get_logger("orchestrator", settings.log_level)


async def run_example() -> dict[str, Any]:
    results: dict[str, Any] = {}

    results["telegram"] = await send_message("הודעת בדיקה")
    results["ollama"] = await generate("Hello")
    results["github"] = await trigger_workflow("build.yml", ref="main")
    results["n8n"] = await call_flow("webhook", {"ping": "pong"})

    log.info("Orchestration results: %s", results)
    return results


if __name__ == "__main__":
    asyncio.run(run_example())
