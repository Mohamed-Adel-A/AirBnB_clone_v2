#!/usr/bin/python3
"""
- /hbnb_filters: display a HTML page like 6-index.html,
  which was done during the project 0x01. AirBnB clone - Web static
    * Copy files 3-footer.css, 3-header.css, 4-common.css and 6-filters.css
      from web_static/styles/ to the folder web_flask/static/styles
    * Copy files icon.png and logo.png from web_static/images/
      to the folder web_flask/static/images
    * Update .popover class in 6-filters.css to allow scrolling
      in the popover and a max height of 300 pixels.
    * Use 6-index.html content as source code for the template
      10-hbnb_filters.html:
    * Replace the content of the H4 tag under each filter title
      (H3 States and H3 Amenities) by &nbsp;
      * State, City and Amenity objects must be loaded from DBStorage and sorted by name (A->Z)
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/hbnb")
def hbnb_route():
    states_list = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return (render_template("100-hbnb.html",
                           states_list=states_list,
                           amenities=amenities,
                           places=places))


@app.teardown_appcontext
def close_db(error):
    """
    close file or db connection
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
