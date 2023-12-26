import socket
import threading
import pygame
import cv2
import numpy as np

# Get the host IP address, PORT address
HOST = socket.gethostbyname(socket.gethostname())
PORT = 55555

#initalize pygame window
pygame.init()
width, height = 1280, 720
nickname = "Player"
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fight Flight")

#temp button stuff
button_width, button_height = 200, 50
button_color = (0, 128, 255)
button_text_color = (255, 255, 255)
button_font = pygame.font.Font(None, 36)
button_x = (width - button_width) // 2
button_y = (height // 2) - 10
font = pygame.font.Font(None, 36)

#health bars
health = 100
enemy_health = 100
health_bar_width, health_bar_height = width - 40, 30
health_bar_rect = pygame.Rect(20, height - health_bar_height - 20, 10, 10)
enemy_health_bar_width, enemy_health_bar_height = width - 40, 30
enemy_health_bar_rect = pygame.Rect(50, height - enemy_health_bar_width - 20, enemy_health_bar_width, enemy_health_bar_height)

#misc game variables
you_lose = False
you_win = True

#initalize opencv
vc = cv2.VideoCapture(0,cv2.CAP_DSHOW)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
rval, frame = vc.read()
detected = False

#connect to server
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((HOST, PORT))

def receive():
    global health
    while True:
        try:
            #How damage is calculated
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == '2':
                health = health - 1
            elif message == '2M':
                health = health - 25
            elif message == '2E':
                health = health - 50
            elif message == '2P':
                health = health - 10
            else:
                print(message)
                # You can handle displaying the message in the Pygame window here
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    message = '1'
    client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

while True:
    #define frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #define color range (high and low)
    lower_pink = np.array([140, 50, 50])
    upper_pink = np.array([180, 255, 255])

    #draw frame with only color, black and white
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    #find color in original frame
    colorcnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    #check if drone is in center of screen (fire range)
    if len(colorcnts) > 0:
        color_area = max(colorcnts, key=cv2.contourArea)
        (xg,yg,wg,hg) = cv2.boundingRect(color_area)
        #print((xg,yg,wg,hg))
        #cv2.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(0,255,0),2)
        if xg <= width/2 and yg <= height/2 and yg + hg >= height/2 and xg + wg >= width/2:
            detected = True
        else:
            detected = False

    #display colors
    #if frame is not None:
      #cv2.imshow("preview", frame)
      #cv2.imshow('mask',mask)
      #cv2.imshow('res',res)
    
    #modify video feed for pygame
    frame = np.fliplr(frame)
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    surf = pygame.surfarray.make_surface(frame)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button rectangle
                if button_rect.collidepoint(event.pos):
                    if detected: 
                        #print(health - 1)
                        message = '2'
                        #client.send(message.encode('ascii'))
                        enemy_health = enemy_health - 1
    screen.blit(surf, (0,0))

    button_rect = pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    button_text = button_font.render("Fire!", True, button_text_color)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    name_text = font.render(str(health), True, button_text_color)
    screen.blit(name_text,(text_rect.left, text_rect.top - 30))
    
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

    crosshair = pygame.image.load("crosshair188.png").convert()
    screen.blit(crosshair, (width/2, height/2))

    rval, frame = vc.read()
    pygame.display.flip()
    #press q to quit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break