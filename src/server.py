from flask import Flask, request

app = Flask(__name__)

ADMIN_PASSWORD = "ababacaabbcbcababacaabbcbc"


@app.route("/admin/login", methods=["POST"])
def vulnerable_route():
    if not request.is_json:
        return "Bad Request", 400
    if request.get_json()["password"] == ADMIN_PASSWORD:
        return "Success", 200
    else:
        return "Wrong password!", 401


if __name__ == "__main__":
    app.run()
