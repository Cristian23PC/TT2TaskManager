from flask import Flask, render_template, request, session, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from datetime import datetime

app = Flask(__name__)

#Configuración de la bd
USER_DB = 'postgres'
PASS_DB = 'admin.1302'
URL_DB = 'localhost'
NAME_DB = 'gestion_tareas_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'admin.1302'

#Inicializacion del objeto db de sqlalchemy
db = SQLAlchemy(app)

#configurar flask migrate
migrate = Migrate()
migrate.init_app(app, db)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))
    #contrasena = db.Column(db.String(250))
    password = db.Column(db.String(250))

class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250))
    titulo = db.Column(db.String(250))
    descripcion = db.Column(db.String(2000))
    date_task = db.Column(db.DateTime())

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    conn = psycopg2.connect('dbname=gestion_tareas_db user=postgres password=admin.1302')
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario where email= %s AND password = %s",(email,password))
    user = cur.fetchone()
    cur.close()

    if user is not None:
        session['email'] = user[0]
        session['nombre'] = user[1]
        session['apellido'] = user[2]
        return redirect(url_for('tasks'))
    else:
        return render_template('index.html', message="Las credenciales no son correctas")

@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/new-task', methods=['POST'])
def newTasks():
    titulo = request.form['title']
    descripcion = request.form['description']
    email = session['email']
    d = datetime.now()
    dateTask = d.strftime("%Y-%m-%d %H:%M:%S")

    if titulo and descripcion and email:
        conn = psycopg2.connect('dbname=gestion_tareas_db user=postgres password=admin.1302')
        cur = conn.cursor()
        sql = "INSERT INTO tareas (email, titulo, descripcion, date_task) VALUES (%s,%s,%s,%s)"
        data = (email, titulo, descripcion, dateTask)
        cur.execute(sql,data)
        conn.commit()
    return redirect(url_for("tasks"))

@app.route('/new-user', methods = ['POST'])
def newUser():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']

    if nombre and apellido and email and password:
        conn = psycopg2.connect('dbname=gestion_tareas_db user=postgres password=admin.1302')
        cur = conn.cursor()
        sql = "INSERT INTO usuario (nombre, apellido , email, password) VALUES (%s,%s,%s,%s)"
        data = (nombre, apellido, email, password)
        cur.execute(sql, data)
        psycopg2.connect.commit()
    return redirect(url_for('tasks'))



