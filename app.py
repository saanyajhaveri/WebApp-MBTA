
from flask import Flask, render_template, request

from mbta_helper import find_stop_near

"""Import flask and function from mbta_helper"""

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    """Header for page is referenced from template"""
    return render_template("index.html")

@app.route("/POST/nearest", methods=["POST","GET"])
def find():
    """
    Utilizes find_stop_near function to output station and wheelchair accessibility on Web App.
    """
    if request.method == "POST":
        place = request.form["location"]
        place = str(place)
        result = find_stop_near(place)
        if result == "MBTA Not Available":
            return render_template("notavailable.html")
        else:
            result = result.split(",")
            return render_template("available.html", location = result[0], wheelchair = result[1])


if __name__ == '__main__':
    app.run(debug=True)