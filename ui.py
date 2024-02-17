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
