# main.py
from database import setup_database
from game import start_ui  # Pygame login/register UI

# 1️⃣ Make sure database exists
setup_database()

# 2️⃣ Launch the full Pygame UI
start_ui()
