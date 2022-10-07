from flask import Flask , render_template, request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    des = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno}-{self.title}'
        


@app.route("/" , methods=['GET' , 'POST'])
def hello_world():
    if request.method == 'POST':
        title=request.form['title']
        des=request.form['des']
        todo = Todo(title=title, des=des)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html" , all_todo = all_todo)

   
# @app.route("/show")
# def products():
#     all_todo = Todo.query.all()
#     print(all_todo)
#     return "<h1>Products</h1>"

@app.route("/update/<int:sno>",methods=['GET' , 'POST'])
def update(sno):
    if request.method == 'POST':
        title=request.form['title']
        des=request.form['des']
        update_todo = Todo.query.filter_by(sno=sno).first()
        update_todo.title=title
        update_todo.des=des
        db.session.add(update_todo)
        db.session.commit()
        return redirect("/")

    update_todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html" , update_todo = update_todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    del_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)