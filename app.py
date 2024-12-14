from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='food_data'
    )
    return conn

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_info (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                food_type VARCHAR(255), 
                amount VARCHAR(255), 
                location VARCHAR(255), 
                contact VARCHAR(255), 
                available_time VARCHAR(255)
            )
        ''')
        conn.commit()
    except Exception as e:
        logging.error(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

# Initialize table
create_table()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if request.method == 'POST':
        food_type = request.form['food_type']
        amount = request.form['amount']
        location = request.form['location']
        contact = request.form['contact']
        available_time = request.form['available_time']
        
        # Insert into the database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO food_info (food_type, amount, location, contact, available_time) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (food_type, amount, location, contact, available_time))
            conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('seeker'))
    
    return render_template('donor.html')

@app.route('/seeker')
def seeker():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM food_info')
        records = cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        records = []
    finally:
        cursor.close()
        conn.close()

    return render_template('seeker.html', records=records)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6939)

    
