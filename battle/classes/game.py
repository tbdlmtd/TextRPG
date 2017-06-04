import random


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class person:
	def __init__(self, name, hp, mp, atk, df, magic, item):
		self.max_hp = hp
		self.hp = hp
		self.max_mp = mp
		self.mp = mp
		self.atkl = atk - 10
		self.atkh = atk + 10
		self.df = df
		self.magic = magic
		self.item = item
		self.actions = ["Attack", "Magic", "Items"]
		self.name = name

	def generate_damage(self):
		return random.randrange(self.atkl, self.atkh)

	def take_damage(self, dmg):
		self.hp -= dmg
		if self.hp < 0:
			self.hp = 0
			return self.hp

	def get_hp(self):
		return self.hp

	def get_max_hp(self):
		return self.max_hp

	def get_mp(self):
		return self.mp

	def get_max_mp(self):
		return self.max_mp

	def reduce_mp(self, cost):
		self.mp -= cost

	def heal(self, dmg):
		self.hp += dmg
		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def choose_action(self):
		print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
		print(bcolors.OKBLUE + bcolors.BOLD + 'Actions:' + bcolors.ENDC)
		i = 1
		for action in self.actions:
			print("	" + str(i) + ':', action)
			i += 1

	def choose_magic(self):
		print("\n" + bcolors.OKBLUE + bcolors.BOLD + 'Magic:' + bcolors.ENDC)
		i = 1
		for spell in self.magic:
			print("	" + str(i) + ')', spell.name, '{cost:', str(spell.cost) + '}')
			i += 1

	def choose_item(self):
		print("\n" + bcolors.OKBLUE + bcolors.BOLD + 'Items:' + bcolors.ENDC)
		i = 1
		for item in self.item:
			print("	" + str(i) + ")", item["item"].name, ':', item['item'].description + ' (x' + str(item['quantity']) +')')
			i += 1

	def choose_target(self, enemies):
		i=1
		print("\n" + bcolors.BOLD + bcolors.FAIL + "TARGET:" + bcolors.ENDC)

		for enemy in enemies:
			if enemy.get_hp() != 0:
				print(str(i) + "." + enemy.name)
				i += 1
		choice = int(input("Choose target: ")) - 1
		return choice

	def get_enemy_stats(self):
		hp_bar = ""
		hp_ticks = (self.hp/self.max_hp) * 100 / 2

		while hp_ticks >= 0:
			hp_bar += "█"
			hp_ticks -= 1

		while len(hp_bar) < 50:
			hp_bar += " "

		hp_string = str(self.hp) + "/" + str(self.max_hp)
		current_hp = ""

		if len(hp_string) < 11:
			decrease = 11 - len(hp_string)

			while decrease > 0:
				current_hp += " "
				decrease -= 1
				current_hp += hp_string
		else:
			current_hp = hp_string

		print("                    ___________________________________________________")
		print(bcolors.BOLD + self.name + " " + current_hp + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC +
			  bcolors.BOLD + "|")

	def get_stats(self):
		hp_bar = ""
		hp_ticks = (self.hp/self.max_hp) * 100 / 4
		mp_bar = ""
		mp_ticks = (self.mp/self.max_mp) * 100/ 10

		while hp_ticks >= 0:
			hp_bar += "█"
			hp_ticks -= 1

		while len(hp_bar) < 25:
			hp_bar += " "

		while mp_ticks >= 0:
			mp_bar += "█"
			mp_ticks -= 1

		while len(mp_bar) < 10:
			mp_bar += " "

		hp_string = str(self.hp) + "/" + str(self.max_hp)
		current_hp = ""

		if len(hp_string) < 9:
			decrease = 9 - len(hp_string)

			while decrease > 0:
				current_hp += " "
				decrease -= 1
				current_hp += hp_string
		else:
			current_hp = hp_string

		mp_string = str(self.mp) + "/" + str(self.max_mp)
		current_mp = ""

		if len(mp_string) < 7:
			decrease = 7 - len(mp_string)

			while decrease > 0:
				current_mp += " "
				decrease -= 1
				current_mp += mp_string
		else:
			current_mp = mp_string

		print("                  __________________________           ___________ ")
		print(bcolors.BOLD + self.name + " " + current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC +
			  bcolors.BOLD + "|  " + current_mp + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + bcolors.BOLD + "|")

	def choose_enemy_spell(self):
		magic_choice = random.randrange(0, len(self.magic))
		spell = self.magic[magic_choice]
		magic_dmg = spell.generate_damage()
		cost = spell.cost

		pct = (self.mp/self.max_mp) * 100

		if self.mp < spell.cost or spell.type == "white" and pct < 50:
			self.choose_enemy_spell()
		else:
			return spell, magic_dmg
