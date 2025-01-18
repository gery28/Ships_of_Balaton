import random
import time

import pygame
import math

pygame.init()
WIDHT = 1200
HEIGHT = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Ships of Balaton")
player_x = WIDHT / 2
player_y = HEIGHT / 2
starting_difficulty = 5
difficulty = starting_difficulty
health = 100
OutOfHealth = False
gold = 0
alternate_speed = 5

chest_number = 10
collected_chests = 0

try:
    with open("number.txt", "r") as f:
        gold = int(f.read())
except:
    gold = 0
savestate = False

spawn_timer = pygame.USEREVENT + 1
difficulty_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 15000)
pygame.time.set_timer(difficulty_timer, 3000)

game_font = pygame.font.SysFont('arial', 60)
lostdisplay = game_font.render('', True, (255, 0, 0))
difficultydisplay = game_font.render('Difficulty: ' + str(int(difficulty)), True, (255, 0, 0))
golddisplay = game_font.render('Gold: ' + str(int(gold)), True, (255, 0, 0))
chestdisplay = game_font.render('Chests opened: ' + f"{collected_chests}/{chest_number}", True, (255, 0, 0))
pausedisplay = game_font.render('', True, (255, 0, 0))

chestButtonSpawned = False

canMoveUp = True
canMoveDown = True
canMoveLeft = True
canMoveRight = True


def inScreen(x_pos, y_pos):
    if x_pos > 0 and x_pos < WIDHT and y_pos > 0 and y_pos < HEIGHT:
        return True
    else:
        return False


def distenceCalculate(x_1, y_1, x_2, y_2):
    return int((abs(x_1 - x_2)) + (abs(y_1 - y_2)))


def drawbar(x: int, y: int, width: int, height: int, percent: float, color1: tuple, color2: tuple):
    if percent >= 100:
        percent = 100
    pygame.draw.rect(screen, color1, (x, y, width, height))
    pygame.draw.rect(screen, color2, (x, y, int(percent / 100 * width), height))


Q_key_image = pygame.image.load("img/Q_key1.jpg").convert_alpha()
R_key_image = pygame.image.load("img/R_key1.jpg").convert_alpha()


class PlayerShip(pygame.sprite.Sprite):
    global health

    def __init__(self):
        super(PlayerShip, self).__init__()
        self.image = pygame.image.load("img/Ship_full.png").convert_alpha()
        self.xsize = 250
        self.ysize = 200
        self.image = pygame.transform.scale(pygame.image.load("img/Ship_full.png").convert_alpha(),
                                            (self.xsize, self.ysize))
        self.rect = self.image.get_rect(center=(WIDHT / 2, HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.collision = [False] * 9

    def rotation(self, rotationface):
        if rotationface == 1:
            self.image = pygame.transform.rotate(
                pygame.transform.scale(pygame.image.load("img/Ship_full.png").convert_alpha(),
                                       (self.xsize, self.ysize)), 90)
        elif rotationface == 2:
            self.image = pygame.transform.scale(pygame.image.load("img/Ship_full.png").convert_alpha(),
                                                (self.xsize, self.ysize))
        elif rotationface == 3:
            self.image = pygame.transform.rotate(
                pygame.transform.scale(pygame.image.load("img/Ship_full.png").convert_alpha(),
                                       (self.xsize, self.ysize)), 270)
        elif rotationface == 4:
            self.image = pygame.transform.flip(
                pygame.transform.rotate(pygame.transform.scale(pygame.image.load("img/Ship_full.png").convert_alpha(),
                                                               (self.xsize, self.ysize)), 180), False, True)

    def keys_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rotation(1)
        elif keys[pygame.K_d]:
            self.rotation(2)
        elif keys[pygame.K_s]:
            self.rotation(3)
        elif keys[pygame.K_a]:
            self.rotation(4)

    def collisionCheck(self):
        global health, canMoveUp, canMoveDown, canMoveLeft, canMoveRight
        canMoveUp = True
        canMoveDown = True
        canMoveLeft = True
        canMoveRight = True
        rect = []
        if pygame.sprite.spritecollide(playership.sprite, fishes, True, pygame.sprite.collide_mask):
            health -= 5

        if pygame.sprite.spritecollide(self, islands, False, pygame.sprite.collide_mask):
            collided_enemies = pygame.sprite.spritecollide(self, islands, False, pygame.sprite.collide_mask)
            for enemy in collided_enemies:
                rect = enemy.rect
                self.collision[0] = rect.collidepoint(self.rect.topleft)
                self.collision[1] = rect.collidepoint(self.rect.topright)
                self.collision[2] = rect.collidepoint(self.rect.bottomleft)
                self.collision[3] = rect.collidepoint(self.rect.bottomright)

                self.collision[4] = rect.collidepoint(self.rect.midleft)
                self.collision[5] = rect.collidepoint(self.rect.midright)
                self.collision[6] = rect.collidepoint(self.rect.midtop)
                self.collision[7] = rect.collidepoint(self.rect.midbottom)

                self.collision[8] = rect.collidepoint(self.rect.center)

                if ((self.rect.centery - rect.height < rect.midtop[1] and self.rect.centery + rect.height >
                     rect.midbottom[1])
                        and (self.collision[0] or self.collision[2] or self.collision[4])):
                    canMoveLeft = False
                else:
                    canMoveLeft = True
                if ((self.rect.centery - rect.height < rect.midtop[1] and self.rect.centery + rect.height >
                     rect.midbottom[1])
                        and (self.collision[1] or self.collision[3] or self.collision[5])):
                    canMoveRight = False
                else:
                    canMoveRight = True
                if (self.rect.centerx - rect.width / 3 < rect.midright[0] and self.rect.centerx + rect.width / 3 >
                    rect.midleft[0]) and (
                        self.collision[0] or self.collision[1] or self.collision[6]):
                    canMoveUp = False
                else:
                    canMoveUp = True
                if (self.rect.centerx - rect.width / 3 < rect.midright[0] and self.rect.centerx + rect.width / 3 >
                    rect.midleft[0]) and (
                        self.collision[2] or self.collision[3] or self.collision[7]):
                    canMoveDown = False
                else:
                    canMoveDown = True

            rect = []

    def collision_debug(self):
        global canMoveUp, canMoveDown, canMoveLeft, canMoveRight

        if self.collision[0] or self.collision[2] or self.collision[4]:
            print("left")

        if self.collision[1] or self.collision[3] or self.collision[5]:
            print("right")

        if self.collision[0] or self.collision[1] or self.collision[6]:
            print("top")

        if self.collision[2] or self.collision[3] or self.collision[7]:
            print("bottom")
        if self.collision[8]:
            print("center")

    def update(self):
        self.keys_down()
        self.collisionCheck()
        # self.collision_debug()
        self.collision = [False] * 9
        player_x = self.rect.centerx
        player_y = self.rect.centery
        # healthdisplay = game_font.render('Health: ' + str(self.health), True, (255, 0, 0))


class Island(pygame.sprite.Sprite):
    def __init__(self):
        super(Island, self).__init__()
        self.x_size = 250
        self.y_size = 250
        self.image = pygame.transform.scale(pygame.image.load("img/island.png").convert_alpha(),
                                            (self.x_size, self.y_size))
        self.rect = self.image.get_rect(center=(random.randint(-1200, 2400), random.randint(-800, 1600)))
        self.mask = pygame.mask.from_surface(self.image)
        self.alternatespeed = alternate_speed

    def keys_down(self):
        self.alternatespeed = alternate_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and canMoveUp:
            self.rect.centery += self.alternatespeed
        if keys[pygame.K_s] and canMoveDown:
            self.rect.centery -= self.alternatespeed
        if keys[pygame.K_a] and canMoveLeft:
            self.rect.centerx += self.alternatespeed
        if keys[pygame.K_d] and canMoveRight:
            self.rect.centerx -= self.alternatespeed

    def update(self):
        self.keys_down()


goldColor = (242, 230, 65)


class GoldCircle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(player_x, player_y))
        self.radius = 100
        self.expansion_rate = 10
        self.thickness = 5
        self.maxRadius = 220

    def Use(self):
        self.radius += self.expansion_rate
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, goldColor, (self.radius, self.radius), self.radius, self.thickness)
        self.rect = self.image.get_rect(center=self.rect.center)
        pygame.sprite.spritecollide(self, fishes, True)
        if self.radius >= self.maxRadius:
            self.kill()

    def update(self):
        self.Use()


class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super(Fish, self).__init__()
        self.x_size = 170
        self.y_size = 80
        self.maxHealth = {"swordfish": 2, "squid": 3}
        self.goldLootTable = {"swordfish": (1, 3), "squid": (4, 6)}
        self.type = "swordfish"
        self.health = 100
        if self.type == "swordfish":
            self.x_size = 170
            self.y_size = 80
            self.health = self.maxHealth[self.type]
        elif self.type == "squid":
            self.x_size = 250
            self.y_size = 150
            self.health = self.maxHealth[self.type]

        forward1 = pygame.transform.scale(pygame.image.load(f"img/{self.type}-1.png").convert_alpha(),
                                          (self.x_size, self.y_size))
        forward2 = pygame.transform.scale(pygame.image.load(f"img/{self.type}-2.png").convert_alpha(),
                                          (self.x_size, self.y_size))
        forward3 = pygame.transform.scale(pygame.image.load(f"img/{self.type}-3.png").convert_alpha(),
                                          (self.x_size, self.y_size))
        forward4 = pygame.transform.scale(pygame.image.load(f"img/{self.type}-4.png").convert_alpha(),
                                          (self.x_size, self.y_size))
        self.forward_pics = [forward1, forward2, forward3, forward4]
        backward1 = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load(f"img/{self.type}-1.png").convert_alpha(),
                                   (self.x_size, self.y_size)), True, False)
        backward2 = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load(f"img/{self.type}-2.png").convert_alpha(),
                                   (self.x_size, self.y_size)), True, False)
        backward3 = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load(f"img/{self.type}-3.png").convert_alpha(),
                                   (self.x_size, self.y_size)), True, False)
        backward4 = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load(f"img/{self.type}-4.png").convert_alpha(),
                                   (self.x_size, self.y_size)), True, False)
        self.backward_pics = [backward1, backward2, backward3, backward4]
        self.image = forward1
        self.rect = self.image.get_rect(center=(random.randint(-1200, 2400), random.randint(-800, 1600)))
        self.mask = pygame.mask.from_surface(self.image)
        self.movement_speed = 7
        self.alternatespeed = alternate_speed
        self.forward = True
        self.picIndex = 0
        self.target_x = WIDHT / 2
        self.target_y = HEIGHT / 2
        self.x_float = self.rect.centerx
        self.y_float = self.rect.centery

    def keys_down(self):
        self.alternatespeed = alternate_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and canMoveUp:
            self.rect.centery += self.alternatespeed
        if keys[pygame.K_s] and canMoveDown:
            self.rect.centery -= self.alternatespeed
        if keys[pygame.K_a] and canMoveLeft:
            self.rect.centerx += self.alternatespeed
        if keys[pygame.K_d] and canMoveRight:
            self.rect.centerx -= self.alternatespeed

    def meleeAttack(self):
        angle = math.atan2(self.target_y - self.y_float, self.target_x - self.x_float)
        dx = self.movement_speed * math.cos(angle)
        dy = self.movement_speed * math.sin(angle)
        # end of pulled code

        self.x_float += dx
        self.y_float += dy
        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)
        if player_x - self.rect.centerx < 0:
            self.forward = False
        elif player_x - self.rect.centerx > 0:
            self.forward = True
        # if player_x - self.rect.centerx < 0:
        #     self.rect.right -= self.movement_speed
        #     self.forward = False
        # elif player_x - self.rect.centerx > 0:
        #     self.rect.right += self.movement_speed
        #     self.forward = True
        # if player_y - self.rect.centery > 0:
        #     self.rect.top += self.movement_speed
        # elif player_y - self.rect.centery < 0:
        #     self.rect.top -= self.movement_speed

    def health_bar(self):
        global gold
        if pygame.sprite.spritecollide(self, canonballs, True):
            self.health -= 1

        drawbar(self.rect.topleft[0] + self.rect.width / 10, self.rect.topleft[1] + self.rect.height / 10,
                self.rect.width - self.rect.width / 5, self.rect.height / 5,
                self.health / self.maxHealth[self.type] * 100, (255, 0, 0),
                (0, 255, 0))
        if self.health <= 0:
            gold += random.randint(*self.goldLootTable[self.type])
            self.kill()

    def imageLoad(self):
        if self.picIndex < len(self.forward_pics) - 1:
            self.picIndex += 0.3
        else:
            self.picIndex = 0

        if self.forward:
            self.image = self.forward_pics[int(self.picIndex)]
        else:
            self.image = self.backward_pics[int(self.picIndex)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.meleeAttack()
        self.imageLoad()
        self.keys_down()
        self.health_bar()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, target_x, target_y):
        super(Bullet, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("img/canonball.png").convert_alpha(), (40, 40))
        self.rect = self.rect = self.image.get_rect(center=(WIDHT / 2, HEIGHT / 2))
        self.target_x = target_x
        self.target_y = target_y
        self.center_x = WIDHT / 2
        self.center_y = HEIGHT / 2
        self.x_float = self.center_x
        self.y_float = self.center_y
        self.speed = 15
        self.goldget = 0
        self.hittedenemy = ""

    def shoot(self):
        # path calculations by Nealholt
        angle = math.atan2(self.target_y - self.y_float, self.target_x - self.x_float)
        dx = self.speed * math.cos(angle)
        dy = self.speed * math.sin(angle)
        # end of pulled code

        self.x_float += dx
        self.y_float += dy
        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)

    def reach(self):
        global gold
        if abs(self.rect.centerx - self.target_x) <= 10 and abs(self.rect.centery - self.target_y) <= 10:
            self.kill()

        if pygame.sprite.spritecollide(self, fishes, False):
            # needed when multiple enemy types added
            collided_enemies = pygame.sprite.spritecollide(self, fishes, False)
            # for enemy in collided_enemies:
            #     self.hittedenemy = enemy.type

    def update(self):
        self.shoot()
        self.reach()


class Chest(pygame.sprite.Sprite):
    def __init__(self):
        super(Chest, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("img/Chest_closed.png").convert_alpha(), (100, 100))
        self.rect = self.image.get_rect(center=(random.randint(-1200, 2400), random.randint(-800, 1600)))
        self.opened = False
        self.alternatespeed = alternate_speed
        self.buttonimage = pygame.image.load("img/E_key1.jpg")
        self.buttonrect = self.buttonimage.get_rect(center=(self.rect.centerx, self.rect.centery + 100))
        while pygame.sprite.spritecollide(self, islands, False):
            self.rect.centerx, self.rect.centery = random.randint(-1200, 2400), random.randint(-800, 1600)
            print("asd")

    def alternatemovement(self):
        self.alternatespeed = alternate_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and canMoveUp:
            self.rect.centery += self.alternatespeed
        if keys[pygame.K_s] and canMoveDown:
            self.rect.centery -= self.alternatespeed
        if keys[pygame.K_a] and canMoveLeft:
            self.rect.centerx += self.alternatespeed
        if keys[pygame.K_d] and canMoveRight:
            self.rect.centerx -= self.alternatespeed

    def openState(self):
        global gold, collected_chests
        if self.inRange() and not self.opened and pygame.key.get_pressed()[pygame.K_e]:
            self.opened = True
            self.image = pygame.transform.scale(pygame.image.load("img/Chest _open.png").convert_alpha(), (100, 100))
            gold += random.randint(1, 5)
            collected_chests += 1

    def inRange(self):
        if abs(player_x - self.rect.centerx) + abs(player_y - self.rect.centery) <= 250 and not self.opened:
            return True

    def buttonSpawn(self):
        if self.inRange():
            self.buttonrect = self.buttonimage.get_rect(center=(self.rect.centerx, self.rect.centery))
            screen.blit(self.buttonimage, self.buttonrect)

    def update(self):
        self.alternatemovement()
        self.openState()
        self.buttonSpawn()


class StartButton(pygame.sprite.Sprite):
    def __init__(self):
        super(StartButton, self).__init__()
        self.xsize = 400
        self.ysize = 200
        self.image = pygame.transform.scale(pygame.image.load("img/start2_button_red.png").convert_alpha(),
                                            (self.xsize, self.ysize))
        self.rect = self.image.get_rect(center=(WIDHT / 2, 500))
        self.logoimage = pygame.image.load("img/Logo1.png").convert_alpha()
        self.logorect = self.logoimage.get_rect(center=(self.rect.centerx, self.rect.centery - 400))

    def Clicking(self):
        global inGame, pause
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.transform.scale(pygame.image.load("img/start2_button_green.png").convert_alpha(),
                                                (self.xsize, self.ysize))
            if pygame.mouse.get_pressed()[0] and inGame == False:
                inGame = True
                pause = False
                spawn_timer = pygame.USEREVENT + 1
                pygame.time.set_timer(difficulty_timer, 3000)
                health = 100
                self.kill()
        else:
            self.image = pygame.transform.scale(pygame.image.load("img/start2_button_red.png").convert_alpha(),
                                                (self.xsize, self.ysize))

    def update(self):
        self.Clicking()
        screen.blit(self.logoimage, self.logorect)


class SaveButton(pygame.sprite.Sprite):
    def __init__(self):
        super(SaveButton, self).__init__()
        self.xsize = 200
        self.ysize = 100
        self.image = pygame.transform.scale(pygame.image.load("img/start2_button_red.png").convert_alpha(),
                                            (self.xsize, self.ysize))
        self.rect = self.image.get_rect(center=(WIDHT - 100, HEIGHT - 50))

    def Clicking(self):
        global inGame
        global savestate
        global canPressSave
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            if savestate == True and canPressSave:
                self.lastpressed = now
                savestate = False
            elif savestate == False and canPressSave:
                self.lastpressed = now
                savestate = True

    def update(self):
        self.Clicking()
        if savestate:
            self.image = pygame.transform.scale(pygame.image.load("img/save_off.png").convert_alpha(),
                                                (self.xsize, self.ysize))
        else:
            self.image = pygame.transform.scale(pygame.image.load("img/save_on.png").convert_alpha(),
                                                (self.xsize, self.ysize))
        if inGame:
            self.kill()


playership = pygame.sprite.GroupSingle()
islands = pygame.sprite.Group()
fishes = pygame.sprite.Group()
canonballs = pygame.sprite.Group()
goldCirce = pygame.sprite.GroupSingle()
startButton = pygame.sprite.GroupSingle()
saveButton = pygame.sprite.GroupSingle()
chests = pygame.sprite.Group()


def respawn_sequence():
    fishes.empty()
    chests.empty()
    islands.empty()
    for i in range(int(difficulty)):
        fishes.add(Fish())
    for i in range(10):
        islands.add(Island())
    for i in range(chest_number):
        chests.add(Chest())


playership.add(PlayerShip())
respawn_sequence()

lastshoot = pygame.time.get_ticks()
lastUseCircle = pygame.time.get_ticks()
lastHealed = pygame.time.get_ticks()
lastSaved = pygame.time.get_ticks()
now = pygame.time.get_ticks()
delay = 250
goldcircledelay = 2000
healdelay = 3000

running = True
inGame = False
noStartButton = True
noSaveButton = True
canPressSave = False
quit_signal = False
pause = False

while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if savestate:
                with open("number.txt", "w") as f:
                    f.write(str(gold))
            quit_signal = True
        if inGame:
            if event.type == spawn_timer:
                if len(fishes) < int(difficulty):
                    fishes.add(Fish())
            if event.type == difficulty_timer:
                difficulty += 0.7
            if pygame.mouse.get_pressed()[0] and now - lastshoot >= delay:
                lastshoot = pygame.time.get_ticks()
                canonballs.add(Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and now - lastUseCircle >= goldcircledelay and gold >= 5:
                    lastUseCircle = pygame.time.get_ticks()
                    gold -= 5
                    goldCirce.add(GoldCircle())
                if event.key == pygame.K_r and now - lastHealed >= healdelay and gold >= 10:
                    healdelay = pygame.time.get_ticks()
                    health += 20
                    gold -= 10
                    if health > 100:
                        health = 100
                    lastHealed = pygame.time.get_ticks()
                if event.key == pygame.K_ESCAPE:
                    inGame = False
                    pause = True
                    noStartButton = True
                    noSaveButton = True
    if quit_signal:
        pygame.quit()
        break
    if pause:
        pausedisplay = game_font.render('Paused', True, (255, 0, 0))
    if inGame:
        if health <= 0:
            lostdisplay = game_font.render('You lost', True, (255, 0, 0))
            screen.blit(lostdisplay, (400, 300))
            OutOfHealth = True
        if chest_number <= collected_chests:
            lostdisplay = game_font.render('You won', True, (0, 255, 0))
            screen.blit(lostdisplay, (400, 300))
            collected_chests = 0
            gold += 10
            OutOfHealth = True

        screen.fill((0, 0, 255))

        goldCirce.draw(screen)
        islands.draw(screen)
        playership.draw(screen)
        chests.draw(screen)
        fishes.draw(screen)
        canonballs.draw(screen)
        playership.update()
        fishes.update()
        canonballs.update()
        goldCirce.update()
        islands.update()
        chests.update()
        drawbar(25, 25, 300, 25, health, (0, 0, 0), (255, 0, 0))
        drawbar(WIDHT - 360, HEIGHT - 70, 300, 25, min((now - lastUseCircle) / goldcircledelay * 100, 100),
                (242, 128, 15), (242, 230, 65))
        drawbar(WIDHT - 360, HEIGHT - 170, 300, 25, min((now - lastHealed) / healdelay * 100, 100), (255, 0, 0),
                (0, 255, 0))
        screen.blit(Q_key_image, (WIDHT - 400, HEIGHT - 70))
        screen.blit(R_key_image, (WIDHT - 400, HEIGHT - 170))
        golddisplay = game_font.render('Gold: ' + str(int(gold)), True, (255, 0, 0))
        chestdisplay = game_font.render('Chests opened: ' + f"{collected_chests}/{chest_number}", True, (255, 0, 0))
        difficultydisplay = game_font.render('Difficulty: ' + str(int(difficulty)), True, (255, 0, 0))
        # screen.blit(difficultydisplay, (0, HEIGHT - 70))
        # screen.blit(golddisplay, (WIDHT - 250, 0))
        # screen.blit(lostdisplay, (400, 300))
        screen.blit(difficultydisplay, (0, HEIGHT - 140))
        screen.blit(golddisplay, (0, HEIGHT - 210))
        screen.blit(chestdisplay, (0, HEIGHT - 70))
        screen.blit(lostdisplay, (400, 300))
        pygame.display.update()
        clock.tick(30)
        if OutOfHealth:
            time.sleep(3)
            inGame = False
            noStartButton = True
            difficulty = starting_difficulty
            respawn_sequence()
            health = 100
    else:
        health = 100
        OutOfHealth = False
        lostdisplay = game_font.render('', True, (255, 0, 0))
        screen.fill((66, 245, 242))
        screen.blit(pausedisplay, (WIDHT / 2, 300))
        if noStartButton:
            startButton.add(StartButton())
            noStartButton = False
        if noSaveButton:
            saveButton.add(SaveButton())
        if now - lastSaved >= 100:
            canPressSave = True
        saveButton.update()
        startButton.update()
        saveButton.draw(screen)
        startButton.draw(screen)
        pygame.display.update()
        clock.tick(30)
