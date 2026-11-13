from __future__ import annotations

from pathlib import Path

import requests


class JiraHelper:
    def __init__(self, config):
        self._config = config
        self.enabled = bool(getattr(config, "jira_api_token", ""))

    def _auth(self):
        return (self._config.jira_email, self._config.jira_api_token)

    def _headers(self):
        return {"Accept": "application/json", "Content-Type": "application/json"}

    def _ticket_exists(self, summary: str) -> bool:
        key = self._config.jira_project_key
        jql = f'project = "{key}" AND summary ~ "{summary}" AND statusCategory != Done'
        url = f"{self._config.jira_base_url}/rest/api/3/issue/search"
        try:
            resp = requests.get(
                url, params={"jql": jql, "maxResults": 1}, auth=self._auth(), timeout=10
            )
            if resp.status_code == 200:
                return len(resp.json().get("issues", [])) > 0
        except Exception:
            pass
        return False

    def create_bug(
        self, summary: str, description: str, screenshot_path: Path | None
    ) -> str | None:
        if not self.enabled:
            return None
        if self._ticket_exists(summary):
            return None

        payload = {
            "fields": {
                "project": {"key": self._config.jira_project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}],
                        }
                    ],
                },
                "issuetype": {"name": self._config.jira_issue_type},
            }
        }

        url = f"{self._config.jira_base_url}/rest/api/3/issue"
        try:
            resp = requests.post(
                url, json=payload, headers=self._headers(), auth=self._auth(), timeout=10
            )
            if resp.status_code != 201:
                return None
            key = resp.json().get("key")
            if key and screenshot_path and Path(screenshot_path).exists():
                self._attach_screenshot(key, screenshot_path)
            return key
        except Exception:
            return None

    def _attach_screenshot(self, issue_key: str, path: Path) -> None:
        url = f"{self._config.jira_base_url}/rest/api/3/issue/{issue_key}/attachments"
        headers = {"X-Atlassian-Token": "no-check"}
        try:
            with open(path, "rb") as f:
                requests.post(
                    url, files={"file": f}, headers=headers, auth=self._auth(), timeout=15
                )
        except Exception:
            pass
