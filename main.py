import pygame, math
from PIL import Image

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption("Pygame Raycaster")
clock = pygame.time.Clock()
running = True
TILESIZE = 32
pxData = []
gameMap = []

img = Image.open("map.png")
for i in range(20):
    gameMap.append([])
    for j in range(20):
        gameMap[i].append(0 if img.getpixel((i, j)) == (0, 0, 0, 255) else 1)

img = Image.open("map_large.png")
for i in range(640):
    pxData.append([])
    for j in range(640):
        pxData[i].append(1 if img.getpixel((i, j)) == (255, 255, 255, 255) else 0)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = math.pi
        self.speed = 1
        self.fov = math.pi / 2
        self.max_depth = 640
        self.casted_rays = 120

    def draw(self):
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (self.x, self.y),
            (self.x - math.sin(self.angle) * 50, self.y + math.cos(self.angle) * 50),
            1,
        )
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 15)

    def cast_rays(self):
        start_angle = self.angle - self.fov / 2
        for ray in range(self.casted_rays):
            for depth in range(self.max_depth):
                x = self.x - math.sin(start_angle) * depth
                y = self.y + math.cos(start_angle) * depth
                if pxData[int(y)][int(x)] == 1:
                    break
            # pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (x, y), 1)
            start_angle += self.fov / self.casted_rays
        
            color = 255 / (1 + depth * depth * 0.0001)
            depth *= math.cos(self.angle - start_angle)
            wall_height = 21000 / depth
            SCALE = (640) / self.casted_rays
            pygame.draw.rect(screen, (color, color, color), (640 + ray * SCALE, (640 / 2) - wall_height / 2,
                SCALE+1, wall_height))


player = Player(320, 240)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    x, y = 0, 0
    for _y in gameMap:
        for _x in _y:
            if _x == 1:
                pygame.draw.rect(
                    screen,
                    (0, 185, 185),
                    (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE),
                )
            x += 1
        x = 0
        y += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.angle -= 0.02
    if keys[pygame.K_d]:
        player.angle += 0.02
    if keys[pygame.K_w]:
        nextX = player.x + -math.sin(player.angle) * player.speed
        nextY = player.y + math.cos(player.angle) * player.speed
        if pxData[int(nextY)][int(nextX)] == 0:
            player.x = nextX
            player.y = nextY
    if keys[pygame.K_s]:
        nextX = player.x + math.sin(player.angle) * player.speed
        nextY = player.y + -math.cos(player.angle) * player.speed
        if pxData[int(nextY)][int(nextX)] == 0:
            player.x = nextX
            player.y = nextY

    fps = f"FPS: {round(clock.get_fps())}"
    screen.blit(
        pygame.font.SysFont("comicsans", 16).render(str(fps), True, (255, 255, 255)),
        (0, 0),
    )

    player.draw()
    pygame.draw.rect(screen, (150, 150, 150), (640, 0, 640, 320))
    pygame.draw.rect(screen, (100, 100, 100), (640, 320, 640, 320))
    player.cast_rays()

    pygame.display.flip()
    clock.tick(120)
