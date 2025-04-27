import psycopg2

conn = psycopg2.connect(
    dbname="judo",
    user="postgres",
    password="mobin@nooshi2003",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    judoka_1 TEXT,
    judoka_2 TEXT,
    winner TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id),
    time TEXT,
    judoka_1_action TEXT,
    judoka_2_action TEXT
)
""")

conn.commit()

import json
import os

json_folder = "/home/mobin/Desktop/mr.abdollahi/data_iran"  # مسیر پوشه‌ای که فایل‌هات داخلشه

for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        with open(os.path.join(json_folder, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        judoka_1 = data["judoka_1"]
        judoka_2 = data["judoka_2"]
        winner = data["winner"]
        events = data["events"]

        # ذخیره مسابقه
        cursor.execute("""
            INSERT INTO matches (judoka_1, judoka_2, winner) VALUES (%s, %s, %s) RETURNING id
        """, (judoka_1, judoka_2, winner))
        match_id = cursor.fetchone()[0]

        # ذخیره اتفاقات
        for e in events:
            cursor.execute("""
                INSERT INTO events (match_id, time, judoka_1_action, judoka_2_action)
                VALUES (%s, %s, %s, %s)
            """, (match_id, e.get("time"), e.get(judoka_1), e.get(judoka_2)))

conn.commit()
cursor.close()
conn.close()
print("✅ داده‌ها با موفقیت وارد PostgreSQL شدند.")
