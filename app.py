from flask import Flask, render_template, redirect, url_for, request
import os
import requests
#import webbrowser
import time
import base64

backendServer = "backend"
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        with open("passwords.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line == "":
                    break
                decodedCheck = base64.b64decode(line.split(" ")[1].encode()).decode("utf-8")
                if (line.split(" ")[0] == request.form['username'] and decodedCheck == request.form['password']):
                        command = str(os.system('curl -X POST ' + backendServer + ' -H \'content-type: application/json\' -d \'"' + request.form['username']  + '"\''))
                        print(command)
                        time.sleep(5)
                        toEncode = str.encode(str('vcd-' + request.form['username']))
                        encoded = base64.b64encode(toEncode)
                        newUrl = 'http://localhost:81/vcd/?=' + str(encoded.decode("utf-8"))
                        return redirect(newUrl)
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
