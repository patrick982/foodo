import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from datetime import datetime

from helpers import apology, login_required

UPLOAD_FOLDER = '/home/ubuntu/workspace/FinalProject/foodo/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///foodo.db")

@app.route("/")
@login_required
def index():
    """Show Foodo landing page"""
    # show a greeting
    user = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])
    return render_template("index.html", user = user[0]["username"])


@app.route("/recipes")
@login_required
def recipes():
    """Show all recipes"""
    recipes = db.execute("SELECT id, name, description, ingredients, directions, prep_time, cooking_time, tips FROM recipes")
    # create the recipe list to display
    for recipe in recipes:
        recipe_id = recipe["id"]
        name = recipe["name"]
        description = recipe["description"]
        ingredients = recipe["ingredients"]
        directions = recipe["directions"]
        prep_time = recipe["prep_time"]
        cooking_time = recipe["cooking_time"]
        tips = recipe["tips"]

        return render_template("recipes.html", recipes=recipes)

@app.route("/recipes_pizza")
@login_required
def recipes_pizza():
    """Show all pizza recipes"""
    recipes = db.execute("SELECT id, name, description, ingredients, directions, prep_time, cooking_time, tips FROM recipes WHERE name LIKE '%pizza%'")
    # create the recipe list to display
    for recipe in recipes:
        recipe_id = recipe["id"]
        name = recipe["name"]
        description = recipe["description"]
        ingredients = recipe["ingredients"]
        directions = recipe["directions"]
        prep_time = recipe["prep_time"]
        cooking_time = recipe["cooking_time"]
        tips = recipe["tips"]

        return render_template("recipes.html", recipes=recipes)

@app.route("/recipes_pasta")
@login_required
def recipes_pasta():
    """Show all pasta recipes"""
    recipes = db.execute("SELECT id, name, description, ingredients, directions, prep_time, cooking_time, tips FROM recipes WHERE name LIKE '%pasta%'")
    # create the recipe list to display
    for recipe in recipes:
        recipe_id = recipe["id"]
        name = recipe["name"]
        description = recipe["description"]
        ingredients = recipe["ingredients"]
        directions = recipe["directions"]
        prep_time = recipe["prep_time"]
        cooking_time = recipe["cooking_time"]
        tips = recipe["tips"]

        return render_template("recipes.html", recipes=recipes)


@app.route("/recipes_salad")
@login_required
def recipes_salad():
    """Show all pizza recipes"""
    recipes = db.execute("SELECT id, name, description, ingredients, directions, prep_time, cooking_time, tips FROM recipes WHERE name LIKE '%salad%'")
    # create the recipe list to display
    for recipe in recipes:
        recipe_id = recipe["id"]
        name = recipe["name"]
        description = recipe["description"]
        ingredients = recipe["ingredients"]
        directions = recipe["directions"]
        prep_time = recipe["prep_time"]
        cooking_time = recipe["cooking_time"]
        tips = recipe["tips"]

        return render_template("recipes.html", recipes=recipes)


@app.route("/recipe_detail/<recipe_id>")
@login_required
def recipe_detail(recipe_id):
    """Show recipe detail page"""

    recipe_detail = db.execute("SELECT id, name, description, ingredients, directions, prep_time, cooking_time, tips, image FROM recipes WHERE id = :recipe_id", recipe_id=recipe_id)
    # create recipe data fields
    recipe_id = recipe_id
    name = recipe_detail[0]["name"]
    description = recipe_detail[0]["description"]
    ingredients = recipe_detail[0]["ingredients"]
    directions = recipe_detail[0]["directions"]
    prep_time = recipe_detail[0]["prep_time"]
    cooking_time = recipe_detail[0]["cooking_time"]
    tips = recipe_detail[0]["tips"]
    image = recipe_detail[0]["image"]


    return render_template("recipe_detail.html", name=name, description=description, recipe_id=recipe_id,
        image=image, ingredients=ingredients, directions=directions, prep_time=prep_time, cooking_time=cooking_time, tips=tips)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """add recipes to the database"""

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        directions = request.form.get("directions")
        prep_time = int(request.form.get("prep_time"))
        cooking_time = int(request.form.get("cooking_time"))
        tips = request.form.get("tips")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        db.execute("INSERT INTO recipes (user_id, name, description, ingredients, directions, prep_time, cooking_time, tips, image) VALUES (:user_id, :name, :description, :ingredients, :directions, :prep_time, :cooking_time, :tips, :image)",
            user_id=session["user_id"],
            name=name,
            description=description,
            ingredients=ingredients,
            directions=directions,
            prep_time=prep_time,
            cooking_time=cooking_time,
            tips=tips,
            image=filename)

        # insert into Activity log table
        timestamp = datetime.now(tz=None)

        db.execute("INSERT INTO history (user_id, operation, name, datetime) VALUES (:user_id, :operation, :name, :datetime)",
            user_id=session["user_id"],
            operation='add',
            name=name,
            datetime=timestamp)


        flash("recipe added!")

        # this redirect needs to go to index
        return redirect("/")

    else:
        return render_template("add.html")


@app.route("/recipe_edit/<recipe_id>", methods=["GET", "POST"])
@login_required
def recipe_edit(recipe_id):

    """edit existing recipes"""
    recipe = db.execute("SELECT * FROM recipes WHERE id = :recipe_id", recipe_id=recipe_id)

    # prepare data to populate in form
    name = recipe[0]["name"]
    description = recipe[0]["description"]
    ingredients = recipe[0]["ingredients"]
    directions = recipe[0]["directions"]
    prep_time = recipe[0]["prep_time"]
    cooking_time = recipe[0]["cooking_time"]
    tips = recipe[0]["tips"]


    # update data in DB
    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        directions = request.form.get("directions")
        prep_time = int(request.form.get("prep_time"))
        cooking_time = int(request.form.get("cooking_time"))
        tips = request.form.get("tips")

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        db.execute("UPDATE recipes SET name=:name, description=:description, ingredients=:ingredients, directions=:directions, prep_time=:prep_time, cooking_time=:cooking_time, tips=:tips, image=:image WHERE id = :recipe_id",
            recipe_id = recipe_id,
            name=name,
            description=description,
            ingredients=ingredients,
            directions=directions,
            prep_time=prep_time,
            cooking_time=cooking_time,
            tips=tips,
            image=filename)

        # insert into Activity log table
        timestamp = datetime.now(tz=None)

        db.execute("INSERT INTO history (user_id, operation, name, datetime) VALUES (:user_id, :operation, :name, :datetime)",
            user_id=session["user_id"],
            operation='edit',
            name=name,
            datetime=timestamp)

        flash("processed!")

        # this redirect needs to go to index
        return redirect("/recipes")

    else:
        return render_template("recipe_edit.html", recipe_id=recipe_id, name=name, description=description,
        ingredients=ingredients, directions=directions, prep_time=prep_time, cooking_time=cooking_time, tips=tips)


@app.route("/log")
@login_required
def log():
    """Show history of transactions"""

    # bring recipes into list to be able to iterate over it
    logs = db.execute("SELECT id, name, operation, datetime FROM history WHERE user_id = :user_id", user_id=session["user_id"])
    # build the portfolio data, iterate over stocks list
    for log in logs:
        id = log["id"]
        name = log["name"]
        operation = log["operation"]
        log["datetime"] = log["datetime"]

    return render_template("history.html", logs=logs)


@app.route("/add_todo", methods=["GET", "POST"])
@login_required
def add_todo():
    """add recipes to the database"""

    if request.method == "POST":
        item = request.form.get("item")


        db.execute("INSERT INTO todo (user_id, item, status) VALUES (:user_id, :item, :status)",
            user_id=session["user_id"],
            item=item,
            status="unchecked")

        flash("todo added!")

        # this redirect needs to go to index
        return redirect("/todo")

    else:
        return render_template("add_todo.html")


@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    """Show all todos"""
    todos = db.execute("SELECT id, item, user_id, status FROM todo")

    if request.method == "POST":
        # update the status in DB
        todo_id = request.form.get("delete")
        print(todo_id)

        db.execute("DELETE FROM todo WHERE id = :todo_id",
            todo_id=todo_id)

        return redirect("/todo")

    else:
        # create the recipe list to display
        for todo in todos:
            id = todo["id"]
            item = todo["item"]
            user_id = todo["user_id"]
            status = todo["status"]

        print("test")

        return render_template("todo.html", todos=todos)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

      # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password is confirmed
        elif not request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Ensure passwords do match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        username = request.form.get("username")

        # Query username already exists
        user = db.execute("SELECT * FROM users")
        index = 0
        exists = 0
        for row in user:
            if user[index]["username"] == request.form.get("username"):
                exists = 1
                return apology("user already exists", 403)
            else:
                index += 1

        # if user does not exist, insert into DB
        if not exists:
            pwd = generate_password_hash(request.form.get("confirmation")) #generate hash
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", request.form.get("username"), pwd)


        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
