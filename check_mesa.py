from config import get_connection

conn = get_connection()
cursor = conn.cursor()
try:
    cursor.execute("INSERT INTO ciudadanos (identificacion,nombre,puesto_id,mesa) VALUES (?, ?, ?, ?)",
                   ("5555555555","Prueba Mesa",2,3))
    conn.commit()
    print('insert successful')
except Exception as e:
    print('error', e)
finally:
    cursor.close()
    conn.close()


conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM ciudadanos WHERE identificacion=?", ("5555555555",))
print(cursor.fetchone())
cursor.close()
conn.close()