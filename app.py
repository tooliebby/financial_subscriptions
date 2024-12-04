from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        dbname="grit_tych_rpp_finance_bd",
        user="grit_tych_rpp_finance",
        password="123",
        host="localhost"
    )


@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscriptions (name, amount, frequency, start_date)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (data['name'], data['amount'], data['frequency'], data['start_date']))
        subscription_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Subscription created successfully!", "id": subscription_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM subscriptions;")
        subscriptions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(subscriptions)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE subscriptions
            SET amount = COALESCE(%s, amount),
                frequency = COALESCE(%s, frequency),
                start_date = COALESCE(%s, start_date)
            WHERE id = %s;
        """, (data.get('amount'), data.get('frequency'), data.get('start_date'), subscription_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Subscription updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE id = %s;", (subscription_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Subscription deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
