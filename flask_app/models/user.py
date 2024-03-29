from flask import flash
from flask_app.__init__ import app
from flask_app.models import zine
from flask_app.config.mysqlconnection import connectToMySQL
import re
REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
REGEX_PW_FORM = re.compile(r'\S\w+\d+[!@#$/*]+')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
db = 'zineverse'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.zines = []
        self.comments = []
        self.friends = []

    @classmethod
    def list_friends(cls, id):
        query = 'SELECT * FROM users as usersfriends INNER JOIN friends ON usersfriends.id = friends.friend_id INNER JOIN users ON users.id = friends.user_id WHERE users.id = %(id)s'
        data = {'id':id}
        result = connectToMySQL(db).query_db(query, data)
        leftsided = []
        for each in result:
            leftId = each['id']
            leftsided.append(leftId)
        query = 'SELECT * FROM users as usersfriends INNER JOIN friends on friends.user_id = usersfriends.id INNER JOIN users on users.id = friends.friend_id WHERE users.id = %(id)s'
        result = connectToMySQL(db).query_db(query, data)
        rightside = []
        if result:
            for each in result:
                rightId = each['id']
                rightside.append(rightId)
        currentUser =  cls.getUserById(id)
        onesided = []
        onesideRequested = []
        for each in leftsided:
            if (each in rightside):
                currentUser.friends.append(cls.getUserById(each))
            else: 
                onesided.append(cls.getUserById(each))
        for each in rightside:
            if not (each in leftsided):
                onesideRequested.append(cls.getUserById(each))
        return([currentUser.friends,onesided,onesideRequested])

    # def list_requests(self,cls):
    #     query = 'SELECT * FROM users 
    #     data = {'id': self.id}
    #     result = connectToMySQL(db).query_db(query, data)
    #     list to check = []
    #     for request in result:
    #         cls(request)



# does this work does this add rows redundantly? Should I query first the DB to see if this entry exists.
    def request_friend(self, id):
        validateQuery = 'SELECT * FROM friends WHERE(user_id = %(selfId)s AND friend_id = %(id)s)'
        query = 'INSERT INTO friends (user_id, friend_id) VALUES(%(selfId)s, %(id)s)' 
        # query = 'IF NOT  (SELECT * FROM friends WHERE (user_id = %(selfId)s and friend_id = %(id)s)) BEGIN INSERT INTO friends(user_id, friend_id) VALUES (%(selfId)s,%(id)s)'
        data = {'selfId':self.id, 'id':id}
        duplicate = connectToMySQL(db).query_db(validateQuery,data)
        if not duplicate:
            result = connectToMySQL(db).query_db(query,data)
            return(result)
        else:
            return(None)



    @classmethod
    def getUserByEmail(cls,email):
        query = 'SELECT * FROM users WHERE users.email = %(email)s'
        data = {'email': email}
        result = connectToMySQL(db).query_db(query, data)
        if result:
            return(cls(result[0]))
        else:
            return(False)

    # should return a User object
    @classmethod
    def getUserById (cls,id):
        query = 'SELECT * FROM users WHERE users.id = %(id)s'
        data = {'id': id}
        result = connectToMySQL(db).query_db(query, data)
        return(cls(result[0]))

    @classmethod
    def get_user_with_zines(cls,id):
        query = 'SELECT * FROM users LEFT join collections ON users.id = collections.user_id LEFT JOIN zines ON collections.zine_id = zines.id WHERE users.id = %(id)s'
        data = {'id':id}
        result = connectToMySQL(db).query_db(query, data)
        currentUser = cls(result[0])
        for each in result:
            zine_data = {
                'id': each['zines.id'],
                'title': each['title'],
                'author': each['author'],
                'path': each['path'],
                'description': each['description'],
                'created_at':each['zines.created_at'],
                'updated_at':each['zines.updated_at']
            }
            currentUser.zines.append(zine.Zine(zine_data))
        return(currentUser)

    # pass here from request.form the searchText....i.e the result of the form.
    @classmethod
    def user_search(cls, text):
        data= {'searchText':text}
        query = 'SELECT * FROM users WHERE users.username LIKE %(searchText)s'
        result = connectToMySQL(db).query_db(query,data)
        if result:
            users = []
            for user in result:
                users.append(cls(user))
            return(users)
        else:
            empty = []
            return(empty)
                

    @classmethod
    def insertUser(cls, data):
        query = 'INSERT INTO users (username, email, password) VALUES(%(username)s,%(email)s, %(password)s)'
        data['password']= bcrypt.generate_password_hash(data['password'])
        user = connectToMySQL(db).query_db(query,data)
        return(user)

    @classmethod
    def getall(cls):
        query = 'SELECT * FROM users'
        result = connectToMySQL(db).query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return(users)



# data returns a dictionary from request form
    @staticmethod
    def validate(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        if len(data['username'])< 2:
            flash('username must have more than 2 characters')
            is_valid = False
        if len(data['password']) < 6:
            flash('password must be at least 6 characters long')
            is_valid = False
        if not REGEX_EMAIL.match(data['email']):
            flash('invalid email format')
            is_valid = False
        if not REGEX_PW_FORM.match(data['password']):
            flash('password must not contain spaces and must contain both alpha and numeric characters and at least one ! @ # $, or ? * symbol')
            is_valid = False
        if not data['password'] == data['confirm_password']:
            flash('password and confirm password do not match')
            is_valid = False
        if  User.getUserByEmail(data['email']):
            flash('that email is already registered to another account')
            is_valid = False
        return(is_valid)
        
    @staticmethod
    def validate_login(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        user = User.getUserByEmail(data['email'])
        if user:
            if not bcrypt.check_password_hash(user.password, data['password']):
                flash("THATS IT! YOUR ARE A HACKER AND I AM CALLING THE POLICE THE PASSWORD DOESNT MATCH..or it was just a typo!!!")
                is_valid = False
        else:
            flash('information does not match an existing user')
            is_valid = False
        return(is_valid)
