from flask import Flask, render_template, request, Response
import sqlite3
import io
import xlwt

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('download.html')

@app.route('/download/report/excel')
def download_report():
    conn=sqlite3.connect('data.db', check_same_thread=False)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchall()

    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Data')

    #add headers
    sh.write(0, 0, 'Time Stamp')
    sh.write(0, 1, 'Temperature')
    sh.write(0, 2, 'Humidity')


    idx = 0
    for row in result:
        time = str(row[0])
        temp =row[1]
        hum =row[2]
        sh.write(idx+1, 0, time)
        sh.write(idx+1, 1, temp)
        sh.write(idx+1, 2, hum)
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=data.xls"})


if __name__ == '__main__':
    app.run(debug=True)
