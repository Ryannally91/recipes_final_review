from dataclasses import dataclass
from email import message
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import recipe, user
from flask_app.controllers import users

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/recipes/new')
def new_recipes_page():
    return render_template('new_recipe.html')


@app.route('/recipes/create_recipe', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return render_template('index.html')
    if recipe.Recipe.create_recipe(request.form):
        return redirect (f"/dashboard/{session['user_id']}")
    return redirect ('/recipes/new')

@app.route('/recipes/<id>')
def view_instructions(id):
    return render_template('view_instructions.html', recipe = recipe.Recipe.get_recipe_by_id(id))

@app.route('/recipes/edit/<id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return render_template('index.html')
    return render_template('edit.html', recipe = recipe.Recipe.get_recipe_by_id(id))

@app.route('/update/recipe', methods= ['POST'])
def update():
    if recipe.Recipe.validate_recipe(request.form):
        recipe.Recipe.update_recipe(request.form)
        return redirect (f"/dashboard/{session['user_id']}")
    return redirect(f"/recipes/edit/{request.form['id']}")


@app.route('/recipes/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return render_template('index.html')
    recipe.Recipe.delete_recipe(id)
    return redirect (f"/dashboard/{session['user_id']}")