
from cgitb import text
import pygame, os, requests, math
from pygame import K_BACKSPACE , font
from random import randint
import webbrowser

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.font.init()
pygame.init()
font = pygame.font.SysFont('Serif', 170)
font2 = pygame.font.SysFont('Serif', 140)
font3 = pygame.font.SysFont('Serif', 40)
font4 = pygame.font.SysFont('Serif', 30)
font6 = pygame.font.SysFont('Serif', 60)

version = '0.12'
versioncheck = '12'

wintxt = font.render("NEW ROUND", (0, 5), BLACK)

class GameController():
    def __init__(self, rnd, points):
        self.rnd = rnd
        self.points = points
        self.size = 1320, 724
        self.BULLCOLOR = BLACK
        self.dialogue = False


gc = GameController(1,70)

size = (1320,737)
win = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)

class Shop():
    def __init__(self, one, two, three, four, yeezus, five, hpadd, six):
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.yeezus = yeezus
        self.five = five
        self.hpadd = hpadd
        self.six = six

class EnemyPlayer(pygame.sprite.Sprite):
    def __init__(self, img, x, y, v, m, hp, speed, facing, dmg):
        self.attack = False
        self.img = img
        self.x = x
        self.y = y
        self.v = v
        self.m = m
        self.hp = hp
        self.speed = speed
        self.facing = facing
        self.dmg = dmg
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # NEW
        self.yeezus = False

    def changeImg(self, newimg):
        self.img = newimg 

    def move(self, var1, var2):
        if (var1 > var2 and not self.attack):
            if self.yeezus:
                self.changeImg(yeezusimg['yeezus6'])
            else:
              self.changeImg(players['PlayerBLUE2'])
            self.x += self.speed
            self.facing = -1
        if(var1 < var2 and not self.attack):
            if self.yeezus:
                self.changeImg(yeezusimg['yeezus3'])
            else:
                self.changeImg(players['PlayerBLUE'])
            self.x -= self.speed
            self.facing = 1

class Player():
    def __init__(self, img, x, y, v, m, speed, facing, hp, dmg, bulletcnt, cc, abilitycount):
        self.img = img
        self.x = x
        self.y = y
        self.v = v
        self.m = m
        self.speed = speed
        self.facing = facing
        self.hp = hp
        self.dmg = dmg
        self.yeezus = False
        self.bulletcnt = bulletcnt
        self.cc = cc
        self.faceval1 = 1
        self.faceval2 = -1
        self.darkspecial = False
        self.lightspecial = False
    def changeImg(self, newimg):
        self.img = newimg 

    def checkFacing(self):

        if(self.img == players["PlayerRED"]):
            self.facing = self.faceval2
        else:
            self.facing = self.faceval1

pygame.display.set_caption("Geneva")
players = {
    'PlayerRED' :  pygame.image.load(os.path.join('./Assets/character/', 'player.png')).convert_alpha(),
    'PlayerRED2' :  pygame.transform.flip(pygame.image.load(os.path.join('./Assets/character/', 'player.png')), True, False).convert_alpha(),
    'PlayerBLUE' :  pygame.image.load(os.path.join('./Assets/character/', 'enemy.png')).convert_alpha(),
    'PlayerBLUEswing' :  pygame.image.load(os.path.join('./Assets/character/', 'enemy2.png')).convert_alpha(),
    'PlayerBLUEswing2' :  pygame.image.load(os.path.join('./Assets/character/', 'enemy3.png')).convert_alpha(),
    'PlayerBLUEswing3' :  pygame.image.load(os.path.join('./Assets/character/', 'enemy4.png')).convert_alpha(),
    'PlayerBLUE2' :  pygame.transform.flip(pygame.image.load(os.path.join('./Assets/character/', 'enemy.png')), True, False).convert_alpha()

}
yeezusimg = {
    'yeezus' :  pygame.image.load(os.path.join('./Assets/yeezus/', 'yeezuz.png')).convert_alpha(),
    'yeezus2' :  pygame.transform.flip(pygame.image.load(os.path.join('./Assets/yeezus/', 'yeezuz.png')), True, False).convert_alpha(),
    'yeezus3' :  pygame.image.load(os.path.join('./Assets/yeezus/', 'yeezus2.png')).convert_alpha(),
    'yeezusswing2' :  pygame.image.load(os.path.join('./Assets/yeezus/', 'yeezusSwing2.png')).convert_alpha(),
    'yeezusswing' :  pygame.image.load(os.path.join('./Assets/yeezus/', 'yeezusSwing.png')).convert_alpha(),
    'yeezus6' :  pygame.transform.flip(pygame.image.load(os.path.join('./Assets/yeezus/', 'yeezus2.png')), True, False).convert_alpha()

}

button_imgs = {
    'settings_button': pygame.image.load(os.path.join('./Assets/buttons/', 'settings.png')).convert_alpha(),
    'login': pygame.image.load(os.path.join('./Assets/buttons/', 'Login.png')).convert_alpha(),
    'restart': pygame.image.load(os.path.join('./Assets/buttons/', 'restart.png')).convert_alpha(),
    'start': pygame.image.load(os.path.join('./Assets/buttons/', 'start.png')).convert_alpha(),
    'discord': pygame.image.load(os.path.join('./Assets/buttons/', 'discord.png')).convert_alpha(),
    'credits': pygame.image.load(os.path.join('./Assets/buttons/', 'credits.png')).convert_alpha(),
    'resolution': pygame.image.load(os.path.join('./Assets/buttons/', 'resolution.png')).convert_alpha(),
    'resolution1': pygame.image.load(os.path.join('./Assets/buttons/', 'resolution1.png')).convert_alpha(),
    'resolution2': pygame.image.load(os.path.join('./Assets/buttons/', 'resolution2.png')).convert_alpha(),
    'back': pygame.image.load(os.path.join('./Assets/buttons/', 'back.png')).convert_alpha(),


}

logo = pygame.image.load(os.path.join('./Assets/', 'logo.png'))
pygame.display.set_icon(logo)

p = Player(players['PlayerRED'], 120, 460, 5, 1, 4.5, -1, 100, 10, 5, 10, 0)
p2 = EnemyPlayer(players['PlayerBLUE'], 1020, 460, 5, 1, 100, 2, -1, 1)

# - SHOP -
s = Shop(1,2,3,10,30,20,10,50)

erect = pygame.Rect(p2.x, p2.y, p2.img.get_width(), p2.img.get_height())
prect = pygame.Rect(p.x, p.y, p.img.get_width(), p.img.get_height())

mouserect = pygame.Rect((300, 300),(20,20))
grassRect = pygame.Rect((0,500),(1320,300))
mouserect = pygame.Rect((300, 300),(20,20))
statsrect = pygame.Rect((900, 100),(330,220))


class projectile(object):
    def __init__(self,x,y,radius,color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * p.facing
        self.BULLCOLOR = BLACK

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


bullets = []
settings_button = Button(500,250,button_imgs['settings_button'],3)
login_button = Button(500,50,button_imgs['login'],3)
restart = Button(500,150,button_imgs['restart'],3)
start = Button(500,150,button_imgs['start'],3)
discord = Button(20,20,button_imgs['discord'],3)
creditss = Button(500,350,button_imgs['credits'],3)
resolution = Button(500,150,button_imgs['resolution'],3)
resolution1 = Button(500,150,button_imgs['resolution1'],3)
resolution2 = Button(500,250,button_imgs['resolution2'],3)
back = Button(900,350,button_imgs['back'],3)

moving_sprites = pygame.sprite.Group()

class dialogue():
    def __init__(self,text,text1):
        self.text = text
        self.text1 = text1

    def draw(self):
        txt = font3.render(self.text,(0,5), BLACK)
        txt1 = font4.render(self.text1,(0,5), BLACK)
        win.blit(txt,(500,200))
        win.blit(txt1,(500,260))
    def changeText(self, t1, t2):
        self.text = t1
        self.text1 = t2

d = dialogue('', '')

def restartgame():
    p.hp = 100
    p2.hp = 100
    gc.rnd = 100
    gc.points = 0
    p.speed = 4.5
    p2.speed = 2
    p.dmg = 10
    p2.dmg = 1
    p.bulletcnt = 5
    p.cc = 10
    s.one = 1
    s.two = 2
    s.three = 3
    s.four = 10
    s.five = 20
    s.yeezus = 30

vers = requests.get("https://maxor.xyz/geneva/version.txt")
versi = vers.text

def update():
    update = requests.get("https://maxor.xyz/geneva/status.txt")
    updatetxt = update.text
    pygame.display.set_caption("updating.... " + version)

    if updatetxt == 'update':
        widthreq = requests.get("https://maxor.xyz/geneva/width.txt")
        width = widthreq.text
        heightreq = requests.get("https://maxor.xyz/geneva/height.txt")
        height = heightreq.text
        gc.size = (int(width), int(height))
        win = pygame.display.set_mode(gc.size)
        if(int(versioncheck) < int(versi)):
            pygame.display.set_caption("Geneva OUTDATED beta " + version)
        else:
            pygame.display.set_caption("Geneva")
        VARS = requests.get("https://maxor.xyz/geneva/vars.txt")
        vars2 = VARS.text
        maxor2 = vars2[0:5]
        maxor5 = vars2[6:8]
        maxor6 = vars2[9:11]
        s.hpadd = int(maxor5)
        s.yeezus = maxor6

        if maxor2 == 'BLACK':
            gc.BULLCOLOR = BLACK
        else:
            maxor3 = maxor2.translate({ord('-'): None})
            gc.BULLCOLOR = maxor3
        main()


def resetRes():
    grassRect.width = 0
    grassRect.height = 0

def getAbility():
    ability = randint(1,2)
    if ability == 1:
        if(p.lightspecial == False):
            p.lightspecial = True
            gc.dialogue = True
            d.changeText('You unlocked ability light!', 'when you die you will get a free revive!')
            p.abilitycnt += 1
        else:
            getAbility()
    if ability == 2:
        if(p.darkspecial == False):
            p.darkspecial = True
            gc.dialogue = True
            d.changeText('You unlocked ability dark!', 'every 20 hits this will kill the enemy for you!')
            p.abilitycnt += 1
        else:
            getAbility()


def main():

    run = True
    clock = pygame.time.Clock()
    lost = False
    won = False
    login = False
    shop = False
    username = ''
    password = ''
    passtime = False
    loggedin = False
    paused = False
    settings = False
    yeezus = False
    hptxtx = 515
    hpcheck = True
    critvalue = 0
    crit = False
    startclicked = False
    value = 0
    creditsactive = False
    resolutionclicked = False
    unlockedability = False
    darkvalue = 0
    lightused = False

    while run:
        
        if not startclicked and not creditsactive and not settings and not resolutionclicked:
            start.draw(win)
            discord.draw(win)
            creditss.draw(win)           
            if creditss.clicked:
                creditsactive = True

            if discord.clicked:
                disc = requests.get("https://maxor.xyz/geneva/discord.txt")                        
                disco = disc.text
                webbrowser.open(str(disco))  # Go to example.com

            if start.clicked:
                startclicked = True
                
        if creditsactive:
          
            duncan = font3.render("AvgJew - Lead Dev", (0, 5), BLACK)
            william = font3.render("William - Co Dev", (0, 5), BLACK)
            jusuf = font3.render("Jusuf - Playtesting/Bugfinding", (0, 5), BLACK)
            archer = font3.render("Archer - Art" , (0, 5), BLACK)
            win.blit(duncan, (200, 50))
            win.blit(william, (200, 150))
            win.blit(jusuf, (200, 250))
            win.blit(archer, (200, 350))
            back.draw(win)
            if back.clicked:
                creditsactive = False
                


        if settings and not resolutionclicked:
            resolution.draw(win)           
            if resolution.clicked:
                resolutionclicked = True
        
        if resolutionclicked:
            resolution1.draw(win)           
            resolution2.draw(win)           

            if resolution1.clicked:
                size = (1320, 737)
                resetRes()
                grassRect.width += 1320
                grassRect.height += 737
                resolutionclicked = False
                settings = False
                pygame.display.set_mode(size)
            if resolution2.clicked:
                size = (1460, 900)
                resetRes()
                grassRect.width += 1460
                grassRect.height += 900
                settings = False
                resolutionclicked = False
                pygame.display.set_mode(size)               


        hp = font3.render("hp: " + str(p.hp), (0, 5), BLACK)
        spd = font3.render("spd: " + str(p.speed), (0, 5), BLACK)
        dmg = font3.render("dmg: " + str(p.dmg), (0, 5), BLACK)
        points = font3.render("points: " + str(round(gc.points)), (0, 5), BLACK)
        cc = font3.render("critchance: " + str(p.cc), (0, 5), BLACK)

        shoptxt = font2.render("SHOP", (0, 5), BLACK)
        shoptxt2 = font3.render("HP: KEY 1 PRC:" + str(s.one), (0, 5), BLACK)
        shoptxt3 = font3.render("Speed: KEY 2 PRC:" + str(s.two), (0, 5), BLACK)
        shoptxt4 = font3.render("DMG: KEY: 3 PRC:" + str(s.three), (0, 5), BLACK)
        shoptxt5 = font3.render("WEAPON: KEY: 4 PRC:" + str(s.four), (0, 5), BLACK)
        shoptxt6 = font3.render("CC: KEY: 5 PRC:" + str(s.five), (0, 5), BLACK)
        shoptxt7 = font3.render("Ability: KEY: 6 PRC:" + str(s.six), (0, 5), BLACK)


        weaponstats = font6.render("Weapon Stats", (0, 5), BLACK)
        weaponstats2= font3.render("Bullet Count: " + str(p.bulletcnt), (0, 5), BLACK)
        weaponstats3 = font3.render("BulletSpeed: " + str(p.speed), (0, 5), BLACK)


        if yeezus:
            p2.yeezus = True
            p.yeezus = True
        if paused or not startclicked and not creditsactive and not settings:
            settings_button.draw(win)
            if(settings_button.clicked):
                if not settings:
                    settings = True
                else:
                    settings = False

        if paused and startclicked:
            if not settings:
                login_button.draw(win)
                restart.draw(win)

            if(restart.clicked):
                restartgame()


            if(settings_button.clicked):
                if not settings:
                    settings = True
                else:
                    settings = False
            if(login_button.clicked):
                if not login:
                    login = True
                else:
                    login = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and startclicked:
                    if len(bullets) < p.bulletcnt and not paused and not lost:  # This will make sure we cannot exceed 5 bullets on the screen at once
                            bullets.append(projectile(round(prect.x+prect.width//2), round(prect.y + prect.height//2 - 60), 6, (gc.BULLCOLOR), p.facing))

            else:
                if event.type == pygame.KEYDOWN:
                    if(login and paused):
                        if passtime and event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                            password += event.unicode
                        elif not passtime and event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                            username += event.unicode
                        if event.key == K_BACKSPACE:
                            if not passtime:
                                username = ''
                            else:
                                password = ''
                

                    if event.key == pygame.K_SPACE:
                        if gc.dialogue:
                            gc.dialogue = False
                        else:
                            if(p.y == 460):
                                p.y -= 50
                            if login:
                                passtime = True


                    if event.key == pygame.K_RETURN:
                        if passtime:
                            logins = requests.get("https://maxor.xyz/geneva/logins.json")
                            data = logins.text
                            maxor = data.find(username, 0, 300)
                            maxor2 = data.find(password, 0, 300)
                           
                            if(maxor == -1):
                                username = ''
                                password = ''
                            elif (maxor2 - maxor < 40 and password is not ''):
                                loggedin = True


                    if event.key == pygame.K_n:
                        if(won):
                            won = False
                            if p.x <= 500:
                                p2.x = 1020
                            else:
                                p2.x = 10
                    if event.key == pygame.K_TAB and won:
                        if(shop):
                            shop = False
                        else:
                            shop = True


                    if event.key == pygame.K_ESCAPE:
                        if(not paused):
                            paused = True
                        else:
                            paused = False

                    if(event.key == pygame.K_u and paused):
                        update()

                    if(shop):
                        if(event.key == pygame.K_1):
                            if(gc.points >= s.one):
                                gc.points -= s.one
                                s.one += 1
                                p.hp += s.hpadd
                        if(event.key == pygame.K_2 and p.speed <= 10.5):
                            if(gc.points >= s.two):
                                gc.points -= s.two
                                s.two += 1
                                p.speed += 0.5
                        if(event.key == pygame.K_3):
                            if(gc.points >= s.three):
                                gc.points -= s.three
                                s.three += 1
                                p.dmg += 5
                        if(event.key == pygame.K_4 and p.bulletcnt <= 14):
                            if(gc.points >= s.four):
                                gc.points -= s.four
                                s.four += 15 
                                p.bulletcnt += 1
                                p.faceval2 -= 0.25
                                p.faceval1 += 0.25

                        if(event.key == pygame.K_5 and p.cc <= 75):
                            if(gc.points >= s.five):
                                gc.points -= s.five
                                s.five += 10 
                                p.cc += 5
                        if(event.key == pygame.K_6 and p.abilitycount <= 9):
                            if(gc.points >= s.six):
                                gc.points -= s.six
                                gc.dialogue = True
                                s.six *= 2
                                getAbility()
                        if(event.key == pygame.K_y):
                            if(gc.points >= s.yeezus):
                                gc.points -= s.yeezus
                                s.yeezus += 200 * gc.rnd
                                p.dmg += 10
                                p.speed += 1
                                yeezus = True
        
        if loggedin and startclicked:
            pygame.display.set_caption("Geneva Royale Beta 0.11")
            if hpcheck:
                p.hp = 30000
                hptxtx -= 30
                hpcheck = False
                lost = False

        p.checkFacing()


        if login and paused:
            use = font3.render(username, True, (BLACK))
            win.blit(use, (20,20))
        if passtime and paused:
            pas = font3.render(password, True, (BLACK))
            win.blit(pas, (20,60))

        if shop and won and not paused and startclicked:
            win.blit(shoptxt, (20, 10))
            win.blit(shoptxt2, (20, 150))
            win.blit(shoptxt3, (20, 190))
            win.blit(shoptxt4, (20, 230))
            win.blit(shoptxt5, (20, 270))
            win.blit(points, (985, 10))
            win.blit(shoptxt6, (20, 310))
            win.blit(shoptxt7, (20, 350))           
            pygame.draw.rect(win, (120,120,120),statsrect)
            win.blit(weaponstats, (900, 100))
            win.blit(weaponstats2, (920, 190))
            win.blit(weaponstats3, (920, 240))



        if not paused and startclicked:
            win.blit(hp, (hptxtx, 10))
            win.blit(spd, (650, 10))
            win.blit(dmg, (800, 10))
            if not shop:
                win.blit(cc, (950, 10))

        if p.hp <= 0:
            lost = font.render("Ratio U LOST", (20,20), BLACK)
            win.blit(lost, (150, 20))
            if p.lightspecial == True:
                if lightused == False:
                    p.hp = 100
                    won = True
        # MOVE PLAYER 2
        if not paused:
            p2.move(p.x, p2.x)


        # JUMP
        if(p.y < 460):
            p.y += 1.25

        # WIN TEXT

        if(won and not shop and not paused):
            win.blit(wintxt, (180, 20))

        # KEY HANDLING 2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if(p.x > 2):
                p.x -= p.speed
                if yeezus:
                    p.changeImg(yeezusimg['yeezus'])
                else:
                 p.changeImg(players['PlayerRED']) 
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] :
            if(p.x < 1240):
                if yeezus:
                    p.changeImg(yeezusimg['yeezus2'])
                else:
                    p.changeImg(players['PlayerRED2'])
                p.x += p.speed

        if crit:
            if critvalue <= 10:
                critvalue += 0.5
                cctxt = font4.render("crit", (0, 5), RED)
                win.blit(cctxt, (p2.x + 60, p2.y - 80))
            else:
                critvalue = 0
                crit = False


        prect.x = p.x
        prect.y = p.y
        if(p.x < p2.x):
         erect.x = (p2.x + 80)
        if(p.x > p2.x):
         erect.x = (p2.x - 80)
        erect.y = p2.y
        
        # HITBOXES
        p2.hitbox = (p2.x + 17, p2.y + 11, 29, 52) # NEW
        if (erect.colliderect(prect)):
            p2.attack = True
            value += 0.5
            if(value >= 63):
                value = 0
        else:
            p2.attack = False
            value = 0

        for bullet in bullets:

            bullet.draw(win)

            if bullet.x < 1240 and bullet.x > 0: 
                bullet.x += bullet.vel  # Moves the bullet by its vel
            else:
                bullets.pop(bullets.index(bullet))  # This will remove the bullet if it is off 

            if not lost and not won and not paused:
                if bullet.y + bullet.radius < p2.hitbox[1] + 60 + p2.hitbox[3] and bullet.y + bullet.radius > p2.hitbox[1] - 60 or prect.colliderect(erect):
                    if bullet.x + bullet.radius > p2.hitbox[0] + 13 and bullet.x - bullet.radius < p2.hitbox[0] + p2.hitbox[2] - 13 or prect.colliderect(erect):
                        if(randint(1, 100) <= p.cc):
                            p2.hp -= (p.dmg * 2)
                            crit = True
                            if p.darkspecial == True:
                                darkvalue += 1
                                if darkvalue == 20:
                                    p2.hp = 0
                                    darkvalue = 0
                        else:
                            if p.darkspecial == True:
                                darkvalue += 1
                                if darkvalue == 20:
                                    p2.hp = 0
                                    darkvalue = 0

                            p2.hp -= p.dmg

                        if not won:
                            bullets.pop(bullets.index(bullet))
                        # SCALE ENEMY
                        if not won:
                            if(p2.hp <= 0):
                                won = True
                                if(p.speed >= p2.speed):
                                    p2.speed += 0.25
                                elif p.speed <= p2.speed and p.speed <= 9.5:
                                    p2.speed += 0.1

                                gc.rnd += 1
                                p2.hp += 100 
                                p2.hp += gc.rnd * 20
                                p2.dmg += 0.25
                                gc.points += (1 + (gc.rnd * 0.1))
                                print(str(gc.points))
        # DRAW PLAYER
        if not lost and startclicked:         
          win.blit(p.img, (p.x, p.y - 40))
        if not won and not paused and not lost and startclicked:
          if(value <= 25):
            win.blit(p2.img, (p2.x, p2.y - 40))
          if(value > 25 and value <= 55):
            if yeezus:
                win.blit(yeezusimg['yeezusswing'], (p2.x, p2.y - 40))
            else:

                win.blit(players['PlayerBLUEswing'], (p2.x, p2.y  - 40))
          if(value > 55 and value <= 60 ):
            if yeezus:
                win.blit(yeezusimg['yeezusswing2'], (p2.x, p2.y - 40))
            else:
             win.blit(players['PlayerBLUEswing2'], (p2.x, p2.y - 40))
            p.hp -= p2.dmg
          if(value > 60 and value <= 65 ):
            if yeezus:
                win.blit(yeezusimg['yeezusswing2'], (p2.x, p2.y - 40))
            else:
                win.blit(players['PlayerBLUEswing3'], (p2.x, p2.y - 40))
                p.hp -= p2.dmg

        if gc.dialogue == True:
            d.draw()    
        pygame.draw.rect(win,(0,200,0), grassRect)
        mouserect.x ,mouserect.y = pygame.mouse.get_pos()
        pygame.draw.rect(win, (0,0,0),mouserect)

        pygame.display.flip()


        clock.tick(60)
        pygame.display.update()

        win.fill(WHITE)

    pygame.quit()

if int(versioncheck) < int(float(versi)):
    update()
else:
    main()