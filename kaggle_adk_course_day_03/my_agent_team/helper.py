import sqlite3
import os


def check_data_in_db():
    with sqlite3.connect("my_agent_data.db") as connection:
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0] for _ in result.description])
        for each in result.fetchall():
            print(each)


def clear_database():
    if os.path.exists("my_agent_data.db"):
        os.remove("my_agent_data.db")
        print("✅ Old database file removed.")
    else:
        print("ℹ️ No existing database file found to remove.")   

clear_database()
# check_data_in_db()