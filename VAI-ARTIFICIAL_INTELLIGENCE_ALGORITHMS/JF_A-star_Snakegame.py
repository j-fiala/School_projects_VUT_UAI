import pygame
import random

import heapq
import numpy as np

# Colors definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Initial setup for game
fps = 60
blocksize = 20
h_number = 40
w_number = 30


pygame.init()
dis = pygame.display.set_mode((blocksize * h_number, blocksize * w_number))
pygame.display.set_caption("Snake Game with A-STAR alg - made by Jan Fiala")
clock = pygame.time.Clock()

#init fonts
font_style = pygame.font.SysFont("Arial", 25)
score_font = pygame.font.SysFont("Arial", 25)
menu_font = pygame.font.SysFont("Arial", 40)
quit_font = pygame.font.SysFont("Arial", 15)

# Define a node class with position and attributes for parent, g, h, and f values
class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0  # cost from start to current node
        self.h = 0  # heuristic cost from current node to goal
        self.f = 0  # total cost of the node (g + h)

    # Define a comparison method for the priority queue
    def __lt__(self, other):
        return self.f < other.f

# Define the A* algorithm
def a_star(start, goal, obstacles, blocksize, h_number, w_number):
    # Initialize the visited set, cost dictionary, frontier priority queue, and parent dictionary
    
    visited = set()
    cost = {tuple(start): 0}
    frontier = []
    heapq.heappush(frontier, (0, Node(start)))
    parent = {}

    # Loop until the frontier is empty
    while frontier:
        # Pop the node with the lowest f value from the frontier
        current = heapq.heappop(frontier)[1]

        # If the current node is the goal, construct the path and return it
        if np.allclose(current.pos, goal):
            path = []
            while current in parent:
                path.append(current.pos)
                current = parent[current]
            return path[::-1]

        # Add the current node to the visited set
        visited.add(tuple(current.pos))

        # Generate the neighbors of the current node
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbor_pos = np.array(current.pos) + np.array([dx*blocksize, dy*blocksize])
            np.reshape(neighbor_pos,[2])
            neighbor_pos = np.array(neighbor_pos)
            
            # Check if the neighbor is not an obstacle and is within the bounds of the grid
            if (not any(np.array_equal(neighbor_pos, x) for x in obstacles)) and (
                0 < neighbor_pos[0] < h_number*blocksize) and 0 < (neighbor_pos[1] < w_number*blocksize):
                
                neighbor = Node(neighbor_pos, current)
                
                # Calculate the tentative cost from the start to the neighbor
                tentative_cost = cost[tuple(current.pos)] + 1

                # If the neighbor has not been visited or the tentative cost is lower than its previous cost, 
                # update its cost and add it to the frontier
                if tuple(neighbor.pos) not in cost or tentative_cost < cost[tuple(neighbor.pos)]:
                    cost[tuple(neighbor.pos)] = tentative_cost
                    parent[neighbor] = current
                    neighbor.h = np.linalg.norm(neighbor.pos - goal)
                    neighbor.f = tentative_cost + neighbor.h
                    if tuple(neighbor.pos) not in visited:
                        heapq.heappush(frontier, (neighbor.f, neighbor))

    # If the goal cannot be reached, return None
    return None


# Functions
def Your_score(score):
    value = score_font.render("Score: " + str(score), True, green)
    dis.blit(value, [0, 0])

    mesg = quit_font.render("To QUIT press Q", True, red)
    dis.blit(mesg, [0, 25])

def our_snake(blocksize, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], blocksize, blocksize])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [blocksize * h_number / 6, blocksize * w_number / 4])

# Function to generate obstacles
def generate_obstacles(num_obstacles):
    obstacles = []
    
    # Random obstacles based on number
    for i in range(1, num_obstacles + 1):
        lo = random.randrange(1, h_number - 1)*blocksize, random.randrange(
            1, w_number - 1)*blocksize  # last obstacle
        obstacles.append(lo)
        for j in range(1, random.randint(1, int(num_obstacles / 2))):
            if random.randint(1, 2) == 1:
                lo = (lo[0] + blocksize, lo[1])
            else:
                lo = (lo[0], lo[1] + blocksize)
            if 0 < lo[0] <= h_number*blocksize and 0 < lo[1] <= w_number*blocksize:
                obstacles.append(lo)
    return obstacles

def menu_message():
    mesg = menu_font.render("Menu", True, green)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (4*blocksize)))
    dis.blit(mesg, text_rect)

    mesg = font_style.render("Press H for Human player", True, white)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (blocksize * w_number / 2) - blocksize))
    dis.blit(mesg, text_rect)

    mesg = font_style.render("Press C for Computer player", True, white)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (blocksize * w_number / 2) + blocksize))
    dis.blit(mesg, text_rect)

    mesg = font_style.render("To QUIT press Q", True, white)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (blocksize * w_number / 2) + (10*blocksize)))
    dis.blit(mesg, text_rect)

def gameover_message():
    mesg = menu_font.render("GAME OVER", True, red)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (blocksize * w_number / 2) - (10*blocksize)))
    dis.blit(mesg, text_rect)

    mesg = font_style.render("Play again? - press C", True, white)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (blocksize * w_number / 2)))
    dis.blit(mesg, text_rect)

    mesg = font_style.render("To QUIT press Q", True, white)
    text_rect = mesg.get_rect(center=((blocksize * h_number / 2), (blocksize * w_number / 2) + (10*blocksize)))
    dis.blit(mesg, text_rect)

# Gameloop
def gameLoop():
    # Game init variables
    game_over = False
    game_close = False
    selected_mode = False
    food_finded = False
    obstacles = generate_obstacles(17)
    snake_List = []
    Length_of_snake = 1

    # Spawn position
    x1 = (blocksize * h_number) / 2
    y1 = (blocksize * w_number) / 2

    # Idle
    x1_change = 0
    y1_change = 0

    while selected_mode is False:
            # menu
            dis.fill(black)
            menu_message()
            pygame.display.update()

            for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_over = True
                            selected_mode = True
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_h:
                                gamemode = 1
                                snake_speed = 25
                            if event.key == pygame.K_c:
                                gamemode = 2
                                snake_speed = 100
                            selected_mode = True

    # Spawn first food
    while True:
        foodx = round(random.randrange(1, h_number - 1))*blocksize
        foody = round(random.randrange(1, w_number - 1))*blocksize
        if not all(elem in (obstacles) for elem in [(foodx,foody)]):
            break
    
    while not game_over:
        clock.tick(fps)
        
        # Game closed window
        while game_close == True:
            dis.fill(black)
            gameover_message()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Human player
        if gamemode == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change != blocksize:
                        x1_change = -blocksize
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change != -blocksize:
                        x1_change = blocksize
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change != blocksize:
                        y1_change = -blocksize
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change != -blocksize:
                        y1_change = blocksize
                        x1_change = 0

            if (
                x1 >= (blocksize * h_number) - 1
                or x1 < 0
                or y1 >= (blocksize * w_number)
                or y1 < 0
                or all(elem in obstacles for elem in [(x1, y1)])
            ):
                game_close = True

            x1 += x1_change
            y1 += y1_change
            dis.fill(black)

            pygame.draw.rect(
                dis, red, [foodx, foody, blocksize, blocksize]
            )
             
            for obstacle in obstacles:
                pygame.draw.rect(
                    dis,
                    white,
                    (
                        obstacle[0],
                        obstacle[1],
                        blocksize,
                        blocksize,
                    ),
                )


            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)

            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(blocksize, snake_List)
            Your_score(Length_of_snake - 1)

            pygame.display.update()

        # Computer game
        if gamemode == 2:
                            
            # Find the path from start to goal using A*
            if food_finded == False:
                start = np.array([x1, y1])
                goal = np.array([foodx, foody])
                # snake_List = np.array(snake_List[0:-1])/blocksize
                all_obstacles = np.array(obstacles)
                if snake_List != [] and len(snake_List) > 1:
                    snake_List2 = np.array(snake_List[:-1])
                    all_obstacles = np.vstack([all_obstacles,snake_List2]) 
                index = 0
                path = a_star(start, goal, all_obstacles, blocksize, h_number, w_number)
               
                if path is not None:
                    food_finded = True
                else:
                    game_close = True

            if path is not None:
                selectedpath = path[index]
            x1 = selectedpath[0]
            y1 = selectedpath[1]
            index +=1
            
            if (
                x1 >= (blocksize * h_number) - 1
                or x1 < 0
                or y1 >= (blocksize * w_number)
                or y1 < 0
            ):
                game_close = True
            
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_close = True


            dis.fill(black)

            pygame.draw.rect(
                dis, red, [foodx, foody, blocksize, blocksize]
            )
            
            for obstacle in obstacles:
                pygame.draw.rect(
                    dis,
                    white,
                    (
                        obstacle[0],
                        obstacle[1],
                        blocksize,
                        blocksize,
                    ),
                )
           
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)

            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(blocksize, snake_List)
            Your_score(Length_of_snake - 1)

            pygame.display.update()

        # Generationd of new food
        if x1 == foodx and y1 == foody:
            while True:
                food_finded = False
                foodx = round(random.randrange(1, h_number - 1))*blocksize
                foody = round(random.randrange(1, w_number - 1))*blocksize
                if not all(elem in (obstacles) for elem in [(foodx,foody)]) and not all(elem in (snake_List) for elem in [[foodx,foody]]):
                    break
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()
gameLoop()