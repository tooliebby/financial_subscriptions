import os
from flask import Flask, request, jsonify
import psycopg2
import json

app = Flask(__name__)

# DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    try:
        # conn = psycopg2.connect(DATABASE_URL)
        conn = psycopg2.connect(dbname="grit_tych_rpp_finance_bd", user="grit_tych_rpp_finance", password="123", host="127.0.0.1")
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def format_db_results(db_results):
    return [{'id': row[0], 'name': row[1], 'amount': row[2], 'frequency': row[3], 'start_date': row[4], 'active': row[5]} for row in db_results]

@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500
    try:
        data = request.get_json()
        cur = conn.cursor()
        cur.execute("INSERT INTO subscriptions (name, amount, frequency, start_date, active) VALUES (%s, %s, %s, %s, TRUE) RETURNING id", (data['name'], data['amount'], data['frequency'], data['start_date']))
        conn.commit()
        new_subscription_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({'message': 'Subscription created', 'id': new_subscription_id}), 201
    except (psycopg2.Error, KeyError, json.JSONDecodeError) as e:
        print(f"Error creating subscription: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({'error': 'Error creating subscription'}), 500

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM subscriptions")
        subscriptions = cur.fetchall()
        cur.close()
        conn.close()
        formatted_subscriptions = format_db_results(subscriptions)
        return jsonify({'subscriptions': formatted_subscriptions})
    except psycopg2.Error as e:
        print(f"Error getting subscriptions: {e}")
        return jsonify({'error': 'Error getting subscriptions'}), 500

@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500
    try:
        data = request.get_json()
        cur = conn.cursor()
        cur.execute("UPDATE subscriptions SET name=%s, amount=%s, frequency=%s, start_date=%s WHERE id=%s", (data['name'], data['amount'], data['frequency'], data['start_date'], subscription_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Subscription updated'}), 200
    except (psycopg2.Error, KeyError) as e:
        print(f"Error updating subscription: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({'error': 'Error updating subscription'}), 500

@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500
    try:
        cur = conn.cursor()
        cur.execute("UPDATE subscriptions SET active = FALSE WHERE id=%s", (subscription_id,)) #мягкое удаление
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Subscription deleted'}), 200
    except psycopg2.Error as e:
        print(f"Error deleting subscription: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({'error': 'Error deleting subscription'}), 500

if __name__ == '__main__':
    app.run(debug=True)
