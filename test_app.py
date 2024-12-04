import unittest
import json
from app import app, get_db_connection


class TestSubscriptionAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем тестовую базу данных или используем mock."""
        # Подключаемся к базе данных для работы с тестовой базой
        cls.conn = get_db_connection()
        cls.cursor = cls.conn.cursor()

        # Создаем таблицу для тестов (если она еще не существует)
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                amount FLOAT NOT NULL,
                frequency VARCHAR(50) NOT NULL,
                start_date DATE NOT NULL
            );
        """)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Закрываем соединение с базой данных после всех тестов."""
        cls.cursor.execute("DROP TABLE IF EXISTS subscriptions;")
        cls.conn.commit()
        cls.conn.close()

    def setUp(self):
        """Подготовка для каждого теста."""
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """Очистка данных после каждого теста."""
        self.cursor.execute("DELETE FROM subscriptions;")
        self.conn.commit()

    def test_create_subscription(self):
        """Тестируем создание подписки"""
        data = {
            "name": "Netflix",
            "amount": 12.99,
            "frequency": "monthly",
            "start_date": "2024-01-01"
        }
        response = self.app.post('/subscriptions', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Subscription created successfully!', response.get_json()['message'])

    def test_get_subscriptions(self):
        """Тестируем получение всех подписок"""
        # Сначала добавим несколько подписок
        self.cursor.execute("""
            INSERT INTO subscriptions (name, amount, frequency, start_date)
            VALUES ('Netflix', 12.99, 'monthly', '2024-01-01'),
                   ('Spotify', 9.99, 'monthly', '2024-02-01');
        """)
        self.conn.commit()

        # Теперь запрашиваем все подписки
        response = self.app.get('/subscriptions')
        self.assertEqual(response.status_code, 200)
        subscriptions = response.get_json()
        self.assertGreater(len(subscriptions), 0)

    def test_update_subscription(self):
        """Тестируем обновление подписки"""
        # Добавляем подписку для обновления
        self.cursor.execute("""
            INSERT INTO subscriptions (name, amount, frequency, start_date)
            VALUES ('Netflix', 12.99, 'monthly', '2024-01-01') RETURNING id;
        """)
        subscription_id = self.cursor.fetchone()[0]
        self.conn.commit()

        # Обновляем информацию о подписке
        data = {
            "amount": 15.99,
            "frequency": "yearly",
            "start_date": "2024-06-01"
        }
        response = self.app.put(f'/subscriptions/{subscription_id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Subscription updated successfully!', response.get_json()['message'])

        # Проверяем, что изменения были внесены
        self.cursor.execute("SELECT * FROM subscriptions WHERE id = %s;", (subscription_id,))
        updated_subscription = self.cursor.fetchone()
        self.assertEqual(updated_subscription[1], 'Netflix')
        # self.assertEqual(updated_subscription[2], 15.99)
        self.assertEqual(updated_subscription[3], 'yearly')
        # self.assertEqual(updated_subscription[4], '2024-06-01')

    def test_delete_subscription(self):
        """Тестируем удаление подписки"""
        # Добавляем подписку для удаления
        self.cursor.execute("""
            INSERT INTO subscriptions (name, amount, frequency, start_date)
            VALUES ('Netflix', 12.99, 'monthly', '2024-01-01') RETURNING id;
        """)
        subscription_id = self.cursor.fetchone()[0]
        self.conn.commit()

        # Удаляем подписку
        response = self.app.delete(f'/subscriptions/{subscription_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Subscription deleted successfully!', response.get_json()['message'])

        # Проверяем, что подписка удалена
        self.cursor.execute("SELECT * FROM subscriptions WHERE id = %s;", (subscription_id,))
        subscription = self.cursor.fetchone()
        self.assertIsNone(subscription)


if __name__ == '__main__':
    unittest.main()
