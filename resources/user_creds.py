import os

from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    USERNAME = os.environ["ADMIN_EMAIL"]
    PASSWORD = os.environ["ADMIN_PASSWORD"]