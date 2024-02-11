import socket
import threading
import pygame
import cv2
import numpy as np
import ui
import vision
import audio

#initalize pygame window
pygame.init()
width, height = 1280, 720
nickname = "Player"
#fullscreen
#screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
#not full screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fight Flight")

#health bars
health = 100
enemy_health = 100
health_bar_width, health_bar_height = width - 40, 30
health_bar_rect = pygame.Rect(20, height - health_bar_height - 20, 10, 10)
enemy_health_bar_width, enemy_health_bar_height = width - 40, 30
enemy_health_bar_rect = pygame.Rect(50, height - enemy_health_bar_width - 20, enemy_health_bar_width, enemy_health_bar_height)

#settings parameters
audio_level = 0.5

#drone class variables
basic = False
wings_of_corona = False
steel_talons = False
galm_corps = False
foehn_wind = False

#menu game variables
main_menu = False
game_mode_select = False
player_select = False
game_start = False
font = pygame.font.SysFont('comicsans', 36)
you_lose = False
you_win = False

#multiplayer lobby menus
multiplayer_lobby = False
join_lobby = True
host_lobby = False
ip_add = ''
port_add = ''
text_count = 0
host_button = ui.Button((0,255,0),width/7,height/4,225,350,"host")
join_button = ui.Button((0,255,0),width * (2/3),height/4,225,350,"join")

#play main menu music on startup
pygame.mixer.init()
main_music = audio.Music('audio/menu_music.mp3')
main_music.play_on_loop()

#initalize opencv
#vc = cv2.VideoCapture(0,cv2.CAP_DSHOW) #windows
vc = cv2.VideoCapture(0) #macos
vc.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
rval, frame = vc.read()
pink_detection = vision.Vision(rval,vc,frame,height,width)

def receive():
    global health
    while True:
        try:
            #How damage is calculated
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == '1':
                if p1:    
                    health = health - 10
            elif message == '2':
                if not p1:
                    health = health - 10   
            elif message == 'START':
                if join_lobby:
                    join_lobby = False
                    game_start = True
                if host_lobby:
                    host_lobby = False
                    game_start = True
            else:
                print(message)
                # You can handle displaying the message in the Pygame window here
        except:
            print("An error occurred!")
            client.close()
            break

def display_menu(image):
    img = pygame.image.load(image).convert()
    img = pygame.transform.scale(img, (width,height))
    screen.blit(img,(0,0))

#receive_thread = threading.Thread(target=receive)
#receive_thread.start()
while True:
    
    #menu screens
    #main menu
    if main_menu:
        display_menu("images/main_menu.png")
    
    #gamemode select menu
    if game_mode_select:
        display_menu("images/gamemode_select.png")

        play_button = ui.Button((0,255,0),width/7,height/4,225,350,"play")
        #play_button.draw(screen)
        demo_button = ui.Button((0,255,0),width * (2/3),height/4,225,350,"demo")
        #demo_button.draw(screen)
        settings_button = ui.Button((0,255,0),(width //2) - 120,height-130,220,70,"settings")
        #settings_button.draw(screen)

    #player select menu
    if player_select:
        display_menu("images/player_select.png")
    
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

    #health checker
    if health <= 0:
        you_lose = True

    #look for the pink drone
    

    #modify video feed for pygame
    frame = np.fliplr(frame)
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    surf = pygame.surfarray.make_surface(frame)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if join_lobby:
                    if event.key == pygame.K_RETURN:
                        text_count = text_count + 1
                        if text_count == 2:
                            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            client.connect((ip_add, int(port_add)))
                    elif event.key == pygame.K_BACKSPACE:
                        if text_count == 0:
                            ip_add = ip_add[:-1]
                        else:
                            port_add = ip_add[:-1]
                    else:
                        if text_count == 0:
                            ip_add += event.unicode
                        else:
                            port_add += event.unicode
                
                if host_lobby:
                    if event.key == pygame.K_RETURN:
                        text_count = text_count + 1
                        if text_count == 1:
                            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            client.connect((socket.gethostbyname(socket.gethostname()), int(port_add)))
                    elif event.key == pygame.K_BACKSPACE:
                        port_add = ip_add[:-1]
                    else:
                        port_add += event.unicode
                    
                #quit game at any time by pressing q
                elif event.key == pygame.K_q:
                    pygame.quit()
                    break
                if event.key == pygame.K_SPACE:
                    #press space at the end of game to replay
                    if you_lose or you_win:
                        you_lose = False
                        you_win = False
                        health = 100
                        enemy_health = 100
                    #press space to start game
                    if main_menu:
                        main_menu = False
                        game_mode_select = True
                #player select
                if event.key == pygame.K_1:
                    if player_select:
                        p1 = True
                        player_select = False
                        game_start = True
                if event.key == pygame.K_2:
                    if player_select:
                        p1 = False
                        player_select = False
                        game_start = True
            
            #button stuff
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button rectangle
                if multiplayer_lobby:
                    if host_button.isOver(event.pos):
                        multiplayer_lobby = False
                        host_lobby = True

                    if join_button.isOver(event.pos):
                        multiplayer_lobby = False
                        join_lobby = True

                if game_mode_select:
                    if play_button.isOver(event.pos):
                        player_select = True
                        game_mode_select = False
                    if demo_button.isOver(event.pos):
                        game_mode_select = False
                        multiplayer_lobby = True
                    if settings_button.isOver(event.pos):
                        print("settings button pressed")

                if game_start:  
                    if fire_button.isOver(event.pos):
                        #hit detection
                        if pink_detection.is_detected(): 
                            print("hit!")
                            if p1:
                                message = '2'
                            else:
                                message = '1'
                            #client.send(message.encode('ascii'))
                            enemy_health = enemy_health - 10
                            if enemy_health <= 0:
                                you_win = True
    
    if game_start:
        pygame.mixer.init()
        main_music.stop()
        screen.blit(surf, (0,0))
        
        pink_detection.see()

        #draw fire button
        fire_button = ui.Button((0,0,255),(width - 200) // 2,height-50,200,50,"FIRE!")
        fire_button.draw(screen)
        
        current_health_rect = pygame.Rect(width/2, 10, health * (health_bar_width / 1000), health_bar_height)
        pygame.draw.rect(screen, (255,0,0), current_health_rect)
        health_text = font.render(f"You: {round(health)}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=current_health_rect.center)
        screen.blit(health_text, text_rect)
        
        enemy_health_rect = pygame.Rect(width/2 - enemy_health, 10, enemy_health * (health_bar_width / 1000), health_bar_height)
        pygame.draw.rect(screen, (0,0,255), enemy_health_rect)
        enemy_health_text = font.render(f"Enemy: {round(enemy_health)}", True, (255, 255, 255))
        text_rect = enemy_health_text.get_rect(center=enemy_health_rect.center)
        screen.blit(enemy_health_text, text_rect)

        #crosshair
        crosshair = pygame.image.load("images/Crosshairs/crosshair086.png").convert_alpha() 
        screen.blit(crosshair, (width/2, height/2))

        ##game over screen##
        if you_lose or you_win:
            if you_win:
                img = pygame.image.load("images/you_win.png").convert()
                img = pygame.transform.scale(img, (width,height))
                screen.blit(img,(0,0))
            elif you_lose:
                img = pygame.image.load("images/game_over.png").convert()
                img = pygame.transform.scale(img, (width,height))
                screen.blit(img,(0,0))


    rval, frame = vc.read()
    pygame.display.flip()

    #press q to quit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pygame.quit()
        break