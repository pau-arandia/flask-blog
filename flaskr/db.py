'''
The application database

The app will use a SQLite database to store users and posts.
Python comes with built-in support for SQLite in the sqlite3 module.

Connecting to the database:
The first thing to do when working with a SQLite database (and most other Python database libraries) is 
to create a connection to it. Any queries and operations are performed using the connection, 
which is closed after the work is finished.

In web applications this connection is typically tied to the request. 
It is created at some point when handling a request, and closed before the response is sent

'''

import sqlite3
import click

# 'g' is a special object that is unique for each request. 
# It is used to store data that might be accessed by multiple functions during the request.
# The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request.

# 'current_app' is another special object that points to the Flask application handling the request.

from flask import current_app, g


def get_db():
    if 'db' not in g:

        # 'sqlite3.connect()' establishes a connection to the file pointed at by the DATABASE configuration key, 
        # which is set in the application factory (create_app() set in __init__.py)
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # 'sqlite3.Row' tells the connection to return rows that behave like dicts. 
        # This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):

    '''
    'close_db()' checks if a connection was created by checking if 'g.db' was set.
    If the connection exists, it is closed.
    '''

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    
    # 'get_db()' returns a database connection, which is used to execute the commands read from the 'schema.sql' file.
    db = get_db()

    # 'open_resource()' opens a file relative to the flaskr package, which is useful since you won’t 
    # necessarily know where that location is when deploying the application later.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    '''
    'click.command()' defines a command line command called 'init-db' that calls the 'init_db()' function 
    and shows a success message to the user.

    With this function, 'init-db' gets registered with the app.
    Hnence, it can be called using the flask command: "flask --app flaskr init-db"

    Running this command will create a 'flaskr.sqlite' file in the /instance directory.
    '''

    # clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    '''
    The 'close_db()' and 'init_db_command()' functions need to be registered with the application instance; 
    otherwise, they will not be used by the application. 
    
    However, since you are using an application factory function ('create_app()' from flaskr/__init__.py), 
    that instance is not available when writing the functions. 

    Instead, this function takes an application and does the registration.
    '''
    
    # 'app.teardown_appcontext()' tells Flask to call 'close_db()' when cleaning up after returning the response.
    app.teardown_appcontext(close_db)

    # 'app.cli.add_command()' adds a new command that can be called with the flask command 'init_db_comand'.
    app.cli.add_command(init_db_command)