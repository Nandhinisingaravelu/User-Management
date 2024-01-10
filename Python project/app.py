from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)
#MYSQL CONNECTION
app.config["MYSQL_HOST"]="127.0.0.1"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="S@n16042003"
app.config["MYSQL_DB"]="newdb1"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#Loading Home Page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    con.close()
    return render_template("home.html",datas=res)
    
#New User
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into users (NAME,EMAIL,CITY,AGE) values (%s,%s,%s,%s)"
        con.execute(sql,(name,email,city,age))
        mysql.connection.commit()
        con.close()
        flash('User Details Added')        
        return redirect(url_for("home"))
    return render_template("addUsers.html")
#update User
@app.route("/editUser/<string:id>",methods=['GET','POST'])

def editUser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        city=request.form['city']
        age=request.form['age']
        sql="UPDATE users SET NAME=%s,EMAIL=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,email,city,age,id])
        mysql.connection.commit()
        con.close()
        flash('User Detail Updated')
        return redirect(url_for("home"))
    con=mysql.connection.cursor()
        
    sql="select * from users where ID=%s"
    con.execute(sql,id)
    res=con.fetchone()
    con.close()
    return render_template("editUser.html",datas=res)
#Delete User
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted')
    return redirect(url_for("home"))

if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)
