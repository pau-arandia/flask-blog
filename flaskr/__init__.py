'''
The '__init__' file

This file serves double duty: 
* it will contain the application factory
* it tells Python that the flaskr directory should be treated as a package

The __init__.py file is a special file placed within directories that Python interprets as packages. 
Its presence allows Python to recognize the directory as a package, enabling the import of modules and sub-packages.

TESTING
Set environment variables for testing:
    While on root directory (/flask-blog)> set FLASK_APP=flaskr\__init__.py
    
    This is equivalent to telling Flask where to find the application

    
Run the Flask app in debug mode:
    While on root directory (/flask-blog)> flask run --debug

'''


import os
from flask import Flask


def create_app(test_config=None):

    '''
    create_app()

    This function is known as the 'application factory'. 
    Any configuration, registration, and other setup the application needs 
    will happen inside the function, then the application will be returned.

    '''

    # create and configure the app by creating a Flask instance called 'app'
    app = Flask(__name__, instance_relative_config=True)

    # set some default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:

        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:

        # load the test config if passed in
        app.config.from_mapping(test_config)


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app