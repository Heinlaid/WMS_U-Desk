from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Задайте строку подключения к вашей БД PostgreSQL
# Формат: postgresql://<username>:<password>@<host>/<dbname>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Marlek2171790!@localhost/wms_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация объекта SQLAlchemy
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

