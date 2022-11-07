'''Buttons: 
r - random cells
0 - empty grid 
[space] - play/pause 
'''

import datetime
import time 
import pygame 
import numpy as np

#colors
COL_BACK = (10, 10, 10)
COL_GRID = (50, 50, 50)
COL_WILL_DIE  = (150, 150, 150) 
COL_WILL_SPAWN = (255, 255, 255)

COL_META_DATA = (200, 200, 255)

#Dimensiopns:
SIZE_CELL = 20

#initial positions
START_EMPTY=np.zeros((60,80))

def update(console, cells, size, will_update=False):
    next_cells=np.zeros((cells.shape[0], cells.shape[1]))

    for r,c in np.ndindex(cells.shape):
        neighbors = np.sum(cells[r-1:r+2, c-1:c+2]) - cells[r,c]
        color = COL_BACK if cells[r, c] == 0 else COL_WILL_SPAWN

        #living cells
        if cells[r,c]==1:
            if neighbors < 2 or neighbors > 3:
                if will_update:
                    color = COL_WILL_DIE
                

            elif neighbors>=2 or neighbors <=3: 
                next_cells[r,c]=1
                if will_update:
                    color = COL_WILL_SPAWN
            

        #dead cells
        else:
            if neighbors == 3:
                next_cells[r,c]=1
                if will_update:
                    color=COL_WILL_SPAWN

        pygame.draw.rect(console, color, (c*size, r*size, size-1, size-1))
    
    #data
    cur_pop=np.sum(cells)
    next_pop=np.sum(next_cells)
    delta_pop=next_pop-cur_pop
    data_str="Population: "+str(next_pop)+" (Δ: "+str(delta_pop)+")"

    pygame.display.set_caption(data_str)
    return next_cells
    

    pygame.display.set_caption(data_str)

def main(sleep=0):
    pygame.init()
    console = pygame.display.set_mode((800,600))    #default screen size

    cells = START_EMPTY                     #flip shape for some reason 
    console.fill(COL_GRID)
    update(console, cells, SIZE_CELL)

    iterations=0
    data_str = "Config: "+"sleep="+str(sleep)+" | "+"size="+str(pygame.display.get_window_size())+" | (max_cells="+str(cells.shape[0]*cells.shape[1])
    #pygame.display.set_caption(data_str)
    pygame.display.flip()
    pygame.display.update()
    pygame.display.set_caption(data_str)

    font=pygame.font.Font('freesansbold.ttf', 12)
    

    run_game=False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_game = not run_game                  #negate run 
                    update(console, cells, SIZE_CELL)
                    pygame.display.update()

                if event.key == pygame.K_r: 
                    cells=np.random.randint(2,size=(60,80))
                    update(console, cells, SIZE_CELL)
                    pygame.display.update()

                if event.key == pygame.K_0:
                    cells=START_EMPTY
                    update(console, cells, SIZE_CELL)
                    pygame.display.update()

                if event.key == pygame.K_s:
                    with open(str(datetime.datetime.now()), "x") as pos_file:
                         for r,c in np.ndindex(cells.shape):
                             pos_file.writelines(str(cells[r,c]))


            if pygame.mouse.get_pressed()[0]:
                #get position of mouse
                pos = pygame.mouse.get_pos()
                loc=cells[pos[1] // SIZE_CELL, pos[0] // SIZE_CELL]
                
                if loc==1:
                    cells[pos[1] // SIZE_CELL, pos[0] // SIZE_CELL]=0
            
                else:
                    cells[pos[1] // SIZE_CELL, pos[0] // SIZE_CELL]=1
                    
                update(console, cells, SIZE_CELL)
                pygame.display.update()

        console.fill(COL_GRID)
            
        if run_game:
            cells = update(console, cells, SIZE_CELL, will_update=True)
            pygame.display.update()
            time.sleep(sleep/100)

main(sleep=0)
    
