from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5001/api/books"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Book Store Viewer</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
  body {
    font-family: 'Poppins', sans-serif;
    background-color: #f4f6f7;
    margin: 0;
    padding: 0;
    color: #2C3E50;
  }
  header {
    background-color: #2E86C1;
    color: white;
    text-align: center;
    padding: 20px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  }
  h1 {
    margin: 0;
    font-size: 28px;
  }
  main {
    width: 80%;
    margin: 30px auto;
    background: white;
    padding: 20px 30px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
  button {
    background-color: #2E86C1;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
  }
  button:hover {
    background-color: #1B4F72;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  th, td {
    text-align: center;
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }
  th {
    background-color: #AED6F1;
  }
  tr:nth-child(even) {
    background-color: #F8F9F9;
  }
  footer {
    text-align: center;
    margin: 25px 0;
  }
  a {
    color: #2E86C1;
    text-decoration: none;
    font-weight: 600;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
</head>
<body>
<header>
  <h1>📚 College Book Store – Viewer (READ Operation)</h1>
</header>
<main>
  <button onclick="loadBooks()">🔄 Refresh Book List</button>
  <table id="booksTable">
    <tr><th>ID</th><th>Title</th><th>Price (₹)</th></tr>
  </table>
  <footer>
    <p>Go to <a href="http://127.0.0.1:5001/">Website 2 (Admin – CRUD Operations)</a></p>
  </footer>
</main>

<script>
async function loadBooks() {
  const res = await fetch("/fetch_books");
  const json = await res.json();
  const table = document.getElementById('booksTable');
  while (table.rows.length > 1) table.deleteRow(1);
  json.forEach(b => {
    const row = table.insertRow();
    row.insertCell().innerText = b.id;
    row.insertCell().innerText = b.title;
    row.insertCell().innerText = b.price;
  });
}
window.onload = loadBooks;
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/fetch_books')
def fetch_books():
    try:
        r = requests.get(API_URL, timeout=3)
        return jsonify(r.json())
    except Exception:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
