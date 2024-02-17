import pygame

#damage, cooldown
#Basic
basic1 = (10,0)
basic2 = (20,10000)

#king raptor
king1 = (10, 0)
king2 = (30, 5000)
king3 = (0,30000)

#alpha auora
auora1 = (10, 0)
auora2 = (30, 5000)
auora3 = (0,0)

#Shinden “Vindicator”
vindicator1 = (5,0)
vindicator2 = (20,10000)
vindicator3 = (0,0)

#Crimson “Chimera”
chimera1 = (10,0)
chimera2 = (20,10000)
chimera3 = (0,45000)

#FALKEN Viper
viper1 = (10,0)
viper2 = (20,10000)
viper3 = (0,65000)

#AVATAR Morgan
morgan1 = (10,0)
morgan2 = (20,10000)
morgan3 = (0,30000)

#ASX03 - Nosferatu
nos1 = (5,0)
nos2 = (35,20000)
nos3 = (0,30000)

#ASX09 - Wyvern
wyvern1 = (10,0)
wyvern2 = (20,10000)
wyvern3 = (0,45000)

class Character:
    def __init__(self, class_type):
        self.health = 100
        self.type = class_type
    
    def change_type(self,type):
        if type == 1:
            self.type = 'BASIC'
        elif type == 2:
            self.type = 'KINGR'
        elif type == 3:
            self.type = 'AUORA'
        elif type == 4:
            self.type = 'VINDI'
        elif type == 5:
            self.type = 'CHIME'
        elif type == 6:
            self.type = 'VIPER'
        elif type == 7:
            self.type = 'MORGA'
        elif type == 8:
            self.type = 'NOSFE'
        elif type == 9:
            self.type = 'WYVER'

    def get_type(self):
        return self.type

    def reset(self):
        self.health = 100

    ##### message description #####
    
    #   1 or 2      DAMAGE/SPECIAL   LETTERS      1,2,3
    # PLAYER_NUM     ATTACK TYPE      TYPE     ATTACK TYPE


    def attack1(self, p1):
        message = ""
        if self.type == 'BASIC':
            message = 'DAMAGE BASIC 1'
        elif self.type == 'KINGR':
            message = 'DAMAGE KINGR 1'
        elif self.type == 'AUORA':
            message = 'DAMAGE AUORA 1'
        elif self.type == 'VINDI':
            message = 'DAMAGE VINDI 1'
        elif self.type == 'CHIME':
            message = 'DAMAGE CHIME 1'
        elif self.type == 'VIPER':
            message = 'DAMAGE VIPER 1'
        elif self.type == 'MORGA':
            message = 'DAMAGE MORGA 1'
        elif self.type == 'NOSFE':
            message = 'DAMAGE NOSFE 1'
        elif self.type == 'WYVER':
            message = 'DAMAGE WYVER 1'
        if p1:
            return "1 " + message
        else:
            return "2 " + message
    
    def attack2(self, p1):
        message = ""
        if self.type == 'BASIC':
            message = 'DAMAGE BASIC 2'
        elif self.type == 'KINGR':
            message = 'DAMAGE KINGR 2'
        elif self.type == 'AUORA':
            message = 'DAMAGE AUORA 2'
        elif self.type == 'VINDI':
            message = 'DAMAGE VINDI 2'
        elif self.type == 'CHIME':
            message = 'DAMAGE CHIME 2'
        elif self.type == 'VIPER':
            message = 'DAMAGE VIPER 2'
        elif self.type == 'MORGA':
            message = 'DAMAGE MORGA 2'
        elif self.type == 'NOSFE':
            message = 'DAMAGE NOSFE 2'
        elif self.type == 'WYVER':
            message = 'DAMAGE WYVER 2'
        if p1:
            return "1 " + message
        else:
            return "2 " + message

    def attack3(self, p1):
        message = ""
        if self.type == 'BASIC':
            message = 'SPECAL BASIC 3'
        elif self.type == 'KINGR':
            message = 'SPECAL KINGR 3'
        elif self.type == 'AUORA':
            message = 'SPECAL AUORA 3'
        elif self.type == 'VINDI':
            message = 'SPECAL VINDI 3'
        elif self.type == 'CHIME':
            message = 'SPECAL CHIME 3'
        elif self.type == 'VIPER':
            message = 'SPECAL VIPER 3'
        elif self.type == 'MORGA':
            message = 'SPECAL MORGA 3'
        elif self.type == 'NOSFE':
            message = 'SPECAL NOSFE 3'
        elif self.type == 'WYVER':
            message = 'SPECAL WYVER 3'

        if p1:
            return "1 " + message
        else:
            return "2 " + message

    def calculate_damage(self, health, message, damage_reduction):
        health -= (self.return_attack_damage(message)[0] * damage_reduction)
        return health

    def return_attack_damage(self, message):
        drone_type = message[9:14]
        if drone_type == 'BASIC':
            if message[15] == '1':
                return basic1
            elif message[15] == '2':
                return basic2
            elif message[15] == '3':
                return (0,0)
        elif drone_type == 'KINGR':
            if message[15] == '1':
                return king1
            elif message[15] == '2':
                return king2
            elif message[15] == '3':
                return king3
        elif drone_type == 'AUORA':
            if message[15] == '1':
                return auora1
            elif message[15] == '2':
                return auora2
            elif message[15] == '3':
                return auora3
        elif drone_type == 'VINDI':
            if message[15] == '1':
                return vindicator1
            elif message[15] == '2':
                return vindicator2
            elif message[15] == '3':
                return vindicator3
        elif drone_type == 'CHIME':
            if message[15] == '1':
                return chimera1
            elif message[15] == '2':
                return chimera2
            elif message[15] == '3':
                return chimera3
        elif drone_type == 'VIPER':
            if message[15] == '1':
                return viper1
            elif message[15] == '2':
                return viper2
            elif message[15] == '3':
                return viper3
        elif drone_type == 'MORGA':
            if message[15] == '1':
                return morgan1
            elif message[15] == '2':
                return morgan2
            elif message[15] == '3':
                return morgan3
        elif drone_type == 'NOSFE':
            if message[15] == '1':
                return nos1
            elif message[15] == '2':
                return nos2
            elif message[15] == '3':
                return nos3
        elif drone_type == 'WYVER':
            if message[15] == '1':
                return wyvern1
            elif message[15] == '2':
                return wyvern2
            elif message[15] == '3':
                return wyvern3
        
        
    def calculate_special(self, health, message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, ticks):
        drone_type = message[9:14] 
        
        #EMP, sheild, small heal, more damage, less damage, poison, mega heal, reduced cooldown

        #EMP - Disables all attacks and abilities for 10s
        if drone_type == 'KINGR':
            attack_cooldown_3 = ticks + 10000
            attack_cooldown_2 = ticks + 10000
            attack_cooldown_1 = ticks + 10000
            damage_reduction = 1
            effect_time = 0
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time
        
        #Small Heal - Heals 20 health to user
        elif drone_type == 'AUORA':
            attack_cooldown_3 = ticks + 60000
            health += 20
            damage_reduction = 1
            effect_time = 0
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time

        #Mega Heal - Gives +50 health but cooldown is insane (five minutes)
        elif drone_type == 'VINDI':
            attack_cooldown_3 = ticks + 300000
            health += 50
            damage_reduction = 1
            effect_time = 0
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time

        #50% less damage for 20 seconds
        elif drone_type == 'CHIME':
            damage_reduction = .5
            effect_time = 20000
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time
        
        #Poison - 30 damage over 10 seconds
        elif drone_type == 'VIPER':
            effect_time = 10000
            damage_reduction = 0.5
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time
        
        #Shield for 10 seconds (no damage)
        elif drone_type == 'MORGA':
            damage_reduction = 0
            effect_time = 10000
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time
        
        #delete cooldown
        elif drone_type == 'NOSFE':
            attack_cooldown_2 = ticks
            attack_cooldown_1 = ticks
            damage_reduction = 1
            effect_time = 0
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time
        
        #1.5x damage for 20 seconds to you and your opponent ;)
        elif drone_type == 'WYVER':
            damage_reduction = 1.5
            effect_time = 20000
            return health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time