import pygame
import math
import copy
import random

dimensions = [1800, 1000]
win = pygame.display.set_mode((dimensions[0], dimensions[1]))
time = 0
root_point = [dimensions[0] / 2, dimensions[1]]


class Branch:
    def __init__(self, parent_branch, angle, start_pos, split_num, branch_spacing=math.pi/6):
        self._parent_branch = parent_branch
        self._child_branches = []
        self._width = 3
        self._length = 0
        self._grow_speed = 1
        self._angle = angle
        self._branch_spacing = branch_spacing
        self._split_num = split_num
        self._start_pos = start_pos
        self._end_pos = copy.copy(start_pos)

    def parent(self):
        return self._parent_branch

    def children(self):
        return self._child_branches

    def start_pos(self):
        return self._start_pos

    def end_pos(self):
        return self._end_pos

    def get_angle(self):
        return self._angle

    def get_width(self):
        return self._width

    def grow(self):
        self._length += self._grow_speed
        self.update_end_pos()

    def update_end_pos(self):
        self._end_pos[0] = self._start_pos[0] + self._length * math.sin(self._angle)
        self._end_pos[1] = self._start_pos[1] - self._length * math.cos(self._angle)

        for child in self._child_branches:
            child.update_end_pos()

    def split(self):
        for i in range(self._split_num):
            angle = self._angle + (-1 * (self._split_num - 1) * self._branch_spacing / 2) + (i * self._branch_spacing)
            self._child_branches.append(Branch(self, angle, self._end_pos, self._split_num, copy.copy(self._branch_spacing)))


def draw_tree(branch):
    draw_branch(branch)
    for child in branch.children():
        draw_tree(child)


def draw_branch(branch):
    pygame.draw.line(win, (0, 150, 150), branch.start_pos(), branch.end_pos(), branch.get_width())


def draw_world():  # Draws the background
    win.fill((100, 200, 100))


def grow_branch(branch, counter):
    if counter == 0:
        branch.grow()
    else:
        for child in branch.children():
            grow_branch(child, counter - 1)


def split_branch(branch, counter):
    if counter == 0:
        branch.split()
    else:
        for child in branch.children():
            split_branch(child, counter - 1)


def main():
    running = True
    global time
    global root_point
    main_stem = Branch(None, 0, root_point, random.randint(2, 8), math.pi/random.randint(2, 8))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_world()
        draw_tree(main_stem)

        step_rate = 10
        split_time = step_rate * 100

        if time % 30  == 0:
            main_stem.grow()

        if time % split_time == 0:
            split_branch(main_stem, time / split_time - 1)

        if time % step_rate == 0:
            grow_branch(main_stem, time // split_time)

        pygame.display.update()
        time += 1


main()
