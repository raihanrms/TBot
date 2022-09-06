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


# Function for raising error when wrong value is entered

# aie raiseerror() ar raiseerror1() madhome error detect kora
# hoy jodi user wrong value enter kore
def raiseerror():
    text1 = font.render("wrong!", 1, (0, 0, 0))
    Window.blit(text1, (20, 570)) 
def raiseerror1():
    text1 = font.render("wrong ! enter a valid key for the game", 1, (0, 0, 0))
    Window.blit(text1, (20, 570)) 

# Function to check if the entered value is valid

# validvalue() check korbe je entered value ki valid naki na
def validvalue(m, k, l, value):

    # range() diye akta sequence start hobe 0 theke and 1 diye
    # increment(barbe) hobe ebong je number dawa ase oiekhane thaime jabe.
    for it in range(9):
        if m[k][it]== value:
            return False
        if m[it][l]== value:
            return False
    it = k//3
    jt = l//3
    for k in range(it * 3, it * 3 + 3):
        for l in range (jt * 3, jt * 3 + 3):
            if m[k][l]== value:
                return False
    return True

# Function to solve sudoku game

# game ta solve korar function
def solvegame(defaultgrid, i, j):

    while defaultgrid[i][j]!= 0:
        if i<8:
            i+= 1
        elif i == 8 and j<8:
            i = 0
            j+= 1
        elif i == 8 and j == 8:
            return True

    # pygame.event.pump() protekta event akta event queue te rakhbe
    pygame.event.pump()   
    for it in range(1, 10):
        if validvalue(defaultgrid, i, j, it)== True:
            defaultgrid[i][j]= it
            global x, z
            x = i
            z = j
            Window.fill((255, 255, 255))
            drawlines()
            highlightbox()
            pygame.display.update()
            pygame.time.delay(20)
            if solvegame(defaultgrid, i, j)== 1:
                return True
            else:
                defaultgrid[i][j]= 0
            Window.fill((0,0,0))
            
            drawlines()
            highlightbox()

            # display update korbe
            pygame.display.update()

            # function ta 50 mili sec er jonno pause hobe
            pygame.time.delay(50)   
    return False 

# Function to show result

# result display kora hobe aie function diye 
def gameresult():
    text1 = font.render("game finished", 1, (0, 0, 0))
    Window.blit(text1, (20, 570)) 

# window run kora hoy flag diye
flag=True  
flag1 = 0
flag2 = 0
rs = 0
error = 0


# rest code

while flag:
    Window.fill((255,182,193))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False   
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            # mouse er position e number enter korar jonno
            pos = pygame.mouse.get_pos()
            cord(pos)
        
        # pygame.KEYDOWN use kora hoy number press korle, number gula enter hobe    
        if event.type == pygame.KEYDOWN:

            # left press korle highlighted box left e move hobe
            if event.key == pygame.K_LEFT:
                x-= 1
                flag1 = 1

            # right press korle highlighted box right e move hobe
            if event.key == pygame.K_RIGHT:
                x+= 1
                flag1 = 1

            # up press korle highlighted box up e move hobe
            if event.key == pygame.K_UP:
                y-= 1
                flag1 = 1
            
            # down press korle highlighted box down e move hobe
            if event.key == pygame.K_DOWN:
                
                y+= 1
                flag1 = 1   
            if event.key == pygame.K_1:
                value = 1
            if event.key == pygame.K_2:
                value = 2   
            if event.key == pygame.K_3:
                value = 3
            if event.key == pygame.K_4:
                value = 4
            if event.key == pygame.K_5:
                value = 5
            if event.key == pygame.K_6:
                value = 6
            if event.key == pygame.K_7:
                value = 7
            if event.key == pygame.K_8:
                value = 8
            if event.key == pygame.K_9:
                value = 9 
            if event.key == pygame.K_RETURN:
                flag2 = 1  
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                defaultgrid=[
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                defaultgrid  =[
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
    if flag2 == 1:
        if solvegame(defaultgrid , 0, 0)== False:
            error = 1
        else:
            rs = 1
        flag2 = 0   
    if value != 0:           
        fillvalue(value)
        if validvalue(defaultgrid , int(x), int(z), value)== True:
            defaultgrid[int(x)][int(z)]= value
            flag1 = 0
        else:
            defaultgrid[int(x)][int(z)]= 0
            raiseerror1()  
        value = 0   

    if error == 1:
        raiseerror() 
    if rs == 1:
        gameresult()       
    drawlines() 
    if flag1 == 1:
        highlightbox()      
    pygame.display.update() 

# game theke ber hoye jawar function
pygame.quit()    