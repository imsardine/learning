from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    return 'Profile of the user. (ID: %s)' % user_id

@app.route('/image/<path:locator>/view')
def view_image(locator):
    # 'path' converter can be used in the middle of the URL rule.
    # Visit http://127.0.0.1:5000/image/path/to/image.jpg/view
    return 'Here is the content of image (%s).' % locator

@app.errorhandler(404)
def page_not_found(error):
    # Visit http://127.0.0.1:5000 will see 'Oops!'
    return render_template('page_not_found.html'), 404

# To test routings, run python -i routing.py
#
# >>> with app.test_request_context():
# ...     print url_for('profile', user_id=999)
# ...
# /profile/999

