from flask import Flask, g, jsonify, request, render_template, redirect, url_for, flash
import sqlite3

DATABASE = 'clothesline.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

app = Flask(__name__)
app.secret_key = 'fDbRbj3x1KHNmINHUj1uzg'

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def index():
  db = get_db()
  cursor = db.execute('SELECT * FROM clothing_items')
  items = cursor.fetchall()
  items = [dict(row) for row in items]
  return render_template('index.html', items=items)

@app.route('/clothing/new', methods=['GET'])
def new_clothing():
    return render_template('new_clothing.html')
  
@app.route('/clothing', methods=['POST'])
def create():
  name = request.form.get('name')
  image_url = request.form.get('image_url')
  location = request.form.get('location')

  if not name or location not in ['HOME', 'SCHOOL']:
    flash('Invalid data', 'error')  # Use flash messages to display error messages
    return redirect(url_for('index'))
  
  db = get_db()
  db.execute('INSERT INTO clothing_items (name, image_url, location) VALUES (?, ?, ?)', (name, image_url, location))
  db.commit()
  
  flash('Clothing item created successfully', 'success')  # Use flash messages to display success messages
  return redirect(url_for('index'))  # Redirect to the index route
  
@app.route('/clothing/<int:id>', methods=['PUT'])
def update(id):
  data = request.json
  location = data.get('location')
  
  db = get_db()
  db.execute('UPDATE clothing_items SET location = ? WHERE id = ?', (location, id))
  db.commit()
  item = db.execute('SELECT * FROM clothing_items WHERE id = ?', (id,)).fetchone()
  return jsonify({'success': True, 'item': dict(item)}), 200
  
      
@app.route('/clothing/<int:id>', methods=['DELETE'])
def delete(id):
  print('deleting item', id)
  db = get_db() 
  db.execute('DELETE FROM clothing_items WHERE id = ?', (id,))
  db.commit()
  return jsonify({'success': True}), 200
  
  
