import sys

from flask import Flask, abort, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


#db.create_all()


@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    description = request.get_json()['description']
    todo = Todo(description=description)
    try:
        db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        if error:
            abort(400)
        else:
            return jsonify({
                'description': todo.description
            })
        db.session.close()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


if __name__ == '__main__':
    app.run()
