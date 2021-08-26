import pygame
import random
import time
import os
import sys
from win32com.client import Dispatch

pygame.init()
pygame.mixer.init()

# Defines some color
white = (255, 255, 255)
black = (0, 0, 0)
bright_red = (255, 0, 0)
red = (200, 0, 0)
bright_green = (0, 255, 0)
green = (0, 200, 0)
bright_blue = (0, 0, 255)
blue = (0, 0, 200)

# Defines Global Variables
SCREENWIDTH = 800
SCREENHEIGHT = 600
FPS = 60
SPRITES = {}
SOUNDS = {}

with open(os.path.join("text_file", "level.txt"), "r") as f:
    LEVEL = f.read()
LEVEL = int(LEVEL)

def Speak(text):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(text)


def blit_image(image, x, y):
    screen.blit(image, (x, y))


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, fontsize, fontcolor, x, y):
    font = pygame.font.Font("freesansbold.ttf", fontsize)
    textSurf, textRect = text_objects(text, font, fontcolor)
    textRect.center = (x, y)
    screen.blit(textSurf, textRect)
    pygame.display.update()


def small_text(text, x, y):
    font = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects(text, font, black)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)


def paused():
    global pause
    message_display("Paused", 100, black, SCREENWIDTH//2, SCREENHEIGHT//3)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit(1)

        button("Continue!", bright_green, green, 200, 400, 150, 50)
        button("Quit!", bright_red, red, 500, 400, 150, 50)
        button("Home", bright_blue, blue, 350, 520, 120, 50)

        pygame.display.update()
        clock.tick(15)


def instruction_message():
    msg = "This is a basic game to design for enjoy."
    msg5 = "In this particular game we take star to increase our scores."
    msg1 = "Press Left key of arrow buttons to move towards Left side."
    msg2 = "Press Right key of arrow buttons to move toward Right side."
    msg3 = "Press SPACE or p key or Pause button to Pause you game screen."
    msg4 = "Press A for Speed up your car."

    font = pygame.font.Font(FONT_FAMILY, 40)
    TextSurf, TextRect = text_objects("Controls", font, black)
    TextRect.center = (SCREENWIDTH//2, SCREENHEIGHT//3)
    screen.blit(TextSurf, TextRect)

    small_text(msg1, SCREENWIDTH//2, 260)
    small_text(msg2, SCREENWIDTH//2, 300)
    small_text(msg3, SCREENWIDTH//2, 340)
    small_text(msg4, SCREENWIDTH//2, 380)

    font = pygame.font.Font(FONT_FAMILY, 40)
    TextSurf, TextRect = text_objects("About Game", font, black)
    TextRect.center = (SCREENWIDTH//2, 450)
    screen.blit(TextSurf, TextRect)

    small_text(msg, SCREENWIDTH//2, 490)
    small_text(msg5, SCREENWIDTH//2, 530)


def instruction():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit(1)

        screen.fill(white)
        screen.blit(SPRITES['bg_instruction_image'], (0, 0))

        font = pygame.font.Font(FONT_FAMILY, 80)
        TextSurf, TextRect = text_objects("On Road Game", font, black)
        TextRect.center = (SCREENWIDTH//2, SCREENHEIGHT//6)
        screen.blit(TextSurf, TextRect)

        instruction_message()

        button("Back", bright_blue, blue, 350, 550, 100, 40)

        pygame.display.update()
        clock.tick(15)


def mission():
    global stop
    while stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit(1)
        screen.fill(white)
        screen.blit(SPRITES["bg_instruction_image"], (0, 0))

        font = pygame.font.Font(FONT_FAMILY, 80)
        textSurf, textRect = text_objects("On Road Game", font, black)
        textRect.center = (SCREENWIDTH//2, SCREENHEIGHT//7)
        screen.blit(textSurf, textRect)

        font = pygame.font.Font(FONT_FAMILY, 50)
        textSurf, textRect = text_objects("Mission Summary", font, black)
        textRect.center = (SCREENWIDTH//2, SCREENHEIGHT//3)
        screen.blit(textSurf, textRect)

        font = pygame.font.Font(FONT_FAMILY, 30)
        textSurf, textRect = text_objects(f"Level {LEVEL}", font, black)
        textRect.center = (SCREENWIDTH//2, SCREENHEIGHT//2)
        screen.blit(textSurf, textRect)

        small_text(f"Level {LEVEL} will be completed to collect {10*LEVEL} number of Stars and Dodged will cross {10*LEVEL}.",
                   SCREENWIDTH//2, SCREENHEIGHT//1.7)
        button("Resume", bright_green, green, 120, 460, 150, 50)
        button("Home", bright_blue, blue, 320, 460, 150, 50)
        button("Quit!", bright_red, red, 520, 460, 150, 50)

        pygame.display.update()
        clock.tick(15)


def action(btn_text):
    if btn_text == "Play Again!" or btn_text == "Play!":
        game_loop()
    elif btn_text == "Quit!":
        pygame.quit()
        quit()
    elif btn_text == "Pause":
        pygame.mixer.music.pause()
        global pause
        pause = True
        paused()
    elif btn_text == "Continue!":
        pause = False
    elif btn_text == "Home" or btn_text == "Back":
        game_intro()
    elif btn_text == "Next Level >>":
        global islevel, LEVEL
        islevel = False
        with open("level.txt", "w") as f:
            LEVEL += 1
            f.write(str(LEVEL))
        game_loop()
    elif btn_text == "Instruction!":
        instruction()
    elif btn_text == "Mission":
        pygame.mixer.music.pause()
        global stop
        stop = True
        mission()
    elif btn_text == "Resume":
        stop = False


def button(btn_text, btn_color1, btn_color2, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, btn_color1, (x, y, w, h))
        if click[0] == 1:
            action(btn_text)
    else:
        pygame.draw.rect(screen, btn_color2, (x, y, w, h))

    small_text(btn_text, (x+(w//2)), (y+(h//2)))


def level(count, dodged):
    global islevel
    if count >= (10*LEVEL) == 0 and dodged >= 10*LEVEL:
        pygame.mixer.music.pause()
        while islevel:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    sys.exit(1)
            message_display(f"Level {LEVEL} Up!", 80,
                            black, SCREENWIDTH//2, SCREENHEIGHT//3)
            button("Next Level >>", bright_green, green, 200, 400, 150, 50)
            button("Home", bright_blue, blue, 350, 500, 120, 50)
            button("Quit!", bright_red, red, 450, 400, 150, 50)
            pygame.display.update()
            clock.tick(15)


def Score(count, dodged, level, star_count):
    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Score: {str(count)}", True, black)
    screen.blit(text, (6, 5))

    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Dodged: {str(dodged)}", True, black)
    screen.blit(text, (6, 30))

    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Level: {str(level)}", True, black)
    screen.blit(text, (6, 90))

    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Stars: {str(star_count)}", True, black)
    screen.blit(text, (6, 60))


def start_to_counting(count):
    lst = ["3", "2", "1", "Go!"]

    if count < len(lst):
        if count == 3:
            font = pygame.font.Font("freesansbold.ttf", 100)
            textSurf = font.render(lst[count], True, black)
            textRect = textSurf.get_rect()
            textRect.center = (SCREENWIDTH//2, SCREENHEIGHT//1.7)
            screen.blit(textSurf, textRect)
            pygame.display.update()
            Speak(lst[count])
            time.sleep(0.01)
        else:
            font = pygame.font.SysFont(None, 130)
            text = font.render(lst[count], True, black)
            screen.blit(text, (SCREENWIDTH//2.1, SCREENHEIGHT//2))
            pygame.display.update()
            Speak(lst[count])
            time.sleep(0.01)


def crash():
    message_display("You Crashed", 100, black, SCREENWIDTH//2, SCREENHEIGHT//2)
    Speak("You Crashed")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit(1)

        button("Play Again!", bright_green, green, 200, 450, 150, 50)
        button("Quit!", bright_red, red, 450, 450, 150, 50)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit(1)

        screen.fill(white)

        blit_image(SPRITES["bg_intro_image"], 0, 0)

        msg = pygame.font.Font(FONT_FAMILY, 100)
        TextSurf, TextRect = text_objects("On Road Game", msg, black)
        TextRect.center = (SCREENWIDTH//2, SCREENHEIGHT//2)
        screen.blit(TextSurf, TextRect)

        button("Play!", bright_green, green, 100, 480, 150, 50)
        button("Instruction!", bright_blue, blue, 325, 480, 150, 50)
        button("Quit!", bright_red, red, 550, 480, 150, 50)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global islevel, pause, LEVEL, stop
    islevel = True
    stop = True

    Car_Y1_lst = [SPRITES["car"], SPRITES["car2"],
                  SPRITES["truck1"], SPRITES["truck2"]]
    Car_Y2_lst = [SPRITES["car1"], SPRITES["car3"],
                  SPRITES["truck3"], SPRITES["truck4"]]
    Car_Y3_lst = [SPRITES["car"], SPRITES["car2"],
                  SPRITES["truck1"], SPRITES["truck2"]]
    Car_Y4_lst = [SPRITES["car1"], SPRITES["car3"],
                  SPRITES["truck3"], SPRITES["truck4"]]

    Car_Y1_dir = random.choice(Car_Y1_lst)
    Car_Y2_dir = random.choice(Car_Y2_lst)
    Car_Y3_dir = random.choice(Car_Y3_lst)
    Car_Y4_dir = random.choice(Car_Y4_lst)

    i = 0
    score = 0
    dodged = 0
    count_star_taken = 0

    Road_X = 100
    Road_Y = 0
    Road_Y1 = SPRITES["road"].get_height()

    Grass_X_Left = 0
    Grass_Y_Left = 0
    Grass_Y1_Left = SPRITES["grass"].get_height()

    Grass_X_Right = 700
    Grass_Y_Right = 0
    Grass_Y1_Right = SPRITES["grass"].get_height()

    Car_X = 140*2-20
    Car_Y = 1000
    Car_X_Change = 0
    Change_Car_X_Speed = 7
    Car_Y_Speed = 10

    Car_Width = SPRITES["truck1"].get_width()-73
    Car_Height = SPRITES["truck1"].get_height()-10

    # Another car position of X and Y
    Car_X4 = 150
    Car_Y4 = -random.randrange(100, 600)

    Car_X1 = 140*2-20
    Car_Y1 = -random.randrange(600, 1200)

    Car_X2 = 140*3-10
    Car_Y2 = -random.randrange(1200, 1800)

    Car_X3 = 140*4-40
    Car_Y3 = -random.randrange(600, 1200)

    # Car Y1 and Y3 car speed
    Car_Speed = 2

    # Car Y2 and Y4 car speed
    Car_Speed1 = 7

    gap_bw_both_road = 5
    Road_speed = 5

    # Star X and Y coordinates
    Star_X = random.randrange(160, 300)
    Star_Y = -random.randrange(60, 600)

    Star_X1 = random.randrange(350, 510)
    Star_Y1 = -random.randrange(60, 600)

    # Play Background Music
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Car_X_Change = -Change_Car_X_Speed
                elif event.key == pygame.K_RIGHT:
                    Car_X_Change = Change_Car_X_Speed
                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    pygame.mixer.music.pause()
                    pause = True
                    paused()
                elif event.key == pygame.K_a:
                    Road_speed = 10
                    Car_Speed1 = 15
                    Car_Speed = 7
                    gap_bw_both_road = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Car_X_Change = 0
                elif event.key == pygame.K_RIGHT:
                    Car_X_Change = 0
                elif event.key == pygame.K_a:
                    Road_speed = 5
                    Car_Speed = 2
                    Car_Speed1 = 7
                    gap_bw_both_road = 10

        screen.fill((80, 80, 80))
        blit_image(SPRITES["road"], Road_X, Road_Y)
        blit_image(SPRITES["road"], Road_X, Road_Y1)
        blit_image(SPRITES["grass"], Grass_X_Left, Grass_Y_Left)
        blit_image(SPRITES["grass"], Grass_X_Right, Grass_Y_Right)
        blit_image(SPRITES["grass"], Grass_X_Left, Grass_Y1_Left)
        blit_image(SPRITES["grass"], Grass_X_Right, Grass_Y1_Right)
        blit_image(SPRITES["car"], Car_X, Car_Y)
        blit_image(Car_Y1_dir, Car_X1, Car_Y1)
        blit_image(Car_Y2_dir, Car_X2, Car_Y2)
        blit_image(Car_Y3_dir, Car_X3, Car_Y3)
        blit_image(Car_Y4_dir, Car_X4, Car_Y4)
        blit_image(SPRITES["star"], Star_X, Star_Y)
        blit_image(SPRITES["star"], Star_X1, Star_Y1)

        if i > 3:
            pygame.mixer.music.unpause()

            Star_Y += Road_speed
            Star_Y1 += Road_speed

            if Star_Y+64 > Car_Y and Star_Y < Car_Y+Car_Height:
                if Car_X > Star_X and Car_X < Star_X+50 or Car_X+Car_Width > Star_X and Car_X+Car_Width < Star_X+50:
                    score += 5
                    pygame.mixer.Sound.play(SOUNDS["star_collect"])
                    Star_X = random.randrange(160, 300)
                    Star_Y = -random.randrange(60, 600)
                    count_star_taken += 1
            elif Star_Y1+64 > Car_Y and Star_Y1 < Car_Y+Car_Height:
                if Car_X > Star_X1 and Car_X < Star_X1+50 or Car_X+Car_Width > Star_X1 and Car_X+Car_Width < Star_X1+50:
                    score += 5
                    pygame.mixer.Sound.play(SOUNDS["star_collect"])
                    Star_X1 = random.randrange(350, 510)
                    Star_Y1 = -random.randrange(60, 600)
                    count_star_taken += 1

            if Star_Y > SCREENHEIGHT:
                Star_X = random.randrange(160, 300)
                Star_Y = -random.randrange(60, 600)
            elif Star_Y1 > SCREENHEIGHT:
                Star_X1 = random.randrange(350, 510)
                Star_Y1 = -random.randrange(60, 600)

            # Moving all things
            Road_Y += Road_speed
            Grass_Y_Left += Road_speed
            Grass_Y_Right += Road_speed
            Road_Y1 += Road_speed
            Grass_Y1_Left += Road_speed
            Grass_Y1_Right += Road_speed

            # Below two Car left side go Up on Y axis
            Car_Y4 += Car_Speed1
            Car_Y2 += Car_Speed1

            # Below two Car right side go down on Y axis
            Car_Y1 += Car_Speed
            Car_Y3 += Car_Speed

            # Main Car move in X direction
            Car_X += Car_X_Change

        else:
            start_to_counting(i)
            i += 1

        if Car_X <= 150:
            Car_X = 150
        elif Car_X >= 140*4-40:
            Car_X = 140*4-40

        # Car comes in style form
        if Car_Y > 400:
            Car_Y -= Car_Y_Speed

        # Generate Infinite Car
        if Car_Y1 > SCREENHEIGHT:
            Car_X1 = 140*2-20
            Car_Y1 = -random.randrange(600, 1200)
            dodged += 1
            Car_Y1_dir = random.choice(Car_Y1_lst)

        if Car_Y2 > SCREENHEIGHT:
            Car_X2 = 140*3-10
            Car_Y2 = -random.randrange(1200, 1800)
            dodged += 1
            Car_Y2_dir = random.choice(Car_Y2_lst)

        if Car_Y3 > SCREENHEIGHT:
            Car_X3 = 140*4-40
            Car_Y3 = -random.randrange(600, 1200)
            dodged += 1
            Car_Y3_dir = random.choice(Car_Y3_lst)

        if Car_Y4 > SCREENHEIGHT:
            Car_X4 = 150
            Car_Y4 = -random.randrange(100, 600)
            dodged += 1
            Car_Y4_dir = random.choice(Car_Y4_lst)

        level(count_star_taken, dodged)

        # Logic for moving road and grass
        if Road_Y > SPRITES["road"].get_height() and Grass_Y_Left > SPRITES["grass"].get_height() and Grass_Y_Right > SPRITES["grass"].get_height():
            Road_Y = -SPRITES["road"].get_height()+gap_bw_both_road
            Grass_Y_Left = -SPRITES["grass"].get_height()+gap_bw_both_road
            Grass_Y_Right = -SPRITES["grass"].get_height()+gap_bw_both_road
        elif Road_Y1 > SPRITES["road"].get_height() and Grass_Y1_Left > SPRITES["grass"].get_height() and Grass_Y1_Right > SPRITES["grass"].get_height():
            Road_Y1 = -SPRITES["road"].get_height()+gap_bw_both_road
            Grass_Y1_Left = -SPRITES["grass"].get_height()+gap_bw_both_road
            Grass_Y1_Right = -SPRITES["grass"].get_height()+gap_bw_both_road

        # Logic for Crashed
        if Car_Y1+Car_Height >= Car_Y and Car_Y1 <= Car_Y+Car_Height:
            if Car_X >= Car_X1 and Car_X <= Car_X1+Car_Width or Car_X+Car_Width >= Car_X1 and Car_X+Car_Width <= Car_X1+Car_Width:
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SOUNDS["car_crash"])
                crash()

        elif Car_Y2+Car_Height >= Car_Y and Car_Y2 <= Car_Y+Car_Height:
            if Car_X >= Car_X2 and Car_X <= Car_X2+Car_Width or Car_X+Car_Width >= Car_X2 and Car_X+Car_Width <= Car_X2+Car_Width:
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SOUNDS["car_crash"])
                crash()

        elif Car_Y3+Car_Height >= Car_Y and Car_Y3 <= Car_Y+Car_Height:
            if Car_X >= Car_X3 and Car_X <= Car_X3+Car_Width or Car_X+Car_Width >= Car_X3 and Car_X+Car_Width <= Car_X3+Car_Width:
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SOUNDS["car_crash"])
                crash()

        elif Car_Y4+Car_Height >= Car_Y and Car_Y4 <= Car_Y+Car_Height:
            if Car_X >= Car_X4 and Car_X <= Car_X4+Car_Width or Car_X+Car_Width >= Car_X4 and Car_X+Car_Width <= Car_X4+Car_Width:
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(SOUNDS["car_crash"])
                crash()

        if i > 3:
            Score(int(score), dodged, LEVEL, count_star_taken)
            button("Pause", bright_red, red, 710, 5, 80, 30)
            button("Mission", bright_blue, blue, 710, 40, 80, 30)

        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == "__main__":

    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    pygame.display.set_caption("On Road Game")

    # Load all images and add on dictionary
    SPRITES["road"] = pygame.transform.scale(pygame.image.load(
        os.path.join("sprites", "road.png")).convert_alpha(), (600, 600))
    SPRITES["grass"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "grass.png")).convert_alpha(), 90), (100, 600))
    SPRITES["car"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "car.png")).convert_alpha(), -90), (128, 128))
    SPRITES["car1"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "car.png")).convert_alpha(), 90), (128, 128))
    SPRITES["car2"] = pygame.transform.scale(pygame.image.load(
        os.path.join("sprites", "car1.png")).convert_alpha(), (128, 128))
    SPRITES["car3"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "car1.png")).convert_alpha(), 180), (128, 128))
    SPRITES["truck1"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "truck1.png")).convert_alpha(), -90), (128, 128))
    SPRITES["truck2"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "truck2.png")).convert_alpha(), -90), (128, 128))
    SPRITES["truck3"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "truck1.png")).convert_alpha(), 90), (128, 128))
    SPRITES["truck4"] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
        os.path.join("sprites", "truck2.png")).convert_alpha(), 90), (128, 128))
    SPRITES["bg_intro_image"] = pygame.transform.scale(
        pygame.image.load(os.path.join("sprites", "intro_bg_img.png")).convert_alpha(), (800, 600))
    SPRITES["bg_instruction_image"] = pygame.transform.scale(
        pygame.image.load(os.path.join("sprites", "instruction_bg_img.png")).convert_alpha(), (800, 600))
    SPRITES["star"] = pygame.transform.scale(
        pygame.image.load(os.path.join("sprites", "star.png")).convert_alpha(), (64, 64))

    # Load all sound effects
    pygame.mixer.music.load(os.path.join("sounds", "music_loop.mp3"))
    SOUNDS["car_crash"] = pygame.mixer.Sound(
        os.path.join("sounds", "car_crash.wav"))
    SOUNDS["star_collect"] = pygame.mixer.Sound(
        os.path.join("sounds", "star_collect.wav"))

    # Open Font Family Folder
    FONT_FAMILY = os.path.join("font", "NC.ttf")

    clock = pygame.time.Clock()
    game_intro()
    game_loop()
