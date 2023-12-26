from random import randint as rand
##Needs to have a way to track number of spawns
##Needs to be able to determine when to spawn a new vessel
ZONE_SPAWN_LIMIT=5
##attributes=x,y,depth,speed,
active_vessels={'sh':0,'sn':0,'su':0}
class Vessel:
	# surface_vessels,sniper_vessels,sub_vessels=active_vessels=[0,0,0]
	##INIT FUNCTION IS FOR TESTING, SHOULD NOT BE CALLABLE IN END PRODUCT
	def __init__(self, spawn_depth=-5, spritePath='<SHIPSPRITEPATH>',type=''):
		if type in active_vessels:
			is_facing_right=rand(0,2) #BOOL
			self.facing_right=is_facing_right
			spawn_angle=rand(0,500)
			self.angle=spawn_angle
			self.depth=spawn_depth
			self.spritePath=spritePath
			active_vessels[type]+=1
		#ENDIF
	#END init

	##called whenever a vessel is destroyed
	def __del__(self):
		pass
		##if type(self)=='Ship':
		#	destroyed_vessel_index=0
		##elif type(self)=='Sniper':
		#	destroyed_vessel_index=1`
		##elif type(self)=='Sub':
		#	destroyed_vessel_index=2
		#active_vessels[destroyed_index]-=1
	#END del

	def getAngle(self): return self.angle
	def getDepth(self): return self.depth
	def getCoords(self): return(self.getAngle(),self.getDepth())

	def setAngle(self,angle):self.angle=angle
	def setDepth(self,depth):self.depth=depth

	##function for spawning vessels
	def spawn_vessel(self,spawn_zone_index):
		spawn_zone=active_vessels[spawn_zone_index]
		if spawn_zone>=ZONE_SPAWN_LIMIT: return False
		skew=int(spawn_zone/2) # More ships on level=less likely to spawn
		spawn_chance=rand(0,8-skew)
		if spawn_chance<=2: return True
		else: return False
	#END spawn_vessel

	##Called whenever a vessel attacks
	def attack(self):
		attack_chance=rand(0,10)
		return attack_chance<=3
	#END attack

	def __str__(self):
		print_str=''
		border_str='+-+-+-+-+-+\n'
		for type in active_vessels:
			print_str+=border_str
			type_count=active_vessels[type]
			for j in range(5):
				if j<type_count:
					print_str+='|X'
				else:
					print_str+='|O'
			print_str+='|\n'
			#ENDFOR
		#ENDFOR
		print_str+=border_str
		return print_str
	#END str

	##For moving the vessel
	def move(self,speed):
		pass
	#END move
#ENDCLASS

##Ship subclass of Vessel
##Stays on the surface (determined by highest level on surf)
class Ship(Vessel):
	def __init__(self):
		super().__init__(type='sh')
	#END init
#ENDCLASS

##Sniper subclass of Vessel
##Hover high in the water and attack subs on either side
##spawns from 240-540
class Sniper(Vessel):
	def __init__(self):
		depth=rand(100,541)
		super().__init__(spawn_depth=depth,type='sn')
	#END init
#ENDCLASS

##Sub subclass of Vessel
##spawns from 600-900
class Sub(Vessel):
	def __init__(self):
		depth=rand(600,900)
		super().__init__(spawn_depth=depth,type='su')
	#END init
#ENDCLASS
