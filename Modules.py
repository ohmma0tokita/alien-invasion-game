import pygame, sys, os, random, time, json, getpass
pygame.init() # for the fonts

# classes for basic game functions
class Settings:
    '''sets the screen and its basic parts'''
    def __init__(self):
        self.logo_img = pygame.image.load('Images_and_sounds/logo_ufo.png')
        self.bg_img = pygame.image.load('Images_and_sounds/bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img, (800, 600))

        #y cordinate counter for bg
        self.y = 0

    def screen(self):
        """sets the screen settings"""
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Alien Invasion')
        return screen

    def set_logo(self):
        """sets the logo"""
        pygame.display.set_icon(self.logo_img)

    def animated_bg(self, screen):
        '''animates the bg img'''
        screen.blit(self.bg_img, (0, self.y))  # first rolling image
        screen.blit(self.bg_img, (0, -600 + self.y))  # second rolling image
        self.y += 0.5
        if self.y == 600:  # loop again
            self.y = 0

    def bg_sound(self, file_path):
        """runs sus bg music"""
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)


class Stats:
    '''for stats like ship health, player score, etc...'''
    def __init__(self, name):
        self.name = name
        self.health = 10
        self.points = 0


# ship-type classes
class Ship(pygame.sprite.Sprite):
    """sets all ship kind of objects"""
    def __init__(self, screen, pos_x, pos_y, path):
        """Initialize the ship and set its starting position and mouvements and shoots."""
        super().__init__()
        self.screen = screen

        # sprites
        self.sprites = []
        #   looping through files
        for file in os.listdir(path):
            self.sprites.append(pygame.image.load(path+'/'+file))

        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos_x, pos_y

    def update(self):
        # animation
        self.current_sprite += 0.1
        if int(self.current_sprite) == len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]


class Asteroids(Ship):
    '''ship type = asteroid'''
    def __init__(self, screen, pos_x, pos_y, path):
        super().__init__(screen, pos_x, pos_y, path)

    def update(self):
        # animation
        self.current_sprite += 0.1
        if int(self.current_sprite) == len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        # motion for asteroids
        self.rect.centerx -= 2
        self.rect.centery += 1


class FighterShip(Ship):
    '''ship type = Fighting ship'''
    def __init__(self, screen, pos_x, pos_y, path):
        super().__init__(screen, pos_x, pos_y, path)

    def update(self):
        #animation
        self.current_sprite += 0.1
        if int(self.current_sprite) == len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        #mouvement
        key = pygame.key.get_pressed()
        # setting edges: if it gets out it comes back to starting position
        if 0 < self.rect.centery < 600 and 0 < self.rect.centerx < 800:
            if key[pygame.K_UP]:
                self.rect.centery -= 3
            if key[pygame.K_DOWN]:
                self.rect.centery += 3
            if key[pygame.K_LEFT]:
                self.rect.centerx -= 3
            if key[pygame.K_RIGHT]:
                self.rect.centerx += 3
        else:
            self.rect.centerx, self.rect.centery = 400, 540  # reset x,y cordinates
        
        #shooting
        """in the check events in the main file"""


class AlienShip(Ship):
    '''ship type = alien ship'''
    def __init__(self, screen, pos_x, pos_y, path, bullet_group):
        super().__init__(screen, pos_x, pos_y, path)
        
        self.alien_bullets = bullet_group
        self.counter = 0
        self.bullet_counter = 90

    def update(self):
        #vertival descending
        self.rect.centery += 1
        # surprise teleportation on x axis and shooting
        self.counter += 1
        rand_x = random.randint(-50, 50)
        if self.counter == 200:
            if 20 < (self.rect.centerx + rand_x) < 760:
                self.rect.centerx += rand_x
                self.counter = 0
                
        # shoot bullets
        self.bullet_counter += 1
        if self.bullet_counter == 100:
            self.bullet_counter = 0
            # create bullet
            alien_bullet = AlienBullet('Images_and_sounds/alien_bullet.png', 'Images_and_sounds/alien_b.wav', (5, 15), self.rect.centerx, self.rect.centery)
            # play shooting sound
            alien_bullet.sound.play()
            # add to sprites
            self.alien_bullets.add(alien_bullet)



# bullet-type clsses
class Bullet(pygame.sprite.Sprite):
    """sets all bullet kind of objects"""
    def __init__(self, img_file_path, sound_file_path, size, pos_x, pos_y):
        super().__init__()

        # bullet img, sound and rect
        self.image = pygame.image.load(img_file_path)
        self.image = pygame.transform.scale(self.image, size)

        #ship cords
        self.x = pos_x
        self.y = pos_y

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.y = self.x, self.y

        self.sound = pygame.mixer.Sound(sound_file_path)

    def update(self):
        self.rect.centery -= 5 #bullet speed
        if self.rect.centery < -10 : # if bullet passes by y = -10, stop it
            self.rect.centery = -10


class AlienBullet(Bullet):
    '''bullet type = those coming from alien ships'''
    def __init__(self, img_file_path, sound_file_path, size, pos_x, pos_y):
        super().__init__(img_file_path, sound_file_path, size, pos_x, pos_y)

    def update(self):
        self.rect.centery += 5 # bullet speed


# button type classes
class Button:
    '''sets buttons'''
    def __init__(self, screen, img_file, size, x_pos, y_pos):
        self.img = pygame.image.load(img_file)
        self.img = pygame.transform.scale(self.img, size)
        self.img_rect = self.img.get_rect()
        self.img_rect.centerx, self.img_rect.centery = x_pos, y_pos
        self.screen = screen

    def blit_me(self):
        self.screen.blit(self.img, self.img_rect)

#functions
def write(msg):
    # write message
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(msg, False, (255, 54, 61))
    return text

def beginning_story():
    time.sleep(1)
    print('\n')
    print('\n')
    print('\n')
    print('\tNOTE: pass is 13X + 23 = 920')
    time.sleep(1)
    print('YOU ARE IN FRONT OF A SHIP DOOR')
    time.sleep(1.5)
    print('\tDOOR REQUIRES PASSWORD...')
    time.sleep(1)
    # door password
    password = getpass.getpass('type door pass:')
    if password != '69':
        print('YOU FELL IN A TRAP!!!')
        time.sleep(1)
        print('FALLING...')
        time.sleep(1)
        print('YOU DIED FROM FALL')
        time.sleep(1)
        sys.exit()
    skip = input('you want to know the story? (y/n) ').lower().strip()
    if skip == 'y':
        # entering the ship
        print('\tyear is 3500...')
        time.sleep(1)
        print('\tWELCOME TO THE SHIP')
        time.sleep(2)
        answer = input('\t...you got a message, answer? (y/n) ').lower().strip()
        if answer == 'y':
            # the call starts
            print('[anonym]: my salutes to the pilot.')
            time.sleep(1)
            print('[anonym]: some weird creatures from outer space tried to take down Earth!!')
            time.sleep(3)
            print('[anonym]: only a couple of hundreds of people survived the attack, thankfully.')
            time.sleep(3)
            print('[anonym]: bu- b-..., wait a sec i hear a noise!')
            time.sleep(1.5)
            print('\t(went to check)')
            time.sleep(5)
            print('[anonym]: OH SH*T, its time for me to go..')
            time.sleep(2)
            print('[anonym]: I am one of the survivers, i crea- (coughs)!')
            time.sleep(2)
            print('[anonym]: i created this ship so that we-')
            time.sleep(2)
            print('\t[anonym]: -coughing harder-')
            time.sleep(3)
            print('[anonym]: so that we can stop this attack before it even happens!')
            time.sleep(3)
            print('[anonym]: this is our last-..')
            time.sleep(1)
            # call ends
            print('\tBATTERY DIED!')
            time.sleep(0.5)
            print('\tCLOSING CALL!')
            time.sleep(0.5)
            print('\tGame Starting...')
            time.sleep(0.5)
        else:
            # quit story if error
            print('\tGame Starting...')
            time.sleep(2)
    else:
        time.sleep(0.5)
        print('\tGame Starting...')
        time.sleep(0.5)

# database related
def search(name, data):
    """search name in database"""
    for i in range(len(data["players"])):
        if name in data["players"][i]:
            return i
    else:
        return 0

def check_database(STATS):
    """json manipulation"""

    with open('Alien_Invasion.json', 'r+') as file:
        data = json.load(file)
    
    i = search(STATS.name, data)
    if i:
        time.sleep(0.5)
        print('\tHello again ' + STATS.name.title() + '!')
        time.sleep(0.5)
        
        if data["record"]> STATS.score > data["players"][i][STATS.name]: # if new score is better than old take it
            data["players"][i][STATS.name] = STATS.score
            return "u re getting better"
    
    else:
        data["players"].append({STATS.name: STATS.score})
        file.seek(0)
        json.dump(data, file, indent = 4)
    
    if STATS.score > data["record"]: # checks for new record
        data["record"] = str(STATS.score)
        return f'Congrats {STATS.name} you beat the record holder {data["holder"]}: {data["record"]}'
