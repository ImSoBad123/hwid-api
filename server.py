from flask import Flask, request, jsonify

app = Flask(__name__)

# Giả lập database key & hwid
db = {
    "ABC123": {"hwid": None}
}

@app.route("/redeem", methods=["POST"])
def redeem():
    key = request.json.get("key")
    hwid = request.json.get("hwid")

    if key not in db:
        return jsonify({"success": False, "message": "Key không tồn tại"}), 400

    if db[key]["hwid"] is None:
        db[key]["hwid"] = hwid
        return jsonify({"success": True, "message": "Đã liên kết HWID thành công"})
    elif db[key]["hwid"] == hwid:
        return jsonify({"success": True, "message": "HWID đã khớp"})
    else:
        return jsonify({"success": False, "message": "HWID không khớp"}), 403

@app.route("/reset", methods=["POST"])
def reset():
    key = request.json.get("key")

    if key in db:
        db[key]["hwid"] = None
        return jsonify({"success": True, "message": "Đã reset HWID"})
    return jsonify({"success": False, "message": "Key không tồn tại"}), 400

app.run(host="0.0.0.0", port=10000)
