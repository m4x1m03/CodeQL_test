from flask import Flask, request, g, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'

users = [
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Tim', 'tim@example.com')
]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT
            )
        """)
        cursor.execute("DELETE FROM users")
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    search_results = ""
    search_query = ""
    if request.method == 'POST':
        name = request.form.get('name', '')
        search_query = name
        db = get_db()
        cursor = db.cursor()
        
        # vulnerable SQL query
        query = f"SELECT * FROM users WHERE name = '{name}'"
        cursor.execute(query)
        results = cursor.fetchall()
        
        search_results = f"<h2>Search Results for '{search_query}'</h2><ul>"
        for row in results:
            search_results += f"<li>ID: {row[0]}, Name: {row[1]}, Email: {row[2]}</li>"
        search_results += "</ul>"
    
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>SQL Injection Demo</title>
        </head>
        <body>
            <h1>SQL Injection</h1>
            <p>Search for users:</p>
            <form method="post">
                <input type="text" name="name" placeholder="Enter name">
                <button type="submit">Search</button>
            </form>
            {{ search_results|safe }}
        </body>
        </html>
    ''', search_results=search_results)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


# resources used
# ChatGPT "how to use sqlite in a python project?"
# ChatGPT "how to populate a sqlite table python"
# ChatGPT "how do i close my database after sending a request"
# https://www.geeksforgeeks.org/python-sqlite-cursor-object/