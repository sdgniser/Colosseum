import random
import numpy as np
#import pygame
ty=random.randint(0,2)
def get_bot_class():
    return ty
def get_bot_action(current_game_state,game_archive):
    player_hp=current_game_state['player']['hp']
    player_sp=current_game_state['player']['skill_points']
    inventory=current_game_state['inventory']
    #print(inventory.get("Elixir",0)>0)
    if(ty==0):
        if player_hp<70 and player_sp>=3:
            return "Cast Battle Cry"
        if player_hp<100 and player_hp>=70 and inventory.get("Elixir",0)>0:
            return "Use Elixir"
        if player_hp<130 and player_hp>=100 and inventory.get("Potion",0)>0:
            return "Use Potion"
        if player_hp<130 and inventory.get("Ether",0)>0:
            return "Use Ether"
        if current_game_state['opponent']['hp']<50 and inventory.get("Bomb",0)>0:
            return "Use Bomb"
        if current_game_state['opponent']['hp']<50 and player_sp>=3:
            return "Cast Power Strike"
        if player_sp<=2 and player_hp>80:
            return "Attack"
        if player_hp<100:
            return 'Defend'
        if player_hp>=150:
            t=random.randint(0,1)
            if t==1 and player_sp>=2:
                return "Cast Shield Bash"
            elif t==0:
                return "Attack"
            else:
                return "Defend"
        if player_hp<150 and player_hp>=100:
            t=random.randint(0,1)
            if t==1 and player_sp>=4:
                return "Cast Whirlwind"
            elif t==0:
                return "Attack"
        else:
            return "Attack"
    elif(ty==1):
        if player_hp<30 and player_sp>=4:
            return "Cast Arcane Heal"
        if player_hp<60 and player_hp>=30 and inventory.get("Elixir",0)>0:
            return "Use Elixir"
        if player_hp<90 and player_hp>=60 and inventory.get("Potion",0)>0:
            return "Use Potion" 
        if player_hp<90 and inventory.get("Ether",0)>0:
            return "Use Ether"
        if current_game_state['opponent']['hp']<40 and inventory.get("Bomb",0)>0:
            return "Use Bomb"                   
        if current_game_state['opponent']['hp']<40 and player_sp>=5:
            return "Cast Fireball"
        if player_sp<=3 and player_hp>50:
            return "Attack"
        if player_hp<100:
            return 'Defend'             
        if player_hp>=130:
            t=random.randint(0,1)
            if t==1 and player_sp>=6:
                return "Cast Lightning Bolt"
            elif t==0:
                return "Attack"
            else:
                return "Defend"
        if player_hp<130 and player_hp>=100:
            t=random.randint(0,1)
            if t==1 and player_sp>=3:
                return "Cast Ice Shard"
            elif t==0:
                return "Attack"
        else:
            return "Defend"
    elif(ty==2):
        if player_hp<30 and player_sp>=3:
            return "Cast Shadow Dodge"
        if player_hp<50 and player_hp>=30 and inventory.get("Elixir",0)>0:
            return "Use Elixir"
        if player_hp<80 and player_hp>=50 and inventory.get("Potion",0)>0:
            return "Use Potion"
        if player_hp<100 and inventory.get("Ether",0)>0:
            return "Use Ether"
        if current_game_state['opponent']['hp']<45 and inventory.get("Bomb",0)>0:
            return "Use Bomb"
        if current_game_state['opponent']['hp']<45 and player_sp>=4:
            return "Cast Backstab"
        if player_sp<=3 and player_hp>70:
            return "Attack"
        if player_hp<100:
            return 'Defend'
        if player_hp>=150:
            t=random.randint(0,1)
            if t==1 and player_sp>=2:
                return "Cast Quick Strike"
            elif t==0:
                return "Attack"
            else:
                return "Defend"
        else:
            return "Attack"
