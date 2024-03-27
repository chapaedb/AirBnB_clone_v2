#!/usr/bin/python3
"""
This script starts a Flask web application.

Routes:
- /: Displays 'Hello HBNB!'
- /hbnb: Displays 'HBNB'
- /c/<text>: Displays 'C ' followed by the value of the text variable
- /python/<text>: Displays 'Python ' followed by the value of the text variable
- /number/<int:n>: Displays '{n} is a number' if n is an integer
- /number_template/<int:n>: Displays an HTML page if n is an integer
- /number_odd_or_even/<int:n>: Displays an HTML page indicating if n is odd or even
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route that displays 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route that displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Route that displays 'C ' followed by the value of the text variable"""
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """Route that displays 'Python ' followed by the value of the text variable"""
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Route that displays '{n} is a number' if n is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Route that displays an HTML page if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Route that displays an HTML page indicating if n is odd or even"""
    odd_or_even = 'odd' if n % 2 != 0 else 'even'
    return render_template('6-number_odd_or_even.html', n=n, odd_or_even=odd_or_even)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
