import webbrowser

class Movie():
	def __init__(self ,movie_title, movie_storyline, poster_image, trailer_youtube, movie_release_year, movie_stars):
		self.title = movie_title
		self.storyline = movie_storyline
		self.poster_image_url = poster_image
		self.trailer_youtube_url = trailer_youtube
		self.release_year = movie_release_year
		self.starring = movie_stars

	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)