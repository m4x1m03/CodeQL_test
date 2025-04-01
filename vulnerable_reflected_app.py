from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def search():
    # get search query
    query = request.args.get('query', '')

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Search Engine</title>
        </head>
        <body>
            <h1>Search Engine</h1>
            <form action="/" method="GET">
                <label for="query">Search:</label>
                <input type="text" id="query" name="query" placeholder="Type something...">
                <input type="submit" value="Search">
            </form>

            {% if query %}
                <h2>Results for: <b>{{ query | safe }}</b></h2>
                <p>No results found. Try another query.</p>
            {% endif %}
        </body>
        </html>
    ''', query=query)

if __name__ == '__main__':
    app.run(debug=True)
