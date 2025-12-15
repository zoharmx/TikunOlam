"""
Robust logging system for Tikun Olam

Provides structured logging with context, performance tracking,
and production-ready log formatting.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict
from pythonjsonlogger import jsonlogger


# Custom log format for console
CONSOLE_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

# Custom log format for file
FILE_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
)


class TikunLogger:
    """
    Enhanced logger for Tikun Olam with context management.
    """

    def __init__(self, name: str, logger: logging.Logger):
        self.name = name
        self._logger = logger
        self._context: Dict[str, Any] = {}

    def set_context(self, **kwargs: Any) -> None:
        """Add context data that will be included in all log messages."""
        self._context.update(kwargs)

    def clear_context(self) -> None:
        """Clear all context data."""
        self._context.clear()

    def _format_message(self, msg: str) -> str:
        """Format message with context if available."""
        if not self._context:
            return msg

        context_str = " | ".join(f"{k}={v}" for k, v in self._context.items())
        return f"{msg} | {context_str}"

    def debug(self, msg: str, **kwargs: Any) -> None:
        """Log debug message."""
        self._logger.debug(self._format_message(msg), extra=kwargs)

    def info(self, msg: str, **kwargs: Any) -> None:
        """Log info message."""
        self._logger.info(self._format_message(msg), extra=kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        """Log warning message."""
        self._logger.warning(self._format_message(msg), extra=kwargs)

    def error(self, msg: str, exc_info: bool = False, **kwargs: Any) -> None:
        """Log error message."""
        self._logger.error(self._format_message(msg), exc_info=exc_info, extra=kwargs)

    def critical(self, msg: str, exc_info: bool = False, **kwargs: Any) -> None:
        """Log critical message."""
        self._logger.critical(self._format_message(msg), exc_info=exc_info, extra=kwargs)

    def exception(self, msg: str, **kwargs: Any) -> None:
        """Log exception with traceback."""
        self._logger.exception(self._format_message(msg), extra=kwargs)


# Global logger registry
_loggers: Dict[str, TikunLogger] = {}


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    json_format: bool = False,
    enable_console: bool = True
) -> None:
    """
    Configure logging for Tikun Olam.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        json_format: If True, use JSON formatting (for production)
        enable_console: If True, enable console logging
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        if json_format:
            console_formatter = jsonlogger.JsonFormatter(
                '%(asctime)s %(name)s %(levelname)s %(message)s'
            )
        else:
            console_formatter = logging.Formatter(
                CONSOLE_FORMAT,
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level.upper()))

        if json_format:
            file_formatter = jsonlogger.JsonFormatter(
                '%(asctime)s %(name)s %(levelname)s %(filename)s '
                '%(lineno)d %(funcName)s %(message)s'
            )
        else:
            file_formatter = logging.Formatter(
                FILE_FORMAT,
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Log startup
    logger = get_logger("tikun.logging")
    logger.info(
        f"Logging initialized",
        level=level,
        json_format=json_format,
        log_file=str(log_file) if log_file else None
    )


def get_logger(name: str) -> TikunLogger:
    """
    Get or create a logger for the specified module.

    Args:
        name: Logger name (typically __name__ from calling module)

    Returns:
        TikunLogger instance
    """
    if name not in _loggers:
        base_logger = logging.getLogger(name)
        _loggers[name] = TikunLogger(name, base_logger)

    return _loggers[name]


class LogContext:
    """
    Context manager for temporary log context.

    Example:
        logger = get_logger(__name__)
        with LogContext(logger, sefirah="keter", case="test_001"):
            logger.info("Processing")  # Will include context
    """

    def __init__(self, logger: TikunLogger, **context: Any):
        self.logger = logger
        self.context = context
        self.previous_context: Dict[str, Any] = {}

    def __enter__(self) -> TikunLogger:
        """Save previous context and set new context."""
        self.previous_context = self.logger._context.copy()
        self.logger.set_context(**self.context)
        return self.logger

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Restore previous context."""
        self.logger._context = self.previous_context


class PerformanceLogger:
    """
    Context manager for logging execution time.

    Example:
        logger = get_logger(__name__)
        with PerformanceLogger(logger, "keter_processing"):
            # Code to measure
            process_keter()
    """

    def __init__(
        self,
        logger: TikunLogger,
        operation: str,
        level: str = "INFO"
    ):
        self.logger = logger
        self.operation = operation
        self.level = level.upper()
        self.start_time: Optional[datetime] = None

    def __enter__(self) -> "PerformanceLogger":
        """Start timing."""
        self.start_time = datetime.now()
        self.logger.debug(f"Starting {self.operation}")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Log execution time."""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()

            log_method = getattr(self.logger, self.level.lower())

            if exc_type:
                log_method(
                    f"{self.operation} failed after {elapsed:.2f}s",
                    error_type=exc_type.__name__ if exc_type else None
                )
            else:
                log_method(
                    f"{self.operation} completed in {elapsed:.2f}s",
                    duration_seconds=elapsed
                )
