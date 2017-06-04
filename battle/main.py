from classes.game import person, bcolors
from classes.magic import magic
from classes.inventory import item
import random

#Create black magic
fire = magic('Fire', 110, 1100, 'black')
thunder = magic('Thunder', 120, 1200, 'black')
blizzard = magic('Blizzard', 100, 1000, 'black')
meteor = magic('Meteor', 220, 2000, 'black')
quake = magic('Quake', 120, 1200, 'black')

#Create white magic
cure = magic('Cure', 12, 120, 'white')
cura = magic('Cura', 18, 200, 'white')

#Create items
potion = item("Clover Leaf Potion", "potion", "Heals 50 HP", 50)
high_potion = item("Moon Moss Potion", "potion", "Heals 100 HP", 100)
super_potion = item("Bat Wing Potion", "potion", "Heals 500 HP", 500)
elixir = item("Blooming Blossom Elixir", "elixir", "Restores HP and MP for one member of the party", 9999)
high_elixir = item("Healing Star Elixir", "elixir", "Restores HP and MP for the entire party", 9999)
grenade = item("Grenade", "weapon", "Deals 500 Damage", 500)

#create a list of items and spells for each player
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{'item':potion, 'quantity':15}, {'item':high_potion, 'quantity':5}, {'item':elixir, 'quantity':9}, {'item':high_elixir, 'quantity':5}, {'item':grenade, 'quantity':30}]

#create a list of items and spells for each enemy
enemy_spells = [fire, blizzard, thunder, cure]
enemy_items = []

#Instatiate players
player_1 = person("Aella:", 2000, 350, 260, 34, player_spells, player_items)
player_2 = person("Puabi:", 2000, 500, 160, 34, player_spells, player_items)
player_3 = person("Efua :", 2000, 200, 360, 34, player_spells, player_items)
player_4 = person("Chiro:", 2000, 180, 330, 34, player_spells, player_items)

players = [player_1, player_2, player_3, player_4]

#Instatiate enemies
enemy_1 = person("Xanto:", 10000, 300, 400, 25, enemy_spells, enemy_items)
enemy_2 = person("Vespa:", 50000, 300, 800, 25, enemy_spells, enemy_items)
enemy_3 = person("Brevi:", 10000, 300, 400, 25, enemy_spells, enemy_items)

enemies = [enemy_1, enemy_2, enemy_3]

#The initial set up of the attack
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!!" + bcolors.ENDC)

running = True

while running:
	print("=" * 20)
	print("\n")
	print("NAME              HP                                   MP")

	for player in players:
		player.get_stats()

	print("\n")

	for enemy in enemies:
		enemy.get_enemy_stats()

	print("\n")

#Allow players to choose actions and targets for those actions:
	for player in players:

		player.choose_action()
		choice = input("Choose action: ")
		index = int(choice) - 1

		if index == 0:
			#If the player chooses to attack, a random amount of damage is calculated & dispensed
			dmg = player.generate_damage()
			enemy = player.choose_target(enemies)
			enemies[enemy].take_damage(dmg)

			print("\n" + 'You attacked ' + enemies[enemy].name + " " + str(dmg) + ' points of damage.')

			#if the enemy has no hit points left, they die.
			if enemies[enemy].get_hp() == 0:
				print(enemies[enemy].name + " has died.")
				del enemies[enemy]

		elif index == 1:
			#if the player chooses magic, they have a list of spells to choose from
			player.choose_magic()
			magic_choice = int(input("Choose magic: ")) - 1

			#each spell generates a random amount of damage
			spell = player.magic[magic_choice]
			magic_dmg = spell.generate_damage()
			cost = spell.cost

			#this allows a player to return to the "Magic" menu
			if magic_choice == -1:
				continue

			current_mp = player.get_mp()

			#if you don't have any more magic points (mp) you can't cast spells:/
			if spell.cost > current_mp:
				print("\n" + bcolors.FAIL + '\nYou dont have enough juice for this!\n' + bcolors.ENDC)
				continue

			#Healing spells heal...
			if spell.type == 'white':
				player.heal(magic_dmg)
				print(bcolors.OKBLUE + '\n' + spell.name + ' heals for ' + str(magic_dmg) + ' HP.' + bcolors.ENDC)

			#Black magic is a weapon and generates damage, also we reduce the magic points
			elif spell.type == 'black':

				enemy = player.choose_target(enemies)
				enemies[enemy].take_damage(magic_dmg)

				#magic points reduced
				player.reduce_mp(cost)
				print('\n' + spell.name + ' deals ' + str(magic_dmg) + ' points of damage to ' + enemies[enemy].name + bcolors.ENDC)

			#if enemy has no more HP, they die.
			if enemies[enemy].get_hp() == 0:
				print(enemies[enemy].name + " has died.")
				del enemies[enemy]

		#players also have inventory items they can choose. The quantity decreases as items are used.
		elif index == 2:
			player.choose_item()
			item_choice = int(input("Choose Item: ")) - 1

			item = player.item[item_choice]['item']

			if player.item[item_choice]['quantity'] <= 0:
				print('\n' + bcolors.FAIL + "Shit you ran out!!!" + bcolors.ENDC)
				continue

			player.item[item_choice]['quantity'] -= 1

			if item.type == "potion":
				player.heal(item.prp)
				print("\n" + bcolors.OKGREEN + "You have been HEALED. " + item.name + " " + item.description + bcolors.ENDC)

			elif item.type == 'elixir':
				if item.name == "Healing Star Elixir":
					#this elixir heals everyone in the party
					for i in players:
						i.hp = i.max_hp
						i.mp = i.max_mp
				else:
					player.hp = player.max_hp
					player.mp = player.max_mp
				print("\n" + bcolors.OKGREEN + "It feels good to be restored! HP:", str(player.hp), "MP:", str(player.mp) + bcolors.ENDC)

			elif item.type == "weapon":
				#if the item chosen is a weapon, it will deal a specific (non-random) amt of damage
				enemy = player.choose_target(enemies)
				enemies[enemy].take_damage(item.prp)

				print("\n" + 'You attacked' + enemies[enemy].name + 'for', dmg, 'points of damage.')

				#enemies without HP die.
				if enemies[enemy].get_hp() == 0:
					print(enemies[enemy].name + " has died.")
					del enemies[enemy]

			if item_choice == -1:
				continue

	#check if battle is over
	defeated_enemies = 0
	defeated_players = 0

	for enemy in enemies:
		if enemy.get_hp() == 0:
			defeated_enemies += 1

	for player in players:
		if player.get_hp() == 0:
			defeated_player += 1

	#check to see who won
	if defeated_enemies == 3:
		print(bcolors.OKGREEN + 'You win!' + bcolors.ENDC)
		running = False

	if defeated_players == 4:
		print(bcolors.FAIL + 'You lose:(' + bcolors.ENDC)
		running = False

	#if game is still running, then enemies will choose what to do once they've been attacked
	for enemy in enemies:
		enemy_choice = random.randrange(0,3)
		target = random.randrange(0,4)

		#attack
		if enemy_choice == 0:
			enemy_dmg = enemy.generate_damage()
			players[target].take_damage(enemy_dmg)
			print("\n" + enemy.name + ' attacks' + players[target].name + 'for', enemy_dmg, 'points of damage.')

		#magic
		elif enemy_choice == 1:
			spell, magic_dmg = enemy.choose_enemy_spell()
			players[target].take_damage(magic_dmg)
			enemy.reduce_mp(spell.cost)

			# Healing spells heal...
			if spell.type == 'white':
				enemy.heal(magic_dmg)
				print(bcolors.OKBLUE + '\n' + spell.name + ' heals' + enemy.name + 'for ' + str(magic_dmg) + ' HP.' + bcolors.ENDC)

			# Black magic is a weapon and generates damage, also we reduce the magic points
			elif spell.type == 'black':
				target = random.randrange(0,4)
				players[target].take_damage(magic_dmg)
				print('\n' + spell.name + ' deals ' + str(magic_dmg) + ' points of damage to ' + players[
					target].name + bcolors.ENDC)

			# if enemy has no more HP, they die.
			if players[target].get_hp() == 0:
				print(players[target].name + " has died.")
				del players[target]



