from flask import Flask, render_template, request, redirect, url_for
from config import get_connection, init_database


app = Flask(__name__)

# Inicializar la base de datos al iniciar la aplicación
init_database()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        identificacion = request.form["identificacion"]
        nombre = request.form["nombre"]
        puesto = request.form["puesto"]
        mesa = request.form.get("mesa")

        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO ciudadanos (identificacion,nombre,puesto_id,mesa) VALUES (?, ?, ?, ?)"
        try:
            cursor.execute(sql,(identificacion,nombre,puesto,mesa))
            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return render_template("error.html", message=str(e)), 500
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM puestos_votacion")
    puestos = cursor.fetchall()
    # también tomar las mesas existentes para el formulario
    cursor.execute("SELECT DISTINCT mesa FROM puestos_votacion ORDER BY mesa")
    mesas = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template("registro.html", puestos=puestos, mesas=mesas)


@app.route("/consult", methods=["GET","POST"])
def consult():

    if request.method == "POST":

        identificacion = request.form["identificacion"]

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT c.identificacion, p.lugar, p.direccion, p.mesa, p.zona, c.mesa
        FROM ciudadanos c
        JOIN puestos_votacion p ON c.puesto_id = p.id
        WHERE c.identificacion = ?
        """

        cursor.execute(sql,(identificacion,))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template("resultado.html", data=resultado)

    return render_template("consulta.html")


if __name__ == "__main__":
    app.run(debug=True)