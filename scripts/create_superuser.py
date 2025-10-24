import os
import sys
import django

# Detect the project root (where manage.py is located)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))  # adjust if script deeper
sys.path.insert(0, PROJECT_ROOT)

# Update this to match your settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

try:
    django.setup()
except ModuleNotFoundError as e:
    print("❌ Could not find settings module. Check DJANGO_SETTINGS_MODULE path.")
    print("Current sys.path:", sys.path)
    raise e

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """
    Creates a default superuser if it does not already exist.
    """
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == "__main__":
    create_superuser()
