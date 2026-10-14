# Code by Maxor
# Commits by William, Art from Archer
# DM avg#3851 on discord for Questions
import pygame, os, sys, requests, webbrowser, time
from pygame import K_BACKSPACE , font
from random import randint
from discord_webhook import DiscordWebhook
from os.path import exists
from netplay import Peer
pygame.init()

# SET GAME NAME
pygame.display.set_caption("Geneva")

# Compiled builds (build.py) bundle the assets and save player data in the user's home folder
if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
    datadir = os.path.join(os.path.expanduser('~'), '.geneva')
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(basedir, 'multiplayer', 'server')

def asset(*parts):
    return os.path.join(basedir, 'assets', *parts)

os.makedirs(datadir, exist_ok=True)
userinfopath = os.path.join(datadir, 'userinfo.txt')
file_exists2 = exists(userinfopath)

# INIT COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LBLUE = (75, 127, 199)

# INIT FONT
pygame.font.init()
font = pygame.font.SysFont('Serif', 170)
font2 = pygame.font.SysFont('Serif', 140)
font3 = pygame.font.SysFont('Serif', 40)
font6 = pygame.font.SysFont('Serif', 60)
font4 = pygame.font.SysFont('Serif', 30)
font7 = pygame.font.SysFont('Serif', 100)
font8 = pygame.font.SysFont('Serif', 10)

# NETWORK HELPERS (game still works offline)
def fetch(url, default=''):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.text.strip()
    except requests.RequestException:
        return default

def sendWebhook(url, content):
    try:
        DiscordWebhook(url=url, content=content).execute()
    except Exception:
        pass

# GET HIGHSCORE (None when offline, so nobody gets a fake highscore prompt)
try:
    highscore = int(fetch("https://maxor.xyz/geneva/highscore.txt"))
except ValueError:
    highscore = None

sendWebhook('https://discord.com/api/webhooks/1005947184207892620/MdrkcgX-XJd4z55TfZcHoCzy7jVSOZz2OwyrMloE6FF8fl0aQ89m1f4dTZQeJPfFnU-p', ' Someone has logged into Geneva Original unique id')

# SIZE
size = (1320,737)
win = pygame.display.set_mode(size)

# VERSION
version = '0.16'
versioncheck = '16'

wintxt = font.render("NEW ROUND", (0, 5), BLACK)

# GAME CONTROLLER
class GameController():
    def __init__(self, rnd, points, client):
        self.rnd = rnd
        self.points = points
        self.size = 1320, 724
        self.BULLCOLOR = BLACK
        self.lost = False
        self.client = client
        self.wonmp = False
        self.lostmp = False  
        self.lobbystarted = False
        self.inlobby = False
        self.ernd = 0
        self.consolestage = 0
        self.won = False
        self.login = False
        self.shop = False
        self.singleplayerpromp = False
        self.speedrun = False
        self.rankednameprompt = False    
        self.startclicked = False
        self.sentrankedwin = False
        self.restarted = False
        self.ppr = 0
        self.loggedinasnonadmin = False
        self.moment1 = 0
        self.moment2 = 0
        self.finaltime = 0
        self.username = ''
        self.password = ''
        self.chooseclass1 = False

# INIT GAME CONTROLLER
gc = GameController(1,1,0)

# REMOVE DEFAULT WINDOWS MOUSE
pygame.mouse.set_visible(False)

# CLASSES

class VariableStorage():
    def __init__(self):
        self.value = 0
        self.creditsactive = False
        self.resolutionclicked = False
        self.darkvalue = 0
        self.highscoreprompt = False
        self.namelol = ''
        self.goths = False
        self.singleplayer = True
        self.mpprompt = False
        self.controlspage = False    
        self.startrecentlyclicked = False
        self.classelect = False
        self.modeRecentlyChosen = False
        self.showHitbox = False
        self.ipprompt = False
        self.joinip = ''

class Shop():
    def __init__(self, one, two, three, four, yeezus, five, hpadd, six, weppadd, ccadd, speedadd, dmgadd, seven):
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.yeezus = yeezus
        self.five = five
        self.hpadd = hpadd
        self.six = six
        self.wepadd = weppadd
        self.ccadd = ccadd
        self.speedadd = speedadd
        self.dmgadd = dmgadd
        self.seven = seven


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
        self.abilitycount = abilitycount
        self.lightused = False
        self.uncap = False
        self.jump = False
        self.hasinvinc = False
        self.invinc = False
        self.hasdash = False
        self.dashstate = 0
        self.dashstate2 = 0
        self.playerclass = 0
        self.facingX = 10


    def changeImg(self, newimg):
        self.img = newimg 

    def checkFacing(self):

        if(self.img == players["PlayerRED"] or self.img == players["PlayerGREEN"] ):
            self.facing = self.faceval2
        else:
            self.facing = self.faceval1


class projectile(object):
    def __init__(self,x,y,radius,color, facing, bulletid):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * p.facing
        self.BULLCOLOR = BLACK
        self.bulletid = bulletid

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

# Found this on the internet <3

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

class dialogue():
    def __init__(self,text,text1):
        self.text = text
        self.text1 = text1
        self.dialogue = False

    def draw(self):
        txt = font3.render(self.text,(0,5), BLACK)
        txt1 = font4.render(self.text1,(0,5), BLACK)
        txt2 = font8.render("Press Space",(0,5), BLACK)

        win.blit(txt,(500,200))
        win.blit(txt1,(500,260))
        win.blit(txt2,(550,300))

    def changeText(self, t1, t2):
        self.text = t1
        self.text1 = t2


# IMAGES
players = {
    'PlayerRED' :  pygame.image.load(asset('character', 'Player', 'player.png')).convert_alpha(),
    'PlayerRED2' :  pygame.transform.flip(pygame.image.load(asset('character', 'Player', 'player.png')), True, False).convert_alpha(),
    'PlayerGREEN' :  pygame.image.load(asset('character', 'Player', 'shotgunPlayer.png')).convert_alpha(),
    'PlayerGREEN2' :  pygame.transform.flip(pygame.image.load(asset('character', 'Player', 'shotgunPlayer.png')), True, False).convert_alpha(),    
    'PlayerBLUE' :  pygame.image.load(asset('character', 'Enemy', 'enemy.png')).convert_alpha(),
    'PlayerBLUEswing' :  pygame.image.load(asset('character', 'Enemy', 'enemy2.png')).convert_alpha(),
    'PlayerBLUEswing2' :  pygame.image.load(asset('character', 'Enemy', 'enemy3.png')).convert_alpha(),
    'PlayerBLUEswing3' :  pygame.image.load(asset('character', 'Enemy', 'enemy4.png')).convert_alpha(),
    'PlayerBLUE2' :  pygame.transform.flip(pygame.image.load(asset('character', 'Enemy', 'enemy.png')), True, False).convert_alpha(),
    'PlayerBLUEswing22' :  pygame.transform.flip(pygame.image.load(asset('character', 'Enemy', 'enemy3.png')), True, False).convert_alpha(),
    'PlayerBLUEswing32' :  pygame.transform.flip(pygame.image.load(asset('character', 'Enemy', 'enemy4.png')), True, False).convert_alpha(),
    'PlayerBLUEswing23' :  pygame.transform.flip(pygame.image.load(asset('character', 'Enemy', 'enemy2.png')), True, False).convert_alpha(),

}
yeezusimg = {
    'yeezus' :  pygame.image.load(asset('character', 'yeezus', 'yeezuz.png')).convert_alpha(),
    'yeezus2' :  pygame.transform.flip(pygame.image.load(asset('character', 'yeezus', 'yeezuz.png')), True, False).convert_alpha(),
    'yeezus3' :  pygame.image.load(asset('character', 'yeezus', 'yeezus2.png')).convert_alpha(),
    'yeezusswing2' :  pygame.image.load(asset('character', 'yeezus', 'yeezusswing2.png')).convert_alpha(),
    'yeezusswing' :  pygame.image.load(asset('character', 'yeezus', 'yeezusswing.png')).convert_alpha(),
    'yeezus6' :  pygame.transform.flip(pygame.image.load(asset('character', 'yeezus', 'yeezus2.png')), True, False).convert_alpha(),
    'deezz' : pygame.image.load(asset('ground.png')).convert_alpha(),
    'deez' : pygame.transform.scale(pygame.image.load(asset('ground.png')),(1320,140)).convert_alpha(),
    'deez2' : pygame.transform.scale(pygame.image.load(asset('ground.png')),(1460,140)).convert_alpha(),
    'cloudx' : pygame.image.load(asset('cloud.png')).convert_alpha(),
    'cloud' : pygame.transform.scale(pygame.image.load(asset('cloud.png')),(300,200)).convert_alpha(),
}

button_imgs = {
    'settings_button': pygame.image.load(asset('buttons', 'Settings.png')).convert_alpha(),
    'login': pygame.image.load(asset('buttons', 'Login.png')).convert_alpha(),
    'restart': pygame.image.load(asset('buttons', 'restart.png')).convert_alpha(),
    'start': pygame.image.load(asset('buttons', 'start.png')).convert_alpha(),
    'discord': pygame.image.load(asset('buttons', 'discord.png')).convert_alpha(),
    'credits': pygame.image.load(asset('buttons', 'credits.png')).convert_alpha(),
    'resolution': pygame.image.load(asset('buttons', 'resolution.png')).convert_alpha(),
    'resolution1': pygame.image.load(asset('buttons', 'resolution1.png')).convert_alpha(),
    'resolution2': pygame.image.load(asset('buttons', 'resolution2.png')).convert_alpha(),
    'back': pygame.image.load(asset('buttons', 'back.png')).convert_alpha(),
    'multi': pygame.image.load(asset('buttons', 'Multi.png')).convert_alpha(),
    'multi1': pygame.image.load(asset('buttons', 'Client1.png')).convert_alpha(),
    'multi2': pygame.image.load(asset('buttons', 'Client2.png')).convert_alpha(),
    'DC': pygame.image.load(asset('buttons', 'DC.png')).convert_alpha(),
    'Controls': pygame.image.load(asset('buttons', 'Controls.png')).convert_alpha(),
    'Casual': pygame.image.load(asset('buttons', 'Casual.png')).convert_alpha(),
    'Ranked': pygame.image.load(asset('buttons', 'Ranked.png')).convert_alpha(),
    'Rankings': pygame.image.load(asset('buttons', 'Rankings.png')).convert_alpha(),
    'Speedrun': pygame.image.load(asset('buttons', 'SpeedRun.png')).convert_alpha(),
    'Rifle': pygame.image.load(asset('buttons', 'Rifle.png')).convert_alpha(),
    'Shotgun': pygame.image.load(asset('buttons', 'ShotGun.png')).convert_alpha(),
    'ShotgunClass1': pygame.image.load(asset('buttons', 'PreciseShot.png')).convert_alpha(),
    'ShotgunClass2': pygame.image.load(asset('buttons', 'MultiShot.png')).convert_alpha(),  
    'RifleClass1': pygame.image.load(asset('buttons', 'SMG.png')).convert_alpha(),
    'RifleClass2': pygame.image.load(asset('buttons', 'LaserGun.png')).convert_alpha(),        

}

gsiz = (1320, 300)

logo = pygame.image.load(asset('logo.png'))
pygame.display.set_icon(logo)

p = Player(players['PlayerRED'], 120, 455, 5, 1, 4.5, -1, 100, 10, 5, 10, 0)
p2 = EnemyPlayer(players['PlayerBLUE'], 1020, 455, 5, 1, 100, 2, -1, 1)
p3 = EnemyPlayer(players['PlayerBLUE'], 0, 455, 5, 1, 0, 3, -1, 1)

# - SHOP -
s = Shop(1,2,3,10,30,20,10,50,14,75,10.5,245,70)

enemyRect = pygame.Rect(p2.x, p2.y, p2.img.get_width()- 50, p2.img.get_height())
prect = pygame.Rect(p.x, p.y, p.img.get_width() - 50, p.img.get_height())
enemyRect2 = pygame.Rect(p3.x, p3.y, p3.img.get_width() - 50, p3.img.get_height())

# Rects
mouseRect = pygame.Rect((300, 300),(20,20))
grassRect = pygame.Rect((0,520),(1320,300))
statsrect = pygame.Rect((900, 100),(330,220))
consolenemyRect = pygame.Rect((700, 50),(230,230))

# Bullets List
bullets = []

# MAIN MENU
settings_button = Button(500,200,button_imgs['settings_button'],3)
start = Button(500,100,button_imgs['start'],3)
discord = Button(20,20,button_imgs['discord'],3)
mp = Button(500,300,button_imgs['multi'],3)
controls = Button(500,400,button_imgs['Controls'],3)
creditss = Button(500,500,button_imgs['credits'],3)

# PAUSE
login_button = Button(500,100,button_imgs['login'],3)
restart = Button(500,300,button_imgs['restart'],3)
DC4 = Button(500,500,button_imgs['DC'],3)

# RESOLUTIOn
resolution = Button(500,100,button_imgs['resolution'],3)
resolution1 = Button(500,200,button_imgs['resolution1'],3)
resolution2 = Button(500,300,button_imgs['resolution2'],3)

# OTHER
back = Button(900,350,button_imgs['back'],3)
mp1 = Button(500,50,button_imgs['multi1'],3)
mp2 = Button(500,150,button_imgs['multi2'],3)
DC = Button(500,250,button_imgs['DC'],3)
DC2 = Button(500,350,button_imgs['DC'],3)
Casual = Button(500,200,button_imgs['Casual'],3)
Ranked = Button(500,450,button_imgs['Ranked'],3)
SpeedRun = Button(500,300,button_imgs['Speedrun'],3)
start2 = Button(500,200,button_imgs['start'],3)

# Class Select
rifle = Button(500,400,button_imgs['Rifle'],3)
shotgun = Button(500,500,button_imgs['Shotgun'],3)
rifle2 = Button(900,150,button_imgs['Rifle'],3)
shotgun2 = Button(900,250,button_imgs['Shotgun'],3) 

shotgunclass1 = Button(350,250,button_imgs['ShotgunClass1'],3) 
shotgunclass2 = Button(650,250,button_imgs['ShotgunClass2'],3) 

rifleclass1 = Button(350,250,button_imgs['RifleClass1'],3) 
rifleclass2 = Button(650,250,button_imgs['RifleClass2'],3) 

v = VariableStorage() 

moving_sprites = pygame.sprite.Group()

d = dialogue('', '')

net = Peer()

try:
    versi = int(float(fetch("https://maxor.xyz/geneva/version.txt", versioncheck)))
except ValueError:
    versi = int(versioncheck)

def restartGame():
    # Drop back from round 30 subclasses to the base weapon
    if p.playerclass in (3, 4):
        p.playerclass = 2
    if p.playerclass in (5, 6):
        p.playerclass = 1
    p.hp = 100
    p2.hp = 100
    p3.hp = 0
    p3.dmg = 1
    p2.x = 1050
    p3.x = 0
    bullets.clear()
    gc.won = False
    gc.shop = False
    gc.chooseclass1 = False
    gc.ppr = 0
    gc.moment1 = time.time() * 1000
    d.dialogue = False
    p.faceval1 = 1
    p.faceval2 = -1
    p.lightspecial = p.darkspecial = p.uncap = p.lightused = False
    p.hasinvinc = p.invinc = p.hasdash = False
    p.abilitycount = 0
    v.darkvalue = 0
    s.six = 50
    s.seven = 70
    s.wepadd = 14
    s.ccadd = 75
    s.speedadd = 10.5
    s.dmgadd = 245
    gc.rnd = 1
    gc.points = 0
    p.speed = 4.5
    p2.speed = 2
    p.dmg = 10
    p2.dmg = 1
    p.bulletcnt = 4 if p.playerclass == 2 else 5
    p.cc = 10
    s.one = 1
    s.two = 2
    s.three = 3
    s.four = 10
    s.five = 20
    s.yeezus = 30
    gc.lost = False

def update():
    pygame.display.set_caption("updating.... " + version)
    try:
        gc.size = (int(fetch("https://maxor.xyz/geneva/width.txt")), int(fetch("https://maxor.xyz/geneva/height.txt")))
    except ValueError:
        gc.size = size
    pygame.display.set_mode(gc.size)
    if(int(versioncheck) < versi):
        pygame.display.set_caption("Geneva OUTDATED beta " + version)
    else:
        pygame.display.set_caption("Geneva")
    vars2 = fetch("https://maxor.xyz/geneva/vars.txt")
    try:
        maxor2 = vars2[0:5]
        s.hpadd = int(vars2[6:8])
        s.yeezus = int(vars2[9:11])
        if maxor2 == 'BLACK':
            gc.BULLCOLOR = BLACK
        else:
            gc.BULLCOLOR = pygame.Color(maxor2.translate({ord('-'): None}))
    except ValueError:
        pass

# Reset Resolution
def resetRes():
    grassRect.width = 0
    grassRect.height = 0

def getAbility():
    ability = randint(1,5)
    if ability == 1:
        if(p.lightspecial == False):
            p.lightspecial = True
            d.dialogue = True
            d.changeText('You unlocked ability light!', 'when you die you will get a free revive!')
            p.abilitycount += 1
        else:
            getAbility()
    if ability == 2:
        if(p.darkspecial == False):
            p.darkspecial = True
            d.dialogue = True
            d.changeText('You unlocked ability dark!', 'every 20 hits this will kill the enemy for you!')
            p.abilitycount += 1
        else:
            getAbility()
    if ability == 3:
        if(p.uncap == False):
            p.uncap = True
            d.dialogue = True
            d.changeText('You unlocked the ability uncap!', 'You may add +1 upgrade slots to a shop item!')
            p.abilitycount += 1
        else:
            getAbility()
    if ability == 4:
        if(p.hasinvinc == False):
            p.hasinvinc  = True
            d.dialogue = True
            d.changeText('You unlocked invincibility!', 'Press I once to gain invincibility for 1 round!')
            p.abilitycount += 1
        else:
            getAbility()
    if ability == 5:
        if(p.hasdash == False):
            p.hasdash  = True
            d.dialogue = True
            d.changeText('You unlocked dash!', 'Double Tap A or D to dash!')
            p.abilitycount += 1
        else:
            getAbility()            

def main():

    run = True
    clock = pygame.time.Clock()
    passtime = False
    loggedin = False
    paused = False
    settings = False
    yeezus = False
    hptxtx = 515
    hpcheck = True
    critvalue = 0
    crit = False
    cloudx = 0
    Y_GRAVITY = 0.7
    JUMP_HEIGHT = 12
    Y_VELOCITY = JUMP_HEIGHT
    console = False
    consoletxt = ''
    ranked = False
    value2 = 0

        

    # main
    while run:

        # TEXT VARIABLES
        shoptxt = font2.render("SHOP", (0, 5), BLUE)
        shoptxt3 = font3.render("Speed: KEY 2 PRC:" + str(s.two), (0, 5), BLACK)
        shoptxt2 = font3.render("HP: KEY 1 PRC:" + str(s.one), (0, 5), BLACK)
        shoptxt4 = font3.render("DMG: KEY: 3 PRC:" + str(s.three), (0, 5), BLACK)
        shoptxt5 = font3.render("WEAPON: KEY: 4 PRC:" + str(s.four), (0, 5), BLACK)
        shoptxt6 = font3.render("CC: KEY: 5 PRC:" + str(s.five), (0, 5), BLACK)
        shoptxt7 = font3.render("Ability: KEY: 6 PRC:" + str(s.six), (0, 5), BLACK)
        shoptxt8 = font3.render("Points: KEY: 7 PRC:" + str(s.seven), (0, 5), BLACK)
        
        if p.speed >= 11:
            shoptxt3 = font3.render("Speed: KEY 2 PRC:" + str(s.two), (0, 5), GREEN)
        if p.dmg >= 250:
            shoptxt4 = font3.render("DMG: KEY: 3 PRC:" + str(s.three), (0, 5), GREEN)
        if p.bulletcnt >= 15:
            shoptxt5 = font3.render("WEAPON: KEY: 4 PRC:" + str(s.four), (0, 5), GREEN)
        if p.cc >= 80:
            shoptxt6 = font3.render("CC: KEY: 5 PRC:" + str(s.five), (0, 5), GREEN)
        if p.abilitycount >= 4:
            shoptxt7 = font3.render("ABILITY: KEY: 6 PRC:" + str(s.six), (0, 5), GREEN)


        weaponstats = font6.render("Weapon Stats", (0, 5), BLACK)
        weaponstats2= font3.render("Bullet Count: " + str(p.bulletcnt), (0, 5), BLACK)
        weaponstats3 = font3.render("BulletSpeed: " + str(p.speed), (0, 5), BLACK)
        rounds = font3.render("rnd: " + str(gc.rnd), (0, 5), BLACK)

        weaponselect = font7.render("Weapon Select", (0, 5), BLACK)
        weaponselect2 = font6.render("Weapon Select", (0, 5), BLACK)

        if console:
            pygame.draw.rect(win, (70,70,70),consolenemyRect)
            ctxt = font4.render(consoletxt, (0,5), BLACK)
            win.blit(ctxt,(710,70))

        if gc.client == 1 or gc.client == 2:
            v.singleplayer = False

        if not gc.startclicked and not v.creditsactive and not settings and not v.resolutionclicked and not v.mpprompt and not v.controlspage and not gc.inlobby and not gc.singleplayerpromp and not v.classelect and not v.ipprompt:
            start.draw(win)
            discord.draw(win)
            creditss.draw(win)           
            mp.draw(win)           
            controls.draw(win)
            win.blit(players['PlayerRED2'], (80, 300))
            win.blit(players['PlayerBLUE'], (200, 300))
            win.blit(players['PlayerBLUEswing'], (300, 300))
            gen = font7.render("Geneva", (0, 5), BLACK)
            win.blit(gen,(100,200))

            if controls.clicked and not gc.restarted:
                v.controlspage = True


    
            if mp.clicked:
                v.mpprompt = True

            if creditss.clicked :
                v.creditsactive = True

            if discord.clicked:
                disco = fetch("https://maxor.xyz/geneva/discord.txt")
                if disco:
                    webbrowser.open(disco)

            if start.clicked:
                gc.singleplayerpromp = True
                p2.x = 1050
                v.startrecentlyclicked = True
                gc.restarted = False

        if gc.restarted:
            paused = False

        # GROUND AND CLOUD
        if gc.startclicked:
            if grassRect.width == 1460:
                win.blit(yeezusimg['deez2'],(0,425))
            else:    
                win.blit(yeezusimg['deez'],(0,425))
            if not console:
                win.blit(yeezusimg['cloud'],(cloudx,30))
            if cloudx > 1050: 
                cloudx = 0
            cloudx += 0.1
            pygame.draw.rect(win, (0,0,0),grassRect)
            if d.dialogue == True:
                d.draw()
                
            # SHOP
            if gc.shop and gc.won and not paused:
                win.blit(shoptxt, (20, 10))
                win.blit(shoptxt2, (20, 150))
                win.blit(shoptxt3, (20, 190))
                win.blit(shoptxt4, (20, 230))
                win.blit(shoptxt5, (20, 270))
                win.blit(shoptxt6, (20, 310))
                win.blit(shoptxt7, (20, 350))         
                win.blit(shoptxt8, (20, 390))         

                win.blit(points, (985, 10))
                pygame.draw.rect(win, (120,120,120),statsrect)
                win.blit(weaponstats, (900, 100))
                win.blit(weaponstats2, (920, 190))
                win.blit(weaponstats3, (920, 240))    


        if gc.singleplayerpromp and not v.classelect:
            SpeedRun.draw(win)
            Casual.draw(win)
            if SpeedRun.clicked and not v.startrecentlyclicked:
                v.classelect = True
                gc.singleplayerpromp = False
                gc.speedrun = True
                v.modeRecentlyChosen = True         
            if Casual.clicked and not v.startrecentlyclicked:
                v.classelect = True
                gc.speedrun = False
                gc.singleplayerpromp = False
                
        
        if v.startrecentlyclicked:
            v.startrecentlyclicked = False

        if v.classelect:
    
            rifle.draw(win)
            shotgun.draw(win)
            win.blit(weaponselect,(380,60))
            if rifle.clicked:
                if gc.speedrun:
                    gc.moment1 = time.time() * 1000
                p.playerclass = 1
                v.classelect = False
                gc.startclicked = True
            if shotgun.clicked:
                if gc.speedrun:
                    gc.moment1 = time.time() * 1000
                p.playerclass = 2
                p.changeImg(players['PlayerGREEN'])

                p.bulletcnt = 4
                v.classelect = False
                gc.startclicked = True

        # CREDITS
        if v.controlspage:
          
            control1 = font3.render("TAB - shop", (0, 5), BLACK)
            control2 = font3.render("N - start new round", (0, 5), BLACK)
            control3 = font3.render("ESC - pause", (0, 5), BLACK)
            win.blit(control1, (200, 50))
            win.blit(control2, (200, 150))
            win.blit(control3, (200, 250))
            back.draw(win)
            if back.clicked:
                v.controlspage = False
                
        # CREDITS
        if v.creditsactive:
          
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
                v.creditsactive = False
                
        if v.mpprompt:
            mp1.draw(win)           
            mp2.draw(win)          
            DC.draw(win)
            Ranked.draw(win)

            if Ranked.clicked:
                ranked = True
                if file_exists2:
                    with open(userinfopath) as f:
                        v.namelol = f.read()
                        gc.loggedinasnonadmin = True
                else:
                    gc.rankednameprompt = True

            if DC.clicked:
                gc.client = 0
                gc.inlobby = False
                v.mpprompt = False         

            if mp1.clicked:
                gc.inlobby = True
                gc.client = 1
                v.mpprompt = False
                net.host()
            if mp2.clicked:
                v.ipprompt = True
                v.mpprompt = False

        if v.ipprompt:
            iptxt = font6.render("Enter host IP and press Enter", (0, 5), BLACK)
            iptxt2 = font6.render(v.joinip + '_', (0, 5), BLACK)
            win.blit(iptxt,(200,150))
            win.blit(iptxt2,(200,250))
            back.draw(win)
            if back.clicked:
                v.ipprompt = False
                v.mpprompt = True

        if settings and not v.resolutionclicked:
            resolution.draw(win)           
            if resolution.clicked:
                v.resolutionclicked = True
        
        if v.resolutionclicked:
            resolution1.draw(win)           
            resolution2.draw(win)           

            if resolution1.clicked:
                size = (1320, 737)
                resetRes()
                grassRect.width += 1320
                grassRect.height += 737
                v.resolutionclicked = False
                settings = False
                pygame.display.set_mode(size)
            if resolution2.clicked:
                size = (1460, 900)
                resetRes()
                grassRect.width += 1460
                grassRect.height += 900
                settings = False
                v.resolutionclicked = False
                pygame.display.set_mode(size)               


        hp = font3.render("hp: " + str(round(p.hp)), (0, 5), BLACK)
        spd = font3.render("spd: " + str(p.speed), (0, 5), BLACK)
        dmg = font3.render("dmg: " + str(p.dmg), (0, 5), BLACK)
        points = font3.render("points: " + str(round(gc.points)), (0, 5), BLACK)
        cc = font3.render("critchance: " + str(p.cc), (0, 5), BLACK)


        if gc.inlobby and not gc.lobbystarted:
            if gc.client == 2:
                DC2.draw(win)
                rifle2.draw(win)
                shotgun2.draw(win)
                win.blit(weaponselect2,(860,60))
                if rifle2.clicked:
                    p.playerclass = 1
                if shotgun2.clicked:
                    p.playerclass = 2
                    p.bulletcnt = 4
                if DC2.clicked:
                    net.close()
                    gc.client = 0
                    gc.startclicked = False
                    v.singleplayer = True
                    gc.inlobby = False

                inl = font3.render(net.status, (0, 5), BLACK)
                win.blit(inl,(100,100))       

                if net.started:
                    if p.playerclass == 0:
                        p.playerclass = 1
                    gc.inlobby = False
                    gc.startclicked = True
                    gc.lobbystarted = True            
                    p2.x = 1050
                    p.hp = 100

            if gc.client == 1:
                DC2.draw(win)
                rifle2.draw(win)
                shotgun2.draw(win)
                win.blit(weaponselect2,(860,60))
                if rifle2.clicked:
                    p.playerclass = 1
                if shotgun2.clicked:
                    p.playerclass = 2
                    p.bulletcnt = 4
                if DC2.clicked:
                    net.close()
                    gc.client = 0
                    gc.startclicked = False
                    v.singleplayer = True
                    gc.inlobby = False
                    v.mpprompt = False

                inl21 = font3.render(net.status, (0, 5), BLACK)
                win.blit(inl21,(100,100))

                inl = font3.render("You are hosting the game!", (0, 5), BLACK)
                if net.connected:
                    start2.draw(win)
                if net.connected and start2.clicked:
                    if p.playerclass == 0:
                        p.playerclass = 1
                    p.hp = 100
                    net.send(type='start')
                    gc.inlobby = False
                    gc.startclicked = True
                    gc.lobbystarted = True            
                    p2.x = 1050

                win.blit(inl,(400,50))       

        if gc.rankednameprompt and not file_exists2:
            wmp = font6.render("Enter your name to be logged in the leaderboard!", (0, 5), GREEN)            
            win.blit(wmp,(100,350))
            
        if v.highscoreprompt or gc.rankednameprompt and ranked:
            nm = font6.render(v.namelol, (0, 5), BLACK)
            win.blit(nm,(100,300))

        if gc.lostmp:
            lmp = font6.render("You Lost this game!", (0, 5), RED)
            win.blit(lmp,(400,300))
        if gc.wonmp:
            DC.draw(win)
            if gc.speedrun:
                wmp = font6.render("Speedrun Done!", (0, 5), GREEN)
            else:
                wmp = font6.render("You Won this game!", (0, 5), GREEN)
                if ranked and not gc.sentrankedwin:
                    sendWebhook('https://discord.com/api/webhooks/1007335442917621760/VsmtTUpYO0GS27_iJosLRAuw0Fqyrs_MhC0S9vQ_IyvIizIPBVG_ieJLsHzTNSgbppTy', v.namelol + ' has won a ranked game!')
                    gc.sentrankedwin = True

            win.blit(wmp,(400,300))
            if DC.clicked:
                net.close()
                gc.client = 0
                gc.lobbystarted = False
                gc.wonmp = False
                gc.lostmp = False
                gc.startclicked = False
                v.singleplayer = True
                restartGame()

        if yeezus:
            p2.yeezus = True
            p.yeezus = True
        if paused or not gc.startclicked and not v.creditsactive and not settings and not v.mpprompt and not v.controlspage and not gc.inlobby and not gc.singleplayerpromp and not v.classelect and not v.ipprompt:
            settings_button.draw(win)
            if(settings_button.clicked):
                if not settings:
                    settings = True
                else:
                    settings = False

        if paused and gc.startclicked:
            if not settings:
                login_button.draw(win)
                restart.draw(win)
                DC4.draw(win)
                if DC4.clicked:
                    gc.startclicked = False
                    v.singleplayer = True
                    gc.restarted = True
                    restartGame()

            if(restart.clicked):
                restartGame()

            if(settings_button.clicked):
                if not settings:
                    settings = True
                else:
                    settings = False
            if(login_button.clicked):
                if not gc.login:
                    gc.login = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                net.close()

                run = False


            if event.type == pygame.MOUSEBUTTONDOWN and gc.startclicked:
                        if mouseRect.x > p.x:
                            p.facing = 1
                            p.facingX = -10
                            if p.playerclass == 1 or p.playerclass == 5 or p.playerclass == 6:
                                p.changeImg(players['PlayerRED2'])
                            else:
                                p.changeImg(players['PlayerGREEN2'])

                        else:
                            p.facing = -1
                            p.facingX = 10

                            if p.playerclass == 1 or p.playerclass == 5 or p.playerclass == 6:
                                p.changeImg(players['PlayerRED'])
                            else:
                                p.changeImg(players['PlayerGREEN'])


                        if p.playerclass == 1 and len(bullets) < p.bulletcnt and not paused and p.hp > 0:  # This will make sure we cannot exceed 5 bullets on the screen at once
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10), 6, (gc.BULLCOLOR), p.facing, 1))
                        if p.playerclass == 2 and len(bullets) < p.bulletcnt and not paused and p.hp > 0:
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10), 6, (gc.BULLCOLOR), p.facing, 1))                            
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) - 5, 6, (gc.BULLCOLOR), p.facing, 2))                            
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) + 5, 6, (gc.BULLCOLOR), p.facing, 3))                            
                        if p.playerclass == 3 and len(bullets) < p.bulletcnt and not paused and p.hp > 0:
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10), 6, (gc.BULLCOLOR), p.facing, 0))                            
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) - 5, 6, (gc.BULLCOLOR), p.facing, 0))                            
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) + 5, 6, (gc.BULLCOLOR), p.facing, 0))                            
                        if p.playerclass == 4 and len(bullets) < p.bulletcnt and not paused and p.hp > 0:
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10), 6, (gc.BULLCOLOR), p.facing, 1))                            
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) - 5, 6, (gc.BULLCOLOR), p.facing, 2))                            
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) + 5, 6, (gc.BULLCOLOR), p.facing, 3)) 
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) - 10, 6, (gc.BULLCOLOR), p.facing, 4)) 
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 10) + 10, 6, (gc.BULLCOLOR), p.facing, 5)) 
                        if p.playerclass == 5 and len(bullets) < p.bulletcnt and not paused and p.hp > 0:
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 60), 6, (gc.BULLCOLOR), p.facing, 1))
                            if p.facing == 1:
                                bullets.append(projectile(round(prect.x+prect.width//2 + 20), round(prect.y + prect.height//2 - 60), 6, (gc.BULLCOLOR), p.facing, 1))
                            else:
                                bullets.append(projectile(round(prect.x+prect.width//2 - 20), round(prect.y + prect.height//2 - 60), 6, (gc.BULLCOLOR), p.facing, 1))

                        if p.playerclass == 6 and len(bullets) < p.bulletcnt and not paused and p.hp > 0:
                            bullets.append(projectile(round(prect.x+prect.width//2 - p.facingX), round(prect.y + prect.height//2 - 60), 7, (GREEN), p.facing, 1))


            else:
                if event.type == pygame.KEYDOWN:
                    if v.ipprompt:
                        if event.key == pygame.K_RETURN:
                            v.ipprompt = False
                            gc.inlobby = True
                            gc.client = 2
                            net.join(v.joinip or '127.0.0.1')
                        elif event.key == K_BACKSPACE:
                            v.joinip = v.joinip[:-1]
                        elif event.unicode.isprintable() and event.unicode != ' ':
                            v.joinip += event.unicode
                    if v.highscoreprompt:
                        if event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                            v.namelol += event.unicode
                        if event.key == K_BACKSPACE:
                            v.namelol = ''
                        if event.key == pygame.K_RETURN:
                            if v.highscoreprompt:
                                sendWebhook('https://discord.com/api/webhooks/1005987949067894905/igWvhRDPoDRmTXG2LX-hfMThbmpePBnNpsmACd1saZsHoZRA-_DcMYK95CiosZN3Ul86', v.namelol + ' has beaten the highscore!!')
                                v.highscoreprompt = False
                    if gc.rankednameprompt and ranked and not file_exists2:
                            if event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                                v.namelol += event.unicode
                            if event.key == K_BACKSPACE:
                                v.namelol = ''
                            if event.key == pygame.K_RETURN:
                                gc.rankednameprompt = False
                                gc.loggedinasnonadmin = True
                                with open(userinfopath, 'w') as f:
                                    f.write(v.namelol)
                    if console:
                        if(event.key == pygame.K_ESCAPE and loggedin):
                            console = False
                                
                        if event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                            consoletxt += event.unicode
                        if event.key == K_BACKSPACE:
                            consoletxt = ''                
                        if event.key ==  pygame.K_RETURN and v.singleplayer:
                            if consoletxt == 'php' and gc.consolestage == 0:
                                consoletxt = ''
                                gc.consolestage = 1
                            if consoletxt == 'rnd' and gc.consolestage == 0:
                                consoletxt = ''
                                gc.consolestage = 2      
                            if consoletxt == 'points' and gc.consolestage == 0:
                                consoletxt = ''
                                gc.consolestage = 3    
                            if consoletxt == 'killenemy' and gc.consolestage == 0:
                                p2.hp = 0
                                p3.hp = 0                 
                                consoletxt = ''
                            if consoletxt == 'godmode' and gc.consolestage == 0:
                                p.invinc = True
                                consoletxt = ''
                            if consoletxt == 'showhitboxes' and gc.consolestage == 0:
                                v.showHitbox = True
                                consoletxt = ''

                            if consoletxt == 'class' and gc.consolestage == 0:
                                consoletxt = ''
                                gc.consolestage = 4    


                            if gc.consolestage != 0 and consoletxt != '':
                                try:
                                    if gc.consolestage == 1:
                                        p.hp = int(consoletxt)
                                    if gc.consolestage == 2:
                                        gc.rnd = int(consoletxt)
                                    if gc.consolestage == 3:
                                        gc.points = int(consoletxt)
                                    if gc.consolestage == 4:
                                        p.playerclass = int(consoletxt)
                                except ValueError:
                                    pass
                                gc.consolestage = 0
                                consoletxt = ''
                     
                    else:
                        if event.key == pygame.K_a:
                            if p.hasdash and p.dashstate < 1:
                                p.dashstate += 1
                            elif p.hasdash and p.dashstate >= 1:
                                p.x -= 50
                                if p.x < 0:
                                    p.x = 0                               
                                p.dashstate = 0
                        if event.key == pygame.K_d:
                            if p.hasdash and p.dashstate2 < 1:
                                    p.dashstate2 += 1
                            elif p.hasdash and p.dashstate2 >= 1:
                                    p.x += 50
                                    if p.x > 1240:
                                        p.x = 1240
                                    p.dashstate2 = 0                                

                        if(gc.login and paused):
                            if passtime and event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                                gc.password += event.unicode
                            elif not passtime and event.key is not pygame.K_RETURN and event.key is not pygame.K_ESCAPE and event.key is not pygame.K_SPACE and event.key is not pygame.K_BACKSPACE:
                                gc.username += event.unicode
                            if event.key == K_BACKSPACE:
                                if not passtime:
                                    gc.username = ''
                                else:
                                    gc.password = ''
                    
                        if event.key == pygame.K_SPACE:
                            if d.dialogue:
                                d.dialogue = False
                            else:
                                if(not p.jump):
                                    p.jump = True
                                if gc.login:
                                    passtime = True

                        if event.key == pygame.K_i:
                            if p.hasinvinc:
                                p.invinc = True
                                    
                        if event.key == pygame.K_RETURN:
                            if passtime and not loggedin:
                                data = fetch("https://maxor.xyz/geneva/logins.json")
                                maxor = data.find(gc.username, 0, 340)
                                maxor2 = data.find(gc.password, 0, 340)
                                num = maxor2 - maxor
                                # print(str(num))
                                if(maxor == -1):
                                    gc.username = ''
                                    gc.password = ''

                                elif (num <= 74 and num > 29 and gc.password != '' and gc.password != 'attributes' and gc.password != 'pass'):
                                    loggedin = True
                                    sendWebhook('https://discord.com/api/webhooks/1005947184207892620/MdrkcgX-XJd4z55TfZcHoCzy7jVSOZz2OwyrMloE6FF8fl0aQ89m1f4dTZQeJPfFnU-p', ' Someone has logged into the admin account: ' + gc.username)
                                    v.namelol = gc.username
                                    with open(userinfopath, 'w') as f:
                                        f.write(v.namelol)

                        if event.key == pygame.K_n and not gc.chooseclass1:
                            if(gc.won):
                                gc.won = False
                                if gc.rnd < 40:
                                    # print(str(p.x))
                                    if p.x <= 564:
                                        p2.x = 1020
                                    else:
                                        p2.x = 10
                                else:
                                    p3.x = 0
                                    p2.x = 1020

                        if event.key == pygame.K_TAB and gc.won:
                            if(gc.shop):
                                gc.shop = False
                            else:
                                gc.shop = True


                        if event.key == pygame.K_ESCAPE:
                            if(not paused):
                                paused = True
                            else:
                                paused = False

                        if(event.key == pygame.K_u and paused and not gc.login):
                            update()
                        if(event.key == pygame.K_c and loggedin and v.singleplayer and not gc.speedrun):
                            console = True
                                
                        if(gc.shop):
                            if(event.key == pygame.K_1):
                                if(gc.points >= s.one):
                                    gc.points -= s.one
                                    s.one += 1
                                    p.hp += s.hpadd
                            if(event.key == pygame.K_2):
                                if(p.uncap):
                                    s.speedadd += 1
                                    p.uncap = False                                      
                                if(gc.points >= s.two and p.speed <= s.speedadd):
                                    gc.points -= s.two 
                                    s.two += 1
                                    p.speed += 0.5
                            if(event.key == pygame.K_3):
                                if(p.uncap):
                                    s.dmgadd += 5
                                    p.uncap = False                                
                                if(gc.points >= s.three  and p.dmg <= s.dmgadd):
                                    gc.points -= s.three
                                    s.three += 1
                                    p.dmg += 5
                            if(event.key == pygame.K_4):
                                if(p.uncap):
                                    s.wepadd += 1
                                    p.uncap = False
                                if(gc.points >= s.four and p.bulletcnt <= s.wepadd):
                                    gc.points -= s.four
                                    s.four += 15 
                                    p.bulletcnt += 1
                                    p.faceval2 -= 0.25
                                    p.faceval1 += 0.25

                            if(event.key == pygame.K_5):
                                if(p.uncap):
                                    s.ccadd += 5
                                    p.uncap = False                                
                                if(gc.points >= s.five and p.cc <= s.ccadd):
                                    gc.points -= s.five
                                    s.five += 10 
                                    p.cc += 5
                            if(event.key == pygame.K_6 and p.abilitycount <= 3):
                                if(gc.points >= s.six):
                                    gc.points -= s.six
                                    d.dialogue = True
                                    s.six *= 2
                                    getAbility()
                            if(event.key == pygame.K_7 and gc.ppr < 4):
                                if(gc.points >= s.seven):
                                    gc.points -= s.seven
                                    s.seven *= 2
                                    gc.ppr += 1                                

                            if(event.key == pygame.K_y):
                                if(gc.points >= s.yeezus):
                                    gc.points -= s.yeezus
                                    s.yeezus += 200 * gc.rnd
                                    p.dmg += 10
                                    p.speed += 1
                                    yeezus = True

        if gc.loggedinasnonadmin == True and gc.inlobby or gc.loggedinasnonadmin == True and v.mpprompt:
            nm = font6.render(v.namelol, (0, 5), BLACK)
            win.blit(nm,(100,50))

        if loggedin and gc.startclicked:
            pygame.display.set_caption("Geneva Admin Edition")
            if hpcheck:
                p.hp = 3000
                hptxtx -= 30
                hpcheck = False
                gc.lost = False
        
        p.checkFacing()

        if v.highscoreprompt:
            d.dialogue = True
            d.changeText('You have beaten the hs, what would you like your name to appear as?!' , 'Good Job')

        if gc.login and paused:
            use = font3.render(gc.username, True, (BLACK))
            win.blit(use, (20,20))
        if passtime and paused:
            pas = font3.render(gc.password, True, (BLACK))
            win.blit(pas, (20,60))
            

        if p.hp <= 0 and not gc.lost:
            d.dialogue = True
            if p.lightspecial and not p.lightused:
                d.changeText("Ability light saved you!", 'press N to keep fighting')
                p.hp = 100
                gc.won = True
                p.lightused = True
            else:
                d.changeText("Ratio U LOST", 'ESC then restart to play again :(((')
                gc.lost = True
                if v.goths:
                    sendWebhook('https://discord.com/api/webhooks/1005987949067894905/igWvhRDPoDRmTXG2LX-hfMThbmpePBnNpsmACd1saZsHoZRA-_DcMYK95CiosZN3Ul86', v.namelol + ' had died in their hs run with a final score of ' + str(gc.rnd))
                           
        # MOVE PLAYER 2
        if not paused or not v.singleplayer and gc.lobbystarted and not paused and not v.classelect:
            p2.move(p.x, p2.x)
            if gc.rnd >= 40 and not gc.won:
                p3.move(p.x, p3.x)

        # JUMPING
        if p.jump:
            p.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY < -JUMP_HEIGHT:
                p.jump = False
                Y_VELOCITY = JUMP_HEIGHT
            
        if not  p.jump:
            if p.y < 455:
                p.y += 2 

        # WIN TEXT

        if(gc.won and not gc.shop and not paused and not console):
            win.blit(wintxt, (180, 20))

        if gc.chooseclass1:
            if p.playerclass == 2:
                shotgunclass1.draw(win)
                shotgunclass2.draw(win)
                if shotgunclass1.clicked:
                    gc.chooseclass1 = False
                    p.playerclass = 3 

                if shotgunclass2.clicked:
                    gc.chooseclass1 = False               
                    p.playerclass = 4 
            if p.playerclass == 1:
                rifleclass1.draw(win)
                rifleclass2.draw(win)
                if rifleclass1.clicked:
                    gc.chooseclass1 = False
                    p.playerclass = 5 
                    p.faceval2 -= 3
                    p.faceval1 += 3

                if rifleclass2.clicked:
                    gc.chooseclass1 = False               
                    p.playerclass = 6                 
                    p.faceval2 -= 1
                    p.faceval1 += 1

        # KEY HANDLING 2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if(p.x > 2):
                p.x -= p.speed
                if yeezus:
                    p.changeImg(yeezusimg['yeezus'])
                else:
                    if p.playerclass == 1 or p.playerclass == 5 or p.playerclass == 6:
                        p.changeImg(players['PlayerRED'])
                    else:
                        p.changeImg(players['PlayerGREEN'])
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] :
            if(p.x < 1240):
                if yeezus:
                    p.changeImg(yeezusimg['yeezus2'])
                else:
                    if p.playerclass == 1 or p.playerclass == 5 or p.playerclass == 6:
                        p.changeImg(players['PlayerRED2'])
                    else:
                        p.changeImg(players['PlayerGREEN2'])
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
        prect.y = (p.y - 40)
        if(p.x < p2.x):
         enemyRect.x = (p2.x + 20)
        if(p.x > p2.x):
         enemyRect.x = (p2.x - 20)
        if(p.x < p3.x):
         enemyRect2.x = (p3.x + 20)
        if(p.x > p3.x):
         enemyRect2.x = (p3.x - 20)

        enemyRect2.y = p3.y - 40
        enemyRect.y = p2.y - 40
        if v.showHitbox:
            pygame.draw.rect(win, (0,0,0),enemyRect)
            pygame.draw.rect(win, (0,0,0),prect)

        # HITBOXES
        p2.hitbox = (p2.x + 17, p2.y + 11, 29, 52) # NEW\
        p3.hitbox = (p3.x + 17, p3.y + 11, 29, 52) # NEW
        if (enemyRect2.colliderect(prect)):
            p3.attack = True
            if gc.rnd < 49:
                value2 += 1
            else:
                value2 += 2

            if(value2 >= 70):
                value2 = 0
        else:
            p3.attack = False
            value2 = 0

        if (enemyRect.colliderect(prect)):
            p2.attack = True
            if gc.rnd < 49:
                v.value += 1
            elif gc.rnd < 100:
                v.value += 2
            else:
                v.value += 2.5

            if(v.value >= 70):
                v.value = 0
        else:
            p2.attack = False
            v.value = 0

        for bullet in bullets[:]:

            bullet.draw(win)

            if bullet.x < 1320 and bullet.x > 0: 
                if p.playerclass >= 2 and p.playerclass <= 4:
                    if bullet.bulletid == 2:
                        bullet.y += 0.75
                    if bullet.bulletid == 1:
                        bullet.y -= 0.75   
                    if bullet.bulletid == 3:
                        bullet.y += 0.75
                        if bullet.y > 500:
                            bullets.remove(bullet)
                    if bullet.bulletid == 4:
                        bullet.y -= 0.75
                    if bullet.bulletid == 5:
                        bullet.y += 0.75
                        if bullet.y > 500:
                            bullets.remove(bullet)

                bullet.x += bullet.vel  # Moves the bullet by its vel
            else:
                if(bullet in bullets):
                    bullets.pop(bullets.index(bullet))  # This will remove the bullet if it is off 

            if not gc.lost and not gc.won and not paused:
                if gc.rnd >= 40 and p3.hp > 0:
                    if bullet.y + bullet.radius < p3.hitbox[1] + 60 + p3.hitbox[3] and bullet.y + bullet.radius > p3.hitbox[1] - 60 or prect.colliderect(enemyRect2):
                                        if bullet.x + bullet.radius > p3.hitbox[0] + 13 and bullet.x - bullet.radius < p3.hitbox[0] + p3.hitbox[2] - 13 or prect.colliderect(enemyRect2):
                                            if(randint(1, 100) <= p.cc):
                                                p3.hp -= (p.dmg * 2)
                                                crit = True
                                                if p.darkspecial == True:
                                                    v.darkvalue += 1
                                                    if v.darkvalue == 20:
                                                        p3.hp = 0
                                                        v.darkvalue = 0
                                            else:
                                                if p.darkspecial == True:
                                                    v.darkvalue += 1
                                                    if v.darkvalue == 20:
                                                        p3.hp = 0
                                                        v.darkvalue = 0
                                                        
                                                if p.playerclass == 6:
                                                    p3.hp -= 20           

                                                p3.hp -= p.dmg            
                                                        
                if p2.hp > 0 and (bullet.y + bullet.radius < p2.hitbox[1] + 60 + p2.hitbox[3] and bullet.y + bullet.radius > p2.hitbox[1] - 60 or prect.colliderect(enemyRect)):
                    if bullet.x + bullet.radius > p2.hitbox[0] + 13 and bullet.x - bullet.radius < p2.hitbox[0] + p2.hitbox[2] - 13 or prect.colliderect(enemyRect):
                        if(randint(1, 100) <= p.cc):
                            p2.hp -= (p.dmg * 2)
                            crit = True
                            if p.darkspecial == True:
                                v.darkvalue += 1
                                if v.darkvalue == 20:
                                    p2.hp = 0
                                    v.darkvalue = 0
                        else:
                            if p.darkspecial == True:
                                v.darkvalue += 1
                                if v.darkvalue == 20:
                                    p2.hp = 0
                                    v.darkvalue = 0

                            if p.playerclass == 6:
                                p2.hp -= 20     

                            p2.hp -= p.dmg

                        if not gc.won:
                            if bullet in bullets:
                                bullets.pop(bullets.index(bullet))

        # SCALE ENEMY
        if gc.startclicked and not gc.won and not gc.lost and not paused and p2.hp <= 0 and p3.hp <= 0:
            gc.won = True
            if(p.speed >= p2.speed):
                p2.speed += 0.15
            elif p.speed <= p2.speed and p.speed <= 9.5:
                p2.speed += 0.05

            gc.rnd += 1
            if gc.rnd == 30:
                gc.chooseclass1 = True

            if gc.speedrun:
                if gc.rnd >= 50:
                    gc.moment2 = time.time() * 1000
                    gc.finaltime =  gc.moment2 - gc.moment1
                    gc.finaltime /= 1000
                    d.dialogue = True
                    d.text = 'Final Time ' + str(round(gc.finaltime)) + ' seconds'

                    gc.wonmp = True

            if not v.singleplayer:
                net.send(type='rnd', value=gc.rnd)
            if p.invinc:
                p.hasinvinc = False
                p.invinc = False        

            if gc.rnd < 140:
                p2.hp += 100 
                if gc.rnd >= 40:
                    p3.hp += 100
                    p3.hp += (gc.rnd * 15)

                p2.hp += (gc.rnd * 15)
            else:
                p2.hp += 250
                if gc.rnd > 40:
                    p3.hp += 250
                    p3.hp += (gc.rnd * 20) 
                p2.hp += (gc.rnd * 20)

            if gc.rnd >= 40:
                p3.dmg += 0.1

            p2.dmg += 0.2
            if gc.rnd < 100:
                gc.points += gc.ppr + (1 + (gc.rnd * 0.1)) 
            else:
                gc.points += gc.ppr + (1 + (gc.rnd * 0.05))                               

            if highscore is not None and highscore < gc.rnd and not v.goths and not loggedin:
                v.highscoreprompt = True
                v.goths = True

        if not v.singleplayer and gc.lobbystarted:
            gc.ernd = net.peerrnd
            if net.connected:
                erounds = font3.render("ernd: " + str(gc.ernd), (0, 5), RED)
            else:
                erounds = font3.render(net.status, (0, 5), RED)
            if gc.ernd >= 50 and gc.rnd < 50:
                gc.lostmp = True
                gc.wonmp = False
            if not gc.lostmp and gc.rnd >= 50:
                gc.wonmp = True

        if not paused and gc.startclicked and not v.highscoreprompt:
            win.blit(hp, (hptxtx, 10))
            win.blit(spd, (650, 10))
            win.blit(dmg, (800, 10))
            if not gc.shop or not gc.won:
                win.blit(cc, (950, 10))
            win.blit(rounds,(390,10))
            if not v.singleplayer and gc.lobbystarted:
                win.blit(erounds,(390,50))                        

        # DRAW PLAYER
        if not gc.lost and gc.startclicked:         
          win.blit(p.img, (p.x, p.y - 40))

        if p2.hp > 0 and (not gc.won and not paused and not gc.lost and gc.startclicked or not v.singleplayer and gc.lobbystarted and not gc.won and not paused and not gc.lost and gc.startclicked):
          if(v.value <= 25):
            win.blit(p2.img, (p2.x, p2.y - 40))
          if(v.value > 25 and v.value <= 55):
            if yeezus:
                win.blit(yeezusimg['yeezusswing'], (p2.x, p2.y - 40))
            else:
                if(p2.facing > 0):
                 win.blit(players['PlayerBLUEswing'], (p2.x, p2.y  - 40))
                if(p2.facing < 0):
                 win.blit(players['PlayerBLUEswing23'], (p2.x, p2.y  - 40))

          if(v.value > 55 and v.value <= 60 ):
            if yeezus:
                win.blit(yeezusimg['yeezusswing2'], (p2.x, p2.y - 40))
            else:
                if(p2.facing < 0):                
                    win.blit(players['PlayerBLUEswing22'], (p2.x, p2.y - 40))
                if(p2.facing > 0):
                    win.blit(players['PlayerBLUEswing2'], (p2.x, p2.y - 40))

          if(v.value > 60 and v.value <= 70 ):
            if yeezus:
                win.blit(yeezusimg['yeezusswing2'], (p2.x, p2.y - 40))
            else:
                if(p2.facing < 0):
                    win.blit(players['PlayerBLUEswing32'], (p2.x, p2.y - 40))
                if(p2.facing > 0):
                    win.blit(players['PlayerBLUEswing3'], (p2.x, p2.y - 40))                
            if not p.invinc:
                p.hp -= p2.dmg

        # SECOND ENEMY
        if not gc.won and not paused and not gc.lost and gc.startclicked or not v.singleplayer and gc.lobbystarted and not gc.won and not paused and not gc.lost and gc.startclicked and gc.rnd >= 40:
          if(value2 <= 25 and p3.hp > 0):
            win.blit(p3.img, (p3.x, p3.y - 40))
          if(value2 > 25 and value2 <= 55 and p3.hp > 0):
            if yeezus:
                win.blit(yeezusimg['yeezusswing'], (p3.x, p3.y - 40))
            else:
                if(p3.facing > 0):
                 win.blit(players['PlayerBLUEswing'], (p3.x, p3.y  - 40))
                if(p3.facing < 0):
                 win.blit(players['PlayerBLUEswing23'], (p3.x, p3.y  - 40))

          if(value2 > 55 and value2 <= 60 and p3.hp > 0):
            if yeezus:
                win.blit(yeezusimg['yeezusswing2'], (p3.x, p3.y - 40))
            else:
                if(p3.facing < 0):                
                    win.blit(players['PlayerBLUEswing22'], (p3.x, p3.y - 40))
                if(p3.facing > 0):
                    win.blit(players['PlayerBLUEswing2'], (p3.x, p3.y - 40))

          if(value2 > 60 and value2 <= 70 and p3.hp > 0):
            if yeezus:
                win.blit(yeezusimg['yeezusswing2'], (p3.x, p3.y - 40))
            else:
                if(p3.facing < 0):
                    win.blit(players['PlayerBLUEswing32'], (p3.x, p3.y - 40))
                if(p3.facing > 0):
                    win.blit(players['PlayerBLUEswing3'], (p3.x, p3.y - 40))                
            if not p.invinc:
                p.hp -= p3.dmg

        mouseRect.x ,mouseRect.y = pygame.mouse.get_pos()
        pygame.draw.rect(win, (0,0,0),mouseRect)

        pygame.display.flip()

        clock.tick(60)
        pygame.display.update()

        if gc.startclicked or gc.inlobby:
            win.fill(LBLUE)
        else:
            win.fill(WHITE)

    pygame.quit()

if int(versioncheck) < versi:
    update()
main()

# END
# PLEASE FIX ALL MY MONKEY CODE PLS - MAXOR