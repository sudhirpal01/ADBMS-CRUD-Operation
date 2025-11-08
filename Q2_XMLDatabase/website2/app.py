from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import xml.etree.ElementTree as ET
from pathlib import Path

app = Flask(__name__)
BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "database.xml"

def ensure_db():
    if not DB_PATH.exists():
        root = ET.Element('books')
        ET.ElementTree(root).write(DB_PATH, encoding='utf-8', xml_declaration=True)

def load_tree():
    ensure_db()
    tree = ET.parse(DB_PATH)
    return tree, tree.getroot()

@app.route('/')
def home():
    tree, root = load_tree()
    books = []
    for b in root.findall('book'):
        books.append({
            'id': b.find('id').text if b.find('id') is not None else '',
            'title': b.find('title').text if b.find('title') is not None else '',
            'price': b.find('price').text if b.find('price') is not None else ''
        })

    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Book Store Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
  body { font-family:'Poppins',sans-serif; background:#f4f6f7; margin:0; }
  header { background:#1B4F72; color:white; padding:20px; text-align:center; }
  h1 { margin:0; font-size:28px; }
  main { width:80%; margin:30px auto; background:white; padding:25px; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
  form { margin:15px 0; }
  input { padding:8px; margin:5px; border:1px solid #ccc; border-radius:6px; }
  button { background:#1B4F72; color:white; padding:8px 14px; border:none; border-radius:6px; cursor:pointer; font-weight:600; }
  button:hover { background:#154360; }
  table { width:100%; border-collapse:collapse; margin-top:20px; }
  th,td { border-bottom:1px solid #ccc; padding:10px; text-align:center; }
  th { background:#AED6F1; }
  tr:nth-child(even){ background:#F8F9F9; }
  a { color:#1B4F72; font-weight:600; text-decoration:none; }
  a:hover { text-decoration:underline; }
</style>
</head>
<body>
<header>
  <h1>⚙️ Book Store Admin – CRUD Operations</h1>
  <p>(Create, Read, Update, Delete on XML Database)</p>
</header>
<main>
  <p><a href="http://127.0.0.1:5000/">🔗 Go to Viewer (Website 1)</a></p>
  <h3>Add Book</h3>
  <form method="post" action="/add">
    ID: <input name="id" required> Title: <input name="title" required> Price: <input name="price" required>
    <button type="submit">Add ➕</button>
  </form>

  <h3>Update Book</h3>
  <form method="post" action="/update">
    ID: <input name="id" required> New Title: <input name="title"> New Price: <input name="price">
    <button type="submit">Update 🔄</button>
  </form>

  <h3>Delete Book</h3>
  <form method="post" action="/delete">
    ID: <input name="id" required>
    <button type="submit">Delete ❌</button>
  </form>

  <h3>📘 Current Book List</h3>
  <table>
    <tr><th>ID</th><th>Title</th><th>Price (₹)</th></tr>
    {% for b in books %}
      <tr><td>{{b.id}}</td><td>{{b.title}}</td><td>{{b.price}}</td></tr>
    {% endfor %}
  </table>
</main>
</body>
</html>
"""
    return render_template_string(html, books=books)

@app.route('/add', methods=['POST'])
def add_book():
    tree, root = load_tree()
    book_id = request.form['id'].strip()
    title = request.form['title'].strip()
    price = request.form['price'].strip()
    new_book = ET.Element('book')
    ET.SubElement(new_book, 'id').text = book_id
    ET.SubElement(new_book, 'title').text = title
    ET.SubElement(new_book, 'price').text = price
    root.append(new_book)
    tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_book():
    tree, root = load_tree()
    book_id = request.form['id'].strip()
    new_title = request.form.get('title', '').strip()
    new_price = request.form.get('price', '').strip()
    for b in root.findall('book'):
        if b.find('id').text == book_id:
            if new_title:
                b.find('title').text = new_title
            if new_price:
                b.find('price').text = new_price
    tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_book():
    tree, root = load_tree()
    book_id = request.form['id'].strip()
    for b in root.findall('book'):
        if b.find('id').text == book_id:
            root.remove(b)
    tree.write(DB_PATH, encoding='utf-8', xml_declaration=True)
    return redirect(url_for('home'))

# API for Website1
@app.route('/api/books')
def api_books():
    tree, root = load_tree()
    books = []
    for b in root.findall('book'):
        books.append({
            'id': b.find('id').text,
            'title': b.find('title').text,
            'price': b.find('price').text
        })
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
