from uagame import Window
from pygame.time import Clock, get_ticks
from pygame.event import get as get_events
from pygame import QUIT, MOUSEBUTTONUP, Color, init as start_clock
from pygame.draw import circle as draw_circle
from random import randint
import numpy as np

# version 1 of Poke the dots. This version only displays two dots moving endlessly


def main() :
	game = Game()
	game.play_game()
	
		

	
class Game :
	# object of class Game represents a complete game
	# - window
	# - frame_rate
	# - close_selected
	# - clock
	# - small_dot
	# - big_dot
	def __init__(self) :
		# window -> Game object
		self._window = Game._create_window()
		self._adjust_window()
		self.clock = Clock()
		self.close_selected = False
		self.frame_rate = 90
		self.score = 0
		self.small_dot = Dot( self._window, 'red', [100,200], 30, [1,2])
		self.big_dot = Dot( self._window, 'blue', [200,100], 40, [2,1])
		self.small_dot.randomize_dot( )
		self.big_dot.randomize_dot( )

	def _create_window() :	# return a window object
		#	return window
		window = Window( "Poke the Dots", 500, 400 )
		window.set_bg_color( "black")
		return window

	def _adjust_window( self ) :
		self._window.set_font_name( 'ariel')
		self._window.set_font_size( 64 )
		self._window.set_font_color( 'white')


	def draw_score( self ) :
		score = "Score: " + str( self.score )
		self._window.draw_string(  score , 0, 0 )

	# continuously update the frame while checking if user has clicked the close button
	def play_game(self) :
		self.close_selected = False
		start_clock()	# then, get_ticks() reports elapsed time in milliseconds
		while not self.close_selected :
			self.play_frame()	# understood to affect self.close_selected
		self._window.close()

	# draws the dots and updates their positions. Returns the user action as True/False (True if Quit)
	def play_frame(self ) :
		self.handle_events()
		self.draw_game()
		self.update_game()
	
	# draw dots and refresh display
	def draw_game(self) :
		self._window.clear()
		self.draw_score(  )
		self.small_dot.draw_dot( )
		self.big_dot.draw_dot( )
		self._window.update()

	# return True only if one of the queued events is the user clicking the close button
	def handle_events(self) :
		closed = False
		event_list = get_events()
		for event in event_list :
			if QUIT == event.type :
				closed = True
			elif MOUSEBUTTONUP == event.type :
				self.handle_mouse_up(  )
		self.close_selected = closed
	
	# updates the positions of the dots (doesn't actually move them	and sets display refresh reate
	def update_game(self) :
		self.small_dot.move_dot( )
		self.big_dot.move_dot( )
		# control frame rate
		self.clock.tick(self.frame_rate)
		self.score = get_ticks() // 1000

	def handle_mouse_up( self ) :
		# this makes handle events more readable and maintainable
			 self.small_dot.randomize_dot()
			 self.big_dot.randomize_dot()

	def check_collision( dot1, dot2 ) :
		""" return True if distance between centers < sum of radii """
		# which is same as if sqare of distance < sqare of (sum of ..) :)
		c1 = dot1.get_center()
		c2 = dot2.get_center()
		r1 = dot1.get_radius()
		r2 = dot2.get_radius()
		if ( c1[0] - c2[0] )**2 + ( c1[1] - c2[1] )**2 < (r1 + r2)**2 :
			return True
		else :
			return False
	
	
class Dot :
	# encapsulates the Dot that the game moves around the screen
	# - window
	# - center
	# - radius
	# - velocity
	# - color
	def __init__(self, window, color, center, radius, velocity ) :
		self._window = window
		self._color = color
		self._radius = radius
		self._center = np.array( center )
		self._velocity = np.array( velocity )
		
# from https://scipython.com/blog/two-dimensional-collisions/
	def intersects( self, other ) :
		return np.hypot( *(self._center - other._center ) ) < self.radius + other.radius

	def randomize_dot( self ) :
		# given a dot object, use window height and width and radius to set the
		# center's coordinates to random values
		self._center[0] = randint( self._radius, self._window.get_width() - self._radius )
		self._center[1] = randint( self._radius, self._window.get_height() - self._radius )
	
	# poor name. This does not actually move anything but updates the center of the specified dot
	def move_dot(self ) :	# side affects velocity
		# for i in velocity index list
		# add velocity to center index
		# if the edge of the dot is outside the window, then negate the velocity of the corresponding index
		# wipeout the existing dot by drawing the circle in bgcolor - the duh way, or just use window.clear :)
	
		size = ( self._window.get_width(), self._window.get_height() )

		for index in range(2) :
			self._center[index] += self._velocity[index]
			if self._center[index] - self._radius < 0 or self._center[index] + self._radius > size[index] :
				self._velocity[index] = -self._velocity[index]
	
	# draw a filled circle at specified loction with size/color
	def draw_dot( self ) :
		surface = self._window.get_surface()
		color = Color( self._color )
		draw_circle( surface, color, self._center, self._radius )
		
# from https://scipython.com/blog/two-dimensional-collisions/
	def change_velocities(p1, p2):
		"""
		Dots p1 and p2 have collided elastically: update their
		velocities.
		"""

#		m1, m2 = p1._radius**2, p2._radius**2 	# assuming discs
		m1, m2 = p1._radius**3, p2._radius**3 	# assuming spheres
		
		M = m1 + m2
		r1, r2 = p1._radius, p2._radius
		d = np.linalg.norm(r1 - r2)**2
		v1, v2 = p1._velocity, p2._velocity
		u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
		u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
		p1._velocity = u1
		p2._velocity = u2



# start the program running
main()
