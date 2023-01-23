from flask_app.__init__ import app
from flask_app.controllers import zines, users


if __name__=='__main__':
    app.run(debug = True)
