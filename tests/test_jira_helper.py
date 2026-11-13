from unittest.mock import MagicMock, patch

from config.config import get_config
from utils.jira_helper import JiraHelper


def test_disabled_when_no_token():
    cfg = get_config()
    cfg.jira_api_token = ""
    result = JiraHelper(cfg).create_bug("Summary", "Desc", None)
    assert result is None


@patch("utils.jira_helper.requests.get")
@patch("utils.jira_helper.requests.post")
def test_creates_ticket_when_no_duplicate(mock_post, mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"issues": []})
    mock_post.return_value = MagicMock(status_code=201, json=lambda: {"key": "AE-1"})
    cfg = get_config()
    cfg.jira_api_token = "fake-token"
    cfg.jira_email = "test@example.com"
    result = JiraHelper(cfg).create_bug("Test summary", "Test desc", None)
    assert result == "AE-1"


@patch("utils.jira_helper.requests.get")
def test_skips_duplicate_ticket(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"issues": [{"key": "AE-5"}]},
    )
    cfg = get_config()
    cfg.jira_api_token = "fake-token"
    cfg.jira_email = "test@example.com"
    result = JiraHelper(cfg).create_bug("Test summary", "Test desc", None)
    assert result is None
