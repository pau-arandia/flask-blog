# flask-blog
A blog developed using Flask.

## `url_for()`, View Functions and Endpoints
The `url_for()` function generates the URL to a view based on a name and arguments. The name associated with a view function is also called the endpoint, and by default it’s the same as the name of the view function.

For example, take the following `hello()` view function:

```python
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

@app.route('/hello')
def hello():
    return 'Hello, World!'
```

This view function is named `hello` and can be linked to with `url_for('hello')`. 
If it took an argument, it would be linked to using `url_for('hello', who='World')`.

When using a blueprint, the name of the blueprint is prepended to the name of the function. 
Take this blueprint called `auth` as an example:

```python
from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():

    # ... function code ...

    return render_template('auth/login.html')
```

The endpoint for the `login()` function is `auth.login` because it is added to the `auth` blueprint.


## HTML Templates
Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates through the `render_template()` function that the view functions call.

This application uses templates to render HTML which will display in the user’s browser. In Flask, Jinja is configured to autoescape any data that is rendered in HTML templates. This means that it’s safe to render user input; any characters they’ve entered that could mess with the HTML, such as `<` and `>` will be escaped with safe values that look the same in the browser but don’t cause unwanted effects.

Jinja looks and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. 

* Anything between `{{` and `}}` is an expression that will be output to the final document. 
* `{%` and `%}` denotes a control flow statement like if and for. 
* Unlike Python, blocks are denoted by start and end tags rather than indentation since static text within a block could change indentation.
