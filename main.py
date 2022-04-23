import pygame as pg
import math
import time
import sys
import random

pg.init()

# Setup
run = True

width, height = 1300, 800
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

tank_body = pg.image.load("tank_body.png")
tank_cannon = pg.image.load("tank_cannon.png")
bullet_normal = pg.image.load("bullet_normal.png")
block_normal = pg.image.load("block_normal.png")


class GameStateHandler:
    def __init__(self):
        self.gameState = "titlescreen"
        self.stage = 0
        self.total_stages = 1
        self.lives = 3

        # Timing
        self.transition_time = 5
        self.level_end_time = 3

    def tick(self):
        if self.gameState == "titlescreen":
            self.titlescreen()
        elif self.gameState == "level":
            self.level()
        elif self.gameState == "transition":
            self.transition()
        elif self.gameState == "endscreen":
            self.endscreen()

    def titlescreen(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Screen Zeichnen
        screen.blit(pg.image.load("titlescreen.png"), (0, 0))
        # - Buttons
        button_font = pg.font.SysFont("Franklin Gothic Heavy", 50)
        # - - Einspieler
        singleplayerText = button_font.render("Einspieler", True, [0, 0, 0])
        renderText(singleplayerText, (1085, 580))
        if pg.mouse.get_pressed()[0]:
            if singleplayerText.get_rect(center=(1085, 580)).collidepoint(pg.mouse.get_pos()):
                self.gameState = "transition"
                self.stage = 1
                self.lives = 3
                self.load_level()
        # - - Mehrspieler
        multiplayerText = button_font.render("Mehrspieler", True, [0, 0, 0])
        renderText(multiplayerText, (1085, 690))
        if pg.mouse.get_pressed()[0]:
            if multiplayerText.get_rect(center=(1085, 690)).collidepoint(pg.mouse.get_pos()):
                print("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        pg.display.update()

    def level(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        draw_window()

        if len(tank_group) == 0:
            mission_cleared_img = pg.image.load("mission_cleared.png")
            screen.blit(mission_cleared_img, mission_cleared_img.get_rect(center=(650, 300)))
            pg.display.update()

            # Pausieren
            start_time = time.time()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                if start_time + self.level_end_time <= time.time():
                    break

            # Übergang
            if self.stage != self.total_stages:
                self.gameState = "transition"
                self.stage += 1
            else:
                self.gameState = "endscreen"

        if len(playerGroup) == 0:
            draw_window()
            self.lives -= 1

            # Pausieren
            start_time = time.time()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                if start_time + self.level_end_time <= time.time():
                    break

            # Übergang
            if self.lives > 0:
                self.gameState = "transition"
            else:
                self.gameState = "titlescreen"

    def transition(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Zeichnen
        transition_bg = pg.image.load("level_transition.png")
        screen.blit(transition_bg, (0, 0))

        mission_font = pg.font.SysFont("Franklin Gothic Heavy", 100)
        mission_text = mission_font.render("Mission {0}".format(self.stage), True, (191, 144, 0))
        renderText(mission_text, (650, 335))

        pg.display.update()

        # Pausieren
        start_time = time.time()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            if start_time + self.transition_time <= time.time():
                break

        # Übergang
        self.load_level()
        self.gameState = "level"

    def endscreen(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Zeichnen
        screen.fill((0, 0, 0))
        text_font = pg.font.SysFont("Franklin Gothic Heavy", 50)
        text = text_font.render("GG", True, (255, 255, 255))
        renderText(text, (650, 400))

        text2 = text_font.render("Drücke etwas um fortzufahren", True, (255, 255, 255))
        renderText(text2, (650, 600))

        pg.display.update()

        keys = pg.key.get_pressed()
        if any(keys):
            self.gameState = "titlescreen"

    def load_level(self):
        playerGroup.empty()
        tank_group.empty()
        blockGroup.empty()
        borderGroup.empty()
        bulletGroup.empty()

        if self.stage == 1:
            borderGroup.add(BorderSprite())
            blockGroup.add(BlockSprite([700, 600]))
            blockGroup.add(BlockSprite([700, 300]))

            playerGroup.add(PlayerSprite((600, 600), 1))
            tank_group.add(BrownTank((750, 450)))
            #tank_group.add(BlackTank((700, 450), [(700, 450), (800, 450)]))


            """for i in range(26):
                blockGroup.add(BlockSprite([(i+1) * 50 - 25, 25]))
                blockGroup.add(BlockSprite([(i+1) * 50 - 25, 775]))
            for i in range(14):
                blockGroup.add(BlockSprite([25, (i+1) * 50 + 25]))
                blockGroup.add(BlockSprite([1275, (i + 1) * 50 + 25]))"""
            # for i in range(25):
            #     bulletGroup.add(BulletSprite([100 + 10*i, 700], 0, 3, 0))

        if self.stage == 2:
            print("lol")


class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, pos, player):
        # Sprite setup
        super().__init__()
        if player == 1:
            self.body_path = "tank_body.png"
            self.cannon_path = "tank_cannon.png"
        elif player == 2:
            self.body_path = "tank_body.png"
            self.cannon_path = "tank_cannon.png"
        else:
            self.body_path = "tank_body.png"
            self.cannon_path = "tank_cannon.png"
        self.image = pg.image.load(self.body_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)

        # move Setup
        self.xspeed, self.yspeed = 0, 0
        self.maxspeed = 3
        self.angle = 0
        self.oldPos = pos
        self.newAngle = 0

        # cannon Setup
        self.cannon_image = pg.image.load(self.cannon_path)
        self.cannon_rect = self.cannon_image.get_rect()
        self.shoot_pos = 0
        self.shoot_used = time.time()
        self.cooldown = 0.25
        self.bullet_speed = 3.1
        self.rebounds = 1
        self.invincibleBullets = False

    def update(self):
        if self.shoot_used + self.cooldown <= time.time():
            self.move()
        else:
            self.xspeed = 0
            self.yspeed = 0
        self.bodyRotation()
        self.updatePos()
        self.cannon()

        self.draw()

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.cannon_image, self.cannon_rect)

    def move(self):
        keys = pg.key.get_pressed()

        # Steuerung des Panzers
        if keys[pg.K_w]:
            self.yspeed -= 0.5
        if keys[pg.K_s]:
            self.yspeed += 0.5
        if keys[pg.K_a]:
            self.xspeed -= 0.5
        if keys[pg.K_d]:
            self.xspeed += 0.5

        if abs(self.yspeed) > self.maxspeed:
            self.yspeed = self.maxspeed if self.yspeed > 0 else -self.maxspeed

        if abs(self.xspeed) > self.maxspeed:
            self.xspeed = self.maxspeed if self.xspeed > 0 else -self.maxspeed

        # Diagonale Bewegung verlangsamen
        if (keys[pg.K_w] or keys[pg.K_s]) and (keys[pg.K_a] or keys[pg.K_d]):
            if self.xspeed > 0:
                self.xspeed = round(self.maxspeed / 1.41)
            elif self.xspeed < 0:
                self.xspeed = round(self.maxspeed / -1.41)
            if self.yspeed > 0:
                self.yspeed = round(self.maxspeed / 1.41)
            elif self.yspeed < 0:
                self.yspeed = round(self.maxspeed / -1.41)

        # Bewegung stoppen wenn nichts gedrückt wird
        if not (keys[pg.K_w] or keys[pg.K_s]):
            self.yspeed = 0
        if not (keys[pg.K_a] or keys[pg.K_d]):
            self.xspeed = 0

        # neuer Winkel
        if keys[pg.K_w] or keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d]:
            self.newAngle = round(getVecAngle(pg.math.Vector2(self.xspeed, self.yspeed)))
            if self.newAngle >= 180:
                self.newAngle -= 180

    def bodyRotation(self):
        if self.angle == 0 and self.newAngle == 135:
            self.angle += 180
        elif self.newAngle == 0 and self.angle == 135:
            self.angle -= 180
        elif self.angle < self.newAngle:
            self.angle += 1.5
        elif self.angle > self.newAngle:
            self.angle -= 1.5

        self.image = pg.transform.rotate(pg.image.load(self.body_path), self.angle).convert_alpha()
        self.rect = rotate(pg.image.load(self.body_path), self.rect.center, self.angle)
        self.mask = pg.mask.from_surface(self.image)

    def cannon(self):
        # Winkel der Kanone finden
        mouseX, mouseY = pg.mouse.get_pos()
        cannon_vec = pg.math.Vector2(mouseX - self.rect.centerx, mouseY - self.rect.centery)
        cAngle = getVecAngle(cannon_vec)

        # Offset ausrechnen
        img_height = pg.image.load(self.cannon_path).get_height()
        offset_vec = pg.math.Vector2(0, -img_height / 2).rotate(-cAngle)

        # Bild rotieren und Position anpassen
        self.shoot_pos = pg.math.Vector2(0, -1).rotate(-cAngle)
        self.shoot_pos.scale_to_length(img_height)
        self.shoot_pos += pg.math.Vector2(self.rect.center)
        self.cannon_image = pg.transform.rotate(pg.image.load(self.cannon_path), cAngle)
        self.cannon_rect = rotate(pg.image.load(self.cannon_path), self.cannon_rect.center, cAngle)
        self.cannon_rect.center = (self.rect.centerx + offset_vec[0], self.rect.centery + offset_vec[1])

        # Schiessen
        mouseKeys = pg.mouse.get_pressed()  # Gibt Tuple der Art (linksklick, mittelklick, rechtsklick), alles Booleans
        if mouseKeys[0] and (self.shoot_used + self.cooldown <= time.time()):
            self.shoot(cAngle)

    def shoot(self, angle):
        self.shoot_used = time.time()
        shootPos = (self.shoot_pos[0], self.shoot_pos[1])
        bulletGroup.add(BulletSprite(shootPos, angle, self.bullet_speed, self.rebounds, self.invincibleBullets))

    def updatePos(self):
        if self.angle != self.newAngle:
            return

        self.oldPos = self.rect.center
        self.rect.center = (self.rect.centerx + self.xspeed, self.rect.centery + self.yspeed)
        if self.checkCollision():
            self.rect.center = self.oldPos

    def checkCollision(self):
        if pg.sprite.spritecollide(self, borderGroup, False, pg.sprite.collide_mask):
            return True
        if pg.sprite.spritecollide(self, blockGroup, False, pg.sprite.collide_mask):
            return True
        if len(pg.sprite.spritecollide(self, playerGroup, False, pg.sprite.collide_mask)) + \
           len(pg.sprite.spritecollide(self, tank_group, False, pg.sprite.collide_mask)) > 1:
            return True
        else:
            return False


class BulletSprite(pg.sprite.Sprite):
    def __init__(self, pos, direction, speed, rebounds, invincible):
        super().__init__()
        self.bullet_path = "bullet_normal.png"
        self.image = pg.image.load(self.bullet_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)
        self.coords = self.rect.center

        self.speed = speed
        self.moveVec = pg.math.Vector2(-speed * math.sin(math.radians(direction)),  # https://imgur.com/a/eBhE5Xh
                                       -speed * math.cos(math.radians(direction)))
        self.angle = direction
        self.rebounds = rebounds
        self.isInvincible = invincible

    def update(self):
        self.move()
        self.rotation()
        self.checkCollision()

    def move(self):
        self.moveVec = pg.math.Vector2(-self.speed * math.sin(math.radians(self.angle)),
                                       -self.speed * math.cos(math.radians(self.angle)))
        loc_vec = pg.math.Vector2(self.coords)
        new_loc_vec = pg.math.Vector2(loc_vec[0] + self.moveVec[0], loc_vec[1] + self.moveVec[1])

        self.coords = (new_loc_vec[0], new_loc_vec[1])
        self.rect.center = self.coords

    def rotation(self):
        self.image = pg.transform.rotate(pg.image.load(self.bullet_path), self.angle).convert_alpha()
        self.rect = rotate(pg.image.load(self.bullet_path), self.rect.center, self.angle)
        self.mask = pg.mask.from_surface(self.image)

    def reflect(self, dir):
        if self.rebounds <= 0:
            self.kill()

        if dir == "left" or dir == "right":
            self.moveVec = self.moveVec.reflect(pg.math.Vector2(1, 0))
        else:
            self.moveVec = self.moveVec.reflect(pg.math.Vector2(0, 1))

        self.rebounds -= 1
        self.angle = getVecAngle(self.moveVec)

    def checkCollision(self):
        border_collision = pg.sprite.spritecollide(self, borderGroup, False, pg.sprite.collide_mask)
        if border_collision:
            dir = collisionSideBorder(self.rect.center)
            self.reflect(dir)
        block_collision = pg.sprite.spritecollide(self, blockGroup, False, pg.sprite.collide_mask)
        if block_collision:
            dir = collisionSide(block_collision[0].rect, self.rect)
            self.reflect(dir)

        bullet_collision = pg.sprite.spritecollide(self, bulletGroup, False, pg.sprite.collide_mask)
        if len(bullet_collision) > 1:
            for bullet in bullet_collision:
                if not bullet.isInvincible:
                    bullet.kill()

        player_collision = pg.sprite.spritecollide(self, playerGroup, False, pg.sprite.collide_mask)
        if player_collision:
            player_collision[0].kill()
            self.kill()

        tank_collision = pg.sprite.spritecollide(self, tank_group, False, pg.sprite.collide_mask)
        if tank_collision:
            tank_collision[0].kill()
            self.kill()


class BlockSprite(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.image.load("block_normal.png").convert()
        self.rect = self.image.get_rect(center=pos)

    def getRect(self):
        return self.rect


class BorderSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("border.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(pg.image.load("border_mask.png").convert_alpha())


class BrownTank(PlayerSprite):
    def __init__(self, pos):
        super().__init__(pos, 0)
        self.body_path = "tank textures/brown_body.png"
        self.cannon_path = "tank textures/brown_cannon.png"
        self.image = pg.image.load(self.body_path).convert_alpha()

        self.cannon_moveStart = time.time() - 6
        self.cannon_moveCooldown = 3
        self.aimPoint = (900, 600)
        self.cAngle = 0
        self.aimVec = pg.math.Vector2(0, -100)
        self.targetPlayer = ""
        self.idle = True

        self.shoot_cooldown_range = (5, 15)
        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])
        self.shoot_start = time.time()
        self.invincibleBullets = False

        # Debug
        self.drawAimPoint = False

    def update(self):
        self.chooseState()
        self.cannon()

        self.draw()

    def cannon(self):
        # Zufällige Bewegung der Kanone falls in "Idle"
        if self.cannon_moveStart + self.cannon_moveCooldown < time.time() and self.idle:
            self.cannon_moveStart = time.time()
            randomAngle = random.randint(0, 359)
            self.aimVec = pg.math.Vector2(0, -100).rotate(randomAngle)

            self.aimPoint = (round(self.aimVec[0] + self.rect.centerx), round(self.aimVec[1] + self.rect.centery))

            # print(self.aimPoint)
        if not self.idle:
            self.aimPoint = self.targetPlayer.rect.center
            self.aimVec = pg.math.Vector2(self.aimPoint[0] - self.rect.centerx, self.aimPoint[1] - self.rect.centery)

        # Kanone rotieren
        # self.cAngle innerhalb von [0, 360[ halten
        if self.cAngle < 0:
            self.cAngle = 359
        elif self.cAngle > 359:
            self.cAngle = 0

        # - den kürzeren Weg herausfinden
        if self.cAngle != round(getVecAngle(self.aimVec)):
            diff_ccw = round(getVecAngle(self.aimVec)) - self.cAngle
            if diff_ccw < 0:
                diff_ccw += 360
            if diff_ccw <= 180:
                self.cAngle += 1
            else:
                self.cAngle -= 1

        # Schiessen
        else:
            if self.shoot_start + self.shoot_cooldown <= time.time() and not self.idle:
                self.shoot(self.cAngle)
                self.shoot_start = time.time()
                self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])

        # Offset ausrechnen
        img_height = pg.image.load(self.cannon_path).get_height()
        offset_vec = pg.math.Vector2(0, -img_height / 2).rotate(-self.cAngle)

        # Bild rotieren und Position anpassen
        self.shoot_pos = pg.math.Vector2(0, -1).rotate(-self.cAngle)
        self.shoot_pos.scale_to_length(img_height)
        self.shoot_pos += pg.math.Vector2(self.rect.center)
        self.cannon_image = pg.transform.rotate(pg.image.load(self.cannon_path), self.cAngle)
        self.cannon_rect = rotate(pg.image.load(self.cannon_path), self.cannon_rect.center, self.cAngle)
        self.cannon_rect.center = (self.rect.centerx + offset_vec[0], self.rect.centery + offset_vec[1])

        # Debug
        if self.drawAimPoint: pg.draw.circle(screen, [128, 0, 128], self.aimPoint, 4)

    def chooseState(self):
        # Testen, ob Spieler im Sichtfeld sind
        players_in_sight = []
        for player in playerGroup:
            if in_sight(self, player, 1000, blockGroup):
                players_in_sight.append(player)

        # State ändern
        if len(players_in_sight) == 0:
            self.idle = True
        else:
            self.idle = False

        # Den nähesten Spieler finden   FUNKTIONIERT NONIG SO GANZ!!
        nearest_distance = 999_999
        for player in players_in_sight:
            distance = pg.math.Vector2(self.rect.center, player.rect.center).length()
            if distance < nearest_distance:
                nearest_distance = distance
                self.targetPlayer = player


class GreyTank(BrownTank):
    def __init__(self, pos):
        super().__init__(pos)
        self.body_path = "tank textures/grey_body.png"
        self.cannon_path = "tank textures/grey_cannon.png"

        self.radius = 300
        self.moveStart = time.time()
        self.moveCooldown = 5
        self.movePoint = (700, 700)

        self.shoot_cooldown_range = (3, 12)
        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])

        # Debug
        self.drawMoveRect = False
        self.drawMovePoint = True
        self.drawAimPoint = False

    def update(self):
        # if pg.mouse.get_pressed()[2]:
        #     self.movePoint = pg.mouse.get_pos()
        self.chooseState()
        if self.shoot_used + self.cooldown <= time.time():
            self.move()
        else:
            self.xspeed = 0
            self.yspeed = 0
        self.bodyRotation()
        self.updatePos()
        self.cannon()

        self.draw()

    def move(self):
        moveRect = pg.Rect(self.rect.centerx, self.rect.centery, self.radius, self.radius)
        moveRect.center = self.rect.center

        if self.moveStart + self.moveCooldown <= time.time():
            self.movePoint = self.pick_movePoint(moveRect.bottomleft)
            self.moveStart = time.time()

        if self.rect.center[0] not in [self.movePoint[0] - 1, self.movePoint[0], self.movePoint[0] + 1]:
            if self.rect.centerx > self.movePoint[0]:
                self.xspeed -= 0.5
            elif self.rect.centerx < self.movePoint[0]:
                self.xspeed += 0.5
        else:
            self.xspeed = 0
        if self.rect.center[1] not in [self.movePoint[1] - 1, self.movePoint[1], self.movePoint[1] + 1]:
            if self.rect.centery > self.movePoint[1]:
                self.yspeed -= 0.5
            elif self.rect.centery < self.movePoint[1]:
                self.yspeed += 0.5
        else:
            self.yspeed = 0

        if abs(self.yspeed) > self.maxspeed:
            self.yspeed = self.maxspeed if self.yspeed > 0 else -self.maxspeed

        if abs(self.xspeed) > self.maxspeed:
            self.xspeed = self.maxspeed if self.xspeed > 0 else -self.maxspeed

        # Diagonale Bewegung verlangsamen
        if (self.xspeed != 0) and (self.yspeed != 0):
            if self.xspeed > 0:
                self.xspeed = round(self.maxspeed / 1.41)
            elif self.xspeed < 0:
                self.xspeed = round(self.maxspeed / -1.41)
            if self.yspeed > 0:
                self.yspeed = round(self.maxspeed / 1.41)
            elif self.yspeed < 0:
                self.yspeed = round(self.maxspeed / -1.41)

        # neuer Winkel
        if (self.xspeed != 0) or (self.yspeed != 0):
            self.newAngle = round(getVecAngle(pg.math.Vector2(self.xspeed, self.yspeed)))
            if self.newAngle >= 180:
                self.newAngle -= 180

        # Debug stuff
        if self.drawMoveRect: pg.draw.rect(screen, [0, 255, 0], moveRect, 3)
        if self.drawMovePoint: pg.draw.circle(screen, [255, 0, 0], self.movePoint, 4)
        # print(self.rect.center, self.movePoint)

    def pick_movePoint(self, bottomleft):
        rel_coords = (random.randint(0, self.radius), random.randint(0, self.radius))
        abs_coords = (bottomleft[0] + rel_coords[0], bottomleft[1] - rel_coords[1])

        return abs_coords

    def updatePos(self):
        if self.angle != self.newAngle:
            return

        self.oldPos = self.rect.center
        self.rect.center = (self.rect.centerx + self.xspeed, self.rect.centery + self.yspeed)

        if self.checkCollision():
            self.rect.center = self.oldPos
            vec = pg.math.Vector2(0, -1).rotate(180 + round(getVecAngle(pg.math.Vector2(-self.xspeed, self.yspeed))))
            vec.scale_to_length(50)
            movePointVec = pg.math.Vector2(self.rect.center) + vec

            self.movePoint = round(movePointVec[0]), round(movePointVec[1])
            self.xspeed = 0
            self.yspeed = 0


class GreenTank(GreyTank):
    def __init__(self, pos):
        super().__init__(pos)
        self.body_path = "tank textures/green_body.png"
        self.cannon_path = "tank textures/green_cannon.png"
        self.bullet_speed = 8
        self.shoot_cooldown_range = (3, 10)
        self.moveCooldown = 3

        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])


class RedTank(GreyTank):
    def __init__(self, pos):
        super().__init__(pos)
        self.body_path = "tank textures/red_body.png"
        self.cannon_path = "tank textures/red_cannon.png"
        self.invincibleBullets = True
        self.shoot_cooldown_range = (3, 10)
        self.rebounds = 3

        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])


class YellowTank(GreyTank):
    def __init__(self, pos):
        super().__init__(pos)
        self.body_path = "tank textures/yellow_body.png"
        self.cannon_path = "tank textures/yellow_cannon.png"
        self.maxspeed = 4
        self.moveCooldown = 2
        self.radius = 500
        self.shoot_cooldown_range = (1, 3)

        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])


class PurpleTank(BrownTank):
    def __init__(self, pos):
        super().__init__(pos)
        self.body_path = "tank textures/purple_body.png"
        self.cannon_path = "tank textures/purple_cannon.png"
        self.bullet_speed = 8
        self.rebounds = 3
        self.shoot_cooldown_range = (2, 6)

        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])

    def cannon(self):
        # Zufällige Bewegung der Kanone
        if self.cannon_moveStart + self.cannon_moveCooldown < time.time():
            self.cannon_moveStart = time.time()
            randomAngle = random.randint(0, 359)
            self.aimVec = pg.math.Vector2(0, -100).rotate(randomAngle)

            self.aimPoint = (round(self.aimVec[0] + self.rect.centerx), round(self.aimVec[1] + self.rect.centery))

        # Kanone rotieren
        # self.cAngle innerhalb von [0, 360[ halten
        if self.cAngle < 0:
            self.cAngle = 359
        elif self.cAngle > 359:
            self.cAngle = 0

        # - den kürzeren Weg herausfinden
        if self.cAngle != round(getVecAngle(self.aimVec)):
            diff_ccw = round(getVecAngle(self.aimVec)) - self.cAngle
            if diff_ccw < 0:
                diff_ccw += 360
            if diff_ccw <= 180:
                self.cAngle += 1
            else:
                self.cAngle -= 1

        # Schiessen
        else:
            if self.shoot_start + self.shoot_cooldown <= time.time():
                self.shoot(self.cAngle)
                self.shoot_start = time.time()
                self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])

        # Offset ausrechnen
        img_height = pg.image.load(self.cannon_path).get_height()
        offset_vec = pg.math.Vector2(0, -img_height / 2).rotate(-self.cAngle)

        # Bild rotieren und Position anpassen
        self.shoot_pos = pg.math.Vector2(0, -1).rotate(-self.cAngle)
        self.shoot_pos.scale_to_length(img_height)
        self.shoot_pos += pg.math.Vector2(self.rect.center)
        self.cannon_image = pg.transform.rotate(pg.image.load(self.cannon_path), self.cAngle)
        self.cannon_rect = rotate(pg.image.load(self.cannon_path), self.cannon_rect.center, self.cAngle)
        self.cannon_rect.center = (self.rect.centerx + offset_vec[0], self.rect.centery + offset_vec[1])

        # Debug
        if self.drawAimPoint: pg.draw.circle(screen, [128, 0, 128], self.aimPoint, 4)


class BlackTank(GreyTank):
    def __init__(self, pos, movePoints):
        super().__init__(pos)
        self.body_path = "tank textures/black_body.png"
        self.cannon_path = "tank textures/black_cannon.png"
        self.movePoint1 = movePoints[0]
        self.movePoint2 = movePoints[1]
        self.movePoint = self.movePoint1

        self.bullet_speed = 8
        self.shoot_cooldown_range = (2, 3)
        self.maxspeed = 4

        self.shoot_cooldown = random.randint(self.shoot_cooldown_range[0], self.shoot_cooldown_range[1])

    def move(self):
        if self.rect.center[0] in [self.movePoint[0] - 2, self.movePoint[0] - 1, self.movePoint[0],
                                   self.movePoint[0] + 1, self.movePoint[0] + 2] and \
                self.rect.center[1] in [self.movePoint[1] - 2, self.movePoint[1] - 1, self.movePoint[1],
                                        self.movePoint[1] + 1, self.movePoint[1] + 2]:
            if self.movePoint == self.movePoint1:
                self.movePoint = self.movePoint2
            else:
                self.movePoint = self.movePoint1

        if self.rect.center[0] not in [self.movePoint[0] - 1, self.movePoint[0], self.movePoint[0] + 1]:
            if self.rect.centerx > self.movePoint[0]:
                self.xspeed -= 0.5
            elif self.rect.centerx < self.movePoint[0]:
                self.xspeed += 0.5
        else:
            self.xspeed = 0
        if self.rect.center[1] not in [self.movePoint[1] - 1, self.movePoint[1], self.movePoint[1] + 1]:
            if self.rect.centery > self.movePoint[1]:
                self.yspeed -= 0.5
            elif self.rect.centery < self.movePoint[1]:
                self.yspeed += 0.5
        else:
            self.yspeed = 0

        if abs(self.yspeed) > self.maxspeed:
            self.yspeed = self.maxspeed if self.yspeed > 0 else -self.maxspeed

        if abs(self.xspeed) > self.maxspeed:
            self.xspeed = self.maxspeed if self.xspeed > 0 else -self.maxspeed

        # Diagonale Bewegung verlangsamen
        if (self.xspeed != 0) and (self.yspeed != 0):
            if self.xspeed > 0:
                self.xspeed = round(self.maxspeed / 1.41)
            elif self.xspeed < 0:
                self.xspeed = round(self.maxspeed / -1.41)
            if self.yspeed > 0:
                self.yspeed = round(self.maxspeed / 1.41)
            elif self.yspeed < 0:
                self.yspeed = round(self.maxspeed / -1.41)

        # neuer Winkel
        if (self.xspeed != 0) or (self.yspeed != 0):
            self.newAngle = round(getVecAngle(pg.math.Vector2(self.xspeed, self.yspeed)))
            if self.newAngle >= 180:
                self.newAngle -= 180


def getVecAngle(vec):
    if vec.length() == 0:
        return 0
    else:
        normalVec = pg.math.Vector2(0, -1)
        dotProd = vec.dot(normalVec)
        angle = math.acos(dotProd / (vec.length() * normalVec.length()))  # Zwischenwinkelformel

    if vec.x > 0:
        return 360 - math.degrees(angle)
    else:
        return math.degrees(angle)


def collisionSide(rect1, rect2):
    if rect1.midtop[1] > rect2.midtop[1]:
        return "top"
    elif rect1.midleft[0] > rect2.midleft[0]:
        return "left"
    elif rect1.midright[0] < rect2.midright[0]:
        return "right"
    else:
        return "bottom"


def collisionSideBorder(pos):
    border_top = 90
    border_left = 114
    border_bottom = 627
    border_right = 1182
    # Distanzen zu allen vier Wänden ausrechnen
    dis_top = pos[1] - border_top
    dis_left = pos[0] - border_left
    dis_bottom = border_bottom - pos[1]
    dis_right = border_right - pos[0]

    # kürzeste distanz herausfinden und Seite zurückgeben
    shortest_dis = min(dis_top, dis_left, dis_bottom, dis_right)
    if shortest_dis == dis_top:
        return "top"
    elif shortest_dis == dis_left:
        return "left"
    elif shortest_dis == dis_bottom:
        return "bottom"
    elif shortest_dis == dis_right:
        return "right"


def draw_window():
    screen.fill((234, 198, 139))

    borderGroup.draw(screen)

    playerGroup.update()

    bulletGroup.update()
    bulletGroup.draw(screen)

    blockGroup.draw(screen)

    tank_group.update()

    # FPS
    fps_font = pg.font.SysFont("arial", 50)
    fps_text = fps_font.render(str(round(clock.get_fps())), True, (255, 0, 0))
    renderText(fps_text, (1275, 775))

    pg.display.update()


def rotate(image, pos, angle):  # Rotiert Bild um Punkt und gibt neue Position zurück
    # code von https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(pos[0], pos[1])).center)

    return new_rect


def determineRotation(pos1, pos2, dirVec):
    # Code mit Erklärung von
    # https://stackoverflow.com/questions/14807287/how-can-i-determine-whether-its-faster-to-face-an-object-rotating-clockwise-or
    if (pos1[0] - pos2[0]) * dirVec[1] > (pos1[1] - pos2[1]) * dirVec[0]:
        return "cw"
    else:
        return "ccw"


def get_line(start, end):
    # Quelle: http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def in_sight(shooter, target, range_, obstacles):
    # Quelle: https://stackoverflow.com/questions/37658815/pygame-efficient-detection-of-line-collision-with-sprite
    line_of_sight = get_line(shooter.rect.center, target.rect.center)
    zone = shooter.rect.inflate(range_, range_)
    obstacles_list = [rectangle.rect for rectangle in obstacles]  # to support indexing
    obstacles_in_sight = zone.collidelistall(obstacles_list)
    for x in range(1, len(line_of_sight), 5):
        for obs_index in obstacles_in_sight:
            if obstacles_list[obs_index].collidepoint(line_of_sight[x]):
                return False
    return True


def drawVector(vector, start_pos, length):  # Debug
    vector = pg.math.Vector2(vector)
    vector.scale_to_length(length)
    end_pos_vec = pg.math.Vector2(start_pos) + vector
    pg.draw.line(screen, [0, 150, 0], start_pos, (end_pos_vec[0], end_pos_vec[1]), 3)
    pg.draw.circle(screen, [200, 0, 0], (end_pos_vec[0], end_pos_vec[1]), 3)


def renderText(text, pos):
    text_rect = text.get_rect(center=pos)
    screen.blit(text, text_rect)


playerGroup = pg.sprite.Group()

bulletGroup = pg.sprite.Group()

blockGroup = pg.sprite.Group()

borderGroup = pg.sprite.GroupSingle()

tank_group = pg.sprite.Group()

gameState = GameStateHandler()

while True:
    gameState.tick()
    # print(round(clock.get_fps()))
    clock.tick(60)
