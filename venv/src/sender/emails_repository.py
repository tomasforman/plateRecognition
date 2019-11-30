import psycopg2


def fetch_emails():
    conn = None
    try:
        conn = psycopg2.connect(host="localhost", database="plates", user="postgres", password="postgres")
        cur = conn.cursor()
        cur.execute("SELECT address FROM emails")
        rows = cur.fetchall()
        cur.close()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
