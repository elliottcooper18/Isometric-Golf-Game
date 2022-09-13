import game_functions as gf
import time
import pygame
import pygame_menu
import config
import game_classes
import state
import math
import random

############################
#main game func
############################

def play_game(selected_player_name, selected_player_id):

    # Define game variables
    start_time = time.time()

    level = game_classes.Level("")
    ball = game_classes.Ball(level)
    bad_mystery_box = game_classes.Bad_mystery_box
    good_mystery_box = game_classes.Good_mystery_box

    game_state = state.AIM

    stroke_count = 0
    total_strokes = 0
    running = True

    star_coords = []
    gf.get_star_coords(star_coords)
    db = game_classes.Db()

    player_times = []
    player_strokes = []
    boxes = []

    start_club_index = 1

    platform_move = False
    platform_move_count = 0

    current_power_up = []
    power_up_length = 1

    power_up = False

    plot_projectile = True

    level_name = level.level_name

    bh_moving_x = level.blackhole_startX
    bh_moving_y = level.blackhole_startY

    while running:

        bh_moving_x, bh_moving_y = gf.moving_hole(bh_moving_x, bh_moving_y)


        config.HOLE_ANGLE += config.HOLE_DELTA_ANGLE
        end_time = time.time()
        current_time = end_time - start_time

        if game_state == state.AIM:

            clubs_dict = ball.clubs()
            current_club = clubs_dict[start_club_index]

            config.BALL_MAX_SPEED = (clubs_dict[start_club_index][1])
            screen = pygame.display.set_mode((config.SCREEN_WIDTH,config.SCREEN_HEIGHT))
            screen.fill((0,0,0))
            gf.power_box(screen, current_time)

            if random.randint(0, 100) == 1 and len(boxes) < 2:

                x = random.randint(1,2)

                if x == 1:

                    mb = bad_mystery_box(random.randint(0,200-config.MYSTERY_BOX_WIDTH), random.randint(0,200-config.MYSTERY_BOX_WIDTH), config.BAD_MYSTERY_BOX_COLOUR)
                    boxes.append(mb)

                if x == 2:
                    mb = good_mystery_box(random.randint(0, 200), random.randint(0, 100),(config.BAD_MYSTERY_BOX_COLOUR))
                    boxes.append(mb)

            ball.determine_speed(current_time)
            gf.create_stopwatch(current_time, screen)
            gf.draw_stars(screen, level, ball, star_coords)
            gf.draw_onto_isometric_platform(screen,level,ball)
            gf.draw_ball(screen,level,ball)
            gf.draw_minimap(screen,level,ball)

            # bad_mystery_box_width, bad_mystery_box_height,bad_mystery_box_x, bad_mystery_box_y = bad_mystery_box.get_metrics()
            if plot_projectile == True:
                gf.plot_projectile(screen,level,ball)

            gf.draw_info(screen, stroke_count,total_strokes,ball,level,start_club_index)

            if ball.check_blackhole(screen,level,bh_moving_x,bh_moving_y):
                game_state = state.AIM
                ball.x_metres = level.ball_startX
                ball.y_metres = level.ball_startY
                ball.z_metres = 0

          #add code to check bmb



            for box in boxes:
                if box.check_if_in_black_hole(bh_moving_x, bh_moving_y, level.blackhole_width, level.blackhole_height):
                    boxes.remove(box)

                if box.check_if_in_wormhole(level):
                    boxes.remove(box)




            if ball.flight_angle <0:
                ball.flight_angle = -ball.flight_angle

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_SPACE:
                        ball.flight_angle = ball.initial_flight_angle  # This copy does not change during flight
                        ball.rotation_angle = ball.initial_rotation_angle

                        ball.speed = ball.initial_speed
                        game_state = state.FLYING
                        stroke_count += 1
                        total_strokes += 1

                    elif event.key == pygame.K_a:
                        ball.set_rotation_angle_left()

                    elif event.key == pygame.K_d:
                        ball.set_rotation_angle_right()

                    elif event.key == pygame.K_w:
                        ball.set_flight_angle_increase(start_club_index)

                    elif event.key == pygame.K_s:
                        ball.set_flight_angle_decrease(start_club_index)

                    elif event.key == pygame.K_c:
                        if start_club_index == len(clubs_dict):
                            start_club_index = 1

                        else:
                            start_club_index +=1

                        ball.initial_flight_angle = math.radians(clubs_dict[start_club_index][2])

                    elif event.key == pygame.K_k:

                        if level_name != level.get_last_level_name():

                            stroke_count += 10
                            player_times.append(round(current_time + 10))
                            player_strokes.append(stroke_count)
                            start_time = time.time()
                            level_name = level.get_next_level_name()

                            level = game_classes.Level(level_name)
                            ball = game_classes.Ball(level)

                            for i in boxes:
                                boxes.pop()

                        else:
                            game_state = state.GAME_OVER
                            running = False

        elif game_state == state.FLYING:

            ball.move_ball(level)
            ball.check_bounce()

            if ball.check_hole(screen,level):
                game_state = state.BALL_IN_HOLE

            if ball.check_blackhole(screen,level,bh_moving_x,bh_moving_y):
                game_state = state.AIM
                ball.x_metres = level.ball_startX
                ball.y_metres = level.ball_startY
                ball.z_metres = 0

            if ball.check_wormhole1(screen,level):
                game_state = state.AIM
                ball.x_metres = level.wormhole_startX2
                ball.y_metres = level.wormhole_startY2
                ball.z_metres = level.wormhole_startZ2

            if ball.check_wormhole2(screen, level):
                game_state = state.AIM
                ball.x_metres = level.wormhole_startX1
                ball.y_metres = level.wormhole_startY1
                ball.z_metres  = 0

            if ball.check_boundaries():
                game_state = state.AIM
                ball.x_metres = level.ball_startX
                ball.y_metres = level.ball_startY
                ball.z_metres = 0

            if ball.check_not_moving():
                game_state = state.AIM
                ball.z_metres = 0

            screen = pygame.display.set_mode((config.SCREEN_WIDTH,config.SCREEN_HEIGHT))
            screen.fill((0,0,0))

            gf.draw_stars(screen, level, ball, star_coords)
            gf.draw_onto_isometric_platform(screen,level,ball)
            gf.draw_ball(screen, level, ball)
            gf.draw_minimap(screen,level,ball)
            gf.draw_info(screen, stroke_count,total_strokes,ball, level,start_club_index)

            gf.create_stopwatch(current_time, screen)

        elif game_state == state.BALL_IN_HOLE:

            player_times.append(round(current_time))
            player_strokes.append(stroke_count)

            if level_name != level.get_last_level_name():

                for i in boxes:
                    boxes.pop()

                level_name = level.get_next_level_name()
                stroke_count = 0
                start_time = time.time()
                game_state = state.AIM

                level = game_classes.Level(level_name)
                ball = game_classes.Ball(level)

            else:
                running = False
                game_state = state.GAME_OVER

        for box in boxes:

            if box.check_if_in_black_hole(bh_moving_x,bh_moving_y,level.blackhole_width,level.blackhole_height):
                boxes.remove(box)

            print(bh_moving_x,box.start_x)




            if box.check_if_in_wormhole(level):
                boxes.remove(box)

            box.insert_good_power_ups()
            x, y = (box.get_coords()[0], box.get_coords()[1])
            w, h = box.get_metrics()
            colour = box.get_colour()

            gf.draw_power_up(x, y, w, h, screen,box.colour)

            if box.check_if_hit(ball.x_metres, ball.y_metres):

                boxes.remove(box)

                #GOOD BOX
                if box.get_type():

                    x = box.get_dict()

                    entry_list = list(x.items())

                    random_entry = random.choice(entry_list)
                    print(random_entry[0])

                    if len(current_power_up) <1:
                        if random_entry[0] == 'black_hole_width':
                            level.blackhole_width,level.blackhole_height = box.change_isometric_sizes(random_entry,level.blackhole_width,level.blackhole_height)
                            current_power_up.append(random_entry[0])
                        if random_entry[0] == 'hole_width':
                            level.hole_width,level.hole_height = box.change_isometric_sizes(random_entry,level.hole_width,level.hole_height)
                            current_power_up.append(random_entry[0])

                else:

                    x = box.get_dict()
                    entry_list = list(x.items())
                    random_entry = random.choice(entry_list)

                    if len(current_power_up) < 1:
                        if random_entry[0] == 'hole_width':
                            level.hole_width,level.hole_height = box.change_isometric_sizes(random_entry,level.hole_width,level.hole_height)
                            current_power_up.append(random_entry[0])

                        if random_entry[0] == 'move_platform':
                            current_power_up.append(random_entry[0])
                            platform_move = True

                        if random_entry[0] == 'decrease_power':
                            box.decrease_power_of_clubs(random_entry,clubs_dict)
                            current_power_up.append(random_entry[0])


                        if random_entry[0] == 'aim':
                            current_power_up.append(random_entry[0])
                            plot_projectile = box.no_aim()

        if platform_move == True:
            if config.TILE_START_X > (config.SCREEN_WIDTH * 2) // 3:
                platform_move_count += 1
                config.TILE_MOVE = -1

            if config.TILE_START_X < config.SCREEN_WIDTH // 3:
                platform_move_count += 1
                config.TILE_MOVE = 1

            if platform_move_count == 4:
                config.TILE_START_X, config.TILE_START_Y = config.TILE_RETURN_X, config.TILE_RETURN_Y
                platform_move_count = 0
                platform_move = False

            config.TILE_START_X += config.TILE_MOVE

        if len(current_power_up) == 1:
            power_up = True

        if power_up == True:



            num = random.randint(1,1500)

            if num == 5:
                return_power_up = current_power_up[0]

                if return_power_up == 'hole_width':
                    level.hole_width,level.hole_height = config.HOLE_RETURN_WIDTH,config.HOLE_RETURN_HEIGHT

                if return_power_up == 'black_hole_width':
                    level.blackhole_width,level.blackhole_height = config.BLACK_HOLE_RETURN_WIDTH,config.BLACK_HOLE_RETURN_WIDTH

                if return_power_up == 'decrease_power':
                    config.DRIVER_MAX_SPEED,config.PUTTER_MAX_SPEED = config.DRIVER_RETURN_MAX_SPEED,config.PUTTER_MAX_SPEED

                if return_power_up == 'aim':
                    plot_projectile = True

                current_power_up.pop()

                power_up = False

        pygame.display.flip()
        pygame.time.wait(10)

    if game_state == state.GAME_OVER:
        total = 0

        for i in player_strokes:
            total+=i

        db.insert_player_info(selected_player_id, player_times, total)
        #menu of scores
        ending_menu(player_times,player_strokes)

############################
#menu funcs
############################

def create_player(text_input):

    player_name = text_input.get_value()
    db = game_classes.Db()
    db.create_player(player_name)
    db.get_players()

    if db.in_table == True:
        display_player_insert_fail()

    else:
        display_player_successful()

def create_player_menu():

    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=mytheme)

    player_name_text = menu.add.label('Enter player name', font_color=config.TITLE_COLOUR, padding=0, font_size=config.TITLE_SIZE, background_inflate=(30, 0))
    player_name_text.translate(0, -100)

    player_name_text_input = menu.add.text_input('Name : ', default='')
    menu.add.button('Create player', create_player, player_name_text_input)

    menu.add.button('Back',opening_menu)

    menu.mainloop(surface)

def create_lowest_strokes():

    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=leaderboard_theme)

    db = game_classes.Db()
    users_scores = db.get_lowest_strokes()

    users_on_leaderboard = []

    title = menu.add.label(f'Top scores!', font_color=config.TITLE_COLOUR, padding=0, font_size=config.TITLE_SIZE, background_inflate=(30, 0))

    position_count = 1
    for i in users_scores:
        lowest_shots_text = menu.add.label(f'{position_count}: {i[0]} - {i[1]}  shots ', font_color=config.LEADERBOARD_COLOUR, padding=0, font_size=config.MENU_TEXT_SIZE,background_inflate=(30, 0))
        users_on_leaderboard.append(i[0])
        position_count+=1

    menu.add.button('Back', opening_menu)

    menu.mainloop(surface)

def create_lowest_time():

    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=leaderboard_theme)
    db = game_classes.Db()
    user_times = db.get_lowest_time()

    position_count = 1

    text = menu.add.label(f'FASTEST TIMES', font_color=config.TITLE_COLOUR, padding=0, font_size=config.TITLE_SIZE, background_inflate=(30, 0))

    for i in user_times:
        lowest_time_text = menu.add.label(f'{position_count}:  {i[0]} - {i[1]}  seconds',font_color=config.LEADERBOARD_COLOUR, padding=0,font_size=config.MENU_TEXT_SIZE, background_inflate=(30, 0))
        position_count += 1

    menu.add.button('Back', opening_menu)

    menu.mainloop(surface)

def display_player_insert_fail():
    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=mytheme)

    error_text = menu.add.label('Invalid name', font_color=config.TITLE_COLOUR, padding=0, font_size=config.TITLE_SIZE,
                          background_inflate=(30, 0))
    error_text.translate(0, -100)

    menu.add.button('Back to menu',opening_menu)

    menu.mainloop(surface)

def display_player_successful():
    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=mytheme)

    succesful_text = menu.add.label('Player successfully added', font_color=config.TITLE_COLOUR, padding=0,
                          font_size=config.TITLE_SIZE,
                          background_inflate=(30, 0))
    succesful_text.translate(0, -100)

    menu.add.button('Back to menu', opening_menu)

    menu.mainloop(surface)

def start_game(selected_player):

    tuple = selected_player.get_value()[0]  # Name, Id

    selected_player_name = tuple[0]
    selected_player_id = tuple[1]

    print(selected_player_id, selected_player_name)
    play_game(selected_player_name,selected_player_id)

def welcome_menu():

    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=mytheme)

    title = menu.add.label('SPACE GOLF', font_color=config.TITLE_COLOUR, padding=0, font_size=config.TITLE_SIZE, background_inflate=(30, 0))
    title.translate(0, -160)

    text1 = menu.add.label('Welcome to SPACE  GOLF', font_color=config.SUB_TEXT_COLOUR, padding=0, font_size=config.SUB_TEXT_SIZE,background_inflate=(30, 0))
    text2 = menu.add.label('Click below to create new player', font_color=config.SUB_TEXT_COLOUR, padding=0, font_size=config.SUB_TEXT_SIZE,background_inflate=(30, 0))
    text1.translate(0, -100)
    text2.translate(0,-50)

    menu.add.button('Create new player',create_player_menu)
    menu.mainloop(surface)

def opening_menu():
    db = game_classes.Db()
    player_list = db.get_players()

    if len(player_list) == 0:
        welcome_menu()

    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT,theme=mytheme)

    title = menu.add.label('SPACE GOLF',font_color = config.TITLE_COLOUR, padding = 0,font_size = config.TITLE_SIZE,background_inflate = (30,0) )
    height = title.get_height()

    title.translate(0,-100)

    selected_player = menu.add.selector('Players ', player_list)
    menu.add.button('Start game', start_game,selected_player)
    menu.add.button('Create player', create_player_menu)
    menu.add.button('Lowest strokes', create_lowest_strokes)
    menu.add.button('Lowest times ', create_lowest_time)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

def ending_menu(player_times,player_strokes):

    surface = pygame.display.set_mode((config.MENU_WIDTH, config.MENU_HEIGHT))
    menu = pygame_menu.Menu('', config.MENU_WIDTH, config.MENU_HEIGHT, theme=mytheme)

    title = menu.add.label('GAME OVER', font_color=config.TITLE_COLOUR, padding=0, font_size=config.TITLE_SIZE, background_inflate=(30, 0))

    total_strokes = 0
    for i in player_strokes:
        total_strokes += int(i)

    total_time = 0
    for i in player_times:
        total_time += int(i)

    player_info_text = menu.add.label(f'You completed the game with {total_strokes} \n strokes and a time of {total_time} seconds')

    menu.mainloop(surface)

############################
#main game starts here
############################

pygame.init()
surface = pygame.display.set_mode((config.MENU_WIDTH, config.MENU_HEIGHT))
Theme = pygame_menu.themes.Theme
mytheme = Theme(background_color=(0, 0, 0, 0), widget_padding=25, widget_font = config.MENU_FONT,)
leaderboard_theme = Theme(background_color=(0, 0, 0, 0), widget_padding=25, widget_font = config.LEARDERBOARD_FONT,)
opening_menu()