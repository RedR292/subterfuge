##Tester for the screen display
##Has to be able to rotate and move the vessels
##Need to change Vessel_Surf.set_vs
##	Needs to addend each new surf, rect, and coord
##	Cannot reinstantiate new surfs, rects, and coords

##Only update vessel tracking for those subs on the same depth zone as the player
##	Creates isolation like you're actually underwater

from os import system
from Vessel import *
import pygame
pygame.init()
system('cls')

##Setup the pygame screen and functions
SCREEN_DIMENSIONS=[SCREEN_WIDTH, SCREEN_HEIGHT]=[500,300]
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
    def __init__(self,sonar_filepath,header_filepath,pos):
        self.sonar=pygame.image.load(sonar_filepath).convert_alpha()
        self.header=pygame.image.load(header_filepath).convert_alpha()
        self.header_original=self.header.copy()
        self.pos=tuple(coordinate for coordinate in pos)
        self.facing=0
    #ENDINIT

    ##get the sonar image
    def get_image(self):
        return (self.sonar,self.header)
    #END get_image

    ##get the sonar rect
    ##hardcoded to set center=<pos>
    def get_rect(self):
        pos=self.header.get_rect(topleft=self.pos).topleft
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
sonar_pos=(50,240)
sonar=Sonar('resources\\sonar.png','resources\\sonar_header.png',sonar_pos)
depth_gauge=pygame.image.load('resources\\depth_gauge.png').convert_alpha()
depth_gauge_rect=depth_gauge.get_rect(); depth_gauge_rect.topleft=(100,175)
shuttle_y=195

##A class for handling the vessel_surf
class Vessel_Surf:
	def __init__(self):
		self.surf=drawSurf((500,900),pygame.SRCALPHA).convert_alpha()
	#END init

	##set the surfs
	def _set_surfs(self,vessels: dict):
		self.surfs={}
		for type in vessels:
			self.surfs[type]=[drawSurf((30,30)) for vessel in vessels[type]]
		#ENDFOR
		# print(self.surfs)
	#END set_surfs

	##set the coordinates
	def _set_coords(self,vessels: dict):
		self.coords={}
		for type in vessels:
			self.coords[type]=[(v.getAngle(),v.getDepth()) for v in vessels[type]]
		#ENDFOR
		# print(self.coords)
	#END set_coords

	##set the rects
	def _set_rects(self,vessels: dict):
		self.rects={}
		for type in vessels:
			# print(vessels.keys())
			self.rects[type]=[s.get_rect() for s in self.surfs[type]]
			for index in range(len(self.rects[type])):
				self.rects[type][index].topleft=self.coords[type][index]
			#ENDFOR
		#ENDFOR
	#END set_rects

	##User-level function to call all setters
	def set_vs(self,vessels: dict):
		self._set_surfs(vessels)
		self._set_coords(vessels)
		self._set_rects(vessels)

	##Draw each vessel onto the surf
	def draw_vessels(self):
		for type in self.surfs:
			artbook=self.surfs[type]
			rects=self.rects[type]
			for vessel in range(len(artbook)):
				surf=artbook[vessel]
				rect=rects[vessel]
				surf.fill(0xffffff)
				self.surf.blit(surf,rect)
			#ENDFOR
		#ENDFOR
		return self.surf
	#END draw_vessels

	##Draw surf onto a parent surf and vessels on this nested surf
	def draw(self,surf,elevation):
		self.draw_vessels()
		surf.blit(self.surf,(0,elevation))
	#END draw

	def get(self):
		return [self.surf,self.surfs,self.coords,self.rects]

	def __str__(self):
		str=''
		for type in self.surfs:
			surfs=self.surfs[type]
			coords=self.coords[type]
			rects=self.rects[type]
			str+='\tSurfs\t|\tCoords\t\t|\tRects\n'
			str+='+-------------------------------------------------------------+\n'
			for index in range(len(surfs)):
				str+=f'\tSurf{index+1}\t|\t{coords[index]}\t|\t{rects[index].topleft}\n'
			#ENDFOR
			str+='+-------------------------------------------------------------+\n\n'
		#ENDFOR
		return str
	#END str

	##Move each vessel
	def move(self,speed):
		for type in vessels:
			vessel_type=vessels[type]
			for index in range(len(vessel_type)):
				vessel=vessel_type[index]
				new_angle=vessel.getAngle()+speed
				if new_angle>359: new_angle-=359
				elif new_angle<0: new_angle=359-new_angle
				vessels[type][index].setAngle(new_angle)
			#ENDFOR -> done with vessel
		#ENDFOR -> done with vessel type
#ENDCLASS

vessel_surf=Vessel_Surf()
vessel_surf.set_vs(vessels)

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

##Trigger function for SPAWN_VESSEL
##Random chance to spawn a new vessel
def spawn():
	if vessel_generator.spawn_vessel('sh'): ships.append(Ship())
	if vessel_generator.spawn_vessel('sn'): snipers.append(Sniper())
	if vessel_generator.spawn_vessel('su'): subs.append(Sub())
#ENDSPAWN

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
			vessel_surf.set_vs(vessels)
			system('cls')
			print(vessel_generator)
			print(vessel_surf)
        #ENDELIF
	#ENDFOR -> Stop listening for events for current gameloop

    ##Fill the screen
	screen.fill(blue_background)

    ##Determine depth
	depth_speed=speed_up-speed_down
	able_to_move=(MIN_DEPTH<=elevation+depth_speed<=MAX_DEPTH)
	at_surface=(elevation>-100)
	at_middle=(-100>=elevation>=-600)
	if(depth_speed):
		if able_to_move:
			elevation+=depth_speed
	if at_surface:
		shuttle_y=195
	elif at_middle:
		shuttle_y=231
	else:
		shuttle_y=261
	#ENDIF -> Player has stopped diving

	##Determine facing
	rotate_speed=speed_right-speed_left
	if(rotate_speed):
		sonar.rotate(-rotate_speed)
		vessel_surf.move(rotate_speed)

    #ENDIF -> Player has stopped rotating

    #display widgets in the order of:
	##Screen;
	##surfs onto
	##surf;
	##vessels onto
	##vessels_surf
	##sonar and depth
	for index in SURF_RANGE:
		surf_i=surfs[index]
		surf_pos=(0,index*100)
		surf_i.fill(SCREEN_COLOURS[index])
		surf.blit(surf_i, surf_pos)
	screen.blit(surf, (0,elevation))
    # text=font.render(f'Facing: {int(facing)}°',False, (255,255,255))
    # screen.blit(text, sonar_pos)
	sonar_image=sonar.get_image()
	sonar_rect=sonar.get_rect()
	vs=vessel_surf.draw_vessels()
	screen.blit(vs,(0,elevation))
	blit_sonar(sonar_image,sonar_rect)
	screen.blit(depth_gauge,depth_gauge_rect)
	depth_gauge_shuttle=drawSurf((8,10))
	depth_gauge_shuttle.fill(0xffffff)
	screen.blit(depth_gauge_shuttle,(106,shuttle_y))

	tick()
	clock.tick(30)
#ENDWHILE
