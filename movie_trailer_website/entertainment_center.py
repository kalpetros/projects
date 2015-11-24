import fresh_tomatoes
import media

# Interstellar movie
interstellar = media.Movie("Interstellar",
						   "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
						   "https://a248.e.akamai.net/f/1682/7219/8m/www.hollywoodreporter.com/sites/default/files/custom/Blog_Images/interstellar3.jpg",
						   "https://www.youtube.com/watch?v=zSWdZVtXT7E",
						   "2014",
						   "Matthew McConaughey, Anne Hathaway, Jessica Chastain")

# Avatar movie
avatar = media.Movie("Avatar",
					 "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
					 "http://www.impawards.com/2009/posters/avatar_xlg.jpg",
					 "https://www.youtube.com/watch?v=5PSNL1qE6VY",
					 "2009",
					 "Sam Worthington, Zoe Saldana, Sigourney Weaver")

# Inception movie
inception = media.Movie("Inception",
				        "A thief who steals corporate secrets through use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
				        "http://www.worstpreviews.com/images/headlines/temp/temp2082.jpg",
				        "https://www.youtube.com/watch?v=8hP9D6kZseM",
				        "2010",
				        "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page")

# The Shawshank Redemption movie
the_shawshank_redemption = media.Movie("The Shawshank Redemption",
				                       "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
				                       "http://images.moviepostershop.com/the-shawshank-redemption-movie-poster-1994-1020191906.jpg",
				                       "https://www.youtube.com/watch?v=6hB3S9bIaco",
				                       "1994",
				                       "Tim Robbins, Morgan Freeman, Bob Gunton")

# Schindler's List movie
schindlers_list = media.Movie("Schindler's List",
				              "In Poland during World War II, Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
				              "https://static1.squarespace.com/static/5126bbb4e4b08c2e6d1cb6e4/t/55b10e2de4b08745c532074d/1437666863110/4075786999_124068d23a_o.jpg",
				              "https://www.youtube.com/watch?v=JdRGC-w9syA",
				              "1993",
				              "Liam Neeson, Ralph Fiennes, Ben Kingsley")

# The Pianist movie
the_pianist = media.Movie("The Pianist",
				          "A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of World War II.",
				          "http://filmonizirani.net/wp-content/uploads/2014/12/the-pianist-poster.jpg",
				          "https://www.youtube.com/watch?v=OL8Qs9hpimk",
				          "2002",
				          "Adrien Brody, Thomas Kretschmann, Frank Finlay")

# Define an empty array
movies = [interstellar, avatar, inception, the_shawshank_redemption, schindlers_list, the_pianist]
fresh_tomatoes.open_movies_page(movies)