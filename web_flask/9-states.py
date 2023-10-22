#!/usr/bin/python3
"""
- /states: display a HTML page: (inside the tag BODY)
    * H1 tag: “States”
    * UL tag: with the list of all State objects
      present in DBStorage sorted by name (A->Z) tip
    * LI tag: description of one
      State: <state.id>: <B><state.name></B>
- /states/<id>: display a HTML page: (inside the tag BODY)
    * If a State object is found with this id:
        H1 tag: “State: ”
        H3 tag: “Cities:”
        UL tag: with the list of City objects
                linked to the State sorted by name (A->Z)
        LI tag: description of one City: <city.id>: <B><city.name></B>
    * Otherwise: H1 tag: “Not found!”
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states")
@app.route("/states/<id>")
def states_route(id=None):
    """
    """
    states_list = storage.all(State)
    if id:
        state = states_list.get("State.{}".format(id))
        if state:
            return (render_template("9-states.html", state=state))
        return (render_template("9-states.html"))
    else:
        return (render_template("9-states.html",
                                states_list=states_list.values()))


@app.teardown_appcontext
def close_db(error):
    """
    close file or db connection
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
