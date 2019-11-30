import psycopg2


def find_plate(plate: str) -> bool:
    conn = None
    try:
        conn = psycopg2.connect(host="localhost",database="plates", user="postgres", password="postgres")
        cur = conn.cursor()
        query = f"SELECT id FROM plates AS p WHERE p.plate = {plate}"
        cur.execute(query)
        print("The number of parts: ", cur.rowcount)
        plate_id = cur.fetchone()
        cur.close()
        return plate_id > 0
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()