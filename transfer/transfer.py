from flask import Flask, request, jsonify, abort
from services import transfer_service
from dal import amount_repo

app = Flask(__name__)


@app.route('/transfer/amount/<id>', methods=['GET'])
def get_amount(id):
    try:
        response  = transfer_service.get_amount(id)
        return jsonify(response)
    except Exception as e:
        return str(e), 500


@app.route('/transfer/amount', methods=['POST'])
def transfer():
    try:
        if request.is_json:
            data = request.json
            person_to_take = data.get('from', 0)
            person_to_provide = data.get('to', 0)
            amount_to_transfer = data.get('amount', 0)
            transfer_service.transfer(person_to_take, person_to_provide, amount_to_transfer)
    except Exception as e:
        return str(e), 500

    return '', 200


if __name__ == '__main__':
    app.run(port=5000)
