from time import sleep

from zenplate.config import Config

from config_fixtures import fixtures


def test_config_init():
    config = Config()

    assert config.config_file is None
    assert config.tree_directory is None
    assert config.var_files == []
    assert config.variables == []
    assert config.log_path is None
    assert config.template_path is None
    assert config.tree_directory is None
    assert config.output_path is None
    assert config.jinja_config == {
        "trim_blocks": False,
        "lstrip_blocks": False,
        "keep_trailing_newline": False,
    }
    assert config.jinja_global_vars == {}
    assert not config.dry_run
    assert config.log_level == "ERROR"
    assert not config.stdout
    assert not config.force_overwrite
    assert config.plugin_config == {
        "path_modules": [],
        "named_modules": [
            "zenplate.plugins.default_plugins.data_plugins",
            "zenplate.plugins.default_plugins.jinja_plugins",
        ],
        "plugin_kwargs": {
            "ls": {
                "path": ".",
            }
        },
    }


def test_config_configure_from_path():
    config = Config()
    config2 = Config()

    config_path = fixtures.parent.joinpath("output", "exported_config.yml")
    config.config_file = config_path
    config.export_config()

    sleep(1)
    config.configure_from_path(config_path)
    non_matching = [
        k
        for k, v in config2.__dict__.items()
        if k in config.__dict__.keys()
        and k != "config_file"
        and config.__dict__[k] != config2.__dict__[k]
    ]

    if non_matching:
        raise AssertionError(f"Non-matching keys: {non_matching}")


def test_config_export_config():
    config = Config()
    default_config_file = fixtures / "configs" / "from_defaults.yml"
    config.configure_from_path(default_config_file)
    config.config_file = fixtures / "output" / "exported_config.yml"

    config.export_config()

    assert default_config_file.read_text() == config.config_file.read_text()


if __name__ == "__main__":
    test_config_init()
    test_config_configure_from_path()
    test_config_export_config()
