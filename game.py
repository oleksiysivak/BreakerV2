from winsound import PlaySound
import pgzrun
from random import randint
import time

# Class imports
from paddle import Paddle
from ball import Ball
from brick import Brick

TITLE = "Brickbreaker"
WIDTH = 640
HEIGHT = 480
BRICKS_PER_ROW = 10

paddle: Paddle
ball: Ball
balls = []
bricks = []
is_start = True
is_game = True
is_victory = False
score = 0
start_time = None
total_time = 120 # 2 mins


def init_game():
    global paddle, ball, balls, bricks, is_game, is_victory, score, start_time

    paddle = Paddle(320, 440, "paddle.png", 48)
    ball = Ball(320, 340, 3, 3, "ball.png")
    balls = [ball]
    bricks = []
    place_bricks()

    is_game = True
    is_victory = False
    score = 0
    start_time = time.monotonic()


# Create bricks (brick sprites are 64 by 32)
def place_brick_row(sprite, pos_x, pos_y, health_points):
    global bricks

    for i in range(BRICKS_PER_ROW):
        if randint(1, 10) == 4:
            brick = Brick(pos_x + i * 64, pos_y, health_points, "brick_power.png")
        else:
            brick = Brick(pos_x + i * 64, pos_y, health_points, sprite)
        bricks.append(brick)


def place_bricks():
    brick_sprites = ["brick_green.png", "brick_red.png", "brick_blue.png"]
    current_brick_pos_x = 64 / 2
    current_brick_pos_y = 32 / 2
    health_points = len(brick_sprites)
    for brick_sprite in brick_sprites:
        # random chance to place special brick    
        place_brick_row(brick_sprite, current_brick_pos_x, current_brick_pos_y, health_points)
        current_brick_pos_y += 32
        health_points -= 1


init_game()


# Draw scene
def draw():
    global is_game, is_start
    if is_start:
        screen.fill((100, 149, 237))
        screen.draw.text("Brickbreaker", [WIDTH / 2 - 100, HEIGHT / 2 - 100], fontsize=50, color=(0,255,0))
        screen.draw.text("Press space to start", [WIDTH / 2 - 100, HEIGHT / 2 -50], fontsize=30, color=(0,0,255))
        # write text for escape to exit, in red
        screen.draw.text("Press escape to exit", [WIDTH / 2 - 100, HEIGHT / 2], fontsize=30, color=(255, 0, 0))


    elif is_game:
        screen.fill((100, 149, 237))

        paddle.draw() 

        for x in balls:
            x.draw()


        for brick in bricks:
            brick.draw()

        # draw timer
        # Calculate elapsed time
        elapsed_time = 0
        if start_time is not None:
            elapsed_time = int(time.monotonic() - start_time)
        time_left = total_time - elapsed_time
        if time_left <= 0:
            is_game = False
        timer_text = "Time: %d" % time_left
        screen.draw.text(timer_text, topleft=(10, HEIGHT - 40), fontsize=30)


    else:
        screen.clear()
        if is_victory:
            screen.fill((0, 127, 63))
            screen.draw.text("Victory", [WIDTH / 2 - 60, HEIGHT / 2], fontsize=50)
        else:
            screen.fill((127, 0, 63))
            screen.draw.text("Game Over", [WIDTH / 2 - 60, HEIGHT / 2], fontsize=50)
        screen.draw.text("Score: %i" % score, [WIDTH / 2 - 60, HEIGHT / 2 + 50], fontsize=30)
        screen.draw.text("Press space to restart", [WIDTH / 2 - 60, HEIGHT / 2 + 100], fontsize=30)




def update():
    global is_game, is_victory, score, is_start

    # Paddle update for keyboard
    if keyboard.left:
        paddle.update_left()
    if keyboard.right:
        paddle.update_right()

    if is_start:
        if keyboard.space:
            is_start = False
            init_game()
        if keyboard.escape:
            exit()


    elif is_game:
        # Ball update
        ballcount = 0
        for ball in balls:
            if ball.update():
                ballcount += 1
            ball.interact(paddle)

            # Bricks update
            for brick in bricks:
                if ball.actor.colliderect(brick.actor):
                    if ball.actor.image == "ironball.png":
                        brick.healthPoints = 0
                    else:
                        brick.healthPoints -= 1
                    #play a sound
                    sounds.brick.play()
                    if brick.healthPoints == 0:
                        bricks.remove(brick)
                        if brick.sprite == "brick_power.png":
                            #play a sound
                            sounds.powerup.play() 
                            powerOption = randint(1, 3)
                            if powerOption == 1:
                                paddle.actor.image = "long_paddle.png"
                                paddle.width = 82
                            elif powerOption == 2:
                                for i in range(randint(3,4)):
                                    newball = Ball(320, 340, 3, 3, "ball.png")
                                    balls.append(newball)
                            elif powerOption == 3:
                                for b in balls:
                                    b.actor.image = "ironball.png"
                    score += 1
                    if ball.actor.image != "ironball.png":
                        ball.speed_y *= -1
        if ballcount == 0:
            is_game = False
            is_victory = False
        # If all bricks have been broken
        if not bricks:
            is_game = False
            is_victory = True
    else:
        if keyboard.space:
            init_game()


pgzrun.go()
