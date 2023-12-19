########################################################################
# game only works for aspect ratio 1920x1080 @ 150% zoom level         #
# playing the game off of these settings will result in visual glitches#
# ye be warned                                                         #
########################################################################
import pygame as py
import pygame_menu as pymenu
import random
import challenges
from engi1020.arduino.api import *
py.init()
py.font.init()

oled_clear()

screen = py.display.set_mode((1920,1080))

background = py.image.load('assets/Background/Background.png')
player2 = py.image.load('assets/Player/PlayerRun2.png')
player1 = py.image.load('assets/Player/PlayerRun1.png')
player4 = py.image.load('assets/Player/PlayerRun4.png')
player3 = py.image.load('assets/Player/PlayerRun3.png')
playerdead = py.image.load('assets/Player/playerdead.png')
jumping = py.image.load('assets/Player/PlayerJump.png')
hydrantimg = py.image.load('assets/Obstacles/Hydrant.png')
signimg = py.image.load('assets/Obstacles/Sign.png')

signimg = py.transform.scale(signimg, (128, 128))
hydrantimg = py.transform.scale(hydrantimg, (64,64))
player2 = py.transform.scale(player2, (128,128))
player1 = py.transform.scale(player1, (128,128))
player3 = py.transform.scale(player3, (128,128))
player4 = py.transform.scale(player4, (128,128))
jumping = py.transform.scale(jumping, (128,128))
playerdead = py.transform.scale(playerdead, (128,128))

running = [player1, player2, player3, player4, player3, player2]



clock = py.time.Clock()

class Background(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = background.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (1200, 370)

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = running[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (500,700)

class Hydrant(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hydrantimg.convert_alpha()
        self.rect = self.image.get_rect(center=(1800,795))
        

    def update(self):
        self.rect.move_ip(-6, 0) 
        if self.rect.right < 0:
            self.kill()


class Sign(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = signimg.convert_alpha()
        self.rect = self.image.get_rect(center=(1800,765))

    def update(self):
        self.rect.move_ip(-6, 0)
        if self.rect.right < 0:
            self.kill()

def challengemsg():
    global randomChallenge
    chalList = ['lightson','pressbut','swipeleft','swiperight','lightsoff','dialright', 'dialleft']
    randomChallenge = random.choice(chalList)
    if randomChallenge == 'lightson':
        msg = 'Turn on the lights!'
    elif randomChallenge == 'swiperight':
        msg = 'Swipe the arduino right!'
    elif randomChallenge == 'swipeleft':
        msg = 'Swipe the arduino left!'
    elif randomChallenge == 'pressbut':
        msg = 'Press and hold the button!'
    elif randomChallenge == 'lightsoff':
        msg = 'Turn the lights off!'
    elif randomChallenge == 'dialright':
        msg = 'Turn the dial to the right!'   
    elif randomChallenge == 'dialleft':
        msg = 'Turn the dial to the left!'
    return msg

def challenge():
    if randomChallenge == 'lightson':
        res = challenges.lightson()
    elif randomChallenge == 'swiperight':
        res = challenges.swiperight()
    elif randomChallenge == 'swipeleft':
        res = challenges.swipeleft()
    elif randomChallenge == 'pressbut':
        res = challenges.pressbut()
    elif randomChallenge == 'lightsoff':
        res = challenges.lightsoff()
    elif randomChallenge == 'dialright':
        res = challenges.dialright()
    elif randomChallenge == 'dialleft':
        res = challenges.dialleft()
    return res

def pause(time):
    background = Background()
    global numchal, run
    msg = challengemsg()
    while time > 0:
        font = py.font.SysFont('Comic Sans MS', 30)
        screen.blit(background.image, background.rect)
        surf = font.render(f'{msg} in {time/1000} Seconds', False, (255,255,255))
        screen.blit(surf, dest=(960,500))
        py.display.update()
        py.time.delay(500)
        time -= 500
    res = challenge()
    if res:
        numchal += 1
    else:
        screen.blit(background.image, background.rect)
        font = py.font.SysFont('Comic Sans MS', 30)
        surf = font.render('You ran out of time!', False, (255,255,255))
        screen.blit(surf, dest=(960,500))
        py.display.update()
        py.time.delay(1000)
        highscore(name, numchal)
        run = False


def highscore(name, numchal):
    file = open('highscore.txt', 'a')
    file.write(f'{name} : {numchal}\n')
    file.close()

def Menu():
    global name
    menu = pymenu.Menu('City Dash', 1250, 710, theme=pymenu.themes.THEME_SOLARIZED)
    name = menu.add.text_input('Name: ',)
    menu.add.button('Play Game', Game, name)
    menu.add.button('Quit', py.display.quit)
    menu.mainloop(screen)

def Game(name):
    global obstaclemem, run, numchal
    numchal = 0
    background = Background()
    animation = py.USEREVENT + 1
    py.time.set_timer(animation, 175)
    addob = animation + 1
    py.time.set_timer(addob, 2000)
    paused = addob + 1
    py.time.set_timer(paused, 20000)

    name = name.get_value()
    screen.blit(background.image, background.rect)
    player = Player()
    obstaclemem = py.sprite.Group()
    i = 0
    time = 5000
    jump = False
    jumpHeight = 20
    yVelocity = jumpHeight
    run = True
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    run = False
            elif event.type == animation:
                screen.blit(background.image, background.rect)
                screen.blit(running[i].convert_alpha(), player.rect)
                i += 1
                if i == 6:
                    i = 0
            elif event.type == addob:
                    ob = random.randint(1,2)
                    if ob%2 == 0:
                        ob = Sign()
                    else:
                        ob = Hydrant()

                    obstaclemem.add(ob)

            elif event.type == paused:
                py.time.set_timer(addob, 0)
                pause(time)
                time -= 500
                if time < 2000:
                    time = 2000
                py.time.set_timer(addob, 2000)
                
        keys = py.key.get_pressed() 
        if keys[py.K_SPACE]:
            jump = True

        if jump:
            player.rect.y -= yVelocity
            yVelocity -= 0.9
            if yVelocity < -jumpHeight:
                jump = False
                yVelocity = jumpHeight
                player.rect.topleft = (500,700)
            screen.blit(background.image, background.rect)
            screen.blit(jumping.convert_alpha(), player.rect)
        else:
            screen.blit(background.image, background.rect)
            screen.blit(running[i].convert_alpha(), player.rect)

        obstaclemem.update()

        for obstacle in obstaclemem:
            screen.blit(obstacle.image, obstacle.rect)

        if py.sprite.spritecollideany(player, obstaclemem):
           screen.blit(playerdead, player.rect)
           py.display.update()
           py.time.delay(1000)
           highscore(name, numchal)
           run = False

        obstaclemem.update()     

        clock.tick(60)
        py.display.update()



Menu()
########################################################################
# game only works for aspect ratio 1920x1080 @ 150% zoom level         #
# playing the game off of these settings will result in visual glitches#
# ye be warned                                                         #
########################################################################
import pygame as py
import pygame_menu as pymenu
import random
import challenges
from engi1020.arduino.api import *
py.init()
py.font.init()

oled_clear()

screen = py.display.set_mode((1920,1080))

background = py.image.load('assets/Background/Background.png')
player2 = py.image.load('assets/Player/PlayerRun2.png')
player1 = py.image.load('assets/Player/PlayerRun1.png')
player4 = py.image.load('assets/Player/PlayerRun4.png')
player3 = py.image.load('assets/Player/PlayerRun3.png')
playerdead = py.image.load('assets/Player/playerdead.png')
jumping = py.image.load('assets/Player/PlayerJump.png')
hydrantimg = py.image.load('assets/Obstacles/Hydrant.png')
signimg = py.image.load('assets/Obstacles/Sign.png')

signimg = py.transform.scale(signimg, (128, 128))
hydrantimg = py.transform.scale(hydrantimg, (64,64))
player2 = py.transform.scale(player2, (128,128))
player1 = py.transform.scale(player1, (128,128))
player3 = py.transform.scale(player3, (128,128))
player4 = py.transform.scale(player4, (128,128))
jumping = py.transform.scale(jumping, (128,128))
playerdead = py.transform.scale(playerdead, (128,128))

running = [player1, player2, player3, player4, player3, player2]



clock = py.time.Clock()

class Background(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = background.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (1200, 370)

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = running[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (500,700)

class Hydrant(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hydrantimg.convert_alpha()
        self.rect = self.image.get_rect(center=(1800,795))
        

    def update(self):
        self.rect.move_ip(-6, 0) 
        if self.rect.right < 0:
            self.kill()


class Sign(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = signimg.convert_alpha()
        self.rect = self.image.get_rect(center=(1800,765))

    def update(self):
        self.rect.move_ip(-6, 0)
        if self.rect.right < 0:
            self.kill()

def challengemsg():
    global randomChallenge
    chalList = ['lightson','pressbut','swipeleft','swiperight','lightsoff','dialright', 'dialleft']
    randomChallenge = random.choice(chalList)
    if randomChallenge == 'lightson':
        msg = 'Turn on the lights!'
    elif randomChallenge == 'swiperight':
        msg = 'Swipe the arduino right!'
    elif randomChallenge == 'swipeleft':
        msg = 'Swipe the arduino left!'
    elif randomChallenge == 'pressbut':
        msg = 'Press and hold the button!'
    elif randomChallenge == 'lightsoff':
        msg = 'Turn the lights off!'
    elif randomChallenge == 'dialright':
        msg = 'Turn the dial to the right!'   
    elif randomChallenge == 'dialleft':
        msg = 'Turn the dial to the left!'
    return msg

def challenge():
    if randomChallenge == 'lightson':
        res = challenges.lightson()
    elif randomChallenge == 'swiperight':
        res = challenges.swiperight()
    elif randomChallenge == 'swipeleft':
        res = challenges.swipeleft()
    elif randomChallenge == 'pressbut':
        res = challenges.pressbut()
    elif randomChallenge == 'lightsoff':
        res = challenges.lightsoff()
    elif randomChallenge == 'dialright':
        res = challenges.dialright()
    elif randomChallenge == 'dialleft':
        res = challenges.dialleft()
    return res

def pause(time):
    background = Background()
    global numchal, run
    msg = challengemsg()
    while time > 0:
        font = py.font.SysFont('Comic Sans MS', 30)
        screen.blit(background.image, background.rect)
        surf = font.render(f'{msg} in {time/1000} Seconds', False, (255,255,255))
        screen.blit(surf, dest=(960,500))
        py.display.update()
        py.time.delay(500)
        time -= 500
    res = challenge()
    if res:
        numchal += 1
    else:
        screen.blit(background.image, background.rect)
        font = py.font.SysFont('Comic Sans MS', 30)
        surf = font.render('You ran out of time!', False, (255,255,255))
        screen.blit(surf, dest=(960,500))
        py.display.update()
        py.time.delay(1000)
        highscore(name, numchal)
        run = False


def highscore(name, numchal):
    file = open('highscore.txt', 'a')
    file.write(f'{name} : {numchal}\n')
    file.close()

def Menu():
    global name
    menu = pymenu.Menu('City Dash', 1250, 710, theme=pymenu.themes.THEME_SOLARIZED)
    name = menu.add.text_input('Name: ',)
    menu.add.button('Play Game', Game, name)
    menu.add.button('Quit', py.display.quit)
    menu.mainloop(screen)

def Game(name):
    global obstaclemem, run, numchal
    numchal = 0
    background = Background()
    animation = py.USEREVENT + 1
    py.time.set_timer(animation, 175)
    addob = animation + 1
    py.time.set_timer(addob, 2000)
    paused = addob + 1
    py.time.set_timer(paused, 20000)

    name = name.get_value()
    screen.blit(background.image, background.rect)
    player = Player()
    obstaclemem = py.sprite.Group()
    i = 0
    time = 5000
    jump = False
    jumpHeight = 20
    yVelocity = jumpHeight
    run = True
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    run = False
            elif event.type == animation:
                screen.blit(background.image, background.rect)
                screen.blit(running[i].convert_alpha(), player.rect)
                i += 1
                if i == 6:
                    i = 0
            elif event.type == addob:
                    ob = random.randint(1,2)
                    if ob%2 == 0:
                        ob = Sign()
                    else:
                        ob = Hydrant()

                    obstaclemem.add(ob)

            elif event.type == paused:
                py.time.set_timer(addob, 0)
                pause(time)
                time -= 500
                if time < 2000:
                    time = 2000
                py.time.set_timer(addob, 2000)
                
        keys = py.key.get_pressed() 
        if keys[py.K_SPACE]:
            jump = True

        if jump:
            player.rect.y -= yVelocity
            yVelocity -= 0.9
            if yVelocity < -jumpHeight:
                jump = False
                yVelocity = jumpHeight
                player.rect.topleft = (500,700)
            screen.blit(background.image, background.rect)
            screen.blit(jumping.convert_alpha(), player.rect)
        else:
            screen.blit(background.image, background.rect)
            screen.blit(running[i].convert_alpha(), player.rect)

        obstaclemem.update()

        for obstacle in obstaclemem:
            screen.blit(obstacle.image, obstacle.rect)

        if py.sprite.spritecollideany(player, obstaclemem):
           screen.blit(playerdead, player.rect)
           py.display.update()
           py.time.delay(1000)
           highscore(name, numchal)
           run = False

        obstaclemem.update()     

        clock.tick(60)
        py.display.update()



Menu()
