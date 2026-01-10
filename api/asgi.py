import sys
import os

# Path to your project
project_home = "/home/xceed/ai_ba_agent"

if project_home not in sys.path:
    sys.path.append(project_home)

from api.main import app
