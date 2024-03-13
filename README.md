# flask-blog
A blog developed using Flask.

# Notes
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
