'''
blog: BLOG BLUEPRINT

The blog should list all posts, allow logged in users to create posts, and allow the author of a post to edit or delete it.
'''

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# This line below creates a Blueprint named 'blog'. 
# - Like the application object, the blueprint needs to know where it’s defined, so '__name__' is passed as the second argument. 
# - Unlike the 'auth blueprint', the 'blog' blueprint does not have a 'url_prefix'. So the 'index' view function will be at '/', 
#   the 'create' view function at '/create', and so on. The blog is the main feature of Flaskr, so it makes sense that 
#   the blog index will be the main index.
bp = Blueprint('blog', __name__)

#################################################################################################################################
################################################# V I E W   F U N C T I O N S ###################################################
#################################################################################################################################

'''
'/index' view function

The index will show all of the posts, most recent first. A JOIN is used so that the author information 
from the user table is available in the result.

The endpoint for the 'index' view function will be 'blog.index'. 
Some of the authentication view functions referred to a plain 'index endpoint'. 
'app.add_url_rule()' associates the endpoint name 'index' with the '/' url so that 'url_for('index')' or 'url_for('blog.index')' 
will both work, generating the same '/' URL either way.
'
In another application you might give the 'blog' blueprint a 'url_prefix' and define a separate 'index' view function 
in the application factory. Then the 'index' and 'blog.index' endpoints and URLs would be different.
'''
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)



'''
'/create' view function
The 'create' view function works the same as the 'auth' register view function. 
Either the form is displayed, or the posted data is validated and the post is added to the database or an error is shown.
'
The 'login_required' decorator (defined in the '/logout' view function from the 'auth' blueprint) is used on the 'blog' blueprint 
view functions. A user must be logged in to visit these views, otherwise they will be redirected to the login page.
'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')