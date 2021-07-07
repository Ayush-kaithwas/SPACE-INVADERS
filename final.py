import pygame
from pygame import mixer
import os
import time
import random


# Initializing
pygame.font.init()
pygame.init()


WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
fire = 0
Score = 0

# Title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)

# Load images
INVADER1_SPACE_SHIP = pygame.image.load('images/red_enemy.png')
INVADER2_SPACE_SHIP = pygame.image.load('images/green_enemy.png')
INVADER3_SPACE_SHIP = pygame.image.load('images/blue_enemy.png')
INVADER4_SPACE_SHIP = pygame.image.load('images/yellow_enemy.png')
ALIEN1 = pygame.image.load('images/alien-1.png')
ALIEN2 = pygame.image.load('images/alien-2.png')
ALIEN3 = pygame.image.load('images/alien-3.png')


# Bullets
RED_LASER = pygame.image.load('images/red_laser.png')
GREEN_LASER = pygame.image.load('images/green_laser.png')
BLUE_LASER = pygame.image.load('images/blue_laser.png')
YELLOW_LASER = pygame.image.load('images/yellow_laser.png')
PLAYER_LASER = pygame.image.load('images/bullet-1.png')

# Home Image
homeImage = pygame.image.load('images/bg-2.jpg').convert_alpha()# Changing Height and width using convert_alpha method
homeImage = pygame.transform.scale(homeImage, (WIDTH, HEIGHT))

# Ingame Image
inGameImage = pygame.image.load('images/bg-1.png').convert_alpha()# Changing Height and width using convert_alpha method
inGameImage = pygame.transform.scale(inGameImage, (WIDTH, HEIGHT))


# Player
PLAYER_SPACE_SHIP = pygame.image.load("images/player-1.png")

# To Render Text
def text_screen(text, color, x, y, z):
    text_weigh = pygame.font.SysFont('freesansbold.ttf', z)
    screen_text = text_weigh.render(text, True, color)
    SCREEN.blit(screen_text, [x,y])

# To Show Image
def show_image(image, x , y):
    Img = pygame.image.load(image)
    SCREEN.blit(Img, (x, y))



class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        SCREEN.blit(self.img, (self.x, self.y))
        
    def move(self, velocity):
        self.y += velocity
        
    def off_screen(self,height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30
    
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)    
        
    def getWidth(self):
        return self.ship_img.get_width()
    
    def getHeight(self):
        return self.ship_img.get_height()
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    
    def shoot(self):
        if self.cool_down_counter == 0:
            if fire == 1:
                laser = Laser(self.x +16, self.y, self.laser_img)
                self.lasers.append(laser)
                bullet_sound = mixer.Sound('sounds/shoot.wav')
                bullet_sound.play()
                self.cool_down_counter = 1
            elif fire == 2:
                laser1 = Laser(self.x - 3, self.y+ 4, self.laser_img)
                laser2 = Laser(self.x +36 , self.y, self.laser_img)
                self.lasers.append(laser1)
                self.lasers.append(laser2)
                bullet_sound = mixer.Sound('sounds/shoot.wav')
                bullet_sound.play()
                self.cool_down_counter = 1
            elif fire == 3:
                laser1 = Laser(self.x -3, self.y+4, self.laser_img)
                laser2 = Laser(self.x +16 , self.y, self.laser_img)
                laser3 = Laser(self.x +36 , self.y, self.laser_img)
                self.lasers.append(laser1)
                self.lasers.append(laser2)
                self.lasers.append(laser3)
                bullet_sound = mixer.Sound('sounds/shoot.wav')
                bullet_sound.play()
                self.cool_down_counter = 1
            elif fire == 4:
                laser1 = Laser(self.x-10, self.y+4, self.laser_img)
                laser2 = Laser(self.x +8 , self.y, self.laser_img)
                laser3 = Laser(self.x +30 , self.y, self.laser_img)
                laser4 = Laser(self.x +46 , self.y, self.laser_img)
                self.lasers.append(laser1)
                self.lasers.append(laser2)
                self.lasers.append(laser3)
                self.lasers.append(laser4)
                bullet_sound = mixer.Sound('sounds/shoot.wav')
                bullet_sound.play()
                self.cool_down_counter = 1
            else:
                laser = Laser(self.x + 16 , self.y, self.laser_img)
                self.lasers.append(laser)
                bullet_sound = mixer.Sound('sounds/shoot.wav')
                bullet_sound.play()
                self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y, health =100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.remain_health = health
        
    def move_lasers(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        global Score
                        Score += 1
                        explosion_sound = mixer.Sound('sounds/invaderkilled.wav')
                        explosion_sound.play()
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)



    def draw(self, window):
        super().draw(window)
        self.healthBar(window)

    def healthBar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 15))
        
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 15))
        


class Enemy(Ship):
    COLOR_MAP = {
            "red" : (INVADER1_SPACE_SHIP, RED_LASER),
            "green" :(INVADER2_SPACE_SHIP, GREEN_LASER),
            "blue" : (INVADER3_SPACE_SHIP, BLUE_LASER),
            "yellow" : (INVADER4_SPACE_SHIP, YELLOW_LASER),
            "alien1" : (ALIEN1, GREEN_LASER),
            "alien2" : (ALIEN2, BLUE_LASER),
            "alien3" : (ALIEN3, RED_LASER)
        }
    def __init__(self, x, y, color, health =100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1





def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

        
def gameloop():
    run = True
    FPS = 60
    global Score
    level = 0
    lives = 5
    lost = False
    lost_count = 0
    player_velocity = 5
    laser_velocity = 7
    
    enemies = []
    wave_length = 5
    enemy_velocity = 1    
    
    player = Player(300, 500)
    
    clock = pygame.time.Clock()
    
    # Background Sound
    mixer.music.load('sounds/bg-1.mp3')
    mixer.music.play(-1)
    
    def redraw():
        SCREEN.blit(inGameImage, (0,0))
        # text 
        text_screen(f"Lives : {lives}",(255, 255, 255), 10, 10, 30)
        text_screen(f"Score : {Score}",(255, 255, 255), 10, 40, 30)
        text_screen(f"Level : {level}",(255, 255, 255), (WIDTH - 110), 10, 30)


        for enemy in enemies:
            enemy.draw(SCREEN)
            
        player.draw(SCREEN)
        
        if lost:
            text_screen("Game Over", (255, 255, 255), 280, 280, 60)
            text_screen("Press Enter To Play Again", (255, 255, 255), 220, 330, 40)
            text_screen(f"Your Score : {Score}", (255, 255, 255), 300, 380, 40)
        
            for event in pygame .event.get():
                if event.type == pygame.QUIT:
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
    
    
        pygame.display.update()
    

    while run:
        clock.tick(FPS)
        if lives <= 0 or player.health <=0:
            lost =True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 1:
                run = False
            else:
                continue
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            enemy_velocity += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1000*level, -100), random.choice(["red", "blue", "green", "yellow", "alien1", "alien2", "alien3"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    lives = lives + 1 

                if event.key == pygame.K_f:
                    player.remain_health = player.health = 100


        keys = pygame.key.get_pressed()
                        
        if keys[pygame.K_LEFT]and (player.x - player_velocity) > 0:
            player.x -= player_velocity
                        
        if keys[pygame.K_RIGHT]and (player.x + player_velocity + player.getWidth()) < WIDTH:
            player.x += player_velocity
                        
        if keys[pygame.K_UP] and (player.y - player_velocity) > 0:
            player.y -= player_velocity
        
        if keys[pygame.K_DOWN] and (player.y + player_velocity +player.getHeight() + 30 )< HEIGHT:
            player.y += player_velocity
                 
        if keys[pygame.K_SPACE]:
            player.shoot()
            
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)
            
            if random.randrange(0, 4*60) == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                enemy_explosion_sound = mixer.Sound('sounds/explosion.wav')
                enemy_explosion_sound.play()
                enemies.remove(enemy)
              
            elif enemy.y + enemy.getHeight() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
                
              
        player.move_lasers(-laser_velocity, enemies)
        redraw()

def welcome():
    global fire, PLAYER_SPACE_SHIP
    exit_game = False
    SCREEN.blit(homeImage, (0, 0))
    text_screen("Welcome To Space Invaders", (255, 255, 255), 100, 200, 64)
    text_screen("Press Enter To Start", (255, 255, 255), 260, 270, 40)
    text_screen("Press 1, 2, 3 or 4 to choose One Ship", (255, 255, 255), 150, 350, 40)
    
    ship_1 = "images/ship-1.png"
    ship_2 = "images/ship-2.png"
    ship_3 = "images/ship-3.png"
    ship_4 = "images/ship-4.png"
    show_image(ship_1, 70, 500)
    show_image(ship_2, 270, 500)
    show_image(ship_3, 470, 500)
    show_image(ship_4, 670, 500)
        
    
    mixer.music.load('sounds/intro.mpeg')
    mixer.music.play()
    while not exit_game:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    PLAYER_SPACE_SHIP = pygame.image.load("images/ship-1.png")
                    fire = 1
                    pygame.mixer.music.stop()
                    gameloop()

                if event.key == pygame.K_2:
                    PLAYER_SPACE_SHIP = pygame.image.load("images/ship-2.png")
                    fire = 2
                    pygame.mixer.music.stop()
                    gameloop()

                if event.key == pygame.K_3:
                    PLAYER_SPACE_SHIP = pygame.image.load("images/ship-3.png")
                    fire = 3
                    pygame.mixer.music.stop()
                    gameloop()
                    
                if event.key == pygame.K_4:
                    PLAYER_SPACE_SHIP = pygame.image.load("images/ship-4.png")
                    fire = 4
                    pygame.mixer.music.stop()
                    gameloop()

                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    gameloop()

        pygame.display.update()
       
if __name__ == "__main__":
    welcome()
    