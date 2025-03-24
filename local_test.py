from flask import Flask, render_template, jsonify
import pyodbc

app = Flask(__name__)

# Funcție pentru a te conecta la baza de date Azure SQL
def get_db_connection():
    try:
        server = 'ps2n.database.windows.net'
        database = 'ps2n'
        username = 'Mexic'
        password = 'L0wlevel'
        driver = '{ODBC Driver 17 for SQL Server}'

        # Conectare la baza de date
        connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
        return connection
    except Exception as e:
        print(f"❌ Eroare la conexiune: {e}")
        return None

# Ruta principală - Servește pagina HTML
@app.route('/')
def index():
    return render_template('index.html')

# API - Obține ultima înregistrare din tabelul telemetry
@app.route('/latest')
def latest_data():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Conexiunea la baza de date a eșuat"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT TOP 1 id, temperature, humidity, EventEnqueuedUtcTime FROM telemetry ORDER BY id DESC")
        row = cursor.fetchone()

        if row:
            data = {
                "id": row[0],
                "temperature": row[1],
                "humidity": row[2],
                "timestamp": row[3]
            }
            return jsonify(data)

        return jsonify({"error": "Nu există date disponibile"})

    except Exception as e:
        print(f"❌ Eroare la interogare: {e}")
        return jsonify({"error": "Eroare la extragerea datelor"}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
