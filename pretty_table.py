from flask import Flask, render_template_string
import psycopg2

# Flask application
app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "ecom_db"
DB_USER = "ecom_user"
DB_PASSWORD = "ecom_password"

# HTML Template for rendering the table
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Table Data</title>
    <style>
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: center;
        }
        td {
            text-align: center;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Table Data</h1>
    <table>
        <thead>
            <tr>
                {% for col in columns %}
                <th>{{ col }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                {% for cell in row %}
                <td>{{ cell }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

def fetch_table_data(table_name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Fetch data from the specified table
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Fetch column names
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        return columns, rows

    except Exception as e:
        print(f"Error: {e}")
        return [], []

@app.route("/")
def show_table():
    table_name = "users_useractivitylog"  # Replace with your table name
    columns, rows = fetch_table_data(table_name)
    return render_template_string(HTML_TEMPLATE, columns=columns, rows=rows)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
