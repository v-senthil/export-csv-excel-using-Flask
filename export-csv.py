from flask import Flask, render_template, url_for, Response
import sqlite3
import io
import csv

app = Flask(__name__)

@app.route('/')
def download():
 return render_template('download_csv.html')

@app.route('/download/csv')
def download_report():
    conn=sqlite3.connect('data.db', check_same_thread=False)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)

    line = ['Timestamp, Temperature, Humidity']
    # writer.writerow(line)
    for row in result:
        time = str(row[0])
        temp =str(row[1])
        hum =str(row[2])
        line = [time + ',' + temp + ',' + hum]
        writer.writerow(line)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})

if __name__ == '__main__':
    app.run(debug=True)
