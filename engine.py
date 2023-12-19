##Tester for the screen display
##Must have a sonar
##  Header must be big enough to feel gestalt with rotation speed
##Must have a depth gauge

##Only update vessel tracking for those subs on the same depth zone as the player
##	Creates isolation like you're actually underwater

from os import system
from Vessel import *
import pygame
pygame.init()
system('cls')

##Setup the pygame screen and functions
SCREEN_DIMENSIONS=[SCREEN_WIDTH, SCREEN_HEIGHT]=[500,600]
screen=pygame.display.set_mode(SCREEN_DIMENSIONS)
tick=pygame.display.flip
draw=pygame.draw
drawSurf=pygame.Surface
clock=pygame.time.Clock()
SPAWN_VESSEL=pygame.USEREVENT+1
SPAWN_TIME_MSECONDS=2000
pygame.time.set_timer(SPAWN_VESSEL,SPAWN_TIME_MSECONDS)
vessel_generator=Vessel()
ships=[]
snipers=[]
subs=[]
vessels={'sh':ships,'sn':snipers,'su':subs}

##Trigger function for SPAWN_VESSEL
##Random chance to spawn a new vessel
def spawn():
	if vessel_generator.spawn_vessel('sh'): ships.append(Ship())
	if vessel_generator.spawn_vessel('sn'): snipers.append(Sniper())
	if vessel_generator.spawn_vessel('su'): subs.append(Sub())
#ENDSPAWN

##Setup the surfs (100m intervals deep)
##surfs are drawn onto surf
SCREEN_COLOURS=[0x36a8ff,0x218bdb,0x0d70ba,0x11609c,0x1a5887,0x144a73,0x144366,0x103a59,0x11354f,0x103047,0x0f2a3d,0x0b1f2e,0x061b2b,0x041421,0x03111c]
#                                                   #Sub Level                                            #Twilight Zone
SURF_COUNT=len(SCREEN_COLOURS)
SURF_RANGE=range(SURF_COUNT)
elevation=190
MAX_DEPTH=190
MIN_DEPTH=-900
surf=drawSurf((500,100*SURF_COUNT))
rect=surf.get_rect()
surfs=[drawSurf((500,100)) for i in SURF_RANGE]
rects=[surf_n.get_rect() for surf_n in surfs]
blue_background=0x7ec0f2

##Classes

##A Class for handling the display of the sonar and header sprite
##Should also be able to handle displaying targets when vessels are developed
##Attributes: sonar, header, header_original, pos, facing
##assumes that the pos is the centre of the image
class Sonar:
    def __init__(self,sonar_filepath,header_filepath,pos,offset=0):
        self.sonar=pygame.image.load(sonar_filepath).convert_alpha()
        self.header=pygame.image.load(header_filepath).convert_alpha()
        self.header_original=self.header.copy()
        self.pos=tuple(coordinate+offset for coordinate in pos)
        self.facing=0
    #ENDINIT

    ##get the sonar image
    def get_image(self):
        return (self.sonar,self.header)
    #END get_image

    ##get the sonar rect
    ##hardcoded to set center=<pos>
    def get_rect(self):
        pos=self.header.get_rect(center=self.pos).center
        sonar_rect=self.sonar.get_rect(center=pos)
        header_rect=self.header.get_rect(center=pos)
        return(sonar_rect,header_rect)

    ##Rotates header
    def rotate(self,angle):
        self.facing+=angle
        if self.facing>359: self.facing=0
        elif self.facing<0: self.facing=359
        _,header_original_rect=self.get_rect()
        self.header=pygame.transform.rotate(self.header_original,self.facing)
    #END rotate
#ENDCLASS


##sonar and depth gauge images
sonar_pos=(12,500)
SONAR_OFFSET=43
sonar=Sonar('resources\\sonar.png','resources\\sonar_header.png',sonar_pos,SONAR_OFFSET)
depth_gauge=pygame.image.load('resources\\depth_gauge.png').convert_alpha()
depth_gauge_rect=depth_gauge.get_rect()
shuttle_y=15

##A class for handling the vessel_surf
class Vessel_Surf:
	def __init__(self):
		self.surf=drawSurf((500,900))
	#END init

	##Draw each vessel onto the surf
	def draw_vessels(self):
		for type in vessels:
			active_type=vessels[type]
			vessel_surfs=[drawSurf((30,30)) for vessel in active_type]
			for index in range(len(vessel_surfs)):
				vessel_surfs[index].fill(0x000000)
			vessel_rects=[surf.get_rect() for surf in vessel_surfs]
			for index in range(len(active_type)):
				vessel=active_type[index]
				vessel_topleft=(vessel.getAngle(),vessel.getDepth())
				vessel_rects[index].topleft=vessel_topleft
				self.surf.blit(vessel_surfs[index],vessel_rects[index])
			#ENDFOR
		#ENDFOR
	#END draw_vessels

	##Draw surf onto a parent surf and vessels on this nested surf
	def draw(self,surf,elevation):
		self.draw_vessels()
		surf.blit(self.surf,(0,elevation))
#ENDCLASS

vessel_surf=Vessel_Surf()

##Setup the facing text
##To be replaced with a sonar
# facing=0 #0-359
# font=pygame.font.Font(size=32)
# text=font.render(f'Facing: {facing}°',False, (255,255,255))
# text_rect=text.get_rect()

speed_up,speed_down,speed_left,speed_right=0,0,0,0 #used for moving surf and facing

##Get the sonar images and make the rects
def blit_sonar(image,rect):
    sonar_image,header_image=sonar.get_image()
    sonar_rect,header_rect=sonar.get_rect()
    screen.blit(sonar_image,sonar_rect)
    screen.blit(header_image,header_rect)

##Game loop
print(vessel_generator)
gameon=True
while gameon:
    ##Listen for game events
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			gameon=False

		elif event.type==pygame.KEYDOWN: #keypresses
			keyPressed=event.key
			if keyPressed==pygame.K_DOWN:
				speed_down=20
			elif keyPressed==pygame.K_UP:
				speed_up=20
			elif keyPressed==pygame.K_LEFT:
				speed_left=3
			elif keyPressed==pygame.K_RIGHT:
				speed_right=3
			elif keyPressed==pygame.K_ESCAPE:
				gameon=False

		elif event.type==pygame.KEYUP: #keyreleases
			keyReleased=event.key
			if keyReleased==pygame.K_DOWN:
				# print(elevation)
				speed_down=0
			elif keyReleased==pygame.K_UP:
				# print(elevation)
				speed_up=0
			elif keyReleased==pygame.K_LEFT:
				speed_left=0
			elif keyReleased==pygame.K_RIGHT:
				speed_right=0

		elif event.type==SPAWN_VESSEL:
			spawn()
			system('cls')
			print(vessel_generator)
        #ENDELIF
	#ENDFOR

    ##Fill the screen
	screen.fill(blue_background)

    ##Determine movement and facing
	depth_speed=speed_up-speed_down
	if(depth_speed):
		if MIN_DEPTH<=elevation+depth_speed<=MAX_DEPTH:
			elevation+=depth_speed
	if(elevation>-100):
		shuttle_y=15
	elif(-100>=elevation>=-600):
		shuttle_y=50
	else:
		shuttle_y=80

	rotate_speed=speed_right-speed_left
	if(rotate_speed):
		sonar.rotate(-rotate_speed)
    #ENDIF -> Player has stoppped rotating

    #display widgets
	for index in SURF_RANGE:
		surf_i=surfs[index]
		surf_pos=(0,index*100)
		surf_i.fill(SCREEN_COLOURS[index])
		surf.blit(surf_i, surf_pos)
	# screen.blit(surf, (0,elevation))
    # text=font.render(f'Facing: {int(facing)}°',False, (255,255,255))
    # screen.blit(text, sonar_pos)
	sonar_image=sonar.get_image()
	sonar_rect=sonar.get_rect()
	# blit_sonar(sonar_image,sonar_rect)
	# screen.blit(depth_gauge,(110,480))
    # screen.blit(depth_gauge,depth_gauge_rect)
	# depth_gauge_shuttle=drawSurf((8,10))
	# depth_gauge_shuttle.fill(0xffffff)
	# screen.blit(depth_gauge_shuttle,(116,490+shuttle_y-5))
	vessel_surf.draw(surf,elevation)
	tick()
	clock.tick(30)
#ENDWHILE
