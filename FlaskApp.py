from flask import Flask, request, redirect, render_template, session
import sqlite3, BookSearch, secrets



# Database Initialisation
# --> users --> users
userCon = sqlite3.connect("users.db")
userCur = userCon.cursor()
userCur.execute('''
    CREATE TABLE IF NOT EXISTS users(
    uuid TEXT NOT NULL,
    username TEXT,
    password TEXT)
''')
userCon.close()

# --> books > books
bookCon = sqlite3.connect("books.db")
bookCur = bookCon.cursor()
bookCur.execute('''
    CREATE TABLE IF NOT EXISTS books(
    bookID INTEGER NOT NULL,
    userID INTEGER,
    FOREIGN KEY(userID) REFERENCES users(uuid))
''')
bookCon.close()



app = Flask(__name__)
app.secret_key = "english_monster"


# route for landing page    ------------    LANDING PAGE
@app.route("/")
def index():

    # check session tokens for username
    if "username" in session:
        return redirect("/main")
    
    # html at  ./templates/index.html
    return render_template("index.html")


# POST method to login
@app.route("/login", methods=["POST"])
def login():
    # recall form data
    username = request.form["username"]
    password = request.form["password"]
    
    #  database connection
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    # query the database
    query = "SELECT * FROM users WHERE username=? and password=?"
    result = cur.execute(query, (username, password)).fetchone()
    con.close()

    # determine account validity
    if result:
        session["username"] = username
        return redirect("/main")

    else:
        return redirect("/")


# POST method to signup
@app.route("/signup", methods=["POST"])
def signup():
    # recall data from HTML form
    username = request.form["username"]
    password = request.form["password"]

    # connect to users database
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    # add user data to database
    query = "INSERT INTO users (uuid, username, password) VALUES (?, ?, ?)"
    cur.execute(query, (secrets.token_hex(16), username, password))

    # close connection
    con.commit()
    con.close()

    # redirect to homepage
    session["username"] = username
    return redirect("/main")
    

# route for homepage    ----------------    HOME PAGE
@app.route("/main", methods=["GET", "POST"])
def main():

    # redirect to lading page if not signed in
    if "username" not in session:
        return redirect("/")
    
    # show book search results
    if request.method == "POST":
        return render_template("home.html", username=session["username"], books = BookSearch.searchBook(request.form["query"]))
    
    # show landing page without search
    return render_template("home.html", username=session["username"])


# POST method to logout
@app.route("/logout", methods=["POST"])
def logout():
    # remove username from session
    session.pop("username", None)
    # redirect back to main page
    return redirect("/")




if __name__ == '__main__':
    app.run(debug=True)
