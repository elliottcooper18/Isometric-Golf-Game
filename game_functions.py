import config
import pygame
import random
import game_classes
import math

def scale(x, y, z, max_x, max_y, max_z):
    return x/max_x, y/max_y, z/max_z

def isometric_coordinates(x, y, z):
    #black_hole
    bhx = (x * (0.5 * config.TILE_WIDTH)) - (y * (0.5 * config.TILE_WIDTH)) + config.TILE_START_X
    bhy = (x * (0.5 * config.TILE_HEIGHT)) + (y * (0.5 * config.TILE_HEIGHT)) - (z *config.TILE_Z_HEIGHT) + config.TILE_START_Y
    return (bhx, bhy)

def draw_onto_isometric_platform(screen,level,ball):

    point_a = (config.TILE_START_X,config.TILE_START_Y)
    point_b = (config.TILE_START_X + config.TILE_WIDTH//2,config.TILE_START_Y+config.TILE_HEIGHT//2)
    point_c = (config.TILE_START_X,config.TILE_START_Y+config.TILE_HEIGHT)
    point_d = (config.TILE_START_X-config.TILE_WIDTH//2,config.TILE_START_Y+config.TILE_HEIGHT//2)

    #draw isometric platform
    pygame.draw.polygon(screen,level.colour,(point_a,point_b,point_c,point_d))

    #draw black hole
    q,t = moving_hole(level.blackhole_startX,level.blackhole_startY)

    point_1_scaled_x, point_1_scaled_y,point_1_scaled_z = scale(q, t, 0, config.MAXIMUM_X, config.MAXIMUM_Y,config.MAXIMUM_Z)
    point1 = isometric_coordinates(point_1_scaled_x, point_1_scaled_y, 0)

    point_2_scaled_x, point_2_scaled_y,point_1_scaled_z = scale(q + level.blackhole_width, t, 0, config.MAXIMUM_X,config.MAXIMUM_Y, config.MAXIMUM_Z)
    point2 = isometric_coordinates(point_2_scaled_x, point_2_scaled_y, 0)

    point_3_scaled_x, point_3_scaled_y,point_1_scaled_z = scale(q, t + level.blackhole_height,0, config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    point3 = isometric_coordinates(point_3_scaled_x, point_3_scaled_y, 0)

    point_4_scaled_x, point_4_scaled_y,point_1_scaled_z = scale(q + level.blackhole_width, t + level.blackhole_height,0, config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    point4= isometric_coordinates(point_4_scaled_x, point_4_scaled_y, 0)

    pygame.draw.polygon(screen, (0,0,0), (point1,point2,point4,point3))

    #/////////////////////////////////////////////////

    #draw worm hole

    wh_scaled_x1, wh_scaled_y1,wh_scaled_z1 = scale(level.wormhole_startX1, level.wormhole_startY1, 0, config.MAXIMUM_X, config.MAXIMUM_Y,config.MAXIMUM_Z)
    wh_point1 = isometric_coordinates(wh_scaled_x1, wh_scaled_y1, 0)

    wh_scaled_x2, wh_scaled_y2, wh_scaled_z2 = scale(level.wormhole_startX1 + level.wormhole_width,level.wormhole_startY1, 0, config.MAXIMUM_X,config.MAXIMUM_Y, config.MAXIMUM_Z)
    wh_point2 = isometric_coordinates(wh_scaled_x2, wh_scaled_y2, 0)

    wh_scaled_x3, wh_scaled_y3, wh_scaled_z3 = scale(level.wormhole_startX1,level.wormhole_startY1 + level.wormhole_height, 0,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    wh_point3 = isometric_coordinates(wh_scaled_x3, wh_scaled_y3, 0)

    wh_scaled_x4, wh_scaled_y4, wh_scaled_z4 = scale(level.wormhole_startX1 + level.wormhole_width,level.wormhole_startY1 + level.wormhole_height, 0,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    wh_point4 = isometric_coordinates(wh_scaled_x4, wh_scaled_y4, 0)

    pygame.draw.polygon(screen, level.wormhole_colour, (wh_point1, wh_point2, wh_point4, wh_point3))

    #wormhole2

    wh_scaled_x1, wh_scaled_y1, wh_scaled_z1 = scale(level.wormhole_startX2, level.wormhole_startY2, level.wormhole_startZ2,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    wh2_point1 = isometric_coordinates(wh_scaled_x1, wh_scaled_y1, wh_scaled_z1)

    wh_scaled_x2, wh_scaled_y2, wh_scaled_z2 = scale(level.wormhole_startX2 + level.wormhole_width,level.wormhole_startY2, level.wormhole_startZ2, config.MAXIMUM_X, config.MAXIMUM_Y,config.MAXIMUM_Z)
    wh2_point2 = isometric_coordinates(wh_scaled_x2, wh_scaled_y2, wh_scaled_z1)

    wh_scaled_x3, wh_scaled_y3, wh_scaled_z3 = scale(level.wormhole_startX2,level.wormhole_startY2 + level.wormhole_height, level.wormhole_startZ2,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    wh2_point3 = isometric_coordinates(wh_scaled_x3, wh_scaled_y3, wh_scaled_z1)

    wh_scaled_x4, wh_scaled_y4, wh_scaled_z4 = scale(level.wormhole_startX2 + level.wormhole_width,level.wormhole_startY2 + level.wormhole_height, level.wormhole_startZ2,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    wh2_point4 = isometric_coordinates(wh_scaled_x4, wh_scaled_y4, wh_scaled_z1)

    pygame.draw.polygon(screen, level.wormhole_colour, (wh2_point1, wh2_point2, wh2_point4, wh2_point3))

    #hole
    #q,t = moving_hole(level.hole_x,level.hole_y)

    h_scaled_x1, h_scaled_y1, h_scaled_z1 = scale(level.hole_x, level.hole_y, 0,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    h_point1 = isometric_coordinates(h_scaled_x1, h_scaled_y1, 0)

    h_scaled_x2, h_scaled_y2, h_scaled_z2 = scale(level.hole_x + level.hole_width,level.hole_y, 0, config.MAXIMUM_X, config.MAXIMUM_Y,config.MAXIMUM_Z)
    h_point2 = isometric_coordinates(h_scaled_x2, h_scaled_y2, 0)

    h_scaled_x3, h_scaled_y3, h_scaled_z3 = scale(level.hole_x,level.hole_y + level.hole_height, 0,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    h_point3 = isometric_coordinates(h_scaled_x3, h_scaled_y3, 0)

    h_scaled_x4, h_scaled_y4, h_scaled_z4 = scale(level.hole_x + level.hole_width,level.hole_y + level.hole_height, 0,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    h_point4 = isometric_coordinates(h_scaled_x4, h_scaled_y4, 0)

    pygame.draw.polygon(screen, level.hole_colour, ((h_point1), (h_point2), (h_point4), (h_point3)))

def draw_power_up(x,y,w,h,screen,colour):

    p_scaled_x1, p_scaled_y1, p_scaled_z1 = scale(x, y, 0,config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    p_point1 = isometric_coordinates(p_scaled_x1, p_scaled_y1, 0)

    p_scaled_x2, p_scaled_y2, p_scaled_z2 = scale(x + w,
                                                     y, 0, config.MAXIMUM_X, config.MAXIMUM_Y,
                                                     config.MAXIMUM_Z)
    p_point2 = isometric_coordinates(p_scaled_x2, p_scaled_y2, 0)

    p_scaled_x3, p_scaled_y3, p_scaled_z3 = scale(x,
                                                     y + h, 0,
                                                     config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    p_point3 = isometric_coordinates(p_scaled_x3, p_scaled_y3, 0)

    p_scaled_x4, p_scaled_y4, p_scaled_z4 = scale(x + w,
                                                     y + h, 0,
                                                     config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    p_point4 = isometric_coordinates(p_scaled_x4, p_scaled_y4, 0)

    pygame.draw.polygon(screen, colour, (p_point1, p_point2, p_point4, p_point3))

def draw_ball(screen,level,ball):

    #DRAW
    ball_posX, ball_posY,ball_posZ = scale(ball.x_metres,ball.y_metres,ball.z_metres,config.MAXIMUM_X,config.MAXIMUM_Y,config.MAXIMUM_Z)

    ball_x,ball_y = isometric_coordinates(ball_posX, ball_posY, ball_posZ)

    #shadow
    ball_shaddowX,ball_shaddowY = isometric_coordinates(ball_posX, ball_posY, 0)

    #draw shadow
    pygame.draw.circle(screen, config.TILE_SHADDOW_COLOUR, (ball_shaddowX, ball_shaddowY), config.TILE_BALL_RADIUS)

    #draw ball
    pygame.draw.circle(screen,config.TILE_BALL_COLOUR,(ball_x,ball_y),config.TILE_BALL_RADIUS)

def draw_minimap(screen,level,ball):

    x, y, z = scale(ball.x_metres, ball.y_metres, ball.z_metres, config.MAXIMUM_X, config.MAXIMUM_Y, config.MAXIMUM_Z)
    #draw minimap 1
    start_x = config.MINIMAP_START_X
    start_y = config.MINIMAP_START_Y
    pygame.draw.rect(screen, level.colour,(start_x, start_y, config.MINIMAP_WIDTH, config.MINIMAP_HEIGHT))

    #TOP DOWN VIEW
    #ball
    minimap_ball_x = config.MINIMAP_START_X + x * config.MINIMAP_WIDTH
    minimap_ball_y = config.MINIMAP_START_Y + y * config.MINIMAP_HEIGHT

    if not ball.x_metres > 200:
        pygame.draw.circle(screen, config.TILE_BALL_COLOUR, (minimap_ball_x, minimap_ball_y),
                           config.MINIMAP_BALL_RADIUS)

    #///////////////////////////////

    #draw minimap 2
    start_x = config.MINIMAP_START_X
    start_y = start_y + config.MINIMAP_HEIGHT + config.MINIMAP_MARGIN

    pygame.draw.rect(screen, level.colour,(start_x, start_y, config.MINIMAP_WIDTH, config.MINIMAP_HEIGHT))

    #X SIDE VIEW

    minimap_ball_x = config.MINIMAP_START_X + x * config.MINIMAP_WIDTH
    minimap_ball_z =  start_y  + config.MINIMAP_HEIGHT -  z * config.MINIMAP_HEIGHT

    if not ball.x_metres > 200:
        pygame.draw.circle(screen, config.TILE_BALL_COLOUR, (minimap_ball_x, minimap_ball_z), config.MINIMAP_BALL_RADIUS)

    #draw minimap 3
    start_x = config.MINIMAP_START_X
    start_y = start_y + config.MINIMAP_HEIGHT + config.MINIMAP_MARGIN
    pygame.draw.rect(screen, level.colour,(start_x, start_y, config.MINIMAP_WIDTH, config.MINIMAP_HEIGHT))

    minimap_ball_y = config.MINIMAP_START_Y + y * config.MINIMAP_WIDTH
    minimap_ball_z = start_y + config.MINIMAP_HEIGHT - z * config.MINIMAP_HEIGHT

    if not ball.y_metres > 200:
        pygame.draw.circle(screen, config.TILE_BALL_COLOUR, (minimap_ball_y, minimap_ball_z), config.MINIMAP_BALL_RADIUS)

def draw_info(screen,stroke_count,total_strokes,ball,level,start_club_index):
    #par, shot counter, hole
    #could add a settings menu?
    #add a better way to change clubs?

    pygame.font.init()
    font = pygame.font.SysFont('Courier New ', config.TEXT_SIZE,True)
    colour = config.FONT_COLOUR

    stroke_text = font.render(f'Stroke {stroke_count}', True, colour)
    text_width,text_height = font.size(f'Stroke {stroke_count}')

    total_stroke_text = font.render(f'Total strokes {total_strokes}', True, colour)
    text_width2, text_height2 = font.size(f'Total strokes {total_strokes}')

    ground_angle_text = font.render(f'Ground angle {round(math.degrees(ball.initial_rotation_angle))}', True, colour)
    text_width3, text_height3 = font.size(f'Ground angle {round(math.degrees(ball.initial_rotation_angle))}')

    flight_angle_text = font.render(f'Flight angle {round(math.degrees(ball.initial_flight_angle))}', True, colour)
    text_width4, text_height4 = font.size(f'Flight angle {round(math.degrees(ball.initial_flight_angle))}')

    level_name_text = font.render(f'Level name {level.name}', True, colour)
    text_width5, text_height5 = font.size(f'Level name {level.name}')

    type_of_club = font.render(f'Club {ball.clubs()[start_club_index][0]}', True, colour)
    text_width6, text_height6 = font.size(f'Club {ball.clubs()[start_club_index]}')

    pygame.draw.rect(screen, (31, 31, 31),(config.START_X, config.START_Y, text_width +text_width2 + config.GAP, text_height))
    pygame.draw.rect(screen, (31, 31, 31),(config.START_X-100, config.START_Y + text_height + config.GAP, text_width3 + text_width4 + config.GAP, text_height))

    pygame.draw.rect(screen, (31, 31, 31),(config.START_X+100, config.START_Y+ (3.5*config.GAP), text_width5, text_height))

    power_text = font.render(f'Power {round((ball.initial_speed))}', True, colour)
    power_text_width, power_text_height = font.size(f'Power {round((ball.initial_speed))}')

    pygame.draw.rect(screen, (31, 31, 31),(config.POWER_BOX_X + config.POWER_BOX_WIDTH//2 - power_text_width//2, config.POWER_BOX_Y -config.POWER_BOX_HEIGHT,power_text_width, power_text_height))

    pygame.draw.rect(screen, (31, 31, 31), (config.START_X - 100, config.START_Y + text_height + config.GAP, text_width3 + text_width4 + config.GAP,
    text_height))

    pygame.draw.rect(screen, (31, 31, 31), (
    config.START_X + 100, config.START_Y + (5 * config.GAP), text_width6-270, text_height))

    screen.blit(stroke_text, (config.START_X, config.START_Y))
    screen.blit(total_stroke_text, (config.START_X + text_width + config.GAP, config.START_Y))
    screen.blit(ground_angle_text, (config.START_X -100, config.START_Y+ text_height + config.GAP))
    screen.blit(flight_angle_text, ((config.START_X -100) + text_width3 + config.GAP, config.START_Y + text_height + config.GAP))
    screen.blit(power_text, ((config.POWER_BOX_X + config.POWER_BOX_WIDTH // 2 - power_text_width // 2),config.POWER_BOX_Y - config.POWER_BOX_HEIGHT))
    screen.blit(level_name_text,((config.START_X)+100,config.START_Y+ (3.5*config.GAP)))
    screen.blit(type_of_club, ((config.START_X +100) , config.START_Y + (5 * config.GAP)))

    #current club

def plot_projectile(screen,level,ball):

    ball_trace = game_classes.Ball(level)
    ball_trace.x_metres = ball.x_metres
    ball_trace.y_metres = ball.y_metres
    ball_trace.z_metres = ball.z_metres

    ball_trace.initial_flight_angle = ball.initial_flight_angle
    ball_trace.initial_rotation_angle = ball.initial_rotation_angle
    ball_trace.initial_speed = ball.initial_speed

    ball_trace.rotation_angle = ball.initial_rotation_angle
    ball_trace.flight_angle = ball.initial_flight_angle
    ball_trace.speed = ball.initial_speed

    ball_trace.time = config.TIME_INTERVAL

    while ball_trace.z_metres >= 0 and ball_trace.check_not_moving() == False:

        ball_trace.move_ball(level)
        draw_ball(screen, level, ball_trace)

def get_star_coords(star_coords):

    for i in range(100):
        x, y = random.randint(0, config.SCREEN_WIDTH), random.randint(0, config.SCREEN_HEIGHT)
        radius = random.randint(config.STAR_MIN_RADIUS,config.STAR_MAX_RADIUS)

        star_coords.append((x, y,radius))

def draw_stars(screen,level,ball,star_coords):
    for i in star_coords:

        pygame.draw.circle(screen,config.STAR_COLOUR,(i[0],i[1]),i[2])

def create_stopwatch(x,screen):
    pygame.font.init()
    font = pygame.font.SysFont('Courier New ', config.TEXT_SIZE,True)
    text = f'Time {round(x,1)}'
    stopwatch = font.render(text, False, config.TEXT_COLOUR)

    text_width, text_height = font.size(text)
    text_x, text_y = config.SCREEN_WIDTH//2 -60,50

    text_width, text_height = font.size(text)

    pygame.draw.rect(screen, (31, 31, 31),
                     (text_x, text_y, text_width, text_height))

    screen.blit(stopwatch, (text_x, text_y))

def skip_level(total_strokes,current_time,level_number):
    total_strokes +=10
    level_number+=1
    current_time +=10

#potential for recursiion
def power_box(screen, current_time):
    pygame.draw.rect(screen,config.POWER_BOX_COLOUR,(config.POWER_BOX_X,config.POWER_BOX_Y,config.POWER_BOX_WIDTH,config.POWER_BOX_HEIGHT))
    pygame.draw.rect(screen,config.POWER_BAR_COLOUR,(config.POWER_BAR_X,config.POWER_BOX_Y,config.POWER_BAR_WIDTH,config.POWER_BAR_HEIGHT))

    #d from equil point
    #USING SIMPLE HARMONIC MOTION // ADD TO ANALYSIS

    displacement = ((config.MAX_DISPLACEMENT) * (math.sin(config.OMEGA*current_time)))
    config.POWER_BAR_X = config.POWER_BAR_X_INITIAL_X + displacement

def moving_hole(x,y):
    q = (x-150) * math.cos(config.HOLE_ANGLE) +100
    t = (y-150) * math.sin(config.HOLE_ANGLE) + 100

    return q,t


