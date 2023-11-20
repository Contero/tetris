import pygame
import random
import numpy as np
import math

pygame.init()
pygame.font.init()
random.seed()

class Display:
    # Constructor, initializes screen
    def __init__(self, block_size):
        self.grey = pygame.Color(128, 128, 128)
        self.white = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)
        self.font = pygame.font.SysFont('Ariel Black', block_size, False, False)
        self.font_big = pygame.font.SysFont('Ariel Black', 2 * block_size, False, False)
        self.square_size = block_size - 1
        self.block_size = block_size
        self.screen_width = block_size * 23
        self.screen_height = block_size * 22
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.draw_hud()
        pygame.display.set_caption('Tetris')
        
    # Draws the HUD frames
    # Accepts: the block size
    def draw_hud(self):
        # calculate frame 
        frame_right = (self.block_size * 12 - self.block_size, self.block_size, self.block_size, self.screen_height)
        frame_bottom = (0, self.screen_height - self.block_size, self.screen_width, self.block_size)
        far_right = (self.block_size * 23 - self.block_size, self.block_size, self.block_size, self.screen_height)
        
        # main window frame
        pygame.draw.rect(self.screen, self.grey, (0, 0, self.screen_width, self.block_size)) #top
        pygame.draw.rect(self.screen, self.grey, frame_bottom) #bottom
        pygame.draw.rect(self.screen, self.grey, (0, self.block_size, self.block_size, self.screen_height)) #left
        pygame.draw.rect(self.screen, self.grey, frame_right) #right
        pygame.draw.rect(self.screen, self.grey, far_right) #far right
        
        # preview frame
        pygame.draw.rect(self.screen, self.grey, (13 * self.block_size, 2 * self.block_size, 8 * self.block_size, self.block_size / 2)) #top
        pygame.draw.rect(self.screen, self.grey, (13 * self.block_size, math.ceil(7.5 * self.block_size), 8*  self.block_size, math.ceil(self.block_size / 2))) #bottom
        pygame.draw.rect(self.screen, self.grey, (13 * self.block_size, 2 * self.block_size, self.block_size / 2, 6 * self.block_size)) #left
        pygame.draw.rect(self.screen, self.grey, (math.ceil(20.5 * self.block_size), 2 * self.block_size, self.block_size / 2, 6 * self.block_size)) #right
        next_label = self.font.render('Next Piece:', False, self.white)
        self.screen.blit(next_label, (14 * self.block_size, 3 * self.block_size))
        
        # score frame
        pygame.draw.rect(self.screen, self.grey, (13 * self.block_size, 9 * self.block_size, 8 * self.block_size, math.ceil(self.block_size / 2))) #top
        pygame.draw.rect(self.screen, self.grey, (13 * self.block_size, 19.5 * self.block_size, 8 * self.block_size, math.ceil(self.block_size / 2))) #bottom
        pygame.draw.rect(self.screen, self.grey, (13 * self.block_size, 9.5 * self.block_size, math.ceil(self.block_size / 2), 10 * self.block_size)) #left
        pygame.draw.rect(self.screen, self.grey, (20.5 * self.block_size, 9.5 * self.block_size, math.ceil(self.block_size / 2), 10 * self.block_size)) #right
        
        # Text labels
        self.screen.blit(self.font.render('Level:', False, self.white), (14 * self.block_size, 10 * self.block_size))
        self.screen.blit(self.font.render('Lines:', False, self.white), (14 * self.block_size, 13 * self.block_size))
        self.screen.blit(self.font.render('Score:', False, self.white), (14 * self.block_size, 16 * self.block_size))
        self.screen.blit(self.font.render('[P] for pause/help menu', False, self.white), (13 * self.block_size, 20 * self.block_size))
    
    # Draws a shape at the given coordinates
    # Accepts: the shape array, the coordinates, flag for ghost color, flag if coordinates are on playfield and require offset
    def draw_shape(self, shape, coords, is_ghost, offset):
        color = -1
        
        if offset:
            coords = (coords[0] - 1, coords[1] + 1)
            
        for row in range(len(shape)):
            if row + coords[0] < 1:
                continue
            for col in range(len(shape[row])):
                if shape[row][col] > 0:
                    if color == -1 and is_ghost:
                        color = self.get_ghost_color(shape[row][col])
                    elif color == -1:
                        color = self.get_color(shape[row][col])
                    pygame.draw.rect(self.screen, color, ((col+coords[1]) * self.block_size + 1,(row +coords[0]) * self.block_size + 1, self.square_size, self.square_size)) 
    
    # Paints the screen
    # Accepts: the game state object
    def paint(self, game_state):
        self.paint_field(game_state.field, False)

        pygame.draw.rect(self.screen, self.black, (15 * self.block_size, 4 * self.block_size, 4 * self.block_size, 3 *self.block_size))
        
        if game_state.show_ghost:
            self.draw_shape(game_state.active_shape, game_state.ghost_coords, True, True)
            
        self.draw_shape(game_state.active_shape, game_state.active_coords, False, True)
        
              
        if game_state.show_next:
            # center it
            cols = len(game_state.next_shape[0])
            if cols == 2:
                next_coords = (4.5, 16)
            elif cols == 3:
                next_coords = (4.5, 15.5)
            else:
                next_coords = (4, 15)
            self.draw_shape(game_state.next_shape, next_coords, False, False)
            
        pygame.display.update()

    # paints the pieces at rest_piece
    # Accepts: the field array, a flag indicating if the display should flip after buffer is updated
    def paint_field(self, field, update):
        pygame.draw.rect(self.screen, self.black,(self.block_size, self.block_size, self.block_size*10, self.block_size*20))
        
        for row in range(2, len(field)):
            for col in range(len(field[row])):
                if field[row][col] > 0:
                    pygame.draw.rect(self.screen, self.get_color(field[row][col]), (col*self.block_size+1+self.block_size, (row - 2)*self.block_size+1+self.block_size, self.square_size, self.square_size))
                    
        if update:
            pygame.display.update()

    def set_level_display(self, level):
        pygame.draw.rect(self.screen, self.black,(self.block_size * 14, self.block_size * 11, self.block_size*6, self.block_size*2))
        self.write_right(str(level), (11,20))
    
    def set_score_display(self, score):
        pygame.draw.rect(self.screen, self.black,(self.block_size * 14, self.block_size * 17, self.block_size*6, self.block_size*2))
        self.write_right(str(score), (17,20))
    
    def set_lines_display(self, lines):
        pygame.draw.rect(self.screen, self.black,(self.block_size * 14, self.block_size * 14, self.block_size*6, self.block_size*2))
        self.write_right(str(lines), (14,20))
        
    def write_right(self, text, coords):
        text_obj = self.font_big.render(str(text), False, self.white)
        width = text_obj.get_width()
        self.screen.blit(text_obj, (coords[1] * self.block_size - width, coords[0] * self.block_size))
        
    def get_color(self, id):
        if id == 1:
            return pygame.Color(0,255,255)
        elif id == 2:
            return pygame.Color(255,255,0)
        elif id == 3:
            return pygame.Color(128,0,128)    
        elif id == 4:
            return pygame.Color(0,128,0)
        elif id == 5:
            return pygame.Color(255,0,0)
        elif id == 6:
            return pygame.Color(0,0,255)
        elif id == 7:
            return pygame.Color(255,165,0)
        elif id == 9:
            return pygame.Color(255,255,255)
        
    def get_ghost_color(self, id):
        if id == 1:
            return pygame.Color(0,77,77)
        elif id == 2:
            return pygame.Color(77,77,0)
        elif id == 3:
            return pygame.Color(50,0,50)    
        elif id == 4:
            return pygame.Color(0,50,0)
        elif id == 5:
            return pygame.Color(77,0,0)
        elif id == 6:
            return pygame.Color(0,0,77)
        elif id == 7:
            return pygame.Color(77,50,0)
            
    def show_game_over(self):
        pygame.draw.rect(self.screen, pygame.Color(100,200,100), (1.5 * self.block_size,1.5 * self.block_size, 9 * self.block_size, 4.5  * self.block_size))
        self.screen.blit(self.font_big.render("Game Over!", False, self.white), (2 * self.block_size, 2 * self.block_size))
        self.screen.blit(self.font.render("Space to Play Again", False, self.white), (3 * self.block_size, 4 * self.block_size))
        self.screen.blit(self.font.render("Esc to exit", False, self.white), (4 * self.block_size, 5 * self.block_size))
        pygame.display.update()
        
    def show_pause(self):
        pygame.draw.rect(self.screen, pygame.Color(100,200,100), (1.5 * self.block_size,1.5 * self.block_size, 9 * self.block_size, 12  * self.block_size))
        self.screen.blit(self.font_big.render("Paused!", False, self.white), (3 * self.block_size, 2 * self.block_size))
        self.screen.blit(self.font.render("Controls:", False, self.white), (1.75 * self.block_size, 4 * self.block_size))
        self.screen.blit(self.font.render("Left arrow: move left", False, self.white), (1.75 * self.block_size, 5 * self.block_size))
        self.screen.blit(self.font.render("Right arrow: Move right", False, self.white), (1.75 * self.block_size, 6 * self.block_size))
        self.screen.blit(self.font.render("Up arrow: rotate piece", False, self.white), (1.75 * self.block_size, 7 * self.block_size))
        self.screen.blit(self.font.render("Down arrow: Fast drop", False, self.white), (1.75 * self.block_size, 8 * self.block_size))
        self.screen.blit(self.font.render("Esc: Quit", False, self.white), (1.75 * self.block_size, 9 * self.block_size))
        self.screen.blit(self.font.render("G: Show/hide ghost piece", False, self.white), (1.75 * self.block_size, 10 * self.block_size))
        self.screen.blit(self.font.render("N: Show/hide next piece", False, self.white), (1.75 * self.block_size, 11 * self.block_size))
        self.screen.blit(self.font.render("P: Pause/Help", False, self.white), (1.75 * self.block_size, 12 * self.block_size))
        pygame.display.update()
    
class GameManager:
    def __init__(self, display):
        self.show_ghost = True
        self.show_next = True
        self.display = display
        self.new_game()
        
    def new_game(self):
        self.lines = 0
        self.level = 1
        self.score = 0
        self.game_speed = 500
        self.tick = self.game_speed
        self.field = np.zeros((22,10))
        self.bag = []
        self.bag2 = []
        self.active_shape = []
        self.next = []
        self.active_coords = (0,0)
        self.display.set_level_display(1)
        self.display.set_score_display(0)
        self.display.set_lines_display(0)
        self.to_clear = []
    
    def init_bag(self):
        new_bag = []
        for i in range(1,8):
            new_bag.append(i)
        random.shuffle(new_bag)
        return new_bag
    
    def next_piece(self):
        if len(self.bag) > 0:
            return self.bag[len(self.bag) - 1]
        return self.bag2[6]
        
    def increase_score(self, points):
        self.score += points
        self.display.set_score_display(self.score)
        
    def increase_lines(self, lines):
        self.lines += lines
        self.display.set_lines_display(self.lines)
   
# Updates game state object with the next piece to be played
# Accepts: the game state object
# returns: a boolean indicating whether a new piece will fit on the board
def get_new_piece(game_manager):
    if len(game_manager.bag2) == 0:
        game_manager.bag2 = game_manager.init_bag()
    if len(game_manager.bag) == 0:
        game_manager.bag = game_manager.bag2
        game_manager.bag2 = game_manager.init_bag()
        
    id = game_manager.bag.pop()
    game_manager.active_shape = get_shape(id)
    game_manager.next_shape = get_shape(game_manager.next_piece())
    if len(game_manager.active_shape[0]) == 2:
        game_manager.active_coords = (0,4)
    else:
        game_manager.active_coords = (0,3)
    if not check_fit(game_manager, game_manager.active_shape, game_manager.active_coords):
        return False

    return True

# Gets an array cooresponding to the id
# Accepts: an id
# Returns: The array
def get_shape(id):
    if id == 1:
        return np.array([[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]])
    if id == 2:
        return np.array([[2,2],[2,2]])
    if id == 3:
        return np.array([[0,3,0],[3,3,3],[0,0,0]])
    if id == 4:
        return np.array([[0,4,4],[4,4,0],[0,0,0]])
    if id == 5:
        return np.array([[5,5,0],[0,5,5],[0,0,0]])
    if id == 6:
        return np.array([[6,0,0],[6,6,6],[0,0,0]])
    if id == 7:
        return np.array([[0,0,7],[7,7,7],[0,0,0]])

# Checks to see if a shape will fit at a coordinates
# Accepts: The game state object, the shape array, the coordinates to check
# Returns: A Boolean indicating if the shape will fit
def check_fit(game_manager, shape, new_coords):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] > 0 and (row + new_coords[0] >= 22 or col + new_coords[1] >=10 or col + new_coords[1] < 0 or game_manager.field[row + new_coords[0]][col + new_coords[1]] != 0):
                return False
    return True

# Tries to move a piece in the given direction
# Accepts: dir: the direction, game_manager: the game state object
# Returns: A boolean indicating if the move was succsessful
def try_move(dir, game_manager):
    if dir == 'd':
        new_coords = (game_manager.active_coords[0] + 1, game_manager.active_coords[1])
    elif dir == 'l':
        new_coords = (game_manager.active_coords[0], game_manager.active_coords[1] - 1)
    elif dir == 'r':
        new_coords = (game_manager.active_coords[0], game_manager.active_coords[1] + 1)
    if check_fit(game_manager, game_manager.active_shape, new_coords):
        game_manager.active_coords = new_coords
        return True
    return False

# Finds the location for displaying ghost shapes
# Accepts: game_manager: the game state object
# Returns: a tuple with (row, column) coordinates
def find_ghost_coords(game_manager):
    coords = game_manager.active_coords
    next = (game_manager.active_coords[0] + 1, game_manager.active_coords[1])   
    while len(game_manager.active_shape) > 0 and check_fit(game_manager, game_manager.active_shape, next):
        coords = next
        next = (coords[0] + 1, coords[1])
    return coords

# Attemps to rotate the active piece, will fail if the rotated shape will not fit at current coords   
# Accepts: the game state object 
def try_rotate(game_manager):
    test = np.rot90(game_manager.active_shape, 3)
    
    if check_fit(game_manager, test, game_manager.active_coords):
        game_manager.active_shape = test
        return
    
    #kick left
    test_coords = (game_manager.active_coords[0], game_manager.active_coords[1] - 1)
    if check_fit(game_manager, test, test_coords):
        game_manager.active_shape = test
        game_manager.active_coords = test_coords
        return
    
    #kick right
    
    test_coords = (game_manager.active_coords[0], game_manager.active_coords[1] + 1) 
    if check_fit(game_manager, test, test_coords):
        game_manager.active_shape = test
        game_manager.active_coords = test_coords
        return
    
# Rests the active piece
# Accepts: the game state object
def rest_piece(game_manager):
    for row in range(len(game_manager.active_shape)):
            for col in range(len(game_manager.active_shape[row])):
                if game_manager.active_shape[row][col] > 0:
                    game_manager.field[game_manager.active_coords[0] + row][game_manager.active_coords[1] + col] = game_manager.active_shape[row][col]
    game_manager.tick = game_manager.game_speed
    
def check_lines(game_manager):
    start_row = game_manager.active_coords[0] + 1
    end_row = game_manager.active_coords[0] + len(game_manager.active_shape)
    
    game_manager.active_shape = []
        
    for row in range(start_row - 1, end_row):
        if row < 22 and not 0 in game_manager.field[row]:
            game_manager.to_clear.append(row)
    
def clear_lines(game_manager):
    if len(game_manager.to_clear) > 0:
        for row in range(max(game_manager.to_clear),min(game_manager.to_clear) - 1, -1):
            if row in game_manager.to_clear:
                game_manager.field[row] = 9
        game_manager.display.paint_field(game_manager.field, True)
        pygame.time.wait(100)
        
        for row in range(max(game_manager.to_clear),min(game_manager.to_clear) - 1, -1):
            if row in game_manager.to_clear:
                game_manager.field[row] = 0
                
        game_manager.display.paint_field(game_manager.field, True)
        pygame.time.wait(100)
    
        next_row = max(game_manager.to_clear) - 1
        for row in range(max(game_manager.to_clear), -1, -1):
            if row - len(game_manager.to_clear) < 0:
                game_manager.field[row] = np.zeros(10)
            else: 
                if next_row < 0:
                    game_manager.field[row] = np.zeros(10)
                else:
                    while sum(game_manager.field[next_row]) == 0:
                        next_row = next_row - 1
                    if next_row < 0:
                        game_manager.field[row] = np.zeros(10)
                    else:
                        game_manager.field[row] = game_manager.field[next_row]
                        next_row = next_row - 1
    
def main():
    block_size = 35
    display = Display(block_size)
    game_manager = GameManager(display)
    done = False
    alive = True
    shape_in_play = False
    last_time = pygame.time.get_ticks()
    paused = False
    
    while not done:
        if alive and not paused:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True
                elif event.type == pygame.KEYDOWN and shape_in_play:
                    if event.key == pygame.K_LEFT:
                        try_move('l', game_manager)
                    if event.key == pygame.K_RIGHT:
                        try_move('r', game_manager)
                    if event.key == pygame.K_UP:
                        try_rotate(game_manager)
                    if event.key == pygame.K_DOWN:
                        game_manager.tick = 50
                    if event.key == pygame.K_g:
                        game_manager.show_ghost = not game_manager.show_ghost
                    if event.key == pygame.K_n:
                        game_manager.show_next = not game_manager.show_next
                    if event.key == pygame.K_p:
                        paused = not paused
            if not shape_in_play:
                if not get_new_piece(game_manager):
                    alive = False
                shape_in_play = True
            elif current_time - last_time >= game_manager.tick:
                if not try_move('d', game_manager):
                    rest_piece(game_manager)
                    check_lines(game_manager)
                    if len(game_manager.to_clear) > 0:
                        clear_lines(game_manager)
                        multiplier = 1
                        if len(game_manager.to_clear) == 2:
                            multiplier = 3
                        elif len(game_manager.to_clear) == 3:
                            multiplier = 5
                        elif len(game_manager.to_clear) == 4:
                            multiplier = 8
                        game_manager.increase_score(game_manager.level * 100 * multiplier)
                        game_manager.increase_lines(len(game_manager.to_clear))
                        game_manager.to_clear = []
                        if game_manager.level <= game_manager.lines / 10:
                            game_manager.level += 1
                            game_manager.game_speed -= 25
                            game_manager.tick = game_manager.game_speed
                            display.set_level_display(game_manager.level)
                    shape_in_play = False
                last_time = current_time
            if game_manager.show_ghost:
                game_manager.ghost_coords = find_ghost_coords(game_manager)
            display.paint(game_manager)
        elif not alive:
            display.show_game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_manager.new_game()
                        alive = True
                        shape_in_play = False
        else:
            display.show_pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
main()
