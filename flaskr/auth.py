'''
auth: AUTHENTICATION BLUEPRINT

It will have views to register new users and to log in and log out.
'''

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# This line below creates a Blueprint named 'auth'. 
# - Like the application object, the blueprint needs to know where it’s defined, so '__name__' is passed as the second argument. 
# - The 'url_prefix' will be prepended to all the URLs associated with the 'auth' blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')


#################################################################################################################################
################################################# V I E W   F U N C T I O N S ###################################################
#################################################################################################################################

'''
'/register' view function

When the user visits the '/auth/register' URL, the register view function will return HTML with a form for them to fill out. 
When they submit the form, it will validate their input and either show the form again with an error message or 
create the new user and go to the login page.

'@bp.route' associates the URL '/register' with the register view function. 
When Flask receives a request to '/auth/register', it will call the register view function and use the return value as the response.
'''
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':

        # 'request.form' is a special type of dict mapping submitted from keys and values
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        

        ### VALIDATION ###
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # 'db.execute' takes a SQL query with ? placeholders for any user input, and a tuple of values 
                # to replace the placeholders with.

                # For security, passwords should never be stored in the database directly. 
                # Instead, 'generate_password_hash()' is used to securely hash the password, and that hash is stored. 
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )

                # Since this query modifies data, 'db.commit()' needs to be called afterwards to save the changes.
                db.commit()

            # 'sqlite3.IntegrityError' will occur if the username already exists
            except db.IntegrityError:
                error = f"User '{username}' is already registered."
            else:
                # After storing the username, the user is redirected to the login page. 
                # 'url_for()' generates the URL for the login view function based on the user's username. 
                # This is preferable to writing the URL directly as it allows you to change the URL later 
                # without changing all code that links to it. 
                
                # 'redirect()' generates a redirect response to the URL generated in 'url_for()'.
                return redirect(url_for("auth.login"))


        # If validation fails, the error is shown to the user. 
        # 'flash()' stores messages that can be retrieved when rendering the template.
        flash(error)


    # 'render_template()' will render a template containing the HTML.
    return render_template('auth/register.html')



'''
'/login' view function

When the user visits the '/auth/login' URL, the login view function will return HTML with a form for them to fill out. 
When they submit the form, it will validate their input and either show the form again with an error message or, if the
login is successfull, admit the user into the page.

'@bp.route' associates the URL '/login' with the login view function. 
When Flask receives a request to '/auth/login', it will call the login view function and use the return value as the response.
'''
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        # 'request.form' is a special type of dict mapping submitted from keys and values
        username = request.form['username']
        password = request.form['password']
        db = get_db()


        # The user is queried first and stored in a variable for later use.
        # 'fetchone()' returns one row from the query. If the query returned no results, it returns None. 
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()


        ### VALIDATION ###
        error = None

        if user is None:
            error = 'Incorrect username.'
        
        # 'check_password_hash()' hashes the submitted password in the same way as the stored hash 
        # and securely compares them. If they match, the password is valid.
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:

            # 'session' is a dict that stores data across requests. 
            # When validation succeeds, the user’s id is stored in a new session. 
            # The data is stored in a cookie that is sent to the browser, and the browser then sends it back 
            # with subsequent requests. Flask securely signs the data so that it can’t be tampered with.
            session.clear()
            session['user_id'] = user['id']

            # Now that the user’s id is stored in the session, it will be available on subsequent requests. 
            # At the beginning of each request, if a user is logged in their information should be loaded 
            # and made available to other view functions.


            # 'url_for()' generates the URL that returns the user to the 'index' page.
            # 'redirect()' generates a redirect response to the URL generated in 'url_for()'.
            return redirect(url_for('index'))


        # If validation fails, the error is shown to the user. 
        # 'flash()' stores messages that can be retrieved when rendering the template.
        flash(error)


    # 'render_template()' will render a template containing the HTML.
    return render_template('auth/login.html')



'''
'bp.before_app_request()' registers a function that runs before the view function, 
no matter what URL is requested (notice that no endpoint was provided as argument).
'''
@bp.before_app_request
def load_logged_in_user():
    '''
    'load_logged_in_user' checks if a user id is stored in the session and gets that user’s data from the database, 
    storing it on g.user, which lasts for the length of the request. If there is no user id, or if the id does not exist, 
    g.user will be None.
    '''

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        # The user_id is queried first and stored in a variable for later use.
        # 'fetchone()' returns one row from the query. If the query returned no results, it returns None. 
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()



'''
'/logout view function'
'''
@bp.route('/logout')
def logout():

    '''
    To log out, it is required to remove the user id from the session. 
    Then, 'load_logged_in_user' will not load a user on subsequent requests.
    '''

    session.clear()

    # 'url_for()' generates the URL that returns the user to the 'index' page.
    # 'redirect()' generates a redirect response to the URL generated in 'url_for()'.
    return redirect(url_for('index'))


def login_required(view):
    '''
    Creating, editing, and deleting blog posts will require a user to be logged in. 
    A decorator can be used to check this for each view function it is applied to.

    This decorator returns a new view function that wraps the original view function it is applied to.

    'login_required()' function checks if a user is loaded and redirects to the login page otherwise. 
    If a user is loaded the original view is called and continues normally.
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view