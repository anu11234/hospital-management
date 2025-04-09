from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

# Patient routes
@app.route('/patients')
def patients():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        connection.close()
        return render_template('patients.html', patients=patients)
    return render_template('patients.html', patients=[])

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO patients (name, age, gender, address, phone, email)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (name, age, gender, address, phone, email))
                connection.commit()
                flash('Patient added successfully!', 'success')
            except Error as e:
                flash(f'Error adding patient: {e}', 'danger')
            finally:
                connection.close()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                UPDATE patients 
                SET name=%s, age=%s, gender=%s, address=%s, phone=%s, email=%s
                WHERE id=%s
                """
                cursor.execute(query, (name, age, gender, address, phone, email, id))
                connection.commit()
                flash('Patient updated successfully!', 'success')
            except Error as e:
                flash(f'Error updating patient: {e}', 'danger')
            finally:
                connection.close()
        return redirect(url_for('patients'))
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
        patient = cursor.fetchone()
        connection.close()
        return render_template('edit_patient.html', patient=patient)
    return redirect(url_for('patients'))

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM patients WHERE id = %s", (id,))
            connection.commit()
            flash('Patient deleted successfully!', 'success')
        except Error as e:
            flash(f'Error deleting patient: {e}', 'danger')
        finally:
            connection.close()
    return redirect(url_for('patients'))

# Appointment routes
@app.route('/appointments')
def appointments():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT a.*, p.name as patient_name 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        """
        cursor.execute(query)
        appointments = cursor.fetchall()
        connection.close()
        return render_template('appointments.html', appointments=appointments)
    return render_template('appointments.html', appointments=[])

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        reason = request.form['reason']
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO appointments 
                (patient_id, doctor_name, appointment_date, appointment_time, reason)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (patient_id, doctor_name, appointment_date, appointment_time, reason))
                connection.commit()
                flash('Appointment added successfully!', 'success')
            except Error as e:
                flash(f'Error adding appointment: {e}', 'danger')
            finally:
                connection.close()
        return redirect(url_for('appointments'))
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM patients")
        patients = cursor.fetchall()
        connection.close()
        return render_template('add_appointment.html', patients=patients)
    return render_template('add_appointment.html', patients=[])

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM appointments WHERE id = %s", (id,))
            connection.commit()
            flash('Appointment deleted successfully!', 'success')
        except Error as e:
            flash(f'Error deleting appointment: {e}', 'danger')
        finally:
            connection.close()
    return redirect(url_for('appointments'))

if __name__ == '__main__':
    app.run(debug=True)
