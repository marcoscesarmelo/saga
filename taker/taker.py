from flask import Flask, request, jsonify, abort
from repo import amount_repo
import json

app = Flask(__name__)

@app.route('/taker/amount/<id>', methods=['GET'])
def get_amount(id) -> float:
    all_amounts = amount_repo.get_amount(id)
    if len(all_amounts) > 0:
        return jsonify(all_amounts[0])
    else:
        abort(400, 'Impossible to get amount right now. Try It later')

@app.route('/taker/amount/<id>', methods=['PATCH'])
def take(id):
    if request.is_json:
        data = request.json
        amount_to_take = data.get('amount', 0)        
        try:
            amount_repo.take(id, amount_to_take)
            return '',200
        except Exception as e:
            abort(400, description='Something wrong! Try It later ...')

@app.route('/taker/update-amount/<id>', methods=['PATCH'])
def update_amount(id):
    if request.is_json:
        data = request.json
        amount_to_update = data.get('amount', 0)        
        try:
            amount_repo.update_amount(id, amount_to_update)
            return '',200
        except Exception as e:
            abort(400, description='Something wrong! Try It later ...')

if __name__ == '__main__':
    app.run(debug=True, port=5002)