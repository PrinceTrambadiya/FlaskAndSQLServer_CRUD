from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc


app = Flask(__name__)

#define the server name and the database name
server = 'DESKTOP-G241BV9'
database = 'Company_PriTram'
#define our connection string
conn = pyodbc.connect( 'DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER=' + server + '; \
                        DATABASE=' + database +';\
                        Trusted_Connection=yes;')

app.secret_key = 'many random bytes'

@app.route('/')
def Index():
    return render_template('home.html')

@app.route('/showAll', methods = ['POST'])
def showAll():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMPLOYEE_PROJECT")
    # for driver in pyodbc.drivers():
    #     print(driver)
    data = cursor.fetchall()
    cursor.close()
    return render_template('showAll.html', employees=data )

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        first = request.form['first']
        middle = request.form['middle']
        last = request.form['last']
        ssn = request.form['ssn']
        bdate = request.form['bdate']
        address = request.form['address']
        sex = request.form['sex']
        salary = request.form['salary']
        superssn = request.form['superssn']
        dno = request.form['dno']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO EMPLOYEE_PROJECT (FNAME, MINIT, LNAME,SSN, BDATE, ADDRESS,SEX, SALARY, SUPERSSN,DNO) VALUES (?,?,?,?,?,?,?,?,?,?)", (first, middle, last,ssn,bdate,address,sex,salary,superssn,dno))
        conn.commit()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    print(id_data)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM EMPLOYEE_PROJECT WHERE id=?", (id_data))
    conn.commit()
    return redirect(url_for('Index'))

@app.route('/search', methods = ['POST'])
def search():
    lastName = request.form['lastName']
    flash("Record Has Been Search Successfully")
    print(lastName)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMPLOYEE_PROJECT WHERE LNAME=?", (lastName))
    data = cursor.fetchall()
    print(data)
    cursor.close()
    return render_template('searchResult.html', employees=data )

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        first = request.form['first']
        middle = request.form['middle']
        last = request.form['last']
        ssn = request.form['ssn']
        bdate = request.form['bdate']
        address = request.form['address']
        sex = request.form['sex']
        salary = request.form['salary']
        superssn = request.form['superssn']
        dno = request.form['dno']
        cursor = conn.cursor()
        cursor.execute("""
               UPDATE EMPLOYEE_PROJECT
               SET FNAME=?, MINIT=?, LNAME=?,SSN=?, BDATE=?, ADDRESS=?,SEX=?, SALARY=?, SUPERSSN=?,DNO=? 
               WHERE id=?
            """, (first, middle, last,ssn,bdate,address,sex,salary,superssn,dno, id_data))
        cursor.execute("SELECT * FROM EMPLOYEE_PROJECT WHERE LNAME=?", (last))
        data = cursor.fetchall()
        flash("Data Updated Successfully")
        conn.commit()
        return render_template('searchResult.html', employees=data )

if __name__ == "__main__":
    app.run(debug=True)
