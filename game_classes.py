import config
import math
import sqlite3
import random

class Level:

    def __init__(self, level_name=''):

        if level_name == "":
            #need to look up first level
            self.level_name = self.get_first_level_name()
        else:
            #load level_name
            self.level_name = level_name

        #self.level_number = level_number

        #level_data = open(config.LEVELS_FOLDER + f'/level-{level_number}.txt','r')
        level_data = open(config.LEVELS_FOLDER + f'/{self.level_name}.txt', 'r')

        lines = level_data.readlines()

        for line in lines:
            line = line.strip()

            line_parts = line.split(':')

            key = line_parts[0]
            value = line_parts[1]

            if key == 'name':
                self.name = value

            elif key == 'par':
                self.par = value

            elif key == 'surface':
                self.surface = value

            elif key == 'surface_value':
                self.surface_value = float(value)

            elif key == 'colour':
                value_parts = value.split(',')
                self.colour = (int(value_parts[0]), int(value_parts[1]), int(value_parts[2]))

            elif key == 'gravity':
                self.gravity = float(value)

            elif key == 'ball_start_x':
                self.ball_startX = int(value)

            elif key == 'ball_start_y':
                self.ball_startY = int(value)

            elif key == 'black_hole_start_x':
                self.blackhole_startX = int(value)

            elif key == 'black_hole_start_y':
                self.blackhole_startY = int(value)

            elif key == 'black_hole_width':
                self.blackhole_width = int(value)

            elif key == 'black_hole_height':
                self.blackhole_height = int(value)

            elif key == 'worm_hole_start_x':
                x_coords = value.split(',')
                self.wormhole_startX1 = int(x_coords[0])
                self.wormhole_startX2 = int(x_coords[1])

            elif key == 'worm_hole_start_y':
                y_coords = value.split(',')
                self.wormhole_startY1 = int(y_coords[0])
                self.wormhole_startY2 = int(y_coords[1])

            elif key == 'worm_hole_start_z':
                z_coords = value.split(',')
                self.wormhole_startZ1 = int(z_coords[0])
                self.wormhole_startZ2 = int(z_coords[1])

            elif key == 'worm_hole_width':
                self.wormhole_width = int(value)

            elif key == 'worm_hole_height':
                self.wormhole_height = int(value)

            elif key == 'worm_hole_start_z':
                z_coords = value.split(',')
                self.wormhole_startZ1 = int(z_coords[0])
                self.wormhole_startZ2 = int(z_coords[1])

            elif key == 'worm_hole_colour':
                value_parts = value.split(',')
                self.wormhole_colour = (int(value_parts[0]),int(value_parts[1]),int(value_parts[2]))

            elif key == 'hole_x':
                self.hole_x = int(value)

            elif key == 'hole_y':
                self.hole_y = int(value)

            elif key == 'hole_width':
                self.hole_width = int(value)

            elif key == 'hole_height':
                self.hole_height = int(value)

            elif key == 'hole_colour':
                colour_parts = value.split(',')
                self.hole_colour = (int(colour_parts[0]),int(colour_parts[1]),int(colour_parts[2]))

            elif key == 'bad_mystery_box_x':
                self.bad_mystery_box_x = int(value)

            elif key == 'bad_mystery_box_y':
                self.bad_mystery_box_y = int(value)

    def get_first_level_name(self):
        #return first value in json
        return config.LEVEL_TREE["level_name"]

    def get_last_level_name(self):
        list_of_levels = self.get_recursive_pre_order_levels(config.LEVEL_TREE)
        return list_of_levels[-1]

    def get_next_level_name(self):
        #get currrent level index and +1
        list_of_levels = self.get_recursive_pre_order_levels(config.LEVEL_TREE)
        current_index = list_of_levels.index(self.level_name)
        return list_of_levels[current_index+1]

    def get_recursive_pre_order_levels(self, node, level_lists=[]):
        level_lists.append(node["level_name"])

        if "children" in node:  #have children?
            for child in node["children"]:
                self.get_recursive_pre_order_levels(child, level_lists)

        return level_lists

class Ball:

    def __init__(self, level):

        self.x_metres = level.ball_startX
        self.y_metres = level.ball_startY
        self.z_metres = 0

        self.initial_flight_angle = math.radians(45)
        self.initial_rotation_angle = math.radians(45)
        self.initial_speed = config.BALL_INIT_SPEED

        self.rotation_angle = self.initial_flight_angle
        self.flight_angle = self.initial_rotation_angle# config.BALL_INIT_FLIGHT_ANGLE)

        self.speed = self.initial_speed
        self.gravity = level.gravity
        self.time = config.TIME_INTERVAL
        self.dict = {}

    def clubs(self):
        #types of clubs
        #type of club, max speed, min angle , max angle
        #Driver

        driver = {1:('Driver',config.DRIVER_MAX_SPEED,20,70)}
        self.dict.update(driver)

        putter = {2:('Putter',config.PUTTER_MAX_SPEED,0,20)}
        self.dict.update(putter)

        iron = {3:('Iron',config.IRON_MAX_SPEED,10,60)}
        self.dict.update(iron)

        return self.dict

    def move_ball(self,level):

        if self.initial_flight_angle == 0:
            pass#ball is only moving along the ground

        else:
            #ball is following projectile motion
            pass

        # v = u + at

        initial_speed_horizontal = math.cos(self.flight_angle) * self.speed
        initial_speed_x = initial_speed_horizontal * math.cos(self.rotation_angle)
        initial_speed_y = initial_speed_horizontal * math.sin(self.rotation_angle)

        #handle ball when launched along the ground
        if self.initial_flight_angle == 0:
            initial_speed_z = 0
        else:
            initial_speed_z = math.sin(self.flight_angle) * self.speed

        #v = u + at

        final_horizontal_speed = initial_speed_horizontal
        final_speed_x = initial_speed_x
        final_speed_y = initial_speed_y

        if self.initial_flight_angle == 0:
            final_speed_z = 0
        else:
            final_speed_z = initial_speed_z + (self.gravity * self.time)

        displacement_horizontal = initial_speed_horizontal * self.time
        displacement_x = math.cos(self.rotation_angle) * displacement_horizontal
        displacement_y = math.sin(self.rotation_angle) * displacement_horizontal

        if self.initial_flight_angle <= 0:
            displacement_vertical = 0
        else:
            displacement_vertical = (initial_speed_z * self.time) + (0.5 * (self.gravity) * (self.time**2))

        self.x_metres += displacement_x
        self.y_metres += displacement_y
        self.z_metres += displacement_vertical

        if self.initial_flight_angle <= 0:
            self.speed = level.surface_value * self.speed
        else:
            self.speed = math.sqrt((final_horizontal_speed * final_horizontal_speed) + (final_speed_z ** 2))
            self.flight_angle = math.atan2(final_speed_z, final_horizontal_speed)

    def set_rotation_angle_left(self):
        if self.initial_rotation_angle <=math.radians(360 + config.DELTA_ROTATION_ANGLE):
            self.initial_rotation_angle += math.radians(config.DELTA_ROTATION_ANGLE)
        else:
            self.initial_rotation_angle = 0

    def set_rotation_angle_right(self):
        if self.initial_rotation_angle >= math.radians(-360 + config.DELTA_ROTATION_ANGLE):
            self.initial_rotation_angle -= math.radians(config.DELTA_ROTATION_ANGLE)
        else:
            self.initial_rotation_angle = 0

    def set_flight_angle_increase(self,start_club_index):
        if self.initial_flight_angle < math.radians(self.dict[start_club_index][3]):
            self.initial_flight_angle += math.radians(config.DELTA_FLIGHT_ANGLE)

    def set_flight_angle_decrease(self,start_club_index):
        if not self.initial_flight_angle < math.radians(self.dict[start_club_index][2]):
            self.initial_flight_angle -= math.radians(config.DELTA_FLIGHT_ANGLE)

    def shoot(self):
        #need to create a rect with a rect inside, where if it reaches a specific point it gives a higher power of shot
        pass

    def determine_speed(self,current_time):
        self.initial_speed  = (((config.BALL_MAX_SPEED) *(config.OMEGA)) * (math.cos(current_time*config.OMEGA)))

        if self.initial_speed <0:
            self.initial_speed = -self.initial_speed

    def check_bounce(self):
        if self.z_metres < 0:
            self.z_metres = 0
            self.speed = self.speed * 0.7
            self.flight_angle = -self.flight_angle
            print("bounced")

    def check_boundaries(self):
        if self.x_metres > config.MAXIMUM_X or self.x_metres <0:
            if self.z_metres <=0:
                return True
        if self.y_metres>200 or self.y_metres < 0:
            if self.z_metres <=0:
                return True

        return False

    def check_blackhole(self,screen,level,x,y):
        if self.x_metres >= x - config.TILE_BALL_RADIUS and self.x_metres - config.TILE_BALL_RADIUS <= y + level.blackhole_width:
            if self.y_metres >= y - config.TILE_BALL_RADIUS and self.y_metres - config.TILE_BALL_RADIUS <= y + level.blackhole_height:
                if self.z_metres <=0:
                    print('Entered black hole, restart level')
                    return True
        return False

    def check_wormhole1(self,screen,level):
        #wormhole1
        if self.x_metres >= level.wormhole_startX1 - config.TILE_BALL_RADIUS and self.x_metres - config.TILE_BALL_RADIUS <= level.wormhole_startX1 + level.wormhole_width:
            if self.y_metres >= level.wormhole_startY1 - config.TILE_BALL_RADIUS and self.y_metres - config.TILE_BALL_RADIUS <= level.wormhole_startY1 + level.wormhole_height:
                if self.z_metres <= 0:
                    print('Entered wormhole1, restart level')
                    return True
        return False

    def check_wormhole2(self,screen,level):
        if self.x_metres >= level.wormhole_startX2 - config.TILE_BALL_RADIUS and self.x_metres <= level.wormhole_startX2 + level.wormhole_width + config.TILE_BALL_RADIUS:
            if self.y_metres >= level.wormhole_startY2 - config.TILE_BALL_RADIUS and self.y_metres <= level.wormhole_startY2 + level.wormhole_height + config.TILE_BALL_RADIUS:
                if self.z_metres < 0:
                    return True
        return False

    def check_hole(self,screen,level):
        if self.x_metres >= level.hole_x - config.TILE_BALL_RADIUS and self.x_metres - config.TILE_BALL_RADIUS <= level.hole_x + level.hole_width:
            if self.y_metres >= level.hole_y - config.TILE_BALL_RADIUS and self.y_metres - config.TILE_BALL_RADIUS <= level.hole_y + level.hole_height:
                if self.z_metres <= 0:
                    print('Completed level!')
                    return True
        return False

    def check_bad_mystery_box(self,bad_mystery_box_x,bad_mystery_box_y,bad_mystery_box_width,bad_mystery_box_height):
        if self.x_metres>= bad_mystery_box_x - bad_mystery_box_width//2 and self.x_metres <= bad_mystery_box_x + bad_mystery_box_width//2:
            if self.y_metres >= bad_mystery_box_y and self.y_metres<= bad_mystery_box_y + bad_mystery_box_height:
                return True
        return False

    def check_not_moving(self):
        if self.speed < 0.4:
            return True
        else:
            return False

class Db:
    def __init__(self):
        #connect to database (will create the  database if doesn't already exist)
        self.conn = sqlite3.connect("golf.db")

        #create a cursor object using the cursor() method
        self.cursor = self.conn.cursor()

        query = f"CREATE TABLE IF NOT EXISTS 'player' (id INTEGER PRIMARY KEY, name varchar(12) NOT NULL)"
        self.cursor.execute(query)

        #add level time
        query = f"CREATE TABLE IF NOT EXISTS 'game_stats' (id INTEGER, FOREIGN KEY (id) REFERENCES player(id))"
        self.cursor.execute(query)

        self.in_table = False

    def create_player(self, player_name):
        players_in_database_list = []

        query = f"SELECT * from player WHERE name = '{player_name}'"

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        if len(player_name) > 0 and len(player_name)<=12:
            if len(records) == 0:
                self.cursor.execute(f'''INSERT INTO player(name) VALUES ('{player_name}')''')
                #commit changes in the database
                self.conn.commit()
                self.in_table = False
            else:
                self.in_table = True
        else:
            self.in_table = True

    def get_players(self):
        players = []
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.execute("SELECT * FROM player ORDER BY id")

        for row in cursor:
            players.append((row['name'], row['id']))

        return players

    def insert_player_info(self, selected_player_id, player_times, total_strokes):
        #paramatised queries
        #insert all player times into database, with the correct player id
        time_taken = 0
        for i in player_times:
            time_taken += i

        query = f'INSERT INTO game_stats(id,total_time,total_strokes) VALUES({selected_player_id},{time_taken},{total_strokes})'
        self.cursor.execute(query)
        self.conn.commit()

        return time_taken,total_strokes

    def get_lowest_strokes(self):
        query = f'SELECT name,total_strokes FROM game_stats,player WHERE game_stats.id =player.id ORDER BY total_strokes ASC LIMIT 5'

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_lowest_time(self):
        #joiming
        query = f'SELECT name,total_time FROM game_stats,player WHERE game_stats.id =player.id ORDER BY total_time ASC LIMIT 5'

        self.cursor.execute(query)
        times = self.cursor.fetchall()
        return times

class Power_ups():
    def __init__(self,start_x,start_y,width,height,time):
        self.start_x = start_x
        self.start_y = start_y

        self.width = config.MYSTERY_BOX_WIDTH
        self.height = self.width
        self.time_popped_up_for = time

        self.power_ups = {}
        self.good = False



    def check_if_hit(self, x, y):
        if x >= self.start_x and x <= self.start_x + self.width:
            if y >= self.start_y and y <= self.start_y + self.height:
                return True
        return False

    def check_if_in_black_hole(self,x,y,w,h):
        if self.start_x >= x - self.width and self.start_x <= x + w:
            if self.start_y >= y - self.height and self.start_y <= y + h:
                return True

        print('hi')
        return False


    def check_if_in_wormhole(self,level):
        if self.start_x >= level.wormhole_startX1 and self.start_x <= level.wormhole_startX1 + level.wormhole_width:
            if self.start_y >= level.wormhole_startY1 and self.start_y <= level.wormhole_startY1 + level.wormhole_height:
                return True


        if self.start_x >= level.wormhole_startX2 and self.start_x <= level.wormhole_startX2 + level.wormhole_width:
            if self.start_y >= level.wormhole_startY2 and self.start_y <= level.wormhole_startY2 + level.wormhole_height:
                return True

        return False

    def change_isometric_sizes(self,random_entry,width,height):
        new_width = width * float(random_entry[1])
        new_height = height * float(random_entry[1])
        return new_width,new_height

    def get_coords(self):
        return self.start_x,self.start_y

class Bad_mystery_box(Power_ups):

    def __init__(self,start_x,start_y,colour):
        width = 5
        height = width
        time = 10

        self.colour = colour
        self.platform_move_count = 0
        self.platform_move = False

        super().__init__(start_x,start_y,width,height,time)

        self.good = False
        self.colour = colour

    def get_dict(self):
        return self.power_ups

    def get_metrics(self):
        return self.width, self.height

    def get_colour(self):
        return self.colour

    def insert_good_power_ups(self):
        f = open('bad_power_up_details', 'r')

        for i in f:
            i = i.strip()

            parts = i.split(':')
            key = parts[0]
            value = parts[1]

            self.power_ups.update({key: value})

    def get_type(self):
        return self.good

    def decrease_power_of_clubs(self,random_entry,clubs):
        change = random_entry[1]
        config.DRIVER_MAX_SPEED,config.PUTTER_MAX_SPEED = config.DRIVER_MAX_SPEED * float(change), config.PUTTER_MAX_SPEED * float(change)

    def no_aim(self):
        #something to stop the aim being used
        return False

class Good_mystery_box(Power_ups):
    def __init__(self,start_x,start_y,colour):
        width = 15
        height = width
        time = 10
        self.colour = colour

        super().__init__(start_x,start_y,width,height,time)
        self.good = True

    def insert_good_power_ups(self):
        f = open('good_power_up_details', 'r')

        for i in f:
            i = i.strip()

            parts = i.split(':')
            key = parts[0]
            value = parts[1]

            self.power_ups.update({key: value})

    def get_metrics(self):
        return self.width, self.height

    def get_type(self):
        return self.good

    def get_colour(self):
        return self.get_colour

    def get_dict(self):
        return self.power_ups