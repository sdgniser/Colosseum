import random


def get_bot_class():
	# 2 == Rogue
	return 2


def get_bot_action(current_game_state, game_archive):
	"""Advanced Rogue bot.

	Features:
	- Uses `game_archive` to detect when opponent tends to use big spells and times Shadow Dodge.
	- Manages poison stacks (prefers to stack Poison Dart early and reapply when it runs low).
	- Chooses Backstab for high-damage windows and Quick Strike for SP-efficient pressure.
	- Uses items (Bomb for finishing, Elixir/Potion/Ether to survive) sensibly.
	- Falls back to Attack to regenerate SP when safe.
	"""
	player = current_game_state.get('player', {})
	opponent = current_game_state.get('opponent', {})
	inventory = current_game_state.get('inventory', {})

	hp = int(player.get('hp', 0))
	max_hp = int(player.get('max_hp', 100))
	sp = int(player.get('skill_points', 0))
	opp_hp = int(opponent.get('hp', 0))
	opp_sp = int(opponent.get('skill_points', 0))
	opp_class = opponent.get('character_class', '')

	# conservative damage maxima by class (from docs)
	BASIC_MAX = {'Warrior': 25, 'Mage': 16, 'Rogue': 22}
	SKILL_MAX = {
		'Warrior': {'Power Strike': 40, 'Shield Bash': 30, 'Whirlwind': 35},
		'Mage': {'Fireball': 45, 'Ice Shard': 35, 'Lightning Bolt': 50},
		'Rogue': {'Backstab': 45, 'Poison Dart': 10, 'Quick Strike': 35}
	}

	# Helpers
	def recent_actions(n=12):
		out = []
		for turn in game_archive[-n:]:
			a = turn.get('action', [None, None])[0]
			if isinstance(a, str):
				out.append(a)
		return out

	recent = recent_actions(16)

	# estimate incoming maximum damage
	def estimate_incoming():
		if opp_class in SKILL_MAX:
			s = SKILL_MAX[opp_class]
			possible = []
			if opp_class == 'Warrior':
				if opp_sp >= 4: possible.append(s['Whirlwind'])
				if opp_sp >= 3: possible.append(s['Power Strike'])
				if opp_sp >= 2: possible.append(s['Shield Bash'])
			elif opp_class == 'Mage':
				if opp_sp >= 6: possible.append(s['Lightning Bolt'])
				if opp_sp >= 5: possible.append(s['Fireball'])
				if opp_sp >= 3: possible.append(s['Ice Shard'])
			elif opp_class == 'Rogue':
				if opp_sp >= 4: possible.append(s['Backstab'])
				if opp_sp >= 3: possible.append(s['Poison Dart'])
				if opp_sp >= 2: possible.append(s['Quick Strike'])
			if not possible:
				return BASIC_MAX.get(opp_class, 12)
			return max(possible)
		return BASIC_MAX.get(opp_class, 12)

	est_in = estimate_incoming()

	# Detect if opponent recently used big spells often
	recent_big = any(('Fireball' in a or 'Lightning' in a or 'Power Strike' in a or 'Backstab' in a) for a in recent)

	# Inventory counts
	bombs = inventory.get('Bomb', 0)
	potions = inventory.get('Potion', 0)
	ethers = inventory.get('Ether', 0)
	elixirs = inventory.get('Elixir', 0)

	# 1) Immediate survival: if we are likely to be killed next turn, prioritize survive
	if est_in >= hp:
		# Shadow Dodge gives guaranteed dodge for one turn (cost 3 SP)
		if sp >= 3:
			return "Cast Shadow Dodge"
		if elixirs > 0 and hp <= int(max_hp * 0.45):
			return "Use Elixir"
		if potions > 0 and hp < int(max_hp * 0.6):
			return "Use Potion"
		if ethers > 0 and hp < int(max_hp * 0.5):
			return "Use Ether"
		# Fallback defend
		return "Defend"

	# 2) Low HP (proactive heal)
	if hp < max(45, int(max_hp * 0.3)):
		if elixirs > 0 and hp <= int(max_hp * 0.5):
			return "Use Elixir"
		if potions > 0:
			return "Use Potion"
		if ethers > 0:
			return "Use Ether"

	# 3) Finishing moves: if opponent is in range for bomb or backstab
	if opp_hp <= 50 and bombs > 0:
		# If we can backstab for more reliable finish and have SP
		if sp >= 4 and opp_hp <= 45:
			return "Cast Backstab"
		return "Use Bomb"

	# If we can finish with Backstab, do it
	if sp >= 4 and opp_hp <= 50:
		return "Cast Backstab"

	# 4) Poison management: try to maintain poison stacks on the opponent
	# Look back for last poison applications in archive
	poison_uses = sum(1 for a in recent if isinstance(a, str) and 'Poison Dart' in a)
	# If opponent not frequently poisoned recently, apply Poison Dart early
	if sp >= 3:
		# If opponent health is moderate/high, prefer applying poison to wear them down
		if poison_uses < 1 and opp_hp > 60:
			return "Cast Poison Dart"
		# Reapply if it looks like poison hasn't been used recently
		if poison_uses == 0 and random.random() < 0.5:
			return "Cast Poison Dart"

	# 5) Defensive timing: if opponent recently used big skills, consider Shadow Dodge
	if recent_big and sp >= 3 and hp < int(max_hp * 0.6) and random.random() < 0.8:
		return "Cast Shadow Dodge"

	# 6) High-damage windows: Backstab when SP available and enemy not near-death of others
	if sp >= 4 and (opp_hp > 60 or random.random() < 0.5):
		return "Cast Backstab"

	# 7) Use Quick Strike as efficient pressure (cost 2 SP)
	if sp >= 2:
		# if we've applied poison recently, pair with Quick Strike to pressure
		if poison_uses > 0:
			return "Cast Quick Strike"
		# otherwise sometimes prefer Quick Strike to build SP timing
		if random.random() < 0.7:
			return "Cast Quick Strike"

	# 8) If low SP, Attack to regenerate SP (rogue regains 1 SP on Attack)
	if sp < 2:
		# If it's safe (estimated incoming damage small), attack to regen
		if est_in < hp - 8:
			return "Attack"
		# otherwise defend or use small potion
		if ethers > 0 and hp < int(max_hp * 0.5):
			return "Use Ether"
		return "Defend"

	# Fallback
	return "Attack"

