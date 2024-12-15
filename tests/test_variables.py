import os

from zenplate.template_data import TemplateData

from config_fixtures import new_config, fixtures


def test_template_vars_initializes_with_config():
    config = new_config()
    config.jinja_global_vars = {"global_var": "value"}
    template_vars = TemplateData(config)
    assert template_vars.vars["global_var"] == "value"


def test_template_vars_loads_plugins():
    config = new_config()
    template_vars = TemplateData(config)
    template_vars.load_plugins()

    assert "defaults" in template_vars.vars.keys()
    assert template_vars.vars.get("defaults").get("os").get("name") == os.name


def test_template_vars_loads_file():
    config = new_config()
    template_vars = TemplateData(config)
    var_file = [fixtures / "vars" / "vars.yaml"]
    template_vars.load_files(var_file)
    assert template_vars.vars.get("test") == "a"
    assert template_vars.vars.get("test2") == "b"


def test_template_vars_loads_variables():
    config = new_config()
    template_vars = TemplateData(config)
    variables = ["key1=value1", "key2=value2"]
    template_vars.load(variables)


def test_template_vars_handles_invalid_variable_format():
    config = new_config()
    template_vars = TemplateData(config)
    variables = ["invalid_variable"]
    template_vars.load(variables)
    assert "invalid_variable" not in template_vars.vars.keys()


if __name__ == "__main__":
    test_template_vars_initializes_with_config()
    test_template_vars_loads_plugins()
    test_template_vars_loads_file()
    test_template_vars_loads_variables()
    test_template_vars_handles_invalid_variable_format()
