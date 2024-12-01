import os
from flask import Flask, request, jsonify
import psycopg2
import json

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def format_db_results(db_results):
    return [{'id': row[0], 'name': row[1], 'amount': row[2], 'frequency': row[3], 'start_date': row[4], 'active': row[5]} for row in db_results]

@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
    try:
        data = request.get_json()
        cur = conn.cursor()
        cur.execute("INSERT INTO subscriptions (name, amount, frequency, start_date) VALUES (%s, %s, %s, %s) RETURNING id", (data['name'], data['amount'], data['frequency'], data['start_date']))
        conn.commit()
        new_subscription_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({'message': 'Подписка создана', 'id': new_subscription_id}), 201
    except (psycopg2.Error, KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка создания подписки: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({'error': 'Ошибка создания подписки'}), 500

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM subscriptions")
        subscriptions = cur.fetchall()
        cur.close()
        conn.close()
        formatted_subscriptions = format_db_results(subscriptions)
        return jsonify({'subscriptions': formatted_subscriptions})
    except psycopg2.Error as e:
        print(f"Ошибка получения подписок: {e}")
        return jsonify({'error': 'Ошибка получения подписок'}), 500

@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
    try:
        data = request.get_json()
        cur = conn.cursor()
        cur.execute("UPDATE subscriptions SET name=%s, amount=%s, frequency=%s, start_date=%s WHERE id=%s", (data['name'], data['amount'], data['frequency'], data['start_date'], subscription_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Подписка обновлена'}), 200
    except (psycopg2.Error, KeyError) as e:
        print(f"Ошибка обновления подписки: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({'error': 'Ошибка обновления подписки'}), 500

@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM subscriptions WHERE id=%s", (subscription_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Подписка удалена'}), 200
    except psycopg2.Error as e:
        print(f"Ошибка удаления подписки: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({'error': 'Ошибка удаления подписки'}), 500

if __name__ == '__main__':
    app.run(debug=True)
