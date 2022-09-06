# install pygame with > pip install pygame

# Initializing sudoku game window and variables
import pygame   # pygame library import kortesi
pygame.font.init()

# set_mode display module er akta function jeta diye
# game er jonno window create kora hoy je size mention koire dawa ase
Window = pygame.display.set_mode((500, 500))

# set_caption diye window er opore title show kora hoy
pygame.display.set_caption("SUDOKU GAME")
x = 0
z = 0

# block er size define kora
diff = 500 / 9
value= 0

# nested list er madhome akta default 9X9 grid screen e show korar jonno
defaultgrid =[
        [0, 0, 4, 0, 6, 0, 0, 0, 5],
        [7, 8, 0, 4, 0, 0, 0, 2, 0],
        [0, 0, 2, 6, 0, 1, 0, 7, 8],
        [6, 1, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 7, 5, 4, 0, 0, 6, 1],
        [0, 0, 1, 7, 5, 0, 9, 3, 0],
        [0, 7, 0, 3, 0, 0, 0, 1, 0],
        [0, 4, 0, 2, 0, 6, 0, 0, 7],
        [0, 2, 0, 0, 0, 7, 4, 0, 0],
    ]

# system font diye akta object create hobe
font = pygame.font.SysFont("comicsans", 40) 
font1 = pygame.font.SysFont("comicsans", 20)

# highlight selected cell function
def cord(pos):
    global x
    x = pos[0]//diff
    global z
    z = pos[1]//diff

# aie function er madhome je cell user select korbe oieta highlight hobe
def highlightbox():
    for k in range(2):
        # straight line draw korar function pygame.draw.line() diye
        pygame.draw.line(Window, (0, 0, 0), (x * diff-3, (z + k)*diff), (x * diff + diff + 3, (z + k)*diff), 7)
        pygame.draw.line(Window, (0, 0, 0), ( (x + k)* diff, z * diff ), ((x + k) * diff, z * diff + diff), 7) 

# Function to draw lines for making sudoku grid
def drawlines():
    for i in range (9):
        for j in range (9):
            if defaultgrid[i][j]!= 0:
                
                # rectangle draw korar function
                pygame.draw.rect(Window, (255, 255, 0), (i * diff, j * diff, diff + 1, diff + 1))
                
                # font,render diye font render kora hoy
                text1 = font.render(str(defaultgrid[i][j]), 1, (0, 0, 0))

                # blit() hoche block transfer, mane content ak surface
                # theke arek surface e copy korar jonno lage
                Window.blit(text1, (i * diff + 15, j * diff + 15)) 

    for l in range(10):
        if l % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(Window, (0, 0, 0), (0, l * diff), (500, l * diff), thick)
        pygame.draw.line(Window, (0, 0, 0), (l * diff, 0), (l * diff, 500), thick)

# fillvalue() function diye user er entered number cell e fill kora hoy
def fillvalue(value):
    # value ta text e aieshe store hoy
    text1 = font.render(str(value), 1, (0, 0, 0))
    Window.blit(text1, (x * diff + 15, z * diff + 15))   

pygame.quit()  