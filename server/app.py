# -*- coding: utf-8

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Cross Domain Solve
CORS(app, origins='*', allow_headers='*')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get authetication
        username = request.form['username']
        password = request.form['password']
        print (username, password)
        return jsonify(success=False, reason="Wrong password/username!")
    elif request.method == 'GET':
        # return login page
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
