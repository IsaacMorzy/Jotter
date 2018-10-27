# a simple demo about visit0r-count using django sessions.
# django uses a cookie containing a special session id to identify each browser and its associated session
# with the site.
# actual session data is stored in the site databse by default(more secure than storing data in a cookie)
# you can configure django to store the data in other places(caches, files, cookies)...but default
# is recommended

# you can access the session attribute in the view from the request parameter. An HttpRequest is passed
# in as first argument to the view.
# the session attribute is a dictionary-like object that you can read and write as many times as you like
# in your view.

import django
from django.http import request

# get a session value by its key ('my_car') raising a key error if key not present
my_car = request.session['my_car']

# get a session value, setting a default if it is not present
my_car = request.session.get('my_car', 'mini')

# set a session value
request.session['my_car'] = 'mini'

# delete a session value
del request.session['my_car']

# ------saving session data--------
# django only saves session to db and sends the session cookie to the client when the session has 
# been modified(assigned) or deleted.
request.session['my_car'] = 'mini' # detected as an update to the session so session data is saved



















