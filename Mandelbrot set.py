import pygame
from PIL import Image
import time
import random

pygame.init()

width = 1920
height = 1080
#width and height of screen

character_black_list = ["!", " ", "@", "#","$","%","^","&","*","(",")","=","+","|","{","}",":",";","'",'"',"<",">","?","`","~",""]
#characters not allowed in file names

running = True
screen = pygame.display.set_mode((width, height))
im = Image.new('RGB', (width, height), color = 'black')
pixel_map = im.load()
#sets up black image and defines the pixel map

font = pygame.font.SysFont("None", 30)
font1 = pygame.font.SysFont("None", 60)
instructions_button = pygame.Rect(width-200,50,150,50)
instructions_button_text = font.render("Instructions", True, (0,0,0))

click_lock = True
#prevents user from clicking screen to many times
instructions_on = False
#are the instructions on the screen
input_active = False
#Has the user clicked on the text box to input text
user_input = ''
#Stores the text the user inputs

path_set = False
#Has the user named their files

iteration_cap = 300
#The maximum amount of iterations completed on a given complex point to determine its colour/if its in the set


def save_menu():
  box_left = 50
  box_top = 50
  save_box = pygame.Rect(box_left, box_top, 420, 150)
  pygame.draw.rect(screen, (163,214,224), save_box)
  input_box = pygame.Rect(box_left+25, box_top+75, 370, 50)
  #setting up boxes for the menu
  heading = "File Name"
  text = font1.render(heading, True, (0,0,0))
  screen.blit(text, (box_left+50, box_top+25))
  
  if not input_active:
    pygame.draw.rect(screen, (202, 214, 224), input_box)
  else:
    pygame.draw.rect(screen, (136, 157, 255), input_box)
    text = font.render(user_input, True, (0,0,0))
    screen.blit(text, (box_left+30, box_top+80))
  #This if statement decides whether or not to show visual cues for inputting text
    
  

 
def display_instructions():
  ins_bg = pygame.Rect(560, 100, 800, 200)
  #background size of instruction box
  pygame.draw.rect(screen, (163,214,224), ins_bg)
  
  line = "The fractal on the screen is the Mandelbrot set,"
  text = font.render(line, True, (0,0,0))
  screen.blit(text, (610,150))
  
  line = "it's pattern is chaotic, recurring, and has infinite complexity."
  text = font.render(line, True, (0,0,0))
  screen.blit(text, (610,150+25))
  
  line = 'SPACEBAR - Toggles "zoom lock" a feature to prevent accidental inputs'
  text = font.render(line, True, (0,0,0))
  screen.blit(text, (610,150+25*2))
  
  line = "Left Mouse Button - Generates a closer look at wherever you choose"
  text = font.render(line, True, (0,0,0))
  screen.blit(text, (610,150+25*3))
  
  line = "Click any button to close this window."
  text = font.render(line, True, (0,0,0))
  screen.blit(text, (610,150+25*4))
  #instructions, not the most elegant... but functional


def update_loading_screen(ycounter):
  pygame.draw.rect(screen, (163,214,224), loading_bg)
  
  heading = "Generating. Please wait"
  progress = f"{int((ycounter/1080)*100)}%"
  #percentage completed
  text = font.render(heading, True, (0,0,0))
  screen.blit(text, (845, 515))
  
  text = font1.render(progress, True, (0,0,0))
  screen.blit(text, (925,535))
  

  
def display_zoom_lock():
  if click_lock == True:
    text = font.render("Zoom lock: ON", True, (255,0,0))
  else:
    text = font.render("Ready", True, (0,255,0))
  screen.blit(text, (width-150, height-20))
  #displays whether click lock is active or not


def Image_to_surface(Image):
  return pygame.image.fromstring(Image.tobytes(), Image.size, Image.mode)
  #takes PIL image and makes it displayable in pygame


def coord_converter(mouse):
  centerpoint_x = (mouse[0]*num_val_pp)+(screen_edge[0])
  centerpoint_y = (screen_edge[1])-(mouse[1]*num_val_pp)
  return(centerpoint_x, centerpoint_y)
  #converts screen coordinates of mouse to complex plane


def fz(inp, c):
  out = (inp*inp) + c
  return out
  #one iteration


def generate(screen_edge, pixel_array):
  global loading_bg
  loading_bg = pygame.Rect(835, 490, 255, 100)
  pygame.draw.rect(screen, (163,214,224), loading_bg)
  pygame.display.update()
  #update to get the background for the loading screen text on the screen
  
  y = screen_edge[1]
  x = screen_edge[0]
  #Set the edge coordinates for the region of complex plane to be iterated
  
  lower_y = (screen_edge[1]-(num_val_pp*(height-1)))
  upper_x = (screen_edge[0]+(num_val_pp*(width-1)))
  #Set the other edge of this region to know where to stop
  
  ycounter = 0
  #Keep track of the column of pixels
  while y > lower_y:
    xcounter = 0
    #Keep track of the row of pixels
    while x < upper_x:
      c = complex(x,y)
      iterations = 0
      inp = 0
      #iteration part
      while abs(inp) <= 2 and iterations < iteration_cap: #"Hinky maths" laws of mandelbrot set
        inp = fz(inp, c)
        iterations += 1
      if iterations >= iteration_cap:
        colour = (0,0,0)
      else:
        colour = (int((iterations/iteration_cap)*255), 0, 0)
        #colour is directly correlated with how many iterations it took for the point to leave the set
        
      pixel_array[xcounter,ycounter] = colour
      #updates pixel colour
      
      x += num_val_pp
      xcounter += 1
      #update values
    y -= num_val_pp
    ycounter += 1
    x = screen_edge[0]
    update_loading_screen(ycounter)
    pygame.display.update()
    #update values
  img_name = f"{user_input}_gen{gen}.png"
  im.save(img_name)
  
  #save the image with the users file name an a generation number attached



num_val_pp = 0.003125
gen = 0
#starting value for the width of each pixel in the complex plane and the number of new images generated
screen_edge = (-3,1.6875)
#initial point of reference in the complex plane

begin = time.time()
generate(screen_edge, pixel_map)
end = time.time()
#generates the whole set zoomed out immediately

run_time = end - begin
print(run_time)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    
    if event.type == pygame.KEYDOWN:
      instructions_on = False
      #If any key is pressed, instructions go away
      
      if event.key == pygame.K_SPACE and not input_active:
        if click_lock == True:
          click_lock = False
        else:
          click_lock = True
      #Spacebar turns the zoom lock on and off only if the user is not trying to input a file name

          
      if event.key == pygame.K_RETURN and input_active:
        input_active = False
        path_set = True
      #pressing enter confirms the file name, closing the save menu and stopping input
        
      if event.key == pygame.K_BACKSPACE and input_active:
        user_input = user_input[:-1]
      #delete last character from input for file name
        
      elif input_active and event.unicode not in character_black_list and event.key != pygame.K_TAB:
        user_input += event.unicode
      #Adds whatever character is pressed to the input string unless it is a banned character
        #TESTING#
        #print(user_input)
        
        
    if event.type == pygame.MOUSEBUTTONDOWN:
      instructions_on = False
      input_active = False
      #If the mouse is pressed again out of the input text box, the instructions will go away or the input will stop
      
      mouse = pygame.mouse.get_pos()
      #screen coordinates of mouse click

      if 1720 <= mouse[0] <= 1870 and 50 <= mouse[1] <= 100 and num_val_pp == 0.003125:
        instructions_on = True
        click_lock = True
      #is the mouse clicking on the instructions button

      if 75 <= mouse[0] <= 445 and 125 <= mouse[1] <= 175 and not path_set:
        input_active = True
        click_lock = True
      #is the mouse clicking on the text box
      
      if click_lock == False and instructions_on == False:
        click_lock = True
        centerpoint = coord_converter(mouse)
        print(centerpoint)
        #changes the screen coordinates to complex plane point of reference
        
        num_val_pp = num_val_pp/2
        gen += 1
        #Decreasing the width of each pixel in terms of the complex plane
        
        screen_edge = (centerpoint[0]-(num_val_pp*(width//2)), centerpoint[1]+(num_val_pp*(height//2)))
        #setting coordinates to start iterating from, and iterating using smaller values

        
        
        begin = time.time()
        generate(screen_edge, pixel_map)
        end = time.time()
        run_time = end - begin
        print(gen)
        print(run_time)
        #TESTING#
        
   
  screen.blit(Image_to_surface(im), (0,0))
  #Display mandelbrot to screen

    
  
  display_zoom_lock()
  #Display status of zoom lock
  
  
  
  
  if instructions_on:
    display_instructions()
  #Display instruction box if instruction button has been pressed


  
  if num_val_pp == 0.003125:
    if not path_set:
      save_menu()
    pygame.draw.rect(screen, (0,255,0), instructions_button)
    #Draw instruction button to screen
    screen.blit(instructions_button_text, [width-190,60,150,50])
    #Overlay instruction button text
  #Display instructions button only on the initial screen

    

  
  
  pygame.display.update()
pygame.quit()
