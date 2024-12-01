from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
subscriptions = []  # Список подписок

# 1. Создание подписки
@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    data = request.get_json()
    subscription = {
        'id': len(subscriptions) + 1,
        'name': data['name'],
        'amount': data['amount'],
        'frequency': data['frequency'],
        'start_date': data['start_date'],
        'active': True
    }
    subscriptions.append(subscription)
    return jsonify({'message': 'Подписка создана', 'subscription': subscription}), 201

# 2. Просмотр подписок
@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    return jsonify({'subscriptions': [s for s in subscriptions if s['active']]}), 200

# 3. Редактирование подписки
@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    # ... (реализация обновления подписки по ID) ...
    pass

# 4. Удаление подписки
@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    # ... (реализация удаления подписки по ID) ...
    pass


if __name__ == '__main__':
    app.run(debug=True)
