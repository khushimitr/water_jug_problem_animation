# A Water Jug Problem: You are given two jugs, a 4-gallon one and a 3-gallon one,
# a pump which has unlimited water #which you can use to fill the jug,
# and the ground on which water may be poured. Neither jug has any measuring markings on it.
# How #can you get #exactly 2 gallons of water in the 4-gallon jug?
import copy
from queue import Queue
import pygame
import sys

# specifying the width and height that jugs animation will take
# "WIN" stores the dimensions of the screen that will open up
WIDTH = 600
HEIGHT = 600
WIN = pygame.display.set_mode((800, 800))

LT = []  # list to take initial arguments from command line
# taking command line arguments given by user
# loop starts from 1 because 1st argument is name of file and then desired inputs are there
for i in range(1, len(sys.argv)):
    LT.append(int(sys.argv[i]))

# setting the caption of pygame window
pygame.display.set_caption("A WATER JUG PROBLEM")

# initializing colours for the project
BLUE = (3, 169, 244)
WHITE = (250, 250, 250)
BLACK = (38, 50, 56)
GREY = (158, 158, 158)

# Main class LEVEL that is responsible for a single unit of water level present in jug
# contains all variable and functions that are related for each level (object)

class LEVEL:
    # init declare all the parameters of the object of LEVEL class
    def __init__(self, row, col, width, height, j):
        # specifies object belongs to which row
        # specifies object belongs to which column
        # gives the actual y co-ordinate of the object on the screen 
        # gives the actual x co-ordinate of the object on the screen 
        # initial color of each object
        # defines the width of each object of LEVEL
        # defines the height of each object of LEVEL

        self.row = row
        self.col = col
        self.y = row * height + 100
        self.x = col * width + 100 + (j*80) - 40
        self.color = WHITE
        self.width = width
        self.height = height

    # get the (x,y) co-ordinates of the current object
    def get_pos(self):
        return (self.x, self.y)

    # changes color of the object to blue indicating level is filled
    def make_filled(self):  
        self.color = BLUE

    # changes color of the object to grey indicating level is possible
    def make_possible(self):
        self.color = GREY

    # responsible for drawing the object with specified color and dimensions on win
    def draw(self, win):  
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))


# function that is responsible for making jug and giving it its level
def make_jug(rows, cols, width, height):
    jug = []  # list for holding objects of class LEVEL present in a particular jug
    
    # integer division (//) to get the width "gap_r" and height "gap_c" of each object of class LEVEL
    gap_r = height // rows 
    gap_c = width // cols

    # creating list of object of class LEVEL
    for i in range(rows):
        jug.append([])  # telling jug that it will be a list of lists i.e. 2D list
        for j in range(cols):
            # created the object for the class LEVEL along with the perimeters
            level = LEVEL(i, j, gap_c, gap_r, j)
            # adding object to the particular jug[i] to which it belongs
            jug[i].append(level)
    return jug  # return the list jug that indicates how many jugs there are and levels associated with each jug

# this function is resposible for creating each object of list jug on the screen
def draw_screen(win, jug, rows, cols, width, height):
    win.fill(WHITE)
    for row in jug:
        for level in row:
            level.draw(win)


# this function checks the validity of the new state
def check_state(q, np, vis, curr_state, par, state):
    # check if new state "np" is present in visited or not
    # if "np" is not present in visited then put "np" in vis and q (queue) for further processing
    # now add the current state in par list and new state in state list for retracing of answer
    if np not in vis:
        q.put(np)
        vis.append(np)
        par.append(curr_state)
        state.append(np)


# this function takes state list, par list, and the final state and gives us an ordered path
# in which the states will be traversed
def backtrack(state, par, f_s):
    path = []
    path.append(f_s)

    # this loop runs till the initial state has not been reached and appends each state in path
    # we find the final state in state list and takes its index
    # and add the state present in par list at index k
    # change the final state to the state that is present at index k in par list
    while f_s != (0, 0):
        k = state.index(f_s)
        path.append(par[k])
        f_s = par[k]
    path.reverse()
    return path


# this function runs main algorithm that takes three paramters i.e. jug1, jug2 and how much is to be measured
def water_jug(jug1, jug2, goal):
    # an object q of queue has been instantiated
    # an empty list "vis[]" to store the states that have been visited
    # an empty list "state[]" that stores the current state and helps retrace the final answer states
    # an empty list "par[]" that stores the parent of the current state that from where this current state has been achieved this also helps in retracing the final answer states

    q = Queue()
    vis = []
    state = []
    par = []

    # "s" indicates starting state and "(0,0)" indicates that both jugs are empty
    # put the starting state in queue to process it
    # adding starting state "s" in visited

    s = (0, 0)
    q.put(s)
    vis.append(s)

    # running till there is a state present in queue which is yet to be explored
    while not q.empty():
        curr_state = q.get()  # get the state at the top of the queue to process it

        # check if the goal has been reached i.e. either jug1 or jug2 has goal state
        # if jug1 has the goal state and if some amount of water is present in jug2
        # then empty jug2 since jug1 has measured the goal amount and create new final state "f_s"
        # add the previous state in parent list and add the currents state in state list for retracing answer
        # repeat the same steps but for opposite jugs

        if curr_state[0] == goal or curr_state[1] == goal:
            if curr_state[0] == goal:
                if curr_state[1] >= 0:
                    f_s = (curr_state[0], 0)
                    par.append(curr_state)
                    state.append((curr_state[0], 0))
            else:
                if curr_state[0] >= 0:
                    f_s = (0, curr_state[1])
                    par.append(curr_state)
                    state.append((0, curr_state[1]))

            # call the backtrack function which fetches the path in which final state has been reached
            # then return the list obtained to the main function
            return backtrack(state, par, f_s)

        # create the new states "np" which can be :
        # 1) fill jug1 keeping the other jug unchanged
        # 2) fill jug2 keeping the other jug unchanged
        # 3) empty jug1 keeping the other jug unchanged
        # 4) empty jug2 keeping the other jug unchanged
        # 5) pour water from jug2 to jug1 to the limit that either jug1 is filled or jug2 gets emptied
        # 6) pour water from jug1 to jug2 to the limit that either jug2 is filled or jug1 gets emptied
        # after each new position is created its validity is being checked by check_state function

        np = (jug1, curr_state[1])
        check_state(q, np, vis, curr_state, par, state)

        np = (curr_state[0], jug2)
        check_state(q, np, vis, curr_state, par, state)

        np = (0, curr_state[1])
        check_state(q, np, vis, curr_state, par, state)

        np = (curr_state[0], 0)
        check_state(q, np, vis, curr_state, par, state)

        fill_jug1 = min(jug1 - curr_state[0], curr_state[1])
        np = (curr_state[0] + fill_jug1, curr_state[1] - fill_jug1)
        check_state(q, np, vis, curr_state, par, state)

        fill_jug2 = min(jug2 - curr_state[1], curr_state[0])
        np = (curr_state[0] - fill_jug2, curr_state[1] + fill_jug2)
        check_state(q, np, vis, curr_state, par, state)

    # if the goal can't be measured then function would have not been returned
    # and thus print IMPOSSIBLE
    print("IMPOSSIBLE")


# this function is resposible for making the jugs filled and empty according to the new state
def work_j(j, c_j, row, col, ROWS, COLS, jug, win, width, height):
    # "curr_time" and "draw_time" are the timers for showing the difference in making the
    # levels filled one by one (blue) and making them empty one by one (grey)
    # pygame has the functionality of getting the seconds elapsed through "get_ticks()" and thus this is used
    curr_time = 0
    draw_time = 0

    # "c_j" denotes the current states of jugs how much filled and how much empty
    # "j" denotes the state the jug has to reach

    # if j is greater than c_j means the water level has to increase and thus make_filled(blue)
    # and draw are called for each row at a time after delay of 100ms

    # now if j is smaller than c_j means that water level has to decrease and thus make_possible(grey)
    # and draw are called for each row at a time after a delay of 100ms

    # note that always [ROWS - row - 1] is used as a index because by default first row is the uppermost level
    # of jug but we need to fill from bottom and thus this mathematical relation has been used to get ith level but from bottom
    if j > c_j:
        row = c_j
        while row < j:
            pygame.display.update()
            if curr_time - draw_time > 100:
                jug[ROWS - row - 1][col].make_filled()
                jug[ROWS - row - 1][col].draw(win)
                draw_time = pygame.time.get_ticks()
                row = row + 1
            curr_time = pygame.time.get_ticks()
    elif j < c_j:
        row = c_j-1
        while row >= j:
            pygame.display.update()
            if curr_time - draw_time > 100:
                jug[ROWS - row - 1][col].make_possible()
                jug[ROWS - row - 1][col].draw(win)
                draw_time = pygame.time.get_ticks()
                row = row - 1
            curr_time = pygame.time.get_ticks()


# this is the main function where all function calls to above fumctions are made
# here all the things start to get together one by one
def main(win, width, height, lt):

    # "cap_j1" denotes the max capacity of jug1, "cap_j2" denotes the max capacity of jug2, "goal" denotes the level to be measured
    # which is stored in lt list that were taken via command line arguments
    cap_j1 = lt[0]
    cap_j2 = lt[1]
    goal = lt[2]

    # initializing pygame by calling "init()" method
    # also making the use of Clock provided by pygame and storing it in "clock" variable
    # creating a "font" variable that stores the style of text to be displayed 
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 32)

    # "ROWS" store the maximum rows that a jug can have on specified window size i.e. 10
    # "COLS" store the maximum jugs that we can have on specified window size i.e. 2
    ROWS = 10
    COLS = 2

    # make_jug will return a list of jugs which contain a list of object of class level  
    jug = make_jug(ROWS, COLS, width, height)

    # "curr_time" and "draw_time" are the timers for showing the difference in making the delay in displaying on screen
    # pygame has the functionality of getting the seconds elapsed through "get_ticks()" and thus this is used
    curr_time = 0
    draw_time = 0

    # "pos1" stores the position of the top level of jug1
    # "pos2" stores the position of the top level of jug2
    # "pos_y" stores the min of y-coordinate from pos1 and pos2
    # these variables are maintained to display the current states of jugs at a specified location
    pos1 = jug[ROWS - cap_j1 - 1][0].get_pos()
    pos2 = jug[ROWS - cap_j2 - 1][1].get_pos()
    pos_y = min(pos1[1], pos2[1])

    # "run" is variable signifying our pygame is running (true)
    # "ended" signify when the whole algorithm has taken place (false)
    run = True
    ended = False
    # this loop will run till "x" is clicked or ended has becone true
    while run:
        # willl draw the whole screen continuously
        # update will reflect the changes on the screen
        draw_screen(win, jug, ROWS, COLS, width, height)
        pygame.display.update()

        # getting the events in pygame and for every event
        for event in pygame.event.get():
            # if user closes the window then make run false and quit the game
            if event.type == pygame.QUIT:
                run = False

            # while ended is true i.e. whole algorithm has run through
            while ended:
                pygame.draw.rect(win, WHITE, (0, 0, 800, pos_y+20))
                pygame.draw.rect(win, WHITE, (0, 700, 800, 100))

                # "jug1" and "jug2" stores the string,display on screen(true) and color
                # needs to render the font so that it can be displayed on the screen
                # "blit()" function is responsible for drawing on screen i,e. takes position and what to display
                # make the jug name along with capacity persist on the screen after algorithm has run through
                jug1 = font.render("JUG 1 : " + str(cap_j1), True, BLACK)
                win.blit(jug1, (130, 720))
                jug2 = font.render("JUG 2 : " + str(cap_j2), True, BLACK)
                win.blit(jug2, (530, 720))

                # make the final state persist on the screen after algorithm has run through
                fill1 = font.render(str(path[-1][0]), True, BLACK)
                win.blit(fill1, (pos1[0] + 150 - 16, pos_y - 20))
                fill2 = font.render(str(path[-1][1]), True, BLACK)
                win.blit(fill2, (pos2[0] + 150 - 16, pos_y - 20))
                pygame.display.update()

                # wait for 3000ms (3s) and make run and ended both false and thus quit the game
                if curr_time - draw_time > 3000:
                    draw_time = pygame.time.get_ticks()
                    ended = False
                    run = False
                curr_time = pygame.time.get_ticks()

            # if some key has been pressed by the user
            if event.type == pygame.KEYDOWN:
                # if that key pressed is space_bar then
                if event.key == pygame.K_SPACE:

                    # call the main algorithm function i.e. water_jug which returns the path of states
                    path = water_jug(cap_j1, cap_j2, goal)

                    # if answer was not found then path would not have been returned and thus check
                    # if answer was impossible and then make run false
                    if path == None:
                        run = False
                        break

                    # print the path i.e. how order of states look like finally
                    print(path)

                    # rendering name of jugs and capacity
                    jug1 = font.render("JUG 1 : " + str(cap_j1), True, BLACK)
                    win.blit(jug1, (130, 720))
                    jug2 = font.render("JUG 2 : " + str(cap_j2), True, BLACK)
                    win.blit(jug2, (530, 720))

                    # show the jug1 and jug2 with the specified capacity on the screen
                    # "row" variable moves from 0 to capacity of each jug
                    # "curr_time" and "draw_time" are the timers for showing the difference in making the
                    # levels one by one
                    # pygame has the functionality of getting the seconds elapsed through "get_ticks()" and thus this is used
                    # make_possible(grey) and draw are called for each row at a time after a delay of 300ms
                    # note that always [ROWS - row - 1] is used as a index because by default first row is the uppermost level
                    # of jug but we need to fill from bottom and thus this mathematical relation has been used

                    row = 0
                    while row < cap_j1:
                        pygame.display.update()
                        if curr_time - draw_time > 300:
                            jug[ROWS - row - 1][0].make_possible()
                            jug[ROWS - row - 1][0].draw(win)
                            draw_time = pygame.time.get_ticks()
                            row = row + 1
                        curr_time = pygame.time.get_ticks()
                    draw_time = 0
                    row = 0
                    while row < cap_j2:
                        pygame.display.update()
                        if curr_time - draw_time > 300:
                            jug[ROWS - row - 1][1].make_possible()
                            jug[ROWS - row - 1][1].draw(win)
                            draw_time = pygame.time.get_ticks()
                            row = row + 1
                        curr_time = pygame.time.get_ticks()
                    
                    # "c_j1" and "c_j2" signify the current levels of jug1 and jug2 respectively
                    c_j1 = 0
                    c_j2 = 0
                    for x in path:
                        # "j1" and "j2" signify the new levels of jug1 and jug2 respectively that needs to be displayed
                        j1 = x[0]
                        j2 = x[1]
                        pygame.draw.rect(
                            win, WHITE, (0, 0, 800, pos_y+20))
                        fill1 = font.render(str(j1), True, BLACK)
                        win.blit(fill1, (pos1[0] + 150 - 16, pos_y - 20))
                        fill2 = font.render(str(j2), True, BLACK)
                        win.blit(fill2, (pos2[0] + 150 - 16, pos_y - 20))
                        pygame.display.update()
                        # work_j is called for showing changes in jug1 and make new state visible
                        work_j(j1, c_j1, row, 0, ROWS,
                               COLS, jug, win, width, height)
                        # work_j is called for showing changes in jug2 and make new state visible
                        work_j(j2, c_j2, row, 1, ROWS,
                               COLS, jug, win, width, height)
                        # updating the current state of both the jugs
                        c_j1 = j1
                        c_j2 = j2

                        # make the changes in state after 1500ms (1.5s) so that changes in state can be observed
                        while True:
                            pygame.display.update()
                            if curr_time - draw_time > 1500:
                                draw_time = pygame.time.get_ticks()
                                break
                            curr_time = pygame.time.get_ticks()
                    # whole algorithm has run through and thus make ended true
                    ended = True
        # tick(144) specifies framerate (fps) and is used to help limit the runtime speed of a game.
        # it is controlling our curr_time and draw_time which is responsible for delay
        clock.tick(144)
    # when run becomes false quit the pygame
    pygame.quit()

# call the main function with the constants specified at the top of the program
main(WIN, WIDTH, HEIGHT, LT)

# how to call this file with specifying command line arguments
# python -u "c:\projects\python\ai\water_jug_anim\water_jug_anim.py" 9 5 6
