from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydatabase'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    item_name = request.form['name']
    new_item = Item(name=item_name)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
