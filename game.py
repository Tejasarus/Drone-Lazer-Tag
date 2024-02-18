import socket
import threading
import pygame
import cv2
import numpy as np
import ui
import vision
import audio
import sys
sys.path.append('drone types/')
import Character


#pygame initalization
pygame.init()
clock = pygame.time.Clock()
width, height = 1280, 720
nickname = "Player"
#fullscreen
#screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
#not full screen
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Fight Flight")

#health bars
health = 100
enemy_health = 100

#settings parameters
audio_level = 0.5

#drone class variables
basic = False
wings_of_corona = False
steel_talons = False
galm_corps = False
foehn_wind = False
drone_class = "basic"

#menu game variables
main_menu = False
game_mode_select = False
player_select = False
game_start = False
font = pygame.font.SysFont('/images/ui/recharge bd.otf', 36)
font_menu = pygame.font.Font('images/ui/recharge bd.otf',70)
you_lose = False
you_win = False
waiting = False
drone_select = True
drone_desc_activate = [True, False, False, False, False, False, False, False]

#multiplayer lobby menus
multiplayer_lobby = False
join_lobby = False
host_lobby = False
ip_add = ''
port_add = ''
message = ""
text_count = 0
host_button = ui.Button((0,255,0),width/7,height/4,225,350,"host")
join_button = ui.Button((0,255,0),width * (2/3),height/4,225,350,"join")
p1 = False
hit = False
viper = False
dam_re = False
wyver = False
damage_done = 0
poison_damage = 10

#character stats and checks
max_check3 = 0
max_check2 = 0
max_check1 = 0
ch = Character.Character('BASIC')
ch.change_type(9)
attack_cooldown_1 = 0
attack_cooldown_2 = 0
attack_cooldown_3 = 0
damage_reduction = 1
effect_time = 0
effect_time_other_player = 0
curr_time = pygame.time.get_ticks()

#audio
pygame.mixer.init()
main_music = audio.Music('audio/menu_music.mp3')
main_music.play_on_loop()
pygame.mixer.init()
        
gameplay_music = audio.Music('audio/gameplay_music.mp3')
game_audio = True

weapon1_audio = audio.SoundEffect('audio/pew.mp3')

#define all buttons
play_button = ui.Button((0,255,0),width/7,height/4,225,350,"play")
demo_button = ui.Button((0,255,0),width * (2/3),height/4,225,350,"demo")
settings_button = ui.Button((0,255,0),(width //2) - 120,height-130,220,70,"settings")
player_1_select = ui.Button((0,255,0),width/7,height - 300,225,225,"Player 1")
player_2_select = ui.Button((0,255,0),width * (2/3),height - 300,225,225,"Player 2")

drone_one_button = ui.Button((0,255,0),75,175,110,110,"1")
drone_two_button = ui.Button((0,255,0),75,295,110,110,"2")
drone_three_button = ui.Button((0,255,0),75,415,110,110,"3")
drone_four_button = ui.Button((0,255,0),75,535,110,110,"4")
drone_five_button = ui.Button((0,255,0),215,175,110,110,"5")
drone_six_button = ui.Button((0,255,0),215,295,110,110,"6")
drone_seven_button = ui.Button((0,255,0),215,415,110,110,"7")
drone_eight_button = ui.Button((0,255,0),215,535,110,110,"8")
#initalize opencv
#vc = cv2.VideoCapture(0,cv2.CAP_DSHOW) #windows
vc = cv2.VideoCapture(0) #macos
vc.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
rval, frame = vc.read()
pink_detection = vision.Vision(rval,vc,frame,height,width)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.10', 49152))
#client.connect(('127.0.0.1', 49152))

def receive():
    global health
    global enemy_health
    global waiting
    global game_start
    global attack_cooldown_1
    global attack_cooldown_2
    global attack_cooldown_3
    global damage_reduction
    global effect_time
    global curr_time
    global effect_time_other_player
    global viper
    global dam_re
    global wyver
    while True:
        try:
            #How damage is calculated
            message = client.recv(1024).decode('ascii')
            print(message)
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif 'DAMAGE' in message.upper():
                if p1 and message[0] == '2':
                    health = ch.calculate_damage(health,message, damage_reduction)
                elif not p1 and message[0] == '1':
                    health = ch.calculate_damage(health,message, damage_reduction)
                    
                
            elif 'SPECAL' in message.upper(): 
                #special condition for heal
                if 'AUORA' in message.upper():
                    if p1 and message[0] == '1' or not p1 and message[0] == '2':
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                    else:
                        enemy_health += 20
                elif 'VINDI' in message.upper():
                    if p1 and message[0] == '1' or not p1 and message[0] == '2':
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                    else:
                        enemy_health += 50

                #special condition for damage reduction
                elif 'CHIME' in message.upper() or 'MORGA' in message.upper() or 'WYVER' in message.upper():
                    if p1 and message[0] == '1':
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                        effect_time += curr_time
                        
                    elif not p1 and message[0] == '2':
                        
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                        effect_time += curr_time
                    else:
                        tmp_dam_reduct = damage_reduction
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                        effect_time_other_player = effect_time + curr_time
                        effect_time = 0
                        if 'WYVER' in message.upper():
                            damage_reduction = tmp_dam_reduct
                        #print("here", damage_reduction)
                    if 'WYVER' in message.upper():
                        wyver = True
                    else:
                        dam_re = True

                #special condition for viper
                elif 'VIPER' in message.upper():
                    if p1 and message[0] == '1':
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                        effect_time += curr_time
                    elif not p1 and message[0] == '2':
                        
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                        effect_time += curr_time
                    else:
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                        effect_time_other_player = effect_time + curr_time
                        effect_time = 0
                    viper = True
                
                #special condition for Nosferatu
                elif 'NOSFE' in message.upper():
                    if p1 and message[0] == '1':
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                    elif not p1 and message[0] == '2':
                        health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                
                

                #everything else
                elif p1 and message[0] == '2':
                   health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
                elif not p1 and message[0] == '1':
                    health, attack_cooldown_3, attack_cooldown_2, attack_cooldown_1, damage_reduction, effect_time = ch.calculate_special(health,message,attack_cooldown_3,attack_cooldown_2, attack_cooldown_1, pygame.time.get_ticks())
               
                
            elif 'START 2' in message.upper() and p1 and waiting:
                message = 'START 1'
                client.send(message.encode('ascii'))
                waiting = False
                game_start = True
            elif 'START 1' in message.upper() and not p1 and waiting:
                message = 'START 2'
                client.send(message.encode('ascii'))
                waiting = False
                game_start = True
            else:
                print(message)
                # You can handle displaying the message in the Pygame window here
        except Exception as e:
            print("An error occurred:", e)
            client.close()
            break

def display_menu(image):
    img = pygame.image.load(image).convert()
    img = pygame.transform.scale(img, (width,height))
    screen.blit(img,(0,0))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

while True:
    click = False
    #menu screens
    #main menu
    if main_menu:
        display_menu("images/main_menu.png")
        scale_factor = 0.6
        menu_play_button = pygame.image.load("images/ui/Play.png").convert_alpha() 
        menu_play_button = pygame.transform.scale(menu_play_button,(menu_play_button.get_width() * scale_factor, menu_play_button.get_height() * scale_factor))
        screen.blit(menu_play_button, (width * (30/100),height- 115))

    #gamemode select menu
    if game_mode_select:
        display_menu("images/gamemode_select.png")

        #play_button = ui.Button((0,255,0),width/7,height/4,225,350,"play")
        #play_button.draw(screen)
        #demo_button = ui.Button((0,255,0),width * (2/3),height/4,225,350,"demo")
        #demo_button.draw(screen)
        #settings_button = ui.Button((0,255,0),(width //2) - 120,height-130,220,70,"settings")
        #settings_button.draw(screen)

    if drone_select:
        display_menu("images/drone_select_image.png")
        ui.drone_selection_menu(screen, font_menu, width, height)
        Character.drone_description(drone_desc_activate, screen, width, height)
        scale_factor = 0.5

        select_image = pygame.image.load("images/ui/Select.png").convert_alpha()
        select_image = pygame.transform.scale(select_image,(select_image.get_width() * scale_factor, select_image.get_height() * scale_factor))
        screen.blit(select_image, (700,500))

        #drone_one_button.draw(screen)
        #drone_two_button.draw(screen)
        #drone_three_button.draw(screen)
        #drone_four_button.draw(screen)
        #drone_five_button.draw(screen)
        #drone_six_button.draw(screen)
        #drone_seven_button.draw(screen)
        #drone_eight_button.draw(screen)

    #player select menu
    if player_select:
        display_menu("images/player_select.png")
        #player_1_select = ui.Button((0,255,0),width/7,height - 300,225,225,"Player 1")
        #player_2_select = ui.Button((0,255,0),width * (2/3),height - 300,225,225,"Player 2")
        player_1_select.draw(screen)
        player_2_select.draw(screen)
    
    #multiplayer lobby menus
    if multiplayer_lobby:
        display_menu("images/Multiplayer Lobby/lobby.png")
        #host_button = ui.Button((0,255,0),width/7,height/4,225,350,"host")
        host_button.draw(screen)
        #join_button = ui.Button((0,255,0),width * (2/3),height/4,225,350,"join")
        join_button.draw(screen)
    
    if host_lobby:
        display_menu("images/Multiplayer Lobby/Host.png")
        ip = ui.Text(width/2,height/2,100,100,socket.gethostbyname(socket.gethostname()))
        ip.draw(screen,100)

        port = font.render(port_add, 1, (0, 0, 0))
        screen.blit(port,(width * (8/10),height * (9/10)))

    if join_lobby:
        display_menu("images/Multiplayer Lobby/Join.png")

        ip = font.render(ip_add, 1, (0, 0, 0))
        screen.blit(ip,(width/6,height * (6/10)))

        port = font.render(port_add, 1, (0, 0, 0))
        screen.blit(port,(width * (8/10),height * (6/10)))

    if waiting:
        display_menu("images/waiting.png")
    

    #health checker
    if health <= 0:
        you_lose = True

    if game_start and game_audio:
        pygame.mixer.music.stop()
        gameplay_music.play_on_loop()
        game_audio = False

    #modify video feed for pygame
    frame = np.fliplr(frame)
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    surf = pygame.surfarray.make_surface(frame)
    
    for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                #quit game at any time by pressing q
                if event.key == pygame.K_q:
                    pygame.quit()
                    client.close()
                    break
                elif event.key == pygame.K_SPACE:

                    #press space at the end of game to replay
                    if you_lose or you_win:
                        you_lose = False
                        you_win = False
                        health = 100
                        enemy_health = 100
                        attack_cooldown_1 = 0
                        attack_cooldown_2 = 0
                        attack_cooldown_3 = 0

                    #press space to start game
                    if main_menu:
                        main_menu = False
                        game_mode_select = True

                #player select
                elif event.key == pygame.K_1:
                    if player_select:
                        p1 = True
                        player_select = False
                        game_start = True

                elif event.key == pygame.K_2:
                    if player_select:
                        player_select = False
                        game_start = True
            
            #button stuff
            if event.type == pygame.constants.MOUSEBUTTONDOWN:
                click = True
            else:
                pass
            pygame.event.clear()

    if click:
        print("click")
        event = pygame.mouse.get_pos()
        if player_select:
            if player_1_select.isOver(event):
                p1 = True
                player_select = False
                message = 'START 1'
                client.send(message.encode('ascii'))
                waiting = True
                
            if player_2_select.isOver(event):
                p1 = False
                player_select = False
                message = 'START 2'
                client.send(message.encode('ascii'))
                waiting = True
        
        #elif drone_select:
        elif game_mode_select:
            if play_button.isOver(event):
                drone_select = True
                game_mode_select = False
            if demo_button.isOver(event):
                game_mode_select = False
                player_select = True
            if settings_button.isOver(event):
                print("settings button pressed")
        
        elif drone_select:
            if drone_one_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[0] = True
            elif drone_two_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[1] = True
            elif drone_three_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[2] = True
            elif drone_four_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[3] = True
            elif drone_five_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[4] = True
            elif drone_six_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[5] = True
            elif drone_seven_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[6] = True
            elif drone_eight_button.isOver(event):
                drone_desc_activate = [False, False, False, False, False, False, False, False]
                drone_desc_activate[7] = True
        
        elif main_menu:
            main_menu = False
            game_mode_select = True
        
        elif game_start:  
            #attack 1
            if fire_button1.isOver(event):
                #hit detection
                weapon1_audio.play()
                if pink_detection.is_detected() and attack_cooldown_1 <= pygame.time.get_ticks(): 
                    print("hit!")
                    message = ch.attack1(p1)
                    client.send(message.encode('ascii'))
                    attack_damage = ch.return_attack_damage(message)
                    enemy_health = enemy_health - attack_damage[0]
                    damage_done = attack_damage[0]
                    attack_cooldown_1 = pygame.time.get_ticks() + attack_damage[1]
                    hit = True
                    if enemy_health <= 0:
                        you_win = True
                    
            
            #attack 2
            elif fire_button2.isOver(event):
                #hit detection
                weapon1_audio.play()
                if pink_detection.is_detected() and attack_cooldown_2 <= pygame.time.get_ticks(): 
                    print("hit!")
                    message = ch.attack2(p1)
                    client.send(message.encode('ascii'))
                    attack_damage = ch.return_attack_damage(message)
                    enemy_health = enemy_health - attack_damage[0]
                    damage_done = attack_damage[0]
                    attack_cooldown_2 = pygame.time.get_ticks() + attack_damage[1]
                    hit = True
                    if enemy_health <= 0:
                        you_win = True
                    

            #special 3
            elif fire_button3.isOver(event):
                #hit detection
                weapon1_audio.play()
                if attack_cooldown_3 <= pygame.time.get_ticks(): 
                    print("hit!")
                    message = ch.attack3(p1)
                    client.send(message.encode('ascii'))
                    attack_damage = ch.return_attack_damage(message)
                    #enemy_health = enemy_health - attack_damage[0]
                    attack_cooldown_3 = pygame.time.get_ticks() + attack_damage[1]
                    if enemy_health <= 0:
                        you_win = True

        click = False
        pygame.event.clear()
        pygame.display.update()

    if game_start:
        curr_time = pygame.time.get_ticks()

        screen.blit(surf, (0,0))

        #look for pink
        pink_detection.see()

        #damage reduction timer
        if effect_time > curr_time and not viper and not wyver:
            cooldown_text = ui.Button((0,0,255),(width - 200) // 2,height-50,200,50,str((effect_time-pygame.time.get_ticks())//1000) + "s")
            cooldown_text.draw(screen)
        elif effect_time_other_player >= curr_time and not viper and not wyver:
            if hit:
                enemy_health += ((1-damage_reduction) * damage_done)
                hit = False
        elif effect_time < curr_time or effect_time_other_player < curr_time and dam_re:
            dam_re = False
        elif not viper and not wyver:
            damage_reduction = 1

        #viper drone specifics
        if viper and effect_time >= curr_time and not wyver:
            if poison_damage > ((effect_time-pygame.time.get_ticks())//1000):
                poison_damage = (effect_time-pygame.time.get_ticks())//1000
                enemy_health -= poison_damage

        elif viper and effect_time_other_player >= curr_time and not wyver:
            if poison_damage > ((effect_time_other_player-pygame.time.get_ticks())//1000):
                poison_damage = (effect_time_other_player-pygame.time.get_ticks())//1000
                health -= poison_damage

        elif effect_time < curr_time or effect_time_other_player < curr_time and viper:
            viper = False
        elif not dam_re and not viper and not wyver: 
            damage_reduction = 1
            poison_damage = 10
        
        #wyver drone specifics
        if wyver and effect_time >= curr_time and not viper:
            cooldown_text = ui.Button((0,0,255),(width - 200) // 2,height-50,200,50,str((effect_time-pygame.time.get_ticks())//1000) + "s")
            cooldown_text.draw(screen)
            if hit:
                enemy_health += ((1-damage_reduction) * damage_done)
                hit = False
        #elif not viper and effect_time_other_player >= curr_time and wyver:
            
        elif effect_time < curr_time or effect_time_other_player < curr_time and wyver:
            wyver = False
        

        #draw fire button
        fire_button1 = ui.Button((0,0,255),(width - 300) // 2,height-50,50,50,"1!")
        fire_button1.draw(screen)

        fire_button2 = ui.Button((0,255,0),(width - 200) // 2,height-50,50,50,"2!")
        fire_button2.draw(screen)

        fire_button3 = ui.Button((0,255,255),(width + 100) // 2,height-50,50,50,"3!")
        fire_button3.draw(screen)
        #draw health bars
        ui.draw_health_bar(health, enemy_health,screen)

        #crosshair
        crosshair = pygame.image.load("images/Crosshairs/crosshair086.png").convert_alpha() 
        screen.blit(crosshair, (width/2, height/2))

        #weapon images
        scale_factor = 1.5
        weapon1_image = pygame.image.load("images/weapons/spaceMissiles_024.png").convert_alpha()
        weapon1_image = pygame.transform.scale(weapon1_image,(weapon1_image.get_width() * scale_factor, weapon1_image.get_height() * scale_factor))
        screen.blit(weapon1_image, (width * (74.5/100), height - 110))

        weapon2_image = pygame.image.load("images/weapons/spaceMissiles_021.png").convert_alpha() 
        weapon2_image = pygame.transform.scale(weapon2_image,(weapon2_image.get_width() * scale_factor, weapon2_image.get_height() * scale_factor))
        screen.blit(weapon2_image, (width * (83.75/100), height - 110))

        weapon3_image = pygame.image.load("images/ui/ability.png").convert_alpha() 
        weapon3_image = pygame.transform.scale(weapon3_image,(weapon3_image.get_width() * scale_factor, weapon3_image.get_height() * scale_factor))
        screen.blit(weapon3_image, (width * (91/100), height - 125))

        
        if attack_cooldown_3 > curr_time:
            if ((attack_cooldown_3-pygame.time.get_ticks())//1000) > max_check3:
                max_check3 = ((attack_cooldown_3-pygame.time.get_ticks())//1000)

            #cooldown_text = ui.Button((255,0,0),(width - 200) // 2,height-50,200,50,str((attack_cooldown-pygame.time.get_ticks())//1000) + "s")
            #cooldown_text.draw(screen)

            scale_factor = 0.9
            rate = ((((attack_cooldown_3 - curr_time)/1000)) / max_check3)

            s3 = pygame.Surface((weapon3_image.get_width() * scale_factor * (rate*0.8), weapon3_image.get_height() * scale_factor), pygame.SRCALPHA)   # per-pixel alpha
            s3.fill((255,0,0,128))                         
            screen.blit(s3, (width * (91.5/100), height - 120))
        else:
            max_check3 = 0
        
        if attack_cooldown_2 > curr_time:
            if ((attack_cooldown_2-pygame.time.get_ticks())//1000) > max_check2:
                max_check2 = ((attack_cooldown_2-pygame.time.get_ticks())//1000)

            scale_factor = 0.9
            rate = ((((attack_cooldown_2 - curr_time)/1000)) / max_check2)

            s2 = pygame.Surface((weapon3_image.get_width() * scale_factor * (rate*0.8), weapon3_image.get_height() * scale_factor), pygame.SRCALPHA)   # per-pixel alpha
            s2.fill((255,0,0,128))                         
            screen.blit(s2, (width * (81.5/100), height - 120))
        else:
            max_check2 = 0

        if attack_cooldown_1 > curr_time:
            if ((attack_cooldown_1-pygame.time.get_ticks())//1000) > max_check1:
                max_check1 = ((attack_cooldown_1-pygame.time.get_ticks())//1000)

            scale_factor = 0.9
            rate = ((((attack_cooldown_1 - curr_time)/1000)) / max_check1)

            s = pygame.Surface((weapon3_image.get_width() * scale_factor * (rate*0.8), weapon3_image.get_height() * scale_factor), pygame.SRCALPHA)   # per-pixel alpha
            s.fill((255,0,0,128))                         
            screen.blit(s, (width * (71.5/100), height - 120))
        else:
            max_check1 = 0

        scale_factor = 2
        overlay1 = pygame.image.load("images/ui/border.png").convert_alpha()
        overlay1 = pygame.transform.scale(overlay1,(overlay1.get_width() * scale_factor, overlay1.get_height() * scale_factor))
        screen.blit(overlay1, (width * (70/100), height - 140))

        overlay2 = pygame.image.load("images/ui/border.png").convert_alpha() 
        overlay2 = pygame.transform.scale(overlay2,(overlay2.get_width() * scale_factor, overlay2.get_height() * scale_factor))
        screen.blit(overlay2, (width * (80/100), height - 140))

        overlay3 = pygame.image.load("images/ui/border.png").convert_alpha() 
        overlay3 = pygame.transform.scale(overlay3,(overlay3.get_width() * scale_factor, overlay3.get_height() * scale_factor))
        screen.blit(overlay3, (width * (90/100), height - 140))

        ##game over screen##
        if you_lose or you_win:
            if you_win:
                display_menu("images/you_win.png")
            elif you_lose:
                display_menu("images/game_over.png")

    rval, frame = vc.read()
    pygame.display.flip()

    #press q to quit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pygame.quit()
        client.close()
        break