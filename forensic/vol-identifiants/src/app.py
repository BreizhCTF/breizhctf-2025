from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'  # Clé secrète pour gérer les sessions

# Identifiants valides
VALID_USERNAME = "evil"
VALID_PASSWORD = "BZHCTF{It's_important_t0_us3_HTTPS}"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['user'] = username  # Stocker l'utilisateur dans la session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Identifiants incorrects")
    
    return render_template('login.html', error=None)

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
