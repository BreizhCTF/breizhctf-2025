from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('phones.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/app/track/location/<string:number>')
def get_location(number):
    conn = get_db_connection()
    location = conn.execute('SELECT location FROM phones WHERE phone_number = ?', (number,)).fetchone()
    conn.close()
    
    if location:
        return jsonify({"location": location['location']})
    else:
        return jsonify({"error": "Phone number not found"}), 404

@app.route('/app/track/owner/<string:number>')
def get_owner(number):
    conn = get_db_connection()
    owner = conn.execute('SELECT owner FROM phones WHERE phone_number = ?', (number,)).fetchone()
    conn.close()
    
    if owner:
        return jsonify({"owner": owner['owner']})
    else:
        return jsonify({"owner": "Null (Burner phone)"}), 404

@app.route('/app/track/company/<string:number>')
def get_company(number):
    conn = get_db_connection()
    company = conn.execute('SELECT company FROM phones WHERE phone_number = ?', (number,)).fetchone()
    conn.close()
    
    if company:
        return jsonify({"company": company['company']})
    else:
        return jsonify({"error": "Phone number not found"}), 404

@app.route('/app/track/last-called-number/<string:number>')
def get_last_called(number):
    conn = get_db_connection()
    last_called = conn.execute('SELECT last_called FROM phones WHERE phone_number = ?', (number,)).fetchone()
    conn.close()
    
    if last_called:
        return jsonify({"last_called_number": last_called['last_called']})
    else:
        return jsonify({"error": "Phone number not found"}), 404

@app.route('/app/burner/crack-password/<string:number>')
def crack_password(number):
    conn = get_db_connection()
    password = conn.execute('SELECT password FROM phones WHERE phone_number = ?', (number,)).fetchone()
    conn.close()
    if password:
        if len(password['password']) > 8:
            return jsonify({"error": "Password too long to crack"}), 400
        return jsonify({"password": password['password']})
    else:
        return jsonify({"error": "Phone number not found"}), 404

@app.route('/app/infos/<string:number>')
def get_all_info(number):
    conn = get_db_connection()
    phone_info = conn.execute('SELECT * FROM phones WHERE phone_number = ?', (number,)).fetchone()
    conn.close()

    if phone_info:
        return jsonify({
            "phone_number": phone_info['phone_number'],
            "owner": phone_info['owner'],
            "company": phone_info['company'],
            "location": phone_info['location'],
            "last_called": phone_info['last_called'],
        })
    else:
        return jsonify({"error": "Phone number not found"}), 404

@app.route('/app/company/infos/<string:name>')
def get_company_info(name):
    conn = get_db_connection()
    company_info = conn.execute('SELECT * FROM companies WHERE company_name = ?', (name,)).fetchone()
    
    if company_info:
        block_start = company_info['block_start']
        block_end = company_info['block_end']
        number_of_numbers = conn.execute('SELECT COUNT(*) FROM phones WHERE company = ?', (name,)).fetchone()[0]
        conn.close()
        return jsonify({
            "company_name": company_info['company_name'],
            "block_start": block_start,
            "block_end": block_end,
            "number_of_numbers": number_of_numbers
        })
    else:
        conn.close()
        return jsonify({"error": "Company not found"}), 404
        

# Route to get phone numbers for a specific company
@app.route('/app/company/get-phones/<company>', methods=['GET'])
def get_phones(company):
    # Get the phones for the company
    conn = sqlite3.connect('phones.db')
    cursor = conn.cursor()
    
    # Query to get all phone numbers associated with the company
    cursor.execute('''
    SELECT phone_number FROM phones WHERE company = ? ORDER BY phone_number
    ''', (company,))
    
    phones = cursor.fetchall()
    conn.close()
    
    # Extract the phone numbers from the result
    phone_numbers = [phone[0] for phone in phones]
    
    if phone_numbers:
        return jsonify({"company": company, "phone_numbers": phone_numbers}), 200
    else:
        return jsonify({"error": "No phones found for this company"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)
