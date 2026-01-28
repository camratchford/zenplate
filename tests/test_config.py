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
    assert config.get_by_prefix("jinja_env", trim_prefix=True) == {
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
    config.dump_to_file(config.config_file)

    sleep(1)
    config.load_from_file(config_path)
    non_matching = [
        k
        for k, v in config2._data.items()
        if k in config._data.keys()
        and k != "config_file"
        and config.get(k) != config2.get(k)
    ]

    if non_matching:
        raise AssertionError(f"Non-matching keys: {non_matching}")


def test_config_export_config():
    config = Config()
    default_config_file = fixtures / "configs" / "from_defaults.yml"
    config.dump_to_file(default_config_file)
    config.config_file = fixtures / "output" / "exported_config.yml"
    config.dump_to_file(config.config_file)

    assert default_config_file.read_text() == config.config_file.read_text()


if __name__ == "__main__":
    test_config_init()
    test_config_configure_from_path()
    test_config_export_config()
