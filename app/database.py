import sqlite3

def save_to_database(df, db_path):
    conn = sqlite3.connect(db_path)
    df.to_sql("incidents", conn, if_exists='replace', index=False)
    conn.close()
