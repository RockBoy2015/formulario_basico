from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# NOVO: Model para salvar os dados do segundo formulário
class Formulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    campo1 = db.Column(db.String(200), nullable=False)
    campo2 = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['senha']

        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            return 'Usuário já existente. Por favor, escolha outro nome de usuário.'

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['senha']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return 'Usuário ou senha incorretos. Tente novamente.'
    
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('index.html', username=session['username'])

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        dado1 = request.form['campo1']
        dado2 = request.form['campo2']

        novo_registro = Formulario(
            username=session['username'],
            campo1=dado1,
            campo2=dado2
        )
        db.session.add(novo_registro)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('formulario.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
