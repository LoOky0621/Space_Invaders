import pygame
import random
import math

class Game:
    def __init__(self, width, height):
        """
        Initialisiert das Spiel.

        Args:
            width (int): Die Breite des Spielfensters.
            height (int): Die Höhe des Spielfensters.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.spaceship = Spaceship(self, 370, 515)
        self.score = 0
        self.enemies = []

        # Initialisiert die Feinde
        for i in range(12):
            self.enemies.append(Enemy(self, random.randint(0, 736), random.randint(30, 120)))

        # Hintergrundbild laden
        self.background_img = pygame.image.load("spr_space_himmel.png")

        # Hauptspielschleife
        while self.running:
            self.clock.tick(60)
            self.screen.blit(self.background_img, (0, 0))  # Hintergrund zeichnen
            self.spaceship.update()  # Raumschiff aktualisieren
            for event in pygame.event.get():  # Ereignisse abrufen
                if event.type == pygame.QUIT:  # Überprüft, ob das Spiel geschlossen wurde
                    self.running = False

                # Tastatureingaben verarbeiten
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(-10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_SPACE:
                        self.spaceship.fire_bullet()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(-10)

            # Raumschiff-Updates und Kollisionen mit Feinden überprüfen
            self.spaceship.update()
            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:
                    if bullet.is_fired:
                        bullet.update()
                    else:
                        self.spaceship.bullets.remove(bullet)

            # Feinde aktualisieren und Kollisionen überprüfen
            for enemy in self.enemies:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460:
                    for i in self.enemies:
                        i.y = 1000
                    self.print_game_over()
                    break
            self.print_score()
            pygame.display.update()

    def print_game_over(self):
        """
        Zeigt den Game Over-Bildschirm an.
        """
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(go_text, (200, 250))

    def print_score(self):
        """
        Zeigt den aktuellen Punktestand an.
        """
        score_font = pygame.font.Font("freesansbold.ttf", 24)
        score_text = score_font.render("Punkte: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (8, 8))


class Spaceship:
    def __init__(self, game, x, y):
        """
        Initialisiert das Raumschiff.

        Args:
            game (Game): Die Spielinstanz.
            x (int): Die x-Koordinate des Raumschiffs.
            y (int): Die y-Koordinate des Raumschiffs.
        """
        self.x = x
        self.y = y
        self.change_x = 0
        self.game = game
        self.spaceship_img = pygame.image.load("spr_spaceship.png")
        self.bullets = []

    def update(self):
        """
        Aktualisiert die Position des Raumschiffs.
        """
        self.x += self.change_x
        if self.x < 0:
            self.x = 0
        elif self.x > 736:
            self.x = 736
        self.game.screen.blit(self.spaceship_img, (self.x, self.y))

    def move(self, speed):
        """
        Bewegt das Raumschiff.

        Args:
            speed (int): Die Bewegungsgeschwindigkeit.
        """
        self.change_x += speed

    def fire_bullet(self):
        """
        Feuert eine Kugel ab.
        """
        self.bullets.append(Bullet(self.game, self.x, self.y))
        self.bullets[len(self.bullets) - 1].fire()


class Bullet:
    def __init__(self, game, x, y):
        """
        Initialisiert eine Kugel.

        Args:
            game (Game): Die Spielinstanz.
            x (int): Die x-Koordinate der Kugel.
            y (int): Die y-Koordinate der Kugel.
        """
        self.x = x
        self.y = y
        self.game = game
        self.is_fired = False
        self.bullet_speed = 10
        self.bullet_img = pygame.image.load("spr_patrone.png")

    def fire(self):
        """
        Feuert die Kugel ab.
        """
        self.is_fired = True

    def update(self):
        """
        Aktualisiert die Position der Kugel.
        """
        self.y -= self.bullet_speed
        if self.y <= 0:
            self.is_fired = False
        self.game.screen.blit(self.bullet_img, (self.x, self.y))


class Enemy:
    def __init__(self, game, x, y):
        """
        Initialisiert einen Feind.

        Args:
            game (Game): Die Spielinstanz.
            x (int): Die x-Koordinate des Feindes.
            y (int): Die y-Koordinate des Feindes.
        """
        self.x = x
        self.y = y
        self.change_x = 5
        self.change_y = 60
        self.game = game
        self.enemy_img = pygame.image.load("spr_space_enemy.png")

    def check_collision(self):
        """
        Überprüft, ob eine Kollision mit dem Feind stattfindet.
        """
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt(math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2))
            if distance < 35:
                bullet.is_fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(30, 120)

    def update(self):
        """
        Aktualisiert die Position des Feindes.
        """
        self.x += self.change_x
        if self.x <= 0:
            self.y += self.change_y
            self.change_x *= -1
        elif self.x >= 736:
            self.y += self.change_y
            self.change_x *= -1
        self.game.screen.blit(self.enemy_img, (self.x, self.y))

if __name__ == "__main__":
    game = Game(800, 600)
