import pygame

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True    
        return False

class Text:
    def __init__(self,x,y,width,height,text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self,win,size):
        font = pygame.font.SysFont('comicsans', size)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

def draw_health_bar(health, enemy_health,screen):
    width, height = 1280, 720
    health_bar_width, health_bar_height = width - 40, 30
    health_bar_rect = pygame.Rect(20, height - health_bar_height - 20, 10, 10)
    enemy_health_bar_width, enemy_health_bar_height = width - 40, 30
    enemy_health_bar_rect = pygame.Rect(50, height - enemy_health_bar_width - 20, enemy_health_bar_width, enemy_health_bar_height)
    health_font = pygame.font.SysFont('comicsans', 20)

    current_health_rect = pygame.Rect(10, height - 40, health * (health_bar_width / 500), health_bar_height)
    pygame.draw.rect(screen, (0,0,255), current_health_rect)
    health_text = health_font.render(f"You: {round(health)}", True, (255, 255, 255))
    text_rect = health_text.get_rect(center=current_health_rect.center)
    screen.blit(health_text, text_rect)
    
    enemy_health_rect = pygame.Rect(width/20, 10, enemy_health * (health_bar_width / 100), health_bar_height)
    pygame.draw.rect(screen, (255,0,0), enemy_health_rect)
    enemy_health_text = health_font.render(f"Enemy: {round(enemy_health)}", True, (255, 255, 255))
    text_rect = enemy_health_text.get_rect(center=enemy_health_rect.center)
    screen.blit(enemy_health_text, text_rect)

    scale_factor = 1.5
    heart = pygame.image.load("images/ui/tile_heart.png").convert_alpha() 
    heart = pygame.transform.scale(heart,(heart.get_width() * scale_factor, heart.get_height() * scale_factor))
    screen.blit(heart,(1,-20))

def drone_selection_menu(screen, font_menu, width, height):
    scale_factor = 2.5

    text = font_menu.render('CHOOSE YOUR FIGHTER', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (width // 2, 60)
    screen.blit(text, textRect)

    panel1 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel1 = pygame.transform.scale(panel1,(panel1.get_width() * scale_factor, panel1.get_height() * scale_factor))
    screen.blit(panel1, (50,150))

    panel2 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel2 = pygame.transform.scale(panel2,(panel2.get_width() * scale_factor, panel2.get_height() * scale_factor))
    screen.blit(panel2, (50,270))

    panel3 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel3 = pygame.transform.scale(panel3,(panel3.get_width() * scale_factor, panel3.get_height() * scale_factor))
    screen.blit(panel3, (50,390))

    panel4 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel4 = pygame.transform.scale(panel4,(panel4.get_width() * scale_factor, panel4.get_height() * scale_factor))
    screen.blit(panel4, (50,510))

    panel5 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel5 = pygame.transform.scale(panel5,(panel5.get_width() * scale_factor, panel5.get_height() * scale_factor))
    screen.blit(panel5, (190,150))

    panel6 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel6 = pygame.transform.scale(panel6,(panel6.get_width() * scale_factor, panel6.get_height() * scale_factor))
    screen.blit(panel6, (190,270))

    panel7 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel7 = pygame.transform.scale(panel7,(panel7.get_width() * scale_factor, panel7.get_height() * scale_factor))
    screen.blit(panel7, (190,390))

    panel8 = pygame.image.load("images/ui/border.png").convert_alpha()
    panel8 = pygame.transform.scale(panel8,(panel8.get_width() * scale_factor, panel8.get_height() * scale_factor))
    screen.blit(panel8, (190,510))
    
    scale_factor = 5
    desc_panel = pygame.image.load("images/ui/desc_panel.png").convert_alpha()
    desc_panel = pygame.transform.scale(desc_panel,(desc_panel.get_width() * scale_factor * 1.5, desc_panel.get_height() * scale_factor))
    screen.blit(desc_panel, (500,150))

    scale_factor = 2
    drone1 = pygame.image.load("images/drones/enemy_A.png").convert_alpha()
    drone1 = pygame.transform.scale(drone1,(drone1.get_width() * scale_factor, drone1.get_height() * scale_factor))
    screen.blit(drone1, (65,160))

    drone2 = pygame.image.load("images/drones/enemy_B.png").convert_alpha()
    drone2 = pygame.transform.scale(drone2,(drone2.get_width() * scale_factor, drone2.get_height() * scale_factor))
    screen.blit(drone2, (65,285))

    scale_factor = 1.6
    drone3 = pygame.image.load("images/drones/enemy_C.png").convert_alpha()
    drone3 = pygame.transform.scale(drone3,(drone3.get_width() * scale_factor, drone3.get_height() * scale_factor))
    screen.blit(drone3, (79,425))

    scale_factor = 2
    drone4 = pygame.image.load("images/drones/enemy_D.png").convert_alpha()
    drone4 = pygame.transform.scale(drone4,(drone4.get_width() * scale_factor, drone4.get_height() * scale_factor))
    screen.blit(drone4, (67,527))

    drone5 = pygame.image.load("images/drones/enemy_E.png").convert_alpha()
    drone5 = pygame.transform.scale(drone5,(drone5.get_width() * scale_factor, drone5.get_height() * scale_factor))
    screen.blit(drone5, (205,165))

    drone6 = pygame.image.load("images/drones/satellite_D.png").convert_alpha()
    drone6 = pygame.transform.scale(drone6,(drone6.get_width() * scale_factor, drone6.get_height() * scale_factor))
    screen.blit(drone6, (205,285))

    drone7 = pygame.image.load("images/drones/ship_sidesA.png").convert_alpha()
    drone7 = pygame.transform.scale(drone7,(drone7.get_width() * scale_factor, drone7.get_height() * scale_factor))
    screen.blit(drone7, (205,400))

    drone8 = pygame.image.load("images/drones/ship_sidesB.png").convert_alpha()
    drone8 = pygame.transform.scale(drone8,(drone8.get_width() * scale_factor, drone8.get_height() * scale_factor))
    screen.blit(drone8, (205,525))


def display_player_selection_menu(screen, width, height):
    font = pygame.font.Font('images/ui/neuropol.otf', 45)
    font_header = pygame.font.Font('images/ui/recharge bd.otf', 90)

    text = font_header.render('PLAYER 1 OR 2?', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (width // 2, 70)
    screen.blit(text, textRect)

    scale_factor = 2.5
    panel1 = pygame.image.load("images/ui/glassPanel_cornerBL.png").convert_alpha()
    panel1 = pygame.transform.scale(panel1,(panel1.get_width() * scale_factor * 1.5, panel1.get_height() * scale_factor))
    screen.blit(panel1, (100,300))

    panel2 = pygame.image.load("images/ui/glassPanel_cornerTR.png").convert_alpha()
    panel2 = pygame.transform.scale(panel2,(panel2.get_width() * scale_factor * 1.5, panel2.get_height() * scale_factor))
    screen.blit(panel2, (800,300))

    player_1_text = font.render('PLAYER 1', True, (255,255,255))
    nameRect = player_1_text.get_rect()
    nameRect.center = (285, 425)
    screen.blit(player_1_text, nameRect)

    player_2_text = font.render('PLAYER 2', True, (255,255,255))
    nameRect = player_2_text.get_rect()
    nameRect.center = (985, 425)
    screen.blit(player_2_text, nameRect)

def display_conclusion_menu(screen, width, height):
    
    font = pygame.font.Font('images/ui/neuropol.otf', 45)
    font_header = pygame.font.Font('images/ui/recharge bd.otf', 90)

    scale_factor = 2.5
    panel1 = pygame.image.load("images/ui/glassPanel_cornerBL.png").convert_alpha()
    panel1 = pygame.transform.scale(panel1,(panel1.get_width() * scale_factor * 1.5, panel1.get_height() * scale_factor))
    screen.blit(panel1, (100,300))

    panel2 = pygame.image.load("images/ui/glassPanel_cornerTR.png").convert_alpha()
    panel2 = pygame.transform.scale(panel2,(panel2.get_width() * scale_factor * 1.5, panel2.get_height() * scale_factor))
    screen.blit(panel2, (800,300))

    player_1_text = font.render('REPLAY', True, (0,0,0))
    nameRect = player_1_text.get_rect()
    nameRect.center = (285, 425)
    screen.blit(player_1_text, nameRect)

    player_2_text = font.render('MENU', True, (0,0,0))
    nameRect = player_2_text.get_rect()
    nameRect.center = (985, 425)
    screen.blit(player_2_text, nameRect)
