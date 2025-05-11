import pygame
import sys

pygame.init()
scr = pygame.display.set_mode((1250, 750))
pygame.display.set_caption("Dungeons")

icon = pygame.image.load('foto/icon/Avatar.jpg')
pygame.display.set_icon(icon)

menu_music = 'Music/nejnoe-spokoynoe-bezmyatejnoe-raznogolosoe-penie-ptits-v-lesu.mp3'
tutor_music = 'Music/morning-garden-acoustic-chill-15013_[cut_68sec].mp3'
scene1_music = 'Music/suspense-background-music-332370.mp3'

pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)

font = pygame.font.SysFont('arial', 40)
WHITE = (255, 255, 255)
text_tutor1 = font.render('Щиро радий тебе бачити в моєму проекті ', False, 'white')
text_tutor2 = font.render('коротко раскажу як тут рухатися щоб іти в перед потрібно', False, 'white')
text_tutor3 = font.render('нажати на стрілку в прово ащо в назад стрілку в ліво ', False, 'white')
text_tutor4 = font.render('стрибнути потрібно нажати x стріляти на пробіл тепер ти готовий ', False, 'white')
text_tutor5 = font.render('переїти в наступний рівень для того нажми Lctrl', False, 'white')
end_texct = font.render('Вітаю ти дійшов до кінця гри для того щоб вийти зайди в двері', False, 'white')


background = pygame.image.load('foto/scene/Menu_bg.jpg')
level1 = pygame.image.load('foto/scene/scene1.jpg')
jorj = pygame.image.load('foto/5253577204917465249-removebg-preview.png')
tutorpeople = pygame.image.load('foto/charencter/Vizard_tutorial_4-removebg-preview.png')
end_game = pygame.image.load('foto/End_Idle.png')
Heart = pygame.image.load('foto/Heart.png')
level2 = pygame.image.load('foto/scene/Tutorial_BG.png')
teleport = pygame.image.load('foto/charencter/pixil-frame-0.png')
level3 = pygame.image.load('foto/scene/scene3.jpg')
level4= pygame.image.load('foto/scene/scene4.jpg')
level5 = pygame.image.load('foto/scene/scene5.png')
block = pygame.image.load('foto/block/Granite.jpg')
img_bullet = pygame.image.load('foto/bullet.png')
chp = pygame.image.load('foto/block/spike1.png')
portal = pygame.image.load('foto/block/Goal_scene31.png')
gras = pygame.image.load('foto/block/Grass_Tile_Sheet_2.01.png')
playr = pygame.image.load('foto/playr/playr-removebg-preview.png')
door = pygame.image.load('foto/block/Door.png')
vorog = pygame.image.load('foto/playr/Enemy-removebg-preview1.png')

btn_play = pygame.image.load('foto/batton/image.png').convert_alpha()
btn_exit = pygame.image.load('foto/batton/imageQuti.png').convert_alpha()

def draw_animated_button(image, x, y, scale_hover=1.1, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = image.get_rect(topleft=(x, y))

    if button_rect.collidepoint(mouse):
        w, h = image.get_size()
        new_size = (int(w * scale_hover), int(h * scale_hover))
        scaled_img = pygame.transform.smoothscale(image, new_size)
        new_rect = scaled_img.get_rect(center=button_rect.center)
        scr.blit(scaled_img, new_rect.topleft)

        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    else:
        scr.blit(image, (x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_right = pygame.transform.scale(playr, (40, 60))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = "right"


        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -5
            self.image = self.image_left
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            dx = 5
            self.image = self.image_right
            self.direction = "right"



        if keys[pygame.K_x] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y


        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1250:
            self.rect.right = 1250
        if self.rect.top > 750:
            self.rect.topleft = (50, 500)
            self.vel_y = 0
    def fire(self):
        speed = 10 if self.direction == "right" else -10
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.centery, 15, 10, speed)
        bullets.add(bullet)

bullets = pygame.sprite.Group()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, foto1, w, h):
        super().__init__()
        self.foto1 = foto1
        self.image = pygame.transform.scale(self.foto1, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, foto):
        super().__init__()
        self.foto = foto
        self.image = pygame.transform.scale(self.foto, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, foto):
        super().__init__()
        self.foto = foto
        self.image = pygame.transform.scale(self.foto, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(image_surface, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed  # <-- рухаємо по горизонталі
        if self.rect.right < 0 or self.rect.left > 1250:
            self.kill()
class ShootableEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, foto1, w, h):
        super().__init__()
        self.image = pygame.transform.scale(foto1, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if pygame.sprite.spritecollide(self, bullets, True):  # True – куля зникає
            self.kill()  # Ворог зникає

def main_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    running = True
    while running:
        scr.blit(background, (0, 0))

        draw_animated_button(btn_play, 500, 300, action=tutorial)
        draw_animated_button(btn_exit, 500, 430, action=quit_game)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        pygame.display.update()


def tutorial():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(tutor_music)
    pygame.mixer.music.play(-1)

    running = True
    while running:

        scr.blit(tutorpeople, (1240, 650))
        scr.blit(level1, (0, 0))
        scr.blit(text_tutor1, (0, 0))
        scr.blit(text_tutor2, (0, 50))
        scr.blit(text_tutor3, (0, 100))
        scr.blit(text_tutor4, (0, 150))        
        scr.blit(text_tutor5, (0, 200)) 
                       


        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL:
                running = False
                scene1()


        pygame.display.update()



def scene1():


    player = Player(50, 500)
    platforms = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    platform_list = [
        Platform(0, 700, block),
        Platform(40, 700, block),
        #////////////////////////
        Platform(160, 600, block),
        Platform(200, 600, block),
        Platform(240, 600, block),
        #////////////////////////
        Platform(340, 500, block),
        Platform(380, 500, block),
        Platform(420, 500, block),
        #////////////////////////
        Platform(240, 400, block),
        Platform(200, 400, block),
        #////////////////////////
        Platform(340, 300, block),
        Platform(380, 300, block),
        Platform(420, 300, block),
        #////////////////////////
        Platform(600, 300, block),
        Platform(640, 300, block),
        Platform(680, 300, block),
        #////////////////////////
        Platform(780, 300, block),
        Platform(820, 300, block),
        Platform(860, 300, block),
        #///////////////////////
        Platform(1150, 640, block),
        Platform(1110, 640, block),
        Platform(1070, 640, block),
        Platform(1190, 640, block)


    ]
    spike = [
        Spike(380, 470, chp),
        #Spike(380, 270, chp),
        Spike(640, 270, chp),
        Spike(820, 270, chp)
    ]
    enemy2 = ShootableEnemy(380, 220, vorog, 60, 100)  # Можна інше зображення
    enemies = pygame.sprite.Group(enemy2)

    platforms.add(platform_list)
    spikes.add(spike)
    goal = Enemy(1190, 590, portal, 40, 40)
    

    all_sprites = pygame.sprite.Group(player)
    running = True
    while running:
        scr.blit(level1, (0, 0))
        scr.blit(jorj, (250, 630))
        scr.blit(goal.image, goal.rect)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:           
                    player.fire() 

        player.update(platform_list)
        goal.update(platform_list)
        all_sprites.draw(scr)
        
        platforms.draw(scr)
        spikes.draw(scr)
        bullets.update()
        bullets.draw(scr)
        enemies.update()
        enemies.draw(scr)
        #pygame.draw.rect(scr, (200, 200, 200), goal)
        if pygame.sprite.spritecollide(player, spikes, False):
            scene1()
            return
        if pygame.sprite.spritecollide(player, enemies, False):
            scene1()
            return

        if player.rect.colliderect(goal):
            scene2()
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(60)

def scene2():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(scene1_music)
    pygame.mixer.music.play(-1)

    player = Player(50, 500)
    platforms = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    platform_list = [

        Platform(0, 700, block),
        Platform(40, 700, block),
        Platform(80, 700, block),
        #/////////////////////////
        Platform(160, 600, block),
        Platform(200, 600, block),
        Platform(240, 600, block),
        #////////////////////////
        Platform(340, 500, block),
        Platform(380, 500, block),
        Platform(420, 500, block),
        #////////////////////////
        Platform(500, 600, block),
        Platform(540, 600, block),
        Platform(580, 600, block),
        #////////////////////////
        Platform(640, 500, block),
        Platform(680, 500, block),
        Platform(720, 500, block),        
        #////////////////////////
        Platform(680, 400, block),
        Platform(740, 300, block),
        Platform(680, 200, block),
        #////////////////////////
        Platform(800, 200, block),
        Platform(900, 200, block),
        Platform(980, 200, block),
        #////////////////////////
        Platform(1150, 340, block),
        Platform(1110, 340, block),
        Platform(1070, 340, block),
        Platform(1190, 340, block)

    ]

    spike = [
        Spike(540, 570, chp),
        Spike(900, 170, chp),
    ]

    platforms.add(platform_list)
    enemy2 = ShootableEnemy(800, 120, vorog, 60, 100)  # Можна інше зображення
    enemies = pygame.sprite.Group(enemy2)

    goal = Enemy(1190, 280, portal, 40, 40)

    all_sprites = pygame.sprite.Group(player)
    spikes.add(spike)
    running = True
    while running:
        scr.blit(level3, (0, 0))
        scr.blit(goal.image, goal.rect)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:           
                    player.fire() 


        player.update(platform_list)
        goal.update(platform_list)
        all_sprites.draw(scr)
        platforms.draw(scr)
        spikes.draw(scr)
        enemies.update()
        enemies.draw(scr)
        bullets.update()
        bullets.draw(scr)

        #pygame.draw.rect(scr, (200, 200, 200), goal)  
        if pygame.sprite.spritecollide(player, spikes, False):
            scene1()
            return

        if pygame.sprite.spritecollide(player, enemies, False):
            scene1()
            return

        if player.rect.colliderect(goal):
            running = False
            scene3()

        pygame.display.update()
        pygame.time.Clock().tick(60)

def scene3():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(scene1_music)
    pygame.mixer.music.play(-1)

    player = Player(50, 500)
    platforms = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    platform_list = [
        Platform(0,700, block),
        Platform(40,700, block),
        Platform(80,700, block),
        Platform(120,700, block),
        Platform(160,600, block),
        Platform(240,500, block),
        Platform(280,450, block),
        Platform(500,300, block),
        Platform(400,400, block),
        Platform(400,200, block),
        Platform(440,100, block),
        Platform(480,100, block),
        Platform(520,100, block),
        Platform(680,100, block),
        Platform(720,100, block),
        Platform(760,100, block),
        Platform(880,100, block),
        Platform(920,100, block),
        Platform(960,100, block),
        Platform(1000,100, block),
        Platform(1040,100, block),
        Platform(1080,100, block),
    ]
    platforms.add(platform_list)
    spike = [
        Spike(485, 70, chp),
        Spike(725, 70, chp),
        Spike(1000,70, chp),
    ]

    goal = Enemy(1080,40, portal, 40, 40)
    enemy2 = ShootableEnemy(900, 20, vorog, 60, 100)
    enemies = pygame.sprite.Group(enemy2)

    all_sprites = pygame.sprite.Group(player)
    running = True
    spikes.add(spike)
    while running:
        scr.blit(level4, (0, 0))
        scr.blit(goal.image, goal.rect)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:           
                    player.fire() 


        player.update(platform_list)
        goal.update(platform_list)
        all_sprites.draw(scr)
        platforms.draw(scr)
        spikes.draw(scr)
        bullets.update()
        bullets.draw(scr)
        enemies.update()
        enemies.draw(scr)
 
        if pygame.sprite.spritecollide(player, spikes, False):
            scene1()
            return

        if pygame.sprite.spritecollide(player, enemies, False):
            scene1()
            return

        if player.rect.colliderect(goal):
            running = False
            scene4()

        pygame.display.update()
        pygame.time.Clock().tick(60)

def scene4():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(scene1_music)
    pygame.mixer.music.play(-1)

    player = Player(50, 500)
    platforms = pygame.sprite.Group()
    platform_list = [
        Platform(0,700, block),
        Platform(40,700, block),
        Platform(80,700, block),
        Platform(120,700, block),
        Platform(160,700, block),
        Platform(200,700, block),
        Platform(240,700, block),
        Platform(280,700, block),
        Platform(320,700, block),
        Platform(360,700, block),
        Platform(400,700, block),
        Platform(440,700, block),
        Platform(480,700, block),
        Platform(520,700, block),
        Platform(560,700, block),
        Platform(600,700, block),
        Platform(640,700, block),
        Platform(680,700, block),
        Platform(720,700, block),
        Platform(760,700, block),
        Platform(800,700, block),
        Platform(840,700, block),
        Platform(880,700, block),
        Platform(920,700, block),
        Platform(960,700, block),
        Platform(1000,700, block),
        Platform(1040,700, block),
        Platform(1080,700, block),
        Platform(1120,700, block),
        Platform(1160,700, block),
        Platform(1200,700, block),
        Platform(1240,700, block),
        #////////////////////////
        Platform(0,660, block),
        Platform(40,660, block),
        Platform(80,660, block),
        Platform(120,660, block),
        Platform(160,660, block),
        Platform(200,660, block),
        Platform(240,660, block),
        Platform(280,660, block),
        Platform(320,660, block),
        Platform(360,660, block),
        Platform(400,660, block),
        Platform(440,660, block),
        Platform(480,660, block),
        Platform(520,660, block),
        Platform(560,660, block),
        Platform(600,660, block),
        Platform(640,660, block),
        Platform(680,660, block),
        Platform(720,660, block),
        Platform(760,660, block),
        Platform(800,660, block),
        Platform(840,660, block),
        Platform(880,660, block),
        Platform(920,660, block),
        Platform(960,660, block),
        Platform(1000,660, block),
        Platform(1040,660, block),
        Platform(1080,660, block),
        Platform(1120,660, block),
        Platform(1160,660, block),
        Platform(1200,660, block),
        Platform(1240,660, block),
        #////////////////////////
        Platform(0,620, gras),
        Platform(40,620, gras),
        Platform(80,620, gras),
        Platform(120,620, gras),
        Platform(160,620, gras),
        Platform(200,620, gras),
        Platform(240,620, gras),
        Platform(280,620, gras),
        Platform(320,620, gras),
        Platform(360,620, gras),
        Platform(400,620, gras),
        Platform(440,620, gras),
        Platform(480,620, gras),
        Platform(520,620, gras),
        Platform(560,620, gras),
        Platform(600,620, gras),
        Platform(640,620, gras),
        Platform(680,620, gras),
        Platform(720,620, gras),
        Platform(760,620, gras),
        Platform(800,620, gras),
        Platform(840,620, gras),
        Platform(880,620, gras),
        Platform(920,620, gras),
        Platform(960,620, gras),
        Platform(1000,620, gras),
        Platform(1040,620, gras),
        Platform(1080,620, gras),
        Platform(1120,620, gras),
        Platform(1160,620, gras),
        Platform(1200,620, gras),
        Platform(1240,620, gras),

    ]
    platforms.add(platform_list)

    goal = Enemy(645,515, door, 110, 118)

    all_sprites = pygame.sprite.Group(player)
    running = True
    while running:
        scr.blit(level5, (0, 0))
        scr.blit(goal.image, goal.rect)
        scr.blit(end_texct, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        player.update(platform_list)
        all_sprites.draw(scr)
        platforms.draw(scr)
        goal.update(platform_list)

        #pygame.draw.rect(scr, (222, 184, 135), goal)  

        if player.rect.colliderect(goal):
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(60)


def quit_game():
    pygame.quit()
    sys.exit()

main_menu()