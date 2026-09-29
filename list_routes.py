import sys
sys.path.insert(0, r"C:\Users\HP\Documents\My_Agents\notes-api")
from main import app
for route in app.routes:
    print(route.path, getattr(route, 'methods', ''))
