from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app import app
import re, math
from datetime import datetime
from flask_app.models import user

class Recipe:
    db = 'recipes'
    def __init__(self, data): 
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']#should change to sender (it will have all the info)
        self.cook_date = data['cook_date']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#notice that timestamp is an instance method, not a class
    def timestamp(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    #CREATE
    @classmethod
    def create_recipe(cls, data):
        print(cls.validate_recipe(data))
        if not cls.validate_recipe(data):
            return False
        query='''
        INSERT INTO recipes (name, description, instructions, cook_date, under_30, user_id)
        VALUES (%(name)s,%(description)s,%(instructions)s, %(cook_date)s, %(under_30)s, %(user_id)s);''' # will need hidden input with recipient id when sending recipe
        print('nade it')
        return connectToMySQL(cls.db).query_db(query,data)

    #READ
    @classmethod
    def get_all_recipes_by_user_id(cls, id):
        data= {'id' : id}
        query='''SELECT *
            FROM recipes
            LEFT JOIN users on users.id = recipes.user_id
            WHERE users.id = %(id)s;'''  

        result= connectToMySQL(cls.db).query_db(query, data)
        if result:
            recipes=[]
            for m in result:
                one_recipe = cls(m)
                recipes.append(one_recipe)
            return recipes
        return result
            # The below is not need because of how query is worded, ex users."first_names as sender"
        #     instance_of_recipient = {
        #         "id": m['users.id'],  #also just be users.id?
        #         "first_name": m['first_name'],
        #         "last_name": m['last_name'],
        #         "email" : m['email'],
        #         "password" : m['password'],
        #         "created_at": m['users.created_at'],
        #         "updated_at": m['users.updated_at'],
        #     }
        #     recipient = user.User(instance_of_recipient)
            
        #     one_recipe.recipient = recipient #set to recipient object
        #     one_recipe.sender =sender 
            #Instanse of user (recipient) and append recipe to them, set = to recipe.sender

    @classmethod
    def get_recipe_by_id(cls, id):
        data = {'id': id}
        query='''SELECT *
            FROM recipes
            WHERE id = %(id)s;''' 

        result= connectToMySQL(cls.db).query_db(query, data)
        this_recipe = cls(result[0])   #dont't forget cls here
        print(this_recipe)
        return this_recipe
#Update
    @classmethod
    def update_recipe(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cook_date = %(cook_date)s
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result

    @classmethod
    def delete_recipe(cls, id):
        data ={ "id" : id}
        print('here')
        query= '''
        DELETE FROM recipes
        WHERE id = %(id)s
        ;'''
        print('made it')
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('name must more than 3 characters','recipe')
        if len(data['name']) < 3:
            flash('name must more than 3 characters','recipe')
            is_valid = False
        if len(data['description']) < 3:
            flash('name must more than 3 characters','recipe')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('name must more than 10 characters','recipe')
            is_valid = False
        if data['cook_date'] == '': #not boolean, must compre to empty string to validate
            flash('must enter date', 'recipe') 
            is_valid = False
        # if data['under_30'] == '':
        #     flash('must enter yes or no for under 30','recipe')
        #     is_valid = False
        return is_valid
            