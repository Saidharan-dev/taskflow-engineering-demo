
import os


def get_api_key() -> str:
    api_key = os.getenv("TASKFLOW_API_KEY")

    if not api_key:
        raise RuntimeError(
            "TASKFLOW_API_KEY environment variable is not configured"
        )

    return api_key
