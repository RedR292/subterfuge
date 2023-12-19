from Vessel import *
from os import system
import pygame
pygame.init()
clock=pygame.time.Clock()
SPAWN_VESSEL=pygame.USEREVENT+1
SPAWN_TIME_MSECONDS=2000
pygame.time.set_timer(SPAWN_VESSEL,SPAWN_TIME_MSECONDS)

vessel_generator=Vessel()
ships=[]
snipers=[]
subs=[]
vessels={'sh':ships,'sn':snipers,'su':subs}
print(vessel_generator)

def spawn():
	if vessel_generator.spawn_vessel('sh'): ships.append(Ship())
	if vessel_generator.spawn_vessel('sn'): snipers.append(Sniper())
	if vessel_generator.spawn_vessel('su'): subs.append(Sub())
#ENDSPAWN

while True:
	clock.tick(30)
	for event in pygame.event.get():
		elif event.type==SPAWN_VESSEL:
			spawn()
			system('cls')
			print(vessel_generator)
		#ENDELIF
	#ENDFOR
#ENDWHILE
