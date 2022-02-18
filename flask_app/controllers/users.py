from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import recipe, user
from flask_app.controllers import recipes
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect(f"dashboard/{session['user_id']}")

@app.route('/login', methods=['POST'])
def login():
    if not user.User.login_user(request.form):
        return redirect('/')
    return redirect(f"/dashboard/{session['user_id']}")  #is session unneccessary here?


@app.route('/register/user', methods=['POST'])
def register():
    user_id = user.User.register_user(request.form)
    if user_id:
        return redirect (f"/dashboard/{session['user_id']}")
    return redirect ('/')

    # user_id = user.User.create_user(request.form)
    # if user_id :
    #     return redirect('/users/home')
    # else:
    #     return redirect('/')

@app.route('/dashboard/<id>')
def home(id):
    recipes = recipe.Recipe.get_all_recipes_by_user_id(id)
    return render_template('dashboard.html', recipes = recipes  )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# @app.route('/show_info', methods=["POST"])
# def display():
#     if not user.User.validate_submission(request.form):
#         return redirect('/')
#     session['name'] = request.form["name"]
#     session['location'] = request.form["location"]
#     session['language'] = request.form['language']
#     session['comments'] = request.form['comments']
#     users.append(session)
#     return redirect ('/information') 

# @app.route('/information')
# def show():
#     return render_template('display.html')

# @app.route('/newsubmit')
# def reset():
#     session.clear()
#     return redirect('/')