from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from setup import Restaurant, Base, MenuItem, User
 
engine = create_engine('sqlite:///restaurants.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Dummy Dumm", email="dummyemail@dummyprovider.com", picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#Menu for Gourmet Burger
restaurant1 = Restaurant(user_id=1, name = "Gourmet Burger", logo = "http://cdn.tastecard.co.uk/tasteblog/wp-content/uploads/2012/10/GBK_Logo.jpg", description = "At GBK we say tomorrow\'s burger can always be better, so we spend a lot of time making mess in the kitchen and trying out new ideas. Like all pioneers, though, from time to time we don\'t get it quite right. It happens, okay? Here, we dig through the archives to relive the burgers we\'d really rather forget.")

session.add(restaurant1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$7.50", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "French Fries", description = "with garlic and parmesan", price = "$2.99", course = "Appetizer", restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chicken Burger", description = "Juicy grilled chicken patty with tomato mayo and lettuce", price = "$5.50", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Chocolate Cake", description = "fresh baked and served with ice cream", price = "$3.99", course = "Dessert", restaurant = restaurant1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Sirloin Burger", description = "Made with grade A beef", price = "$7.99", course = "Entree", restaurant = restaurant1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Root Beer", description = "16oz of refreshing goodness", price = "$1.99", course = "Beverage", restaurant = restaurant1)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1, name = "Iced Tea", description = "with Lemon", price = "$.99", course = "Beverage", restaurant = restaurant1)

session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(user_id=1, name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", price = "$3.49", course = "Entree", restaurant = restaurant1)

session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(user_id=1, name = "Veggie Burger", description = "Made with freshest of ingredients and home grown spices", price = "$5.99", course = "Entree", restaurant = restaurant1)

session.add(menuItem8)
session.commit()

#Menu for Rise & Shine
restaurant2 = Restaurant(user_id=1, name = "Rise & Shine", logo = "http://storage.designcrowd.com/design_img/680926/438499/438499_4246564_680926_thumbnail.jpg", description = "At Rise & Shine we say tomorrow\'s steak can always be better, so we spend a lot of time making mess in the kitchen and trying out new ideas. Like all pioneers, though, from time to time we don\'t get it quite right. It happens, okay? Here, we dig through the archives to relive the steak we\'d really rather forget.")

session.add(restaurant2)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Chicken Stir Fry", description = "With your choice of noodles vegetables and sauces", price = "$7.99", course = "Entree", restaurant = restaurant2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Peking Duck", description = " A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", price = "$25", course = "Entree", restaurant = restaurant2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Spicy Tuna Roll", description = "Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ", price = "15", course = "Entree", restaurant = restaurant2)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Nepali Momo ", description = "Steamed dumplings made with vegetables, spices and meat. ", price = "12", course = "Entree", restaurant = restaurant2)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Beef Noodle Soup", description = "A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.", price = "14", course = "Entree", restaurant = restaurant2)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1, name = "Ramen", description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", price = "12", course = "Entree", restaurant = restaurant2)

session.add(menuItem6)
session.commit()

#Menu for Mowgli's
restaurant1 = Restaurant(user_id=1, name = "Mowgli\'s", logo = "http://brandnucreative.co.uk/wp-content/uploads/2013/10/mowglis-indian-logo.jpg", description = "At Mowgli\'s' we say tomorrow\'s curry can always be better, so we spend a lot of time making mess in the kitchen and trying out new ideas. Like all pioneers, though, from time to time we don\'t get it quite right. It happens, okay? Here, we dig through the archives to relive the curry we\'d really rather forget.")

session.add(restaurant1)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Pho", description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", price = "$8.99", course = "Entree", restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chinese Dumplings", description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", price = "$6.99", course = "Appetizer", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Gyoza", description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", price = "$9.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", price = "$6.99", course = "Entree", restaurant = restaurant1)

session.add(menuItem4)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$9.50", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

#Menu for Ashley's
restaurant1 = Restaurant(user_id=1, name = "Ashley\'s", logo = "https://s3.amazonaws.com/midnight-merchant-assets/images/logos/300x300/ashleys_logo_300x300.png", description = "At Ashley\'s we say tomorrow\'s spaghetti can always be better, so we spend a lot of time making mess in the kitchen and trying out new ideas. Like all pioneers, though, from time to time we don\'t get it quite right. It happens, okay? Here, we dig through the archives to relive the spaghetti we\'d really rather forget.")

session.add(restaurant1)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Tres Leches Cake", description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", price = "$2.99", course = "Dessert", restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", price = "$5.99", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", price = "$4.50", course = "Dessert", restaurant = restaurant1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Cauliflower Manchurian", description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", price = "$6.95", course = "Appetizer", restaurant = restaurant1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Aloo Gobi Burrito", description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", price = "$7.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem5)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$6.80", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

#Menu for Fanajeen
restaurant1 = Restaurant(user_id=1, name = "Fanajeen", logo = "http://storage.designcrowd.com/design_img/300918/82247/82247_3268921_300918_thumbnail.jpg", description = "At Fanajeen we say tomorrow\'s tonkatsu can always be better, so we spend a lot of time making mess in the kitchen and trying out new ideas. Like all pioneers, though, from time to time we don\'t get it quite right. It happens, okay? Here, we dig through the archives to relive the tonkatsu we\'d really rather forget.")

session.add(restaurant1)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Shellfish Tower", description = "Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower", price = "$13.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chicken and Rice", description = "Chicken... and rice", price = "$4.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Mom's Spaghetti", description = "Spaghetti with some incredible tomato sauce made by mom", price = "$6.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "Milk, cream, salt, ..., Liquid nitrogen magic", price = "$3.95", course = "Dessert", restaurant = restaurant1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Tonkatsu Ramen", description = "Noodles in a delicious pork-based broth with a soft-boiled egg", price = "$7.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem5)
session.commit()

#Menu for The Noble East
restaurant1 = Restaurant(user_id=1, name = "The Noble East", logo = "http://storage.designcrowd.com/design_img/680926/438499/438499_4246564_680926_thumbnail.jpg", description = "At The Noble East we say tomorrow\'s chicken marsala can always be better, so we spend a lot of time making mess in the kitchen and trying out new ideas. Like all pioneers, though, from time to time we don\'t get it quite right. It happens, okay? Here, we dig through the archives to relive the chicken marsala we\'d really rather forget.")

session.add(restaurant1)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Lamb Curry", description = "Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.", price = "$9.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", price = "$7.95", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", price = "$6.50", course = "Appetizer", restaurant = restaurant1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Nigiri Sampler", description = "Maguro, Sake, Hamachi, Unagi, Uni, TORO!", price = "$6.75", course = "Appetizer", restaurant = restaurant1)

session.add(menuItem4)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$7.00", course = "Entree", restaurant = restaurant1)

session.add(menuItem2)
session.commit()

print "added menu items!"