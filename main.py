#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import ManagementUtility
from django.core.management.commands.runserver import Command as runserver; 
from django.core.management.commands.makemigrations import Command as makemigrations;
from django.core.management.commands.migrate import Command as migrate;

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWebApp.settings')
    runserver.default_addr = '0.0.0.0'
    runserver.default_port = os.getenv('PORT', 3000)
    ManagementUtility(['main.py', 'makemigrations']).execute()
    ManagementUtility(['main.py', 'makemigrations', 'SezioneSpaccio']).execute()
    ManagementUtility(['main.py', 'makemigrations', 'users']).execute()
    ManagementUtility(['main.py', 'migrate']).execute()
    main()
    
