import logging
import logging.config


def setup_logging(log_level: str = "ERROR", log_path: str = None):
    handlers = ["console"]
    if log_path is not None:
        handlers.append("file")

    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "%(process)d:%(filename)s:%(module)s.%(funcName)s:%(lineno)d:%(message)s",
            },
            "rich": {
                "format": "(%(name)s)[/] %(message)s",
            },
        },
        "handlers": {
            "console": {"()": "rich.logging.RichHandler", "formatter": "rich"},
        },
        "loggers": {
            "zenplate": {"handlers": handlers, "level": log_level, "propagate": True},
        },
    }
    if "file" in handlers:
        log_config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": log_path,
            "mode": "w",
        }

    logging.config.dictConfig(log_config)
