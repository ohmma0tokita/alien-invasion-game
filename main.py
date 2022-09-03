import pygame, sys, os, random, json, time, getpass
from Modules import *


# tells the game story
beginning_story()
name = input('ENTER YOUR NAME: ').lower().strip()

#inisialization of pygame: sounds and everything
pygame.init()

#Settings/Stats attributes
AI = Settings() # stands for alien invasion
STATS = Stats(name)

############if not new player salute him##########
#loads_store_username_score(STATS, name)

# screen
SCREEN = AI.screen()
# bg music
AI.bg_sound('Images_and_sounds/space.wav')
# logo
AI.set_logo()
# ships and icons
SHIP = FighterShip(SCREEN, 400, 540, 'Images_and_sounds/sprites/space_ship')
ICON_1 = Ship(SCREEN, 150, 150, 'Images_and_sounds/sprites/icon_1')
ICON_2 = Ship(SCREEN, 400, 300, 'Images_and_sounds/sprites/icon_2')

# buttons
START_BUTTON = Button(SCREEN, 'Images_and_sounds/play_button.png', (200, 90), 400, 500)

#____sprite group____
ICONS = pygame.sprite.Group()
ICONS.add(ICON_1, ICON_2)
# alien ships
ships = pygame.sprite.Group()
#fighter ships
main_ship = pygame.sprite.Group()
main_ship.add(SHIP)

alien_bullets = pygame.sprite.Group()
fighter_bullets = pygame.sprite.Group()

# les compteurs
magazine = 3 # ___limit use of super bullets___
t = 0 # ___manual timer for launching asteroids while in home screen___
a = 0 # ___manual timer for spawning aliens when game begins___

def launch_asteroid():
    '''launches asteroids each t time'''
    global t, ICONS
    t += 1
    if t == 200:
        y = random.randint(50, 550)
        asteroid = Asteroids(SCREEN, 700, y, 'Images_and_sounds/sprites/asteroid')
        ICONS.add(asteroid)
        t = 0

def spawn_ships():
    """creates and spawns alien ships and spawns fighter ship"""
    global a, ships, alien_bullets, SHIP
    a += 1
    if a == 5:
        x = 10
        rand = random.randint(20,750) #random x
        alien_ship = AlienShip(SCREEN, x+rand, 25, 'Images_and_sounds/sprites/aliens', alien_bullets)
        #add to sprites
        ships.add(alien_ship)
        a = -100 # spawn speed
    
    # alien ships
    ships.draw(SCREEN)
    ships.update()

    # alien bullets
    alien_bullets.draw(SCREEN)
    alien_bullets.update()
    
    #__main ship__
    main_ship.draw(SCREEN)
    main_ship.update()

def check_events(button=START_BUTTON):
    '''checks for events when needed: starting quitting moving shooting'''
    global magazine, run, bullets, ships
    # if fighter ship loses 10 health: GAME OVER
    if STATS.health == 0:
        run = True

    #assuring the mouvement of the ship
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if button.img_rect.collidepoint(pos):  # clicks
            if pygame.mouse.get_pressed()[0] == 1:  # 0 sig right click, 1 sig state: True
                run = False
        if event.type == pygame.QUIT:  # quits
            sys.exit()

        # keydown
        if event.type == pygame.KEYDOWN:
            # quits
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            # enters game with space_bar
            if event.key == pygame.K_SPACE:
                run = False
            # shoots normal bullet
            if event.key == pygame.K_x:
                normal_bullet = Bullet('Images_and_sounds/bomb.png', 'Images_and_sounds/nrml_b.wav', (15, 25), SHIP.rect.centerx, SHIP.rect.centery)
                normal_bullet.sound.play()
                fighter_bullets.add(normal_bullet)
            # shoots super bullet
            if event.key == pygame.K_c and magazine > 0:
                STATS.health = 10
                super_bullet = Bullet('Images_and_sounds/nuclear-bomb.png', 'Images_and_sounds/atomic_b.wav', (17, 25), SHIP.rect.centerx, SHIP.rect.centery)
                super_bullet.sound.play()
                fighter_bullets.add(super_bullet)
                magazine -= 1
    fighter_bullets.draw(SCREEN)
    fighter_bullets.update()

def check_collisions():
    global ships, fighter_bullets, alien_bullets, main_ship, SHIP
    #AUTOMATICALLY REMOVES SHIPS WHEN HIT
    #       true and false sig wether that ship/bullet get cleared or not
    #    removes alien ship when hit add 1 point to score
    if pygame.sprite.groupcollide(ships, fighter_bullets, True, True):
        STATS.points += 1
    #    diminish health when fighter ship gets hit
    if pygame.sprite.groupcollide(main_ship, alien_bullets, False, True): # if alien ship hits main ship, it wont shoot again
        STATS.health -= 1

# WONT BE CALLED: ONLY AFTER ASKING: DELETES OUT OF SCREEN SHIPS AND BULLETS
def refrech():
    ''' refrech game by deleting all non useful variables'''
    global ships, alien_bullets
    # removes out range ships
    for ship in ships:
        if ship.rect.centery > 620 or ship.rect.centery < -10:
            ships.remove(ship)
    # removes out range bullets
    for bullet in alien_bullets:
        if bullet.rect.centery > 1000 or bullet.rect.centery < -10:
            alien_bullets.remove(bullet)

# ___main___
run = True
while run:
    #fixed bg
    SCREEN.blit(AI.bg_img, (0, 0))
    #start button
    START_BUTTON.blit_me()
    #icons
    ICONS.draw(SCREEN)
    ICONS.update()
    #asteroids
    launch_asteroid()
    #check for events
    check_events()

    #updates display to newest img
    pygame.display.flip()


while not run:
    #animated screen
    AI.animated_bg(SCREEN)

    #fighter ship and alien ship: mvt and shoot
    spawn_ships()

    # check for events and collisions
    check_events()
    check_collisions()

    #prints health and super bullets left
    health_left = write('health: ' + str(STATS.health))
    magazine_left = write('super bullets left: ' + str(magazine))
    score = write('score: ' + str(STATS.points))
    SCREEN.blit(score, (650, 550))
    SCREEN.blit(magazine_left, (10, 550))
    SCREEN.blit(health_left, (10, 520))

    #updates display to newest img and refrech game
    refrech()
    pygame.display.flip()


game_over = write('Game Over')
score = write('score: ' + str(STATS.points))
########## if new record ##########
congrats_msg = False #loads_store_username_score(STATS, name)
########## congrats_text = write(congrats_msg)##########

while run:
    SCREEN.blit(AI.bg_img, (0, 0))
    #prints game over
    SCREEN.blit(game_over, (320, 270))
    #prints score
    if congrats_msg: # still not working
        SCREEN.blit(congrats_text, (250, 400))
    else:
        SCREEN.blit(score, (320, 330))
    #checks...
    check_events()
    pygame.display.update()

"""
Firas Sghiri...!
"""