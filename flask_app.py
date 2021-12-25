# Importing required packages
from flask import Flask, render_template, request
from search import search_online
import os

# create flask app
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def scrappers():
    if request.method == 'POST':
        # Get search string entered by user
        searchString = request.form['content'].replace(" ", "")

        # search for string online
        reviews = search_online(searchString)

        # showing the review to the user
        return render_template("results.html", reviews=reviews)
    else:
        return render_template("index.html", index=True)


# running the app on the local machine on port 9000
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)