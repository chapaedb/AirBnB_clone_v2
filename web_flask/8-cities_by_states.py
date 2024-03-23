#!/usr/bin/python3
"""starts a flask application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the connection to the database"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """displays a page containing states"""
    states_list = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
