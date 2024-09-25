import hashlib
import hmac
import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'CB374EA7A8262D6FABB895411511D')

def verify_webhook_auth(data, received_signature):
    """ Verifies that the webhook is from LearnUpon by checking the signature. """
    calculated_signature = hmac.new(
        key=WEBHOOK_SECRET.encode('utf-8'),
        msg=data,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(calculated_signature, received_signature)

@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    payload = request.get_data()
    received_signature = request.headers.get('X-Webhook-Signature')

    if not received_signature:
        abort(400, "Missing 'X-Webhook-Signature' header")

    if not verify_webhook_auth(payload, received_signature):
        abort(403, "Unauthorized webhook")

    webhook_data = request.json

    print(f"Received webhook: {webhook_data}")

    # Respond with a success message
    return jsonify({'status': 'success', 'message': 'Webhook received and verified'})

if __name__ == '__main__':
    app.run(port=5000)