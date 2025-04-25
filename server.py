from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Giả lập database key & hwid
db = {}

# Hàm tạo key ngẫu nhiên
def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Tạo 5 key khi server chạy lần đầu
def create_keys():
    for _ in range(5):
        key = generate_key()
        db[key] = {"hwid": None}

create_keys()

# Route để redeem key và liên kết HWID (chỉ một lần sử dụng với HWID đầu tiên)
@app.route("/redeem", methods=["POST"])
def redeem():
    key = request.json.get("key")
    hwid = request.json.get("hwid")

    if key not in db:
        return jsonify({"success": False, "message": "Key không tồn tại"}), 400

    # Kiểm tra xem key đã được redeem chưa
    if db[key]["hwid"] is None:
        # Lưu HWID đầu tiên vào key
        db[key]["hwid"] = hwid
        return jsonify({"success": True, "message": "Đã liên kết HWID thành công"})
    
    elif db[key]["hwid"] == hwid:
        return jsonify({"success": True, "message": "HWID đã khớp và đã liên kết thành công"})
    
    # Nếu HWID khác, không cho phép sử dụng lại key
    else:
        return jsonify({"success": False, "message": "HWID không khớp hoặc key đã được sử dụng"}), 403

# Route để reset key (xóa HWID)
@app.route("/reset", methods=["POST"])
def reset():
    key = request.json.get("key")

    if key in db:
        db[key]["hwid"] = None
        return jsonify({"success": True, "message": "Đã reset HWID"})
    return jsonify({"success": False, "message": "Key không tồn tại"}), 400

# Route để kiểm tra key và HWID
@app.route("/check", methods=["GET"])
def check():
    key = request.args.get("key")

    if key not in db:
        return jsonify({"success": False, "message": "Key không tồn tại"}), 400

    hwid = db[key]["hwid"]

    if hwid is None:
        return jsonify({"success": False, "message": "Key chưa được redeem"}), 400
    else:
        return jsonify({"success": True, "message": f"Key đã liên kết với HWID {hwid}"}), 200

# Route để tạo key mới (chỉ admin)
@app.route("/create_key", methods=["POST"])
def create_key():
    new_key = generate_key()
    db[new_key] = {"hwid": None}
    return jsonify({"success": True, "message": f"Key {new_key} đã được tạo thành công"}), 200

app.run(host="0.0.0.0", port=10000)
