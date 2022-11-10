import pygame
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900,500
win = pygame.display.set_mode((WIDTH, HEIGHT))

white = (255, 255, 255)
black = (0, 0, 0)
Red = (255, 0, 0)
Yellow = (255, 255, 0)

space_w, space_h = 55,40
FPS = 60

VEL = 5

bullet_vel = 7

max_bullets = 3
border = pygame.Rect(WIDTH // 2-5, 0, 10,HEIGHT)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

bullet_shoot_sound = pygame.mixer.Sound("shoott.mp3")
bullet_hit_sound = pygame.mixer.Sound("hit.mp3")


life_font = pygame.font.SysFont("verdania", 40)
winner_font = pygame.font.SysFont("verdania", 70)


yellow_space_ship = pygame.image.load("spaceship_yellow.png")
red_space_ship = pygame.image.load("spaceship_red.png")

space = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH, HEIGHT))



yellow_space_ship = pygame.transform.rotate(pygame.transform.scale(yellow_space_ship,(space_w,space_h)),90)
red_space_ship = pygame.transform.rotate(pygame.transform.scale(red_space_ship,(space_w,space_h)),270)

def draw_winner(text):
     draw_text = winner_font.render(text, 1, white)

     win.blit(draw_text,(WIDTH // 2 - draw_text.get_width() // 2,
                         HEIGHT // 2 - draw_text.get_height() // 2))

     pygame.display.update()

     pygame.time.delay(5000)



def handle_bullets(red_bullets, yellow_bullets, red, yellow):

    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def red_movments(red, key_pressed):
    if key_pressed[pygame.K_a] and red.x - VEL >  border.x + border.w:  # LEFT
        red.x -= VEL
    if key_pressed[pygame.K_d] and red.x + VEL + red.w  <  WIDTH:  # RIGHT
        red.x += VEL
    if key_pressed[pygame.K_w] and red.y - VEL > 15  :  # UP
        red.y -= VEL
    if key_pressed[pygame.K_s] and red.y + VEL + red.h < HEIGHT - 15:  # DOWN
        red.y += VEL

def yellow_movments(yellow, key_pressed):
    if key_pressed[pygame.K_LEFT] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if key_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.w < border.x :
        yellow.x += VEL
    if key_pressed[pygame.K_UP] and yellow.y - VEL > 15:
        yellow.y -= VEL
    if key_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.h < HEIGHT - 15 :
        yellow.y += VEL

def drow_window(red, yellow, red_bullets,yellow_bullets,red_life,yellow_life):

    win.blit(space,(0,0))

    pygame.draw.rect(win, black, border)

    red_life_text = life_font.render("Life "+ str(red_life), 1 , Red)
    yellow_life_text = life_font.render("Life " + str(yellow_life), 1, Red)


    win.blit(red_life_text, (WIDTH - red_life_text.get_width() -10, 10))
    win.blit(yellow_life_text, (10, 10))


    win.blit(yellow_space_ship,(yellow.x,yellow.y))

    win.blit(red_space_ship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(win,Red, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(win,Yellow, bullet)

    pygame.display.update()




def main():
    red_bullets = []
    yellow_bullets = []
    red_life = 10
    yellow_life = 10

    red = pygame.Rect(700,100, space_w, space_h)
    yellow = pygame.Rect(300, 100, space_w, space_h)

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < max_bullets:

                    bullet = pygame.Rect(yellow.x + yellow.w, yellow.y +yellow.h //2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_shoot_sound.play()

                if event.key ==  pygame.K_LCTRL and len(red_bullets) < max_bullets:

                    bullet = pygame.Rect(red.x, red.y + red.h // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_shoot_sound.play()

            if event.type == YELLOW_HIT:
                yellow_life -= 1
                bullet_hit_sound.play()

            if event.type == RED_HIT:
                red_life -= 1
                bullet_hit_sound.play()

            winner_text = ""

            if yellow_life <= 0:
               winner_text = "Red Wins!"

            if red_life <= 0:
                winner_text = "Yellow Wins!"

            if winner_text != "":
                draw_winner(winner_text)
                break


        key_pressed = pygame.key.get_pressed()

        red_movments(red,key_pressed)
        yellow_movments(yellow,key_pressed)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        drow_window(red,yellow, red_bullets,yellow_bullets,red_life, yellow_life)
    main()


if __name__ == "__main__":
    main()


