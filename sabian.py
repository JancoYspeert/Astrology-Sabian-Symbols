#!/usr/bin/env python
import math
import pygame
import random
import time
from pygame.locals import *
from sys import exit
from linecache import getline

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def getString(si, deg):
  li = (si-1)*30 + (si-1)*2 + deg/16 + deg +1
  sp = (si-1)*30 + (si-1)*2 + 16*(deg/16) + 1
  line = getline("sabiansDone.txt", li)
  span = getline("sabiansDone.txt", sp)
  return [line,span]

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

def draw_inverse_circle(screen, color, center, radius, n):
  left = center[0] - radius
  right = center[0] + radius
  top = center[1] - radius
  bottom = center[1] + radius
  screen_width = screen.get_width()
  screen_height = screen.get_height()
  
  # make an inverse square
  pygame.draw.rect(screen, color, Rect(0, 0, left, screen_height))
  pygame.draw.rect(screen, color, Rect(right, 0, screen_width - right, screen_height))
  pygame.draw.rect(screen, color, Rect(left, 0, right - left, top))
  pygame.draw.rect(screen, color, Rect(left, bottom, right - left, screen_height - bottom))
  
  #fill in the corners with pretty roundness

  # list of numbers, 0 through n - 1
  points = range(n) 

  # list of n numbers evenly distributed from 0 to 1.0 inclusive
  points = map(lambda pt: pt / (len(points) - 1.0), points) 

  # list of n radians evenly distributed from 0 to pi/4 inclusive
  points = map(lambda pt: pt * 3.1415926535 * 2 / 4, points) 

  # list of points evenly distributed around the circumference in the first quadrant of a unit circle
  points = map(lambda pt: (math.cos(pt), math.sin(pt)), points) 

  # list of points evenly distributed around the circumference of the circle of desired size centered on the origin
  points = map(lambda pt: (radius * pt[0], radius * pt[1]), points) 
  
  # we'll draw these points with trapezoids that connect to the 
  # top or bottom rectangle and flip them around each quadrant
  for quadrant in ((1, 1), (-1, 1), (-1, -1), (1, -1)): 
    x_flip = quadrant[0]
    y_flip = quadrant[1]
    edge = center[1] + radius * y_flip
    for i in xrange(len(points) - 1):
      A = (points[i][0] * x_flip + center[0], points[i][1] * y_flip + center[1])
      B = (points[i + 1][0] * x_flip + center[0], points[i + 1][1] * y_flip + center[1])
      A_edge = (A[0], edge)
      B_edge = (B[0], edge)
      
      pygame.draw.polygon(screen, color, (A, B, B_edge, A_edge))
      

pygame.init()
screen = pygame.display.set_mode((610, 480), SRCALPHA, 32)
background_image_filename = 'Astrology2.jpg'
aries = pygame.image.load('aries.png').convert()
taurus = pygame.image.load('taurus.png').convert()
gemini = pygame.image.load('gemini.png').convert()
cancer = pygame.image.load('cancer.png').convert()
leo = pygame.image.load('leo.png').convert()
virgo = pygame.image.load('virgo.png').convert()
libra = pygame.image.load('libra.png').convert()
scorpio = pygame.image.load('scorpio.png').convert()
sagitarius = pygame.image.load('sagitarius.png').convert()
capricorn = pygame.image.load('capricorn.png').convert()
aquarius = pygame.image.load('aquarius.png').convert()
pisces = pygame.image.load('pisces.png').convert()
astroDic = {1:aries, 2: taurus, 3:gemini, 4:cancer, 5: leo, 6: virgo, 7:libra, 8: scorpio, 9:sagitarius, 10:capricorn, 11: aquarius, 12:pisces}
astroDic2 = {1:"Aries", 2: "Taurus", 3:"Gemini", 4:"Cancer", 5: "Leo", 6: "Virgo", 7:"Libra", 8: "Scorpio", 9:"Sagittarius", 10:"Capricorn", 11: "Aquarius", 12:"Pisces"}
mouseB = pygame.image.load('MouseBut.jpg').convert()
signsurfaces = [0]*12
numSurface = [0] * 30
font = pygame.font.SysFont("arial", 20);
font2 = pygame.font.SysFont("arial", 40);
font3 = pygame.font.SysFont("arial", 14);
WHITE = (255,255,255)
BLUE =  (23,25,54)
GREY = (205,205,225)
REDGREY = (23,25,75,200)
REDISH = (200, 50, 50) 
for i in range(1,13):
  signsurfaces[i-1] = render_textrect(astroDic2[i], font3, Rect((22,124 + 30*(i-1)),(120,21)), WHITE, REDISH, justification=1)
for i in range (1, 31):
  if i < 10:
    numSt = "0" + str(i)
  else:
    numSt = str(i)
  numSurface[i-1] = render_textrect(numSt, font3, Rect((112 + 30 *((i-1)%5),304 + 30*((i-1)/5)),(25,21)), WHITE, REDISH, justification=1)
  
pygame.display.set_caption("Sabian oracle")
background = pygame.image.load(background_image_filename).convert()


mMes1 = "Cick and Hold" 
mMes2 =  "Left Mouse Button"
mMes3 =  "to Randomize"
mMes1_surf = font.render(mMes1, True, (0,0,0))
mMes2_surf = font.render(mMes2, True, (0,0,0))
mMes3_surf = font.render(mMes3, True, (0,0,0))
mMesheight = mMes1_surf.get_height()

mMesW1 = mMes1_surf.get_width()
mMesW2 = mMes2_surf.get_width()
mMesW3 = mMes3_surf.get_width()
deg_surf = font2.render("01",True, (0,0,0))
degH = deg_surf.get_height()
degW = deg_surf.get_width()
deg = 1
state = 0
sign = 1
stateChange = False
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      exit()
    if event.type == MOUSEBUTTONDOWN:
      (x,y) = pygame.mouse.get_pos()

      if state == 4 and (112 <= x<= 262) and 300 <= y:
	deg = 1 + ((x-112)/30) + 5 *((y -300)/30)
	stateChange = True
	if deg<10:	
	  deg = "0"+str(deg)
	else:
	  deg = str(deg)
      if state == 3 and (22 <= x <= 142) and (120 <= y<= 480):
	sign = (y - 120)/30 + 1 
	stateChange = True
	if deg<10:
	  deg = "0"+str(deg)
	else:
	  deg = str(deg)
      if (112<=x <=188) and (394<=y<=470) and (state ==0 or state ==2):
	state = 4
      if (22<=x <=98) and (394<=y<=470) and (state ==0 or state ==2):
	state = 3

      if (400<= x <= 600) and (394 <= y <= 470): 
	now = time.time()
	sign = random.randint(1,12)
	deg = random.randint(1,30)
	if deg<10:
	  deg = "0"+str(deg)
	else:
	  deg = str(deg)
	state = 1
      if stateChange:
	state = 2
	stateChange = False

    if event.type == MOUSEBUTTONUP and state == 1:
      sign = random.randint(1,12)
      deg = random.randint(1,30)
      if deg<10:
	deg = "0"+str(deg)
      else:
	deg = str(deg)
      state = 2
      
  if state == 0:
    screen.fill(WHITE)
    screen.blit(aries,(20,392))
    draw_inverse_circle(screen,BLUE,(60,432),38,360) 
    pygame.draw.circle(screen,GREY,(150,432),38,0)
    screen.blit(deg_surf,(150-degW/2,432-degH/2))
    #
    pygame.draw.rect(screen, GREY,Rect((400,394),(200,76)))
    screen.blit(mMes1_surf,(500-mMesW1/2,432-3*mMesheight/2-4))
    screen.blit(mMes2_surf,(500-mMesW2/2,432-mMesheight/2))
    screen.blit(mMes3_surf,(500-mMesW3/2,432+mMesheight/2+4))
    screen.blit(background, (5,0))
  
  if state == 1:
    screen.fill(WHITE)

    sign = random.randint(1,12)
    deg = random.randint(1,30)
    if deg<10:
      deg = "0"+str(deg)
    else:
      deg = str(deg)
    screen.blit(astroDic[sign],(20,392))
    draw_inverse_circle(screen,BLUE,(60,432),38,360) 
    pygame.draw.circle(screen,GREY,(150,432),38,0)

    deg_surf = font2.render(deg,True, (0,0,0))
    degH = deg_surf.get_height()
    degW = deg_surf.get_width()  
    screen.blit(deg_surf,(150-degW/2,432-degH/2))
    #
    pygame.draw.rect(screen, GREY,Rect((400,394),(200,76)))
    screen.blit(mMes1_surf,(500-mMesW1/2,432-3*mMesheight/2-4))
    screen.blit(mMes2_surf,(500-mMesW2/2,432-mMesheight/2))
    screen.blit(mMes3_surf,(500-mMesW3/2,432+mMesheight/2+4))
    screen.blit(background, (5,0)) 
  
  if state == 2:
    screen.fill(WHITE)
    screen.blit(astroDic[sign],(20,392))
    draw_inverse_circle(screen,BLUE,(60,432),38,360) 
    pygame.draw.circle(screen,GREY,(150,432),38,0)
    mes2 = astroDic2[sign]+ " " + deg
    mes2_surf = font.render(mes2,True,(255,0,60))
    mes2w = mes2_surf.get_width()
    deg_surf = font2.render(deg,True, (0,0,0))
    degH = deg_surf.get_height()
    degW = deg_surf.get_width()  
    screen.blit(deg_surf,(150-degW/2,432-degH/2))
    #
    pygame.draw.rect(screen, GREY,Rect((400,394),(200,76)))

    screen.blit(mMes1_surf,(500-mMesW1/2,432-3*mMesheight/2-4))
    screen.blit(mMes2_surf,(500-mMesW2/2,432-mMesheight/2))
    screen.blit(mMes3_surf,(500-mMesW3/2,432+mMesheight/2+4))
    screen.blit(background, (5,0)) 
    screen.blit(mes2_surf,(294 - mes2w/2,432-mMesheight/2))
    #pygame.draw.rect(screen, REDGREY,Rect((350,15),(245,50)))
    #pygame.draw.rect(screen, REDGREY,Rect((350,70),(245,50)))
    #pygame.draw.rect(screen, REDGREY,Rect((350,125),(245,120)))
    #pygame.draw.rect(screen, REDGREY,Rect((350,250),(245,120)))
    sgn = int(sign)
    dg = int(deg)
    [a, b] = getString(sgn, dg)
    zdef = (sgn -1)* 30 + dg
    span = b.split("\t")
    span[-1]= span[-1].rstrip()
    sabian = a.split("\t")
    sabian[-1] = sabian[-1].rstrip()
    spanStr = span[0]+"\n" + span[1] + "\n " + span[2]
    spanSabName = sabian[1]
    spanSabInt = sabian[2]
    if 145 < zdef < 297:
      spanSabInt2 = "Unfortunately we do not have extra interpretation for this symbol"
    else:
      spanSabInt2 = sabian[3]
      
    interpString = spanSabInt + "\n\n" + spanSabInt2  
    pygame.draw.rect(screen,REDGREY, Rect((350, 15),(245,59)))
    pygame.draw.rect(screen,REDGREY, Rect((350, 80),(245,59)))
    pygame.draw.rect(screen,REDGREY, Rect((350, 145),(245,224)))
    spanRect = render_textrect(spanStr, font3, Rect((350,19),(245,55)), WHITE, REDGREY, justification=1)
    sabTitRect = render_textrect(spanSabName, font3, Rect((350,99),(245,55)), WHITE, REDGREY, justification=1)
    sabIntRect = render_textrect(interpString, font3, Rect((355,179),(235,220)), WHITE, REDGREY, justification=0)

    
    screen.blit(spanRect,(350,19))
    screen.blit(sabTitRect,(350,84))
    screen.blit(sabIntRect,(355,149))
    pygame.draw.rect(screen,WHITE, Rect((350, 15),(245,59)),1)
    pygame.draw.rect(screen,WHITE, Rect((350, 80),(245,59)),1)
    pygame.draw.rect(screen,WHITE, Rect((350, 145),(245,224)),1)
  if state == 3:
    screen.fill(BLUE)

    pygame.draw.rect(screen, GREY,Rect((400,394),(200,76)))
    screen.blit(mMes1_surf,(500-mMesW1/2,432-3*mMesheight/2-4))
    screen.blit(mMes2_surf,(500-mMesW2/2,432-mMesheight/2))
    screen.blit(mMes3_surf,(500-mMesW3/2,432+mMesheight/2+4))
    screen.blit(background, (5,0))
    for i in range(12):
      pygame.draw.rect(screen,REDISH, Rect((20, 120+30*i),(120,25)))
      screen.blit(signsurfaces[i],(20,124+30*i))      
      pygame.draw.rect(screen,GREY, Rect((20, 120+30*i),(120,25)),1)
  if state == 4:
    screen.fill(WHITE)
    screen.blit(astroDic[sign],(20,392))
    draw_inverse_circle(screen,BLUE,(60,432),38,360) 

    pygame.draw.rect(screen, GREY,Rect((400,394),(200,76)))
    screen.blit(mMes1_surf,(500-mMesW1/2,432-3*mMesheight/2-4))
    screen.blit(mMes2_surf,(500-mMesW2/2,432-mMesheight/2))
    screen.blit(mMes3_surf,(500-mMesW3/2,432+mMesheight/2+4))
    screen.blit(background, (5,0))
    for i in range(30):
      pygame.draw.rect(screen,REDISH, Rect((112+30*(i%5), 300+30*(i/5)),(25,25)))
      screen.blit(numSurface[i],(112+30*(i%5),304+30*(i/5)))
      pygame.draw.rect(screen,GREY, Rect((112+30*(i%5), 300+30*(i/5)),(25,25)),1)
  pygame.display.update()