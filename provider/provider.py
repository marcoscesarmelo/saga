from flask import Flask, request, jsonify, abort
from dal import amount_repo
import json

app = Flask(__name__)

@app.route('/provider/amount/<id>', methods=['GET'])
def get_amount(id) -> float:
    all_amounts = amount_repo.get_amount(id)
    if len(all_amounts) > 0:
        return jsonify(all_amounts[0])
    else:
        abort(400, 'Impossible to get amount right now. Try It later')

@app.route('/provider/amount/<id>', methods=['PATCH'])
def provide(id):
    if request.is_json:
        data = request.json
        amount_to_provide = data.get('amount', 0)        
        try:
            amount_repo.provide(id, amount_to_provide)
            return '',200
        except Exception as e:
            abort(400, description='Something wrong! Try It later ...')

@app.route('/provider/update-amount/<id>', methods=['PATCH'])
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
    app.run(debug=True, port=5001)