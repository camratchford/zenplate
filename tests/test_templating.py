from jinja2.exceptions import TemplateNotFound


from zenplate.template_manager import TemplateManager
from config_fixtures import new_config, fixtures


def template_manager_loads_template():
    config = new_config()
    config.template_path = fixtures / "templates" / "template.html"
    template_manager = TemplateManager(config)
    assert template_manager.render_template() is not None


def template_manager_raises_error_for_missing_template():
    config = new_config()
    config.template_path = fixtures / "templates" / "non_existent_template.html"
    template_manager = TemplateManager(config)
    try:
        template_manager.render_template()
        assert False, "Expected an exception for missing template"
    except FileNotFoundError:
        pass
    except TemplateNotFound:
        pass


def template_manager_handles_empty_template():
    config = new_config()
    config.template_path = fixtures / "templates" / "empty_template.html"
    template_manager = TemplateManager(config)
    template = template_manager.render_template().get("content")
    assert template is None, f"Expected empty template content, got {template}"


if __name__ == "__main__":
    template_manager_loads_template()
    template_manager_raises_error_for_missing_template()
    template_manager_handles_empty_template()
