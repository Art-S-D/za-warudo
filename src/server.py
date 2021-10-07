from flask import Flask, request

app = Flask(__name__)

ADMIN_PASSWORD = "ababacaabbcbcababacaabbcbc"


def string_compare(s1, s2):
    if len(s1) != len(s2):
        return False
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True


@app.route("/admin/login", methods=["POST"])
def vulnerable_route():
    if not request.is_json:
        return "Bad Request", 400
    if string_compare(request.get_json()["password"], ADMIN_PASSWORD):
        return "Success", 200
    else:
        return "Wrong password!", 401


if __name__ == "__main__":
    app.run()
