from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
import re	# the regex module
from flask_bcrypt import Bcrypt   
from flask_app.models import recipe     

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
NAME_REGEX = re.compile('^(/^[A-Za-z]+$/)')

 #CREATE model
class User:
    db = 'recipes'
    def __init__(self, data): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
#CREATE model
    @classmethod
    def register_user(cls, data):
        if not cls.validate_submission(data):
            return False
        data = cls.parsed_data(data)
        query= '''
        Insert INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s)
        ;'''
        #fat model:
        user_id = connectToMySQL(cls.db).query_db(query,data)
        session['user_id'] = user_id
        session['first_name']=  data['first_name']
        return user_id


#READ model
    @classmethod
    def get_all_users(cls):  #To display who you can send messages to
        query = """
        SELECT *
        FROM users
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in result:
            users.append(cls(row))
        return users

    @classmethod
    def get_user_by_id(cls, id):
        data= {'id': id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
        # message.Message.get_all_messages(id) could put in this return or in controller

    @classmethod
    def find_by_email(cls, data):
        query= '''
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;'''
        result =  connectToMySQL(cls.db).query_db(query, data)
        print('_________________', result)
        if result:
            result = cls(result[0])

        return result


    # Validate 
    @staticmethod
    def validate_submission(input):
        is_valid = True
        if len(input['first_name']) < 1:
            flash('name must enter at least 1 characters')
            is_valid = False
        if len(input['last_name']) < 1:
            flash('name must enter at least 1 characters')
            is_valid = False
        if not PASSWORD_REGEX.match(input['password']):
            flash('invalid password')
            is_valid = False
        if input['password'] != input['confirm_password']:
            flash('passwords do not match')
            is_valid = False
        if not EMAIL_REGEX.match(input['email']): 
            flash("Invalid email address!")
            is_valid = False   
        if User.find_by_email(input):
            flash('An account already exists with this email')
            is_valid = False
        return is_valid

        # Check to see if email already in db

    @staticmethod
    def login_user(data):
        user = User.find_by_email(data)
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                return True
        flash('Invalid')
        return False

        
# Make a parse data function.  Takes care of much of the logic in contollers
    @staticmethod
    def parsed_data(data):
        parsed_data={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'].lower(),
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return parsed_data


    