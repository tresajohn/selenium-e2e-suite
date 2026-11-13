from config.config import get_config


def test_config_loads_base_url():
    cfg = get_config()
    assert cfg.base_url == "https://automationexercise.com"


def test_config_headless_overridden_by_env(monkeypatch):
    monkeypatch.setenv("HEADLESS", "true")
    cfg = get_config()
    assert cfg.headless is True


def test_config_timeout_is_int():
    cfg = get_config()
    assert isinstance(cfg.timeout, int)
