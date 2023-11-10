from pygame import *
init()

# Розмір вікна
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))  # створення вікна
display.set_caption("Maze")  # назва вікна

# Завантаження та зміна розміру фонового зображення
background = transform.scale(image.load("background3.png"), (win_width, win_height))

game = True
clock = time.Clock()  # Ігровий таймер
FPS = 60

# Клас-батько для наших об'єктів
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.w = w
        self.h = h
        self.speed = speed

        self.image = transform.scale(image.load(img), (w, h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        if self.direction == "right":
            self.rect.x += self.speed
        
class Wall(sprite.Sprite):
    def __init__(self, color, x, y, w, h):
        super().__init__()
        self.color = color
        self.w = w
        self.h = h

        self.image = Surface((self.w, self.h))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Player("cube.png", 5, win_height - 80, 65, 65, 4)
monster = Enemy("enemy.png", win_width - 80, 280, 65, 65, 2)
final = GameSprite("treasure.png", win_width - 120, win_height - 80, 65, 65, 0)

color = (154, 205, 50)

w1 = Wall(color, 100, 20, 450, 10)
w2 = Wall(color, 100, 490, 360, 10)
w3 = Wall(color, 100, 220, 10, 180)
w4 = Wall(color, 200, 130, 10, 360)
w5 = Wall(color, 450, 130, 10, 360)
w6 = Wall(color, 300, 20, 10, 350)
w7 = Wall(color, 390, 120, 130, 10)
w8 = Wall(color, 80, 120, 130, 10)
w9 = Wall(color, 0, 220, 110, 10)
w10 = Wall(color, 310, 360, 60, 10)
w11 = Wall(color, 390, 260, 180, 10)

w_list = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11]

# Фонова музика

finish = False
while game:
    for e in event.get(): 
        if e.type == QUIT: # Первірка на подію виходу з вікна
            game = False

    if not finish:
        window.blit(background, (0, 0))  # Прикріплення(малювання) фону
        player.update()
        player.reset()  # Прикріплення(малювання) гравця
        monster.update()
        monster.reset()  # Прикріплення(малювання) ворога
        final.reset()  # Прикріплення(малювання) скарбу

        for w in w_list:
            w.reset()
            if player.rect.colliderect(monster.rect) or player.rect.colliderect(w.rect):
                    finish = True
                    f = font.Font(None, 70)
                    lose_text = f.render("YOU LOSE!", True, (180, 0, 0))
                    window.blit(lose_text, (200, 200))
            if player.rect.colliderect(final.rect):
                    finish = True
                    f = font.Font(None, 70)
                    lose_text = f.render("YOU VIN!", True, (180, 0, 0))
                    window.blit(lose_text, (200, 200))

        display.update()
        
    clock.tick(FPS)