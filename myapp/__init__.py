import os
import datetime
import time
from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


conn = sqlite3.connect('project.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS programs (id INTEGER PRIMARY KEY, program_name TEXT NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS classes (id INTEGER PRIMARY KEY, class_name TEXT NOT NULL, program_id INTEGER, FOREIGN KEY(program_id) REFERENCES programs(id))')
    c.execute("CREATE TABLE IF NOT EXISTS class_times (id INTEGER PRIMARY KEY, class_time TEXT, class_id INTEGER, FOREIGN KEY(class_id) REFERENCES classes(id))")
    c.execute("CREATE TABLE IF NOT EXISTS student_schedule (id INTEGER PRIMARY KEY, student_id INTEGER, class_time_id INTEGER, FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(class_time_id) REFERENCES class_times(id))")
    c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name_surname TEXT , email TEXT, password TEXT, class_id INTEGER, FOREIGN KEY(class_id) REFERENCES classes(id))")


def data_entry():
    c.execute("INSERT OR IGNORE INTO programs VALUES(1, 'Faculty of Economic Sciences')")
    c.execute("INSERT OR IGNORE INTO classes VALUES(1, 'Introduction to Python and SQL',1), (2, 'Applied Macroeconomics',1), (3, 'Applied Microeconomics',1), (4, 'Introduction to Data Science',1), (5, 'Introduction to R',1), (6, 'Statistics',1)")
    c.execute("INSERT OR IGNORE INTO class_times VALUES(1,'2021-02-01 15:30:00',1),(2,'2021-02-02 10:30:00',1),(3,'2021-02-03 17:00:00',1),(4,'2021-02-04 16:45:00',2),(5,'2021-02-03 16:45:00',2),(6,'2021-02-05 18:00:00',2),(7,'2021-02-01 10:30:00',3),(8,'2021-02:04 12:00:00',3),(9,'2021-02-05 11:00:00',4),(10,'2021-02-05 09:00:00',5),(11,'2021-02-01 09:00:00',6)")
    conn.commit()
    c.close()
    conn.close()

create_table()
data_entry()

file_path = os.path.abspath(os.getcwd())+"\project.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from myapp import routes
