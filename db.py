import psycopg2
from aiogram import Dispatcher, Bot, Router, types, F

# Подключение к базе данных
conn = psycopg2.connect(dbname="grit_tych_rpp_finance_db", user="grit_tych_rpp_finance", password="123", host="127.0.0.1")
cursor = conn.cursor()

router = Router()
