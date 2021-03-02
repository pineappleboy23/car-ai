import pygame as pg
import math
import random
import statistics

import time

start_time = round(time.time())
g_time = round(time.time()) - start_time
generation = 0

clock = pg.time.Clock()

sw = 1000
sh = 700

pg.display.set_caption("Car AI")
win = pg.display.set_mode((sw, sh))
win.fill((0, 180, 20))

car_img_wrong_size = pg.image.load("icar.png")
car_img = pg.transform.smoothscale(car_img_wrong_size.convert_alpha(), (40, 40))

start_angle = 90


class Car(object):
    def __init__(self, id_in):
        self.time = g_time
        self.img = car_img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw // 4
        self.y = sh // 4
        self.angle = start_angle
        self.speed = 4
        self.reward = 0
        self.update_maths()
        self.distance_checkers = []
        self.get_distance_checkers()
        self.id = id_in
        self.input_values = []
        self.generate_ai_values()
        self.derut = False
        self.last_x = 0
        self.last_y = 0
        self.ai_change_rate = 1/10
        self.alive = True
        self.zones_passed = 0
        self.current_zone_reward = 0
        self.current_zone = 0

    def get_distance_checkers(self):
        for num in range(9):
            self.distance_checkers.append(DistanceCheckers(self, num))

    def generate_ai_values(self):
        self.forward_ai_requirement = random.random() - random.random() + 1
        self.forward_ai_values = []
        for val in range(9):
            much_temp = random.random() - random.random() + 1
            self.forward_ai_values.append(much_temp)

        self.right_ai_requirement = random.random() - random.random() + 1
        self.right_ai_values = []
        for val in range(9):
            much_temp = random.random() - random.random() + 1
            self.right_ai_values.append(much_temp)

        self.left_ai_requirement =  random.random() - random.random() + 1
        self.left_ai_values = []
        for val in range(9):
            much_temp = random.random() - random.random() + 1
            self.left_ai_values.append(much_temp)

    def draw(self, win):
        win.blit(self.rotated_surf, self.rotated_rect)

    def move(self):

        self.input_values = []
        for dc in self.distance_checkers:
            temp_1 = dc.update_distance(self)
            self.input_values.append(temp_1)

        self.ai_calculations() # this moves car

        if self.should_die():
            self.ai_death()

        elif g_time % 4 == 0 and self.derut and self.alive:
            self.derut = False
            if (self.last_x == self.x) and (self.last_y == self.last_y):
                self.ai_death()
            self.last_x = self.x
            self.last_y = self.y
        else:
            self.derut = True

        self.update_maths()
        self.update_reward()

    def ai_calculations(self):
        turn_right = False
        turn_left = False
        self.combined_in_ai_forward = []
        for val in range(9):

            self.combined_in_ai_forward.append( self.input_values[val] * self.forward_ai_values[val])
        if statistics.mean(self.combined_in_ai_forward) / statistics.mean(self.input_values) > self.forward_ai_requirement:
            self.move_forward()



        self.combined_in_ai_right = []
        for val in range(9):
            self.combined_in_ai_right.append(self.input_values[val] * self.right_ai_values[val])

        if statistics.mean(self.combined_in_ai_right) / statistics.mean(self.input_values) > self.right_ai_requirement:
            turn_right = True

        self.combined_in_ai_left = []
        for val in range(9):
            self.combined_in_ai_left.append(self.input_values[val] * self.left_ai_values[val])

        if statistics.mean(self.combined_in_ai_left) / statistics.mean(self.input_values) > self.left_ai_requirement:
            turn_left = True

        if turn_right and turn_left:
            if statistics.mean(self.combined_in_ai_left) > statistics.mean(self.combined_in_ai_right):
                self.turn_left
            else:
               self.turn_right()
            turn_right = False
            turn_left = False
        if turn_right:
            self.turn_right()
        if turn_left:
            self.turn_left()

    def turn_left(self):
        self.angle += 5
        self.update_maths()
        

    def turn_right(self):
        self.angle -= 5
        self.update_maths()
        
    def move_forward(self):
        self.x += self.cosine * self.speed
        self.y -= self.sine * self.speed
        self.update_maths()


    def update_reward(self):
        if (self.x > 20 and self.y > 130) and (self.x < 396 and self.y < 204):
            if self.current_zone == 7:
                self.zones_passed += 1
                self.current_zone = 0
            self.current_zone_reward = self.x - 20

        elif (self.x > 396 and self.y > 111) and (self.x < 471 and self.y < 204):
            if self.current_zone == 0:
                self.zones_passed += 1
                self.current_zone = 1
            self.current_zone_reward = 204 - self.y

        elif (self.x > 396 and self.y > 34) and (self.x < 860 and self.y < 111):
            if self.current_zone == 1:
                self.zones_passed += 1
                self.current_zone = 2
            self.current_zone_reward = self.x - 396

        elif (self.x > 860 and self.y > 34) and (self.x < 934 and self.y < 590):
            if self.current_zone == 2:
                self.zones_passed += 1
                self.current_zone = 3
            self.current_zone_reward = self.y - 34
        elif (self.x > 470 and self.y > 590) and (self.x < 934 and self.y < 664):
            if self.current_zone == 3:
                self.zones_passed += 1
                self.current_zone = 4
            self.current_zone_reward = 934 - self.x
        elif (self.x > 396 and self.y > 570) and (self.x < 470 and self.y < 664):
            if self.current_zone == 4:
                self.zones_passed += 1
                self.current_zone = 5
            self.current_zone_reward = 664 - self.x
        elif (self.x > 86 and self.y > 494) and (self.x < 470 and self.y < 570):
            if self.current_zone == 5:
                self.zones_passed += 1
                self.current_zone = 6
            self.current_zone_reward = 470 - self.x

        elif (self.x > 20 and self.y > 204) and (self.x < 86 and self.y < 570):
            if self.current_zone == 6:
                self.zones_passed += 1
                self.current_zone = 7
            self.current_zone_reward = 570 - self.y


    def ai_death(self):
        dead_cars.append(self)
        self.alive = False

    def fetch_one_minus_value(self, multiplier): #.5 if less than 1 -> 1.5 -> 1/1.5 = .66666 -> return .66666
        my_rand = (random.random() - random.random()) * multiplier
        if my_rand < 0:
            tea_temp = 1 - my_rand
            tea_temp = 1 / tea_temp
            return tea_temp - 1
        else:
            return my_rand


    def change_ai_values(self, good_car_in):

        self.ai_change_rate = 1/14

        self.ai_change_rate *= 1 + self.fetch_one_minus_value(.5)

        self.forward_ai_values = good_car_in.forward_ai_values
        self.forward_ai_requirement = good_car_in.forward_ai_requirement

        self.right_ai_values = good_car_in.right_ai_values
        self.right_ai_requirement = good_car_in.right_ai_requirement

        self.left_ai_values = good_car_in.left_ai_values
        self.left_ai_requirement = good_car_in.left_ai_requirement


        self.forward_ai_requirement *= 1 + self.fetch_one_minus_value(self.ai_change_rate)
        self.temp_forward_ai_values = []
        for val in self.forward_ai_values:
            self.temp_forward_ai_values.append(val * (1 + self.fetch_one_minus_value(self.ai_change_rate)))
        self.forward_ai_values = self.temp_forward_ai_values

        self.right_ai_requirement *= 1 + self.fetch_one_minus_value((10 * self.ai_change_rate))
        self.temp_right_ai_values = []
        for val in self.right_ai_values:
            self.temp_right_ai_values.append(val * (1 + self.fetch_one_minus_value(self.ai_change_rate)))
        self.right_ai_values = self.temp_right_ai_values

        self.left_ai_requirement *= 1 + self.fetch_one_minus_value((10 * self.ai_change_rate))
        self.temp_left_ai_values = []
        for val in self.left_ai_values:
            self.temp_left_ai_values.append(val * (1 + self.fetch_one_minus_value(self.ai_change_rate)))
        self.left_ai_values = self.temp_left_ai_values

        self.time = g_time
        self.x = sw // 4
        self.y = sh // 4
        self.angle = start_angle  # set 0?
        self.update_maths()

        self.reward = 0
        self.derut = False
        self.alive = True

        self.zones_passed = 0
        self.current_zone_reward = 0
        self.current_zone = 0

    def give_life(self):
        self.time = g_time
        self.x = sw // 4
        self.y = sh // 4
        self.angle = start_angle  # set 0?
        self.update_maths()

        self.reward = 0
        self.derut = False
        self.alive = True

        self.zones_passed = 0
        self.current_zone_reward = 0
        self.current_zone = 0

    def update_maths(self):
        self.rotated_surf = pg.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle - 90))
        self.sine = math.sin(math.radians(self.angle - 90))

    def should_die(self):
        if self.check_inside(smol_barrier) or self.check_inside(big_barrier):
            return True
        elif not (self.check_inside(smol_boundary) or self.check_inside(big_boundary)):
            return True

    def check_inside(self, track_in):
        if type(track_in) == type(smol_barrier):
            temp_num = 20
        elif type(track_in) == type(smol_boundary):
            temp_num = -20
        if (self.y > track_in.y - temp_num and self.x > track_in.x - temp_num) and (self.y < track_in.y + track_in.h + temp_num and self.x < track_in.x + track_in.w + temp_num):
            return True


class DistanceCheckers(object):
    def __init__(self, car_in, direction):
        self.x = car_in.x
        self.y = car_in.y
        self.w = 1
        self.h = 1
        self.color = (255, 255, 255)
        self.direction = direction * 22.5 + 180
        self.distance = 0
        self.cosine = math.cos(math.radians(car_in.angle + self.direction))
        self.sine = math.sin(math.radians(car_in.angle + self.direction))

    def update_distance(self, car_in):
        self.cosine = math.cos(math.radians(car_in.angle + self.direction))
        self.sine = math.sin(math.radians(car_in.angle + self.direction))
        self.x = car_in.x
        self.y = car_in.y

        self.distance = 0
        self.move()
        return self.distance

    def move(self):
        while not self.keep_moving():

            self.x += self.cosine
            self.y -= self.sine
            self.distance += 1

    def keep_moving(self):
        if self.check_inside(smol_barrier) or self.check_inside(big_barrier):
            return True
        elif not (self.check_inside(smol_boundary) or self.check_inside(big_boundary)):
            return True
        else:
            return False

    def check_inside(self, track_in):
        temp_num = 0
        if (self.y > track_in.y - temp_num and self.x > track_in.x - temp_num) and (self.y < track_in.y + track_in.h + temp_num and self.x < track_in.x + track_in.w + temp_num):
            return True


    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

class Boundary(object):
    def __init__(self, size, color_in, location):
        self.w, self.h = size
        self.x = sw / location - self.w / 2
        self.y = sh / 2 - self.h / 2
        self.color = color_in

    def draw(self, win):
      pg.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])


class Barrier(object):
    def __init__(self, size, color_in, location):
        self.w, self.h = size
        self.x = sw / location - self.w / 2
        self.y = sh / 2 - self.h / 2
        self.color = color_in

    def draw(self, win):
        pg.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])





def redraw_game_window():
    win.fill((0, 180, 0))

    smol_boundary.draw(win)
    big_boundary.draw(win)
    smol_barrier.draw(win)
    big_barrier.draw(win)

    big_id = 0
    most_zones_redraw = -1
    big_current_zone_reward_redraw = 0

    for c in cars:
        if most_zones_redraw <= c.zones_passed:
            if most_zones_redraw < c.zones_passed:
                most_zones_redraw = c.zones_passed
                big_current_zone_reward_redraw = c.current_zone_reward
                big_id = c.id
            elif c.current_zone_reward > big_current_zone_reward_redraw:
                most_zones_redraw = c.zones_passed
                big_current_zone_reward_redraw = c.current_zone_reward
                big_id = c.id

    drew = False
    for c in cars:
        if c.id == big_id and c.alive:
            c.draw(win)
            for l in c.distance_checkers:
                l.draw(win)
            drew = True

    if not drew:
        for c in cars:
            if c.zones_passed == most_zones_redraw:
                c.draw(win)
                for l in c.distance_checkers:
                    l.draw(win)
                break


    pg.display.update()




cars = []
car_amount = 50
for id in range(car_amount):
    cars.append(Car(id))

dead_cars = [] # remove?

smol_barrier = Barrier((390, 290), (0, 180, 20), 3.55) #80 to 30
big_barrier = Barrier((390, 480), (0, 180, 20), 1.5)

big_boundary = Boundary((540, 630), (150, 150, 150), 1.5) # 50 to 150
smol_boundary = Boundary((530, 440), (150, 150, 150), 3.5)

running = True
while running:

    g_time = round(time.time()) - start_time

    clock.tick(60)

    alive_car_amount = 0
    for c in cars:
        if c.alive:
            alive_car_amount += 1


    #print("alive car: " + str(alive_car_amount) + " dead car: " + str(len(dead_cars)) + " cars count: " + str(len(cars)) )

    pp = True

    if len(dead_cars) == len(cars):

        temp_car_vec = []
        for c in dead_cars:

            big_id_while = 0
            most_zones_while = -1
            big_zone_reward_while = 0
            for c in dead_cars:
                if most_zones_while <= c.zones_passed:
                    if most_zones_while < c.zones_passed:
                        most_zones_while = c.zones_passed
                        big_zone_reward_while = c.current_zone_reward
                        big_id_while = c.id
                    elif c.current_zone_reward > big_zone_reward_while:
                        most_zones_while = c.zones_passed
                        big_zone_reward_while = c.current_zone_reward
                        big_id_while = c.id

            best_car_vec = []
            for c in dead_cars:
                if most_zones_while == c.zones_passed:
                    best_car_vec.append(c)

        cars = []
        for c in dead_cars:
            if c.id == big_id_while:
                c.give_life()
                cars.append(c)
            else:
                c.change_ai_values(random.choice(best_car_vec))
                cars.append(c)



        dead_cars = []
        generation += 1
        print("generation: " + str(generation) + " and most zones passed: " + str(most_zones_while) + " biggest zone score: " + str(big_zone_reward_while))



    for c in cars:
        if c.alive:
            c.move()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            for c in cars:
                print(str(c.left_ai_values) +  ' <lav '  + str(c.left_ai_requirement) +  ' <lar '  + str(c.right_ai_values) +  ' <rav '  + str(c.right_ai_requirement) +  ' <rar ' )
            running = False


    redraw_game_window()

