import os
import logging
import colorlog
import django
from django.core.management import call_command
import sys

# Configure logger with colors
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
))

logger = logging.getLogger("tests")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    try:
        # Set DJANGO_SETTINGS_MODULE to your project's settings
        os.environ["DJANGO_SETTINGS_MODULE"] = "crm_project.settings"  # Update with your project name

        # Set up Django
        django.setup()

        # Run tests for the whole application
        logger.info("🔍 Running tests for the entire application...")
        call_command("test")  # Runs tests for all installed apps

        logger.info("🎉 All tests passed! Ready to push to GitHub.")
    except Exception as e:
        logger.error("❌ Some tests failed. Check the logs above for details.")
        logger.exception(e)
        sys.exit(1)
