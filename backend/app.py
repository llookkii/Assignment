import os
import logging
from flask import Flask, request, jsonify
from psycopg2 import connect, sql, OperationalError
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'config/.env'))

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='logs/app.log', level=logging.DEBUG)

# Database connection function
def get_db_connection():
    try:
        connection = connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
        return connection
    except OperationalError as err:
        logging.error(f"Database connection failed: {err}")
        return None

# Route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.json
        name = data.get('name')
        age = data.get('age')

        if not name or not age:
            logging.error("Validation failed: Name or age is missing.")
            return jsonify({"error": "Name and age are required"}), 400

        # Connect to the database
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # Insert data into the database
        insert_query = sql.SQL("INSERT INTO users (name, age) VALUES (%s, %s)")
        cursor.execute(insert_query, (name, age))
        conn.commit()

        cursor.close()
        conn.close()

        logging.info(f"Data successfully inserted: {name}, {age}")
        return jsonify({"message": "Data successfully submitted"}), 200

    except Exception as e:
        logging.error(f"Error processing data: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
