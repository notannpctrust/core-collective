from flask import Flask, render_template,redirect,abort,request,url_for,flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user,UserMixin    


import pymysql

from dynaconf import Dynaconf

app = Flask(__name__)



config = Dynaconf(settings_file = [ "settings.toml" ])

app.secret_key = config.secret_key

login_manager = LoginManager(app)
login_manager.login_view = '/login'

def connect_db():
    conn = pymysql.connect(
        host= "db.steamcenter.tech",
        user= "cbrown2",
        password= config.password,
        database="cbrown2_Core_Collective",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )  

    return conn


@app.route("/")
def index():
    return render_template("homepage.html.jinja")


@app.route("/browse")
def browse():
    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `Product`")

    result = cursor.fetchall()

    connection.close()
    return render_template("browse.html.jinja",products=result)



@app.route("/product/<product_id>")
def product_page(product_id):
    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `Product` WHERE `ID` = %s", ( product_id ) )


    result = cursor.fetchone()

    connection.close()

    if result is None:
        abort(404)

    return render_template("product.html.jinja", product=result)




@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        connection =connect_db()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM  User WHERE email = %s",(email))

        result = cursor.fetchone()


        connection.close()

        if result is None:
            flash("No User found")
        elif password != result["Password"]:
            flash("Incorrect password")
        else:login_user(User (result))
        return redirect ("/browse")

    return render_template("login.html.jinja")

if __name__ == "main":
    app.run(debug=True)



@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect("/")




@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



