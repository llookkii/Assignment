import os
import logging
from flask import Flask, request, jsonify
from psycopg2 import connect, sql, OperationalError, ProgrammingError, DatabaseError
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), 'config/.env'))

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Setup logging
logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        if not data:
            logging.error("No JSON data received")
            return jsonify({"error": "No data received"}), 400

        name = data.get('name')
        age = data.get('age')

        # Validate input data
        if not name or not age:
            logging.error("Validation failed: Name or age is missing.")
            return jsonify({"error": "Name and age are required"}), 400

        if not isinstance(age, int) or age <= 0:
            logging.error("Validation failed: Invalid age value.")
            return jsonify({"error": "Age must be a positive integer"}), 400

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

    except (ProgrammingError, DatabaseError) as db_error:
        logging.error(f"Database error: {db_error}")
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        logging.error(f"Error processing data: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)