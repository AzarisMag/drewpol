from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_DIR = "/data"

@app.route('/', methods=['GET'])
def index():
    return """
    <form method="POST" action="/submit">
      <label>Rodzaj:</label>
      <select name="rodzaj">
        <option>psd</option>
        <option>psg</option>
        <option>pop</option>
      </select><br>
      <label>Ilość sztuk:</label>
      <input type="number" name="ilosc"><br>
      <label>Kolor:</label>
      <select name="kolor">
        <option>czarna_m</option>
        <option>biała_m</option>
        <option>grey_wm</option>
      </select><br>
      <label>Defekt:</label>
      <select name="defekt">
        <option>rysy</option>
        <option>syf</option>
        <option>fale</option>
        <option>mix</option>
      </select><br>
      <label>Opakowanie:</label>
      <select name="opakowanie">
        <option>czop</option>
        <option>okl</option>
        <option>mag</option>
      </select><br>
      <input type="submit" value="Wyślij">
    </form>
    <div>
      <h3>Dane z dzisiaj:</h3>
      <table border="1">
        <tr><th>Rodzaj</th><th>Ilość</th><th>Kolor</th><th>Defekt</th><th>Opakowanie</th></tr>
        """ + get_today_data_html() + """
      </table>
    </div>
    """

@app.route('/submit', methods=['POST'])
def submit():
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    filename = os.path.join(DATA_DIR, f"{date_str}.txt")
    data = [
        request.form['rodzaj'],
        request.form['ilosc'],
        request.form['kolor'],
        request.form['defekt'],
        request.form['opakowanie']
    ]
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    return '<meta http-equiv="refresh" content="0; url=/" />'

def get_today_data_html():
    date_str = datetime.now().strftime("%d-%m-%Y")
    filename = os.path.join(DATA_DIR, f"{date_str}.txt")
    if not os.path.isfile(filename):
        return ""
    rows = ""
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            rows += f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>"
    return rows

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
