import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Config:
    base_url: str
    browser: str
    headless: bool
    timeout: int
    jira_base_url: str
    jira_email: str
    jira_api_token: str
    jira_project_key: str
    jira_issue_type: str
    test_email: str
    test_password: str


def get_config() -> Config:
    load_dotenv()
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        data = json.load(f)

    headless_env = os.getenv("HEADLESS", "").lower()
    headless = headless_env == "true" if headless_env else data.get("headless", False)

    return Config(
        base_url=data["base_url"],
        browser=os.getenv("BROWSER", data.get("browser", "chrome")),
        headless=headless,
        timeout=int(data.get("timeout", 10)),
        jira_base_url=os.getenv("JIRA_BASE_URL", data["jira"]["base_url"]),
        jira_email=os.getenv("JIRA_EMAIL", ""),
        jira_api_token=os.getenv("JIRA_API_TOKEN", ""),
        jira_project_key=os.getenv("JIRA_PROJECT_KEY", data["jira"]["project_key"]),
        jira_issue_type=data["jira"]["issue_type"],
        test_email=os.getenv("TEST_EMAIL", ""),
        test_password=os.getenv("TEST_PASSWORD", ""),
    )
