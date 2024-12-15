from io import StringIO
import sys

from zenplate.output_handler import OutputHandler
from config_fixtures import new_config, fixtures


def test_output_handler_write_file():
    config = new_config()
    config.output_path = fixtures / "output"
    config.force_overwrite = True
    output_handler = OutputHandler(config)
    template_dict = {
        "test_file": {
            "path": fixtures / "output" / "test_file.txt",
            "content": "test content",
        }
    }
    output_handler.write_file(template_dict)
    assert (fixtures / "output" / "test_file.txt").exists()


def test_output_handler_write_tree():
    config = new_config()
    config.output_path = fixtures / "output"
    config.force_overwrite = True
    output_handler = OutputHandler(config)
    template_dict = {
        "test_file": {
            "path": fixtures / "output" / "tree" / "test_tree1.txt",
            "content": "test content",
        },
        "test_file2": {
            "path": fixtures / "output" / "tree" / "test_tree2.txt",
            "content": "test content",
        },
    }
    output_handler.write_tree(template_dict)

    assert all(template_dict[k]["path"].exists() for k, v in template_dict.items())
    assert all(
        template_dict[k]["path"].read_text() == template_dict[k]["content"]
        for k, v in template_dict.items()
    )


def test_output_handler_write_stdout(monkeypatch):
    config = new_config()
    config.output_path = fixtures / "output" / "test_file.txt"
    config.force_overwrite = True
    output_handler = OutputHandler(config)
    mock_stdout = StringIO()

    monkeypatch.setattr(sys, "stdout", mock_stdout)
    output_handler.write_stdout(config.output_path)

    assert config.output_path.read_text() == "test content"
    assert mock_stdout.getvalue() == "test content\n"


if __name__ == "__main__":
    test_output_handler_write_file()
    test_output_handler_write_tree()
    test_output_handler_write_stdout()
