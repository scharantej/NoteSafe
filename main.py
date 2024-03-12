
# Import Flask, templates, sessions, and database tools
from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask application instance
app = Flask(__name__)

# Configure database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
# Create database instance
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    notes = db.relationship('Note', backref='user', lazy=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('home.html', notes=notes)

@app.route('/create-note', methods=['GET', 'POST'])
def create_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        note = Note(title=title, body=body, user_id=user.id)
        db.session.add(note)
        db.session.commit() 
        return redirect(url_for('home'))

    return render_template('create-note.html')

@app.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    note = Note.query.get(note_id)
    if not note:
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        note.title = title
        note.body = body
        db.session.commit() 
        return redirect(url_for('home'))

    return render_template('edit-note.html', note=note)

@app.route('/delete-note/<int:note_id>', methods=['GET'])
def delete_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    note = Note.query.get(note_id)
    if not note:
        return redirect(url_for('home'))

    db.session.delete(note)
    db.session.commit() 
    return redirect(url_for('home'))

@app.route('/search-notes', methods=['GET'])
def search_notes():
    if 'username' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query')
    notes = Note.query.filter(Note.title.ilike("%{}%".format(query))).all()
    return render_template('search-notes.html', notes=notes)

@app.route('/tag-notes', methods=['GET', 'POST'])
def tag_notes():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        tags = request.form['tags']
        note_ids = request.form.getlist('note_ids')

        for note_id in note_ids:
            note = Note.query.get(note_id)
            note.tags = tags
            db.session.commit() 
            
    notes = Note.query.all()
    return render_template('tag-notes.html', notes=notes)

# Create tables in the database
db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
