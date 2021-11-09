
from flask import Flask, render_template, request

from mbta_helper import find_stop_near

"""Import flask and function from mbta_helper"""

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    """Reference index.html template for page contents"""
    return render_template("index.html")

@app.route("/POST/nearest", methods=["POST","GET"])
def find():
    """
    References templates for instances when "MBTA Not Available" and when available
    """
    if request.method == "POST":
        place = request.form["location"]
        place = str(place)
        result = find_stop_near(place)
        if result == "MBTA Not Available":
            return render_template("notfound.html")
        else:
            result = result.split(",")
            return render_template("found.html", location = result[0], wheelchair = result[1])

if __name__ == '__main__':
    app.run(debug=True)