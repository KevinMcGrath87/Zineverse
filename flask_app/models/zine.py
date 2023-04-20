import sys
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = 'zineverse'
class Zine:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        #file path will be used to open zines...file system for zines.
        self.path = data['path']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []
        # need method to find all zines..

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM zines'
        result = connectToMySQL(db).query_db(query)
        zines = []
        for zine in result:
            zines.append(cls(zine))
        return(zines)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO zineverse.zines(title, author,path, description, created_at, updated_at) VALUES(%(title)s, %(author)s,%(path)s, %(description)s, NOW(),NOW())"
        result =connectToMySQL(db).query_db(query,data)
        # previous query should return the zine id
        # query to get zine id? query to get user id
        data['zineid']=result
        query = "INSERT INTO zineverse.collections(zine_id, user_id) VALUES (%(zineid)s,%(user)s)"
        result = connectToMySQL(db).query_db(query,data)
        return(result)

# data for this query should be a dict with key value id:<some int> comes form controller?
# consider making objects from dictionary data that is returned.
    @classmethod
    def get_by_id(cls,id):
        data = {'id':id}
        query = "SELECT * FROM zineverse.zines WHERE zines.id = %(id)s "
        result =connectToMySQL(db).query_db(query,data)
        return(result)

    @classmethod
    def get_by_user(cls, id):
        query = 'SELECT * FROM users LEFT JOIN collections ON users.id = collections.user_id LEFT JOIN zines ON collections.zine_id = zines.id WHERE users.id = %(id)s'
        data = {'id':id}
        result = connectToMySQL(db).query_db(query,data)
        currentUser = user.User(result[0])
        zines = [];
        for zine in result:
            zines.append(cls(zine))
        for zine in zines:
            currentUser.zines.append(zine)
        return zines

    @classmethod
    def update_zine(cls, data):
        query = 'UPDATE zines SET title = %(title)s, author = %(author)s, description = %(description)s, path = %(path)s WHERE zines.id = %(id)s'
        result = connectToMySQL(db).query_db(query, data)
        return(result)

    @classmethod
    def delete_zine(cls, id):
        query = "DELETE FROM collections WHERE collections.zine_id = %(id)s"
        data = {'id':id}
        result = connectToMySQL(db).query_db(query,data)
        query = "DELETE  from zines WHERE zines.id = %(id)s"
        data = {'id':id}
        result = connectToMySQL(db).query_db(query,data)
        return(result)


    @classmethod
    def get_zine(cls, id):
        query = 'SELECT path, title FROM zines WHERE zines.id = %(id)s'
        data = {'id':id}
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate_zine(data,id):
        is_valid = True
        zineList = Zine.get_by_user(id)
        for zine in zineList:
            if data['title']== zine.title and data['author']== zine.author:
                flash('zine already in database')
                is_valid = False
            if not data['description']:
                flash("cannot have empty description")
                is_valid = False
            if not data['title']:
                flash('cannot have empty title')
                is_valid = False
            if not data['author']:
                flash('cannot have empty author')
                is_valid = False
        return(is_valid)


