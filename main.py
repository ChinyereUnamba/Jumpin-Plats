import pygame as pg
import random
import sys
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(font_name)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname('__filename__')
        img_dir = path.join(self.dir, "img")
        with open(path.join(self.dir, hs_file), "w") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        with open(path.join(self.dir, cn_file), "w") as c:
            try:
                self.coin = int(c.read())
            except:
                self.coin = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, spritesheet))

        # load sounds
        self.jump_sound = pg.mixer.Sound("Jump.wav")
        self.screen_sound = pg.mixer.Sound("Yippee.wav")
        self.boost_sound = pg.mixer.Sound("Power Up.wav")
        self.coin_sound = pg.mixer.Sound("Pickup_coin.wav")
        self.hit_sound = pg.mixer.Sound("Hitl.wav")

    def new(self):
        # start a new game
        self.score = 0
        self.coin = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self)
        for plat in Platform_list:
            Platform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load("Happy Tune.wav")
        for i in range(10):
            c = Cloud(self)
            c.rect.y += randrange(500)
        self.run()

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1)
        self.clock.tick(FPS)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):

        # Game loop - Update
        self.all_sprites.update()

        # spawn mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 8000 + random.choice([-1500, 1500]):
            self.mob_timer = now
            Mob(self)

        # hits mob?
        mob_hits = pg.sprite.spritecollide(
            self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.hit_sound.play()
            self.playing = False

        # check if the player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:

                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
            # if player reaches top 1/4 of screen
        if self.player.rect.top <= height/4:
            if random.randrange(100) < 21:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y), 2)
            for mob in self.platforms:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= height:
                    plat.kill()
                    self.score += 10
        # if player hits a coin
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            if coin.type == 'gold':
                self.coin_sound.play()
                self.coin += 1

        # if player hits a powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # Die!
        if self.player.rect.bottom > height:
            for sprite in self.all_sprites:
                for sprite in self.all_sprites:
                    sprite.rect.y -= max(self.player.vel.y, 10)
                    if sprite.rect.bottom < 0:
                        sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spown new platforms
        while len(self.platforms) < 6:
            Width = random.randrange(10, 100)
            Platform(self, random.randrange(10, width - Width),
                     random.randrange(-75, -30))
        pg.display.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.player = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game loop - draw
        self.screen.fill(bgcolor1)
        self.all_sprites.draw(self.screen)
        self.draw_text("score:" + str(self.score), 30, white, 400, 15)
        self.draw_text("coin:" + str(self.coin), 30, white, 400, 35)
        pg.display.flip()

    def show_start_screen(self):

        pg.mixer.music.load("Yippee.wav")
        pg.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor2)
        self.draw_text(title, 48, white, width/2, height/4)
        self.draw_text("Arrows to move, Space to jump",
                       30, white, width/2, height/2)
        self.draw_text("Press any key to play", 30, white, width/2, height*3/4)
        self.draw_text("High Score:" + str(self.highscore),
                       30, white, width/2, 15)
        self.draw_text("Coin:" + str(self.coin), 30, white, 240, 35)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        if not self.running:
            return

        pg.mixer.music.load("Yippee.wav")
        pg.mixer.music.play(loops=-1)

        self.screen.fill(bgcolor2)
        self.draw_text("GAME OVER", 48, white, width/2, height/4)
        self.draw_text("Score:" + str(self.score),
                       30, white, width/2, height/2)
        self.draw_text("Press any key to play again",
                       30, white, width/2, height*3/4)
        self.draw_text("Total Coin:" + str(self.coin),
                       30, white, width/2, height*2/3-20)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 30, white,
                           width/2, height/2 + 40)

            with open(path.join(self.dir, hs_file), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score:" + str(self.highscore),
                           30, white, width/2, height / 2 + 40)

        with open(path.join(self.dir, cn_file), "w") as c:
            c.write(str(self.coin))
        pg.display.flip()

        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
