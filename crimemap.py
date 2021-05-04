import json

from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import string


app = Flask(__name__)
DB = DBHelper()

categories = ["burglary", "drug-dealing", "murder", "mugging",
              "robbery", "shoplifting", "theft", "vandalism"]

def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)

@app.route("/")
def home():
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template("home.html", crimes=crimes, categories=categories)


@app.route("/submitcrime", methods=["POST"])
def submitcrime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = request.form.get("date")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    description = sanitize_string(request.form.get("description"))
    DB.add_crime(category, date, latitude, longitude, description)
    return home()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
