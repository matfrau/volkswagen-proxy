from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/send-lead", methods=["POST"])
def send_lead():
    token = request.args.get("token")
    if token != os.getenv("ACCESS_TOKEN"):
        return jsonify({"error": "Unauthorized"}), 403

    payload = request.get_json()
    try:
        response = requests.post(
            "https://api.non-prod.volkswagengroup.fr/tools/qa/leads/v2/leads",
            json=payload,
            headers={"Content-Type": "application/json"},
            auth=(os.getenv("VW_USERNAME"), os.getenv("VW_PASSWORD")),
            cert=("SEAT-leads.crt", "SEAT-leads-private.pem"),
        )
        return jsonify({
            "status_code": response.status_code,
            "response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
