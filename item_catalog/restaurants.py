from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True

# import CRUD Operations
from setup import Base, Restaurant, MenuItem, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Authentication & Authorization OAuth
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Catalog"

# Create session and connect to the DB
engine = create_engine('sqlite:///restaurantsdb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create user and get user's info
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Cross-site request forgery (CSRF) prevention
# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print "Invalid state parameter"
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists, if not create a new one
    user_id = getUserID(login_session['email'])
    print "#####################################"
    print "value of user_id is %s" % user_id
    print "#####################################"
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '"style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/logout')
def logout():
    access_token = login_session['credentials']
    print 'The access token is %s' % access_token
    print 'User name is: %s' % login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is %s' % result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON API ENDPOINT (GET REQUEST)
@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItems=menuItem.serialize)

##############################################
################### Routes ###################
##############################################

# Landing page (List all restaurants)
@app.route('/')
@app.route('/restaurants/')
def showRestaurant():
    restaurants = session.query(Restaurant).all()
    if 'username' not in login_session:
        return render_template('public_restaurants.html', restaurants=restaurants)
    else:
        return render_template('restaurants.html', restaurants=restaurants, user=login_session)

# Create a new restaurant
@app.route('/restaurants/new/', methods=['GET','POST'])
def newRestaurant():
	if 'username' not in login_session:
		return render_template('401.html')
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'], description=request.form['description'], logo=request.form['logo'], user_id=login_session['user_id'])
		session.add(newRestaurant)
		session.commit()
		flash("You just added a new restaurant!")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('newrestaurant.html', user=login_session)

# Edit restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	if 'username' not in login_session:
		return render_template('401.html')
	editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editRestaurant.name = request.form['name']
		if request.form['description']:
			editRestaurant.description = request.form['description']
		if request.form['logo']:
			editRestaurant.logo = request.form['logo']
		session.add(editRestaurant)
		session.commit()
		flash("Restaurant's name updated!")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant=editRestaurant, user=login_session)

# Delete restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	if 'username' not in login_session:
		return render_template('401.html')
	deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(deleteRestaurant)
		session.commit()
		flash("Restaurant deleted!")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant=deleteRestaurant, user=login_session)

# List menu items
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:    
        return render_template('public_menu.html', restaurant=restaurant, items=items, user=login_session)
    else:
        return render_template('menu.html', restaurant=restaurant, items=items, creator=creator, user=login_session)

# Create new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if 'username' not in login_session:
		return render_template('401.html')
	if request.method == 'POST':
		newMenuItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id, user_id=login_session['user_id'])
		session.add(newMenuItem)
		session.commit()
		flash("You just added a new menu item!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id, user=login_session)

# Edit menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, item_id):
	if 'username' not in login_session:
		return render_template('401.html')
	editMenuItem = session.query(MenuItem).filter_by(id=item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editMenuItem.name = request.form['name']
		if request.form['description']:
			editMenuItem.description = request.form['description']
		if request.form['price']:
			editMenuItem.price = request.form['price']
		if request.form['course']:
			editMenuItem.course = request.form['course']
		session.add(editMenuItem)
		session.commit()
		flash("Menu item updated!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, item_id=item_id, item=editMenuItem, user=login_session)

# Delete menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, item_id):
	if 'username' not in login_session:
		return render_template('401.html')
	deleteMenuItem = session.query(MenuItem).filter_by(id=item_id).one()
	if request.method == 'POST':
		session.delete(deleteMenuItem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item_id=item_id, item=deleteMenuItem, user=login_session)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)