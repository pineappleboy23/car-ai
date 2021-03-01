import pygame as pg
import math
import random
import statistics

import time

start_time = round(time.time())
g_time = round(time.time()) - start_time
ai_change_rate = 1 # higher number means slower change
ai_values = []
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
        self.current_checkpoint = 0
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
        #ai_values.append((self.forward_ai_values,self.forward_ai_requirement,self.left_ai_values,self.left_ai_requirement,self.right_ai_values,self.right_ai_requirement))
        # if len(ai_values) > 300:
        #    ai_values = []

    def draw(self, win):
        win.blit(self.rotated_surf, self.rotated_rect)

    def move(self):

        self.input_values = []
        for dc in self.distance_checkers:
            temp_1 = dc.update_distance(self)
            self.input_values.append(temp_1)

        self.ai_calculations() # this moves car

        self.checkpoint_touching()

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
        

    def checkpoint_touching(self):
        for cp in checkpoints:
            if self.check_inside(cp) and cp.name == self.current_checkpoint :
                self.reward += 50
                if cp.name == 9:
                    self.current_checkpoint = 0
                else:
                    self.current_checkpoint += 1

    def ai_death(self):
        dead_cars.append(self)
        self.alive = False

    def change_ai_values(self, good_car_in):

        self.ai_change_rate = 1/10

        self.ai_change_rate *= 1 + random.random() - random.random()

        self.forward_ai_values = good_car_in.forward_ai_values
        self.forward_ai_requirement = good_car_in.forward_ai_requirement

        self.right_ai_values = good_car_in.right_ai_values
        self.right_ai_requirement = good_car_in.right_ai_requirement

        self.left_ai_values = good_car_in.left_ai_values
        self.left_ai_requirement = good_car_in.left_ai_requirement


        self.forward_ai_requirement *= (1 + ((random.random() - random.random()) * self.ai_change_rate))
        self.temp_forward_ai_values = []
        for val in self.forward_ai_values:
            self.temp_forward_ai_values.append(val * (1 + ((random.random() - random.random()) * self.ai_change_rate)))
        self.forward_ai_values = self.temp_forward_ai_values

        self.right_ai_requirement *= (1 + ((random.random() - random.random()) * self.ai_change_rate))
        self.temp_right_ai_values = []
        for val in self.right_ai_values:
            self.temp_right_ai_values.append(val * (1 + ((random.random() - random.random()) * self.ai_change_rate)))
        self.right_ai_values = self.temp_right_ai_values

        self.left_ai_requirement *= (1 + ((random.random() - random.random()) * self.ai_change_rate))
        self.temp_left_ai_values = []
        for val in self.left_ai_values:
            self.temp_left_ai_values.append(val * (1 + ((random.random() - random.random()) * self.ai_change_rate)))
        self.left_ai_values = self.temp_left_ai_values

        self.time = g_time
        self.x = sw // 4
        self.y = sh // 4
        self.angle = start_angle  # set 0?
        self.update_maths()

        self.reward = 0
        self.current_checkpoint = 0
        self.derut = False
        self.alive = True

    def give_life(self):
        self.time = g_time
        self.x = sw // 4
        self.y = sh // 4
        self.angle = start_angle  # set 0?
        self.update_maths()

        self.reward = 0
        self.current_checkpoint = 0
        self.derut = False
        self.alive = True

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
        if type(track_in) == type(checkpoints[0]):
            temp_num = 0
        elif type(track_in) == type(smol_barrier):
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
        self.max_distance = self.distance

    def update_distance(self, car_in):
        self.cosine = math.cos(math.radians(car_in.angle + self.direction))
        self.sine = math.sin(math.radians(car_in.angle + self.direction))
        self.x = car_in.x
        self.y = car_in.y

        self.distance = 0
        self.move()
        if self.distance > self.max_distance:
            self.max_distance = self.distance
        return self.max_distance - self.distance + 1

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

class CheckPoint(object):
    def __init__(self, location, orientation, name, color):
        self.x, self.y = location
        self.name = name
        self.color = color
        if orientation == 1:
            self.w = 10
            self.h = 65
        elif orientation == 2:
            self.w = 10
            self.h = 75
        elif orientation == 0:
            self.w = 65
            self.h = 10

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))




def redraw_game_window():
    win.fill((0, 180, 0))

    smol_boundary.draw(win)
    big_boundary.draw(win)
    smol_barrier.draw(win)
    big_barrier.draw(win)

    for cp in checkpoints:
        cp.draw(win)

    big_id = 0
    biggest_reward = -1
    for c in cars:
        if biggest_reward < c.reward:
            biggest_reward = c.reward
            big_id = c.id

    for c in cars:
        if c.id == big_id:

            for l in c.distance_checkers:
                l.draw(win)
            c.draw(win)


    pg.display.update()


checkpoints = []
checkpoints.append(CheckPoint((320,140), 1, 0, (83, 28, 195)))
checkpoints.append(CheckPoint((386,140), 0, 1, (83, 28, 195)))
checkpoints.append(CheckPoint((406,120), 0, 2, (83, 28, 195)))
checkpoints.append(CheckPoint((506,35), 2, 3, (83, 28, 195)))
checkpoints.append(CheckPoint((706,35), 2, 4, (83, 28, 195)))
checkpoints.append(CheckPoint((860,145), 0, 5, (83, 28, 195)))
checkpoints.append(CheckPoint((860,545), 0, 6, (83, 28, 195)))
checkpoints.append(CheckPoint((400,580), 0, 7, (83, 28, 195)))
checkpoints.append(CheckPoint((350,495), 1, 8, (83, 28, 195)))
checkpoints.append(CheckPoint((21,295), 0, 9, (83, 28, 195)))


cars = []
car_amount = 80
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






    if len(dead_cars) == len(cars) :

        temp_car_vec = []
        for c in dead_cars:

            big_id1 = 0
            biggest_reward1 = -1
            for c in dead_cars:
                if biggest_reward1 < c.reward:
                    biggest_reward1 = c.reward
                    big_id1 = c.id

            best_car_vec = []
            for c in dead_cars:
                if biggest_reward1 == c.reward:
                    best_car_vec.append(c)

        cars = []
        for c in dead_cars:
            if c.id == big_id1:
                c.give_life()
                cars.append(c)
            else:
                c.change_ai_values(random.choice(best_car_vec))
                cars.append(c)



        dead_cars = []
        generation += 1
        print("generation: " + str(generation) + " and best score: " + str(biggest_reward1))



    for c in cars:
        if c.alive:
            c.move()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            for c in cars:
                print(str(c.left_ai_values) +  ' <lav '  + str(c.left_ai_requirement) +  ' <lar '  + str(c.right_ai_values) +  ' <rav '  + str(c.right_ai_requirement) +  ' <rar ' )
            running = False


    redraw_game_window()

