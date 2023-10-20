from flask import Flask, g, jsonify, request, render_template, redirect, url_for, flash
import sqlite3
import boto3
from dotenv import load_dotenv
import os

DATABASE = 'clothesline.db'

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")


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
  print(name, image_url, location)

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
  
  
@app.route('/sign-s3', methods=['GET'])
def sign_s3():
    filename = request.args.get('filename')
    s3 = boto3.client('s3')

    bucket_name = 'clothesline'

    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': filename},
        ExpiresIn=3600
    )

    return jsonify({'url': presigned_url, 'bucket': bucket_name, 'filename': filename})