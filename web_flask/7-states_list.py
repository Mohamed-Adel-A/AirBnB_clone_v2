#!/usr/bin/python3
"""
- /states_list: display a HTML page: (inside the tag BODY)
    H1 tag: “States”
    UL tag: with the list of all State objects
    present in DBStorage sorted by name (A->Z)
    LI tag: description of one State: <state.id>: <B><state.name></B>
"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states_list")
def states_list_route():
    """
    display a HTML page of state list
    """
    states_list = storage.all("State").values()
    return (render_template("7-states_list.html", states_list=states_list))


@app.teardown_appcontext
def close_db(error):
    """
    close file or db connection
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
