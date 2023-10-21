#!/usr/bin/python3
"""
a script that starts a Flask web application
- Your web application must be listening on 0.0.0.0, port 5000
- Routes:
    * /: display “Hello HBNB!”
    * /hbnb: display “HBNB”
    * /c/<text>: display “C ” followed by the value of the text variable
      (replace underscore _ symbols with a space )
- You must use the option strict_slashes=False in your route definition
"""

from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', strict_slashes=False)
def hello_route():
    """
    display “Hello HBNB!”
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """
    display “HBNB”
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    display “C ” followed by the value of the text variable
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """
    display “Python ” followed by the value of the text variable
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """
    display “n is a number” only if n is an integer
    """
    return "{} is a number".format(n)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
