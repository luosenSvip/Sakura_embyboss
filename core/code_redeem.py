import json
import os

REDEEM_FILE = "data/redeem_codes.json"

def load_redeem_codes():
    if not os.path.exists(REDEEM_FILE):
        return {}
    with open(REDEEM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_redeem_codes(data):
    with open(REDEEM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def redeem_code(code, user_id):
    code = code.strip().upper()
    data = load_redeem_codes()
    if code not in data:
        return False, "无效的兑换码！"
    if data[code].get("used"):
        return False, "该兑换码已被使用！"

    points = data[code]["points"]
    data[code]["used"] = True
    data[code]["used_by"] = user_id
    save_redeem_codes(data)
    return True, points

def import_redeem_codes(file_path):
    data = load_redeem_codes()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if ':' in line:
                code, points = line.strip().split(':', 1)
                code = code.strip().upper()
                points = int(points.strip())
                if code not in data:
                    data[code] = {"points": points, "used": False}
    save_redeem_codes(data)
    return len(data)
