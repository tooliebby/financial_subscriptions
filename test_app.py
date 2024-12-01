import pytest
from app import create_subscription, get_subscriptions, update_subscription, delete_subscription
import psycopg2
import json
import os
import requests


# Fixture для подключения к базе данных. Замените на свои данные!
@pytest.fixture
def db_connection():
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL")) 
        conn.autocommit = True # Автоматическое подтверждение изменений в тестовой базе данных
        yield conn
        conn.close()
    except psycopg2.Error as e:
        print(f"Ошибка подключения к тестовой базе данных: {e}")
        pytest.fail(f"Ошибка подключения к тестовой базе данных: {e}")

def test_create_subscription(db_connection):
    cur = db_connection.cursor()
    data = {'name': 'Test Subscription', 'amount': 10.00, 'frequency': 'monthly', 'start_date': '2024-03-15'}
    response = create_subscription(data)
    assert response.status_code == 201
    assert response.json['message'] == 'Подписка создана'
    cur.execute("SELECT * FROM subscriptions WHERE name = %s", ('Test Subscription',))
    result = cur.fetchone()
    assert result is not None
    cur.close()


def test_get_subscriptions(db_connection):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO subscriptions (name, amount, frequency, start_date) VALUES (%s, %s, %s, %s)", ('Test Sub 1', 20.00, 'yearly', '2024-01-01'))
    db_connection.commit()
    response = get_subscriptions()
    assert response.status_code == 200
    assert len(response.json['subscriptions']) >= 1 # Проверяем, что хотя бы одна подписка есть
    cur.close()


def test_update_subscription(db_connection):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO subscriptions (name, amount, frequency, start_date) VALUES (%s, %s, %s, %s) RETURNING id", ('Test Sub 2', 30.00, 'monthly', '2024-02-15'))
    subscription_id = cur.fetchone()[0]
    db_connection.commit()
    data = {'name': 'Updated Subscription', 'amount': 40.00, 'frequency': 'yearly', 'start_date': '2025-01-01'}
    response = update_subscription(subscription_id)
    assert response.status_code == 200
    cur.execute("SELECT * FROM subscriptions WHERE id = %s", (subscription_id,))
    result = cur.fetchone()
    assert result[1] == 'Updated Subscription' #Проверяем имя
    assert result[2] == 40.00 #Проверяем сумму
    cur.close()


def test_delete_subscription(db_connection):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO subscriptions (name, amount, frequency, start_date) VALUES (%s, %s, %s, %s) RETURNING id", ('Test Sub 3', 50.00, 'monthly', '2024-03-15'))
    subscription_id = cur.fetchone()[0]
    db_connection.commit()
    response = delete_subscription(subscription_id)
    assert response.status_code == 200
    cur.execute("SELECT * FROM subscriptions WHERE id = %s", (subscription_id,))
    result = cur.fetchone()
    assert result is None #Подписка удалена
    cur.close()
