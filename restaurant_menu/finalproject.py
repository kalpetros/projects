from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# import CRUD Operations
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to the DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
	return render_template('restaurants.html', restaurants=restaurants)

# Create a new restaurant
@app.route('/restaurants/new/', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("You just added a new restaurant!")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('newrestaurant.html')

# Edit restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editRestaurant.name = request.form['name']
		session.add(editRestaurant)
		session.commit()
		flash("Restaurant's name updated!")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant=editRestaurant)

# Delete restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(deleteRestaurant)
		session.commit()
		flash("Restaurant deleted!")
		return redirect(url_for('showRestaurant'))
	else:
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant=deleteRestaurant)

# List menu items
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	return render_template('menu.html', restaurant=restaurant, items=items)

# Create new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newMenuItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newMenuItem)
		session.commit()
		flash("You just added a new menu item!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, item_id):
	editMenuItem = session.query(MenuItem).filter_by(id=item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editMenuItem.name = request.form['name']
			editMenuItem.description = request.form['description']
			editMenuItem.price = request.form['price']
			editMenuItem.course = request.form['course']
		session.add(editMenuItem)
		session.commit()
		flash("Menu item updated!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, item_id=item_id, item=editMenuItem)

# Delete menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, item_id):
	deleteMenuItem = session.query(MenuItem).filter_by(id=item_id).one()
	if request.method == 'POST':
		session.delete(deleteMenuItem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item_id=item_id, item=deleteMenuItem)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
