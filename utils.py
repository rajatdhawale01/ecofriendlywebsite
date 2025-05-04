import json

db_file = "db.json"

def load_db():
    try:
        with open(db_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"cart": {}, "users": [], "orders": []}
    return data

def save_db(data):
    with open(db_file, "w") as f:
        json.dump(data, f, indent=4)
