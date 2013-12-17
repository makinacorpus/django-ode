#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "django_ode.settings.local")
    from django.core.management import execute_from_command_line
    try:
        execute_from_command_line(sys.argv)
    except ImportError:
        os.environ["DJANGO_SETTINGS_MODULE"] = "django_ode.settings.base"
        execute_from_command_line(sys.argv)

