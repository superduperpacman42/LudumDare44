import pygame
import sys

W = 800
H = 500
TIME_STEP = 60
BACKGROUND = (0,0,0)
BORDER = (0,0,0)
CITY = (23, 84, 183)
BEAM = (255,255,0)
WINDOW = (255,255,0)
TEXT = WINDOW
CONVOLUTION = WINDOW
BUILDINGS = (1,4,5,3,2)
SCALE = 50
GROUND = 2.2
DURATION = 3
DELAY = 1
PAUSE = 5
LINE_WIDTH = 4
WINDOW_WIDTH = 0.2
WINDOW_OFFSET = 0.27
WINDOWS = ([0],[1],[2,3,5],[0,4,7],[5,2,8,9],[1,3,6],[2,6],[1,4],[3,1],[2])
WINDOW_SPACING = 0.4
WINDOW_LINE_WIDTH = 3
TEXT_OFFSET = 0
TEXT_SPACE = -0.2
FONT_SIZE = 40
CONV_SCALE = 1.1

def display(screen=False, caption="Convoluted Creations"):
    if not screen:
        pygame.init()
        pygame.display.set_caption(caption)
        screen = pygame.display.set_mode([W, H])
    font = pygame.font.Font("bankgothic/BankGothic Md BT.ttf", FONT_SIZE)
    clock = pygame.time.Clock()
    beam = -DELAY/DURATION
    while beam <= 1+PAUSE/DURATION:
        beam += clock.tick(TIME_STEP)/DURATION/1000 * (1+4*(beam-.5)**2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
        # Draw background
        screen.fill(BACKGROUND)
        y0 = int(GROUND*SCALE+H/2)
        points = [(int((x-len(BUILDINGS)/2+0.5)*SCALE+W/2),y0-h*SCALE) for x, h in enumerate(BUILDINGS)]
        points += [(int((len(BUILDINGS)/2+0.5)*SCALE+W/2),y0)]
        points += [(int((-len(BUILDINGS)/2-0.5)*SCALE+W/2),y0)]
        points = [(p[0], y0-(y0-p[1])*CONV_SCALE-LINE_WIDTH) for p in points]
        pygame.draw.polygon(screen, CONVOLUTION, points)
        screen.fill(BACKGROUND, (beam*(W+SCALE),0,W,H))
        # Draw city
        for x, h in enumerate(BUILDINGS):
            x0 = int((x-len(BUILDINGS)/2)*SCALE+W/2)
            y0 = int((GROUND-h)*SCALE+H/2)
            screen.fill(CITY, (x0,y0,SCALE,SCALE*h))
        # Draw beam
        pygame.draw.rect(screen, BEAM, (beam*(W+SCALE)-SCALE/2,0,SCALE,H/2+GROUND*SCALE),0)
        # Draw outlines
        for x, h in enumerate(BUILDINGS):
            x0 = int((x-len(BUILDINGS)/2)*SCALE+W/2)
            y0 = int((GROUND-h)*SCALE+H/2)
            outline_rect(screen, BORDER, (x0,y0,SCALE,SCALE*h),LINE_WIDTH)
        # Draw windows
        for i, column in enumerate(WINDOWS):
            for window in column:
                if i%2 == 0: # left
                    x0 = int((i//2-len(BUILDINGS)/2)*SCALE+W/2 + WINDOW_OFFSET*SCALE - WINDOW_WIDTH/2*SCALE)
                else: # right
                    x0 = int((i//2-len(BUILDINGS)/2)*SCALE+W/2 + (1-WINDOW_OFFSET)*SCALE - WINDOW_WIDTH/2*SCALE)
                y0 = int((GROUND-BUILDINGS[i//2])*SCALE+H/2 + (window+0.5)*WINDOW_SPACING*SCALE)
                screen.fill(WINDOW, (x0,y0,WINDOW_WIDTH*SCALE,WINDOW_WIDTH*SCALE))
                outline_rect(screen, BORDER, (x0,y0,WINDOW_WIDTH*SCALE,WINDOW_WIDTH*SCALE),WINDOW_LINE_WIDTH)
        # Text
        dy = draw_text(screen, "Convoluted", font, TEXT, (W/2,H/2+(GROUND+TEXT_OFFSET)*SCALE))
        draw_text(screen, "Creations", font, TEXT, (W/2,H/2+dy+(GROUND+TEXT_OFFSET+TEXT_SPACE)*SCALE))
        # Update display
        pygame.display.update()
    return screen

def outline_rect(screen, color, r, w):
    pygame.draw.rect(screen, color, r, w)
    screen.fill(color, (r[0]-w/4,r[1]-w/4,w,w))
    screen.fill(color, (r[0]+r[2]-w/2,r[1]-w/4,w,w))
    screen.fill(color, (r[0]+r[2]-w/2,r[1]+r[3]-w/2,w,w))
    screen.fill(color, (r[0]-w/4,r[1]+r[3]-w/2,w,w))

def draw_text(screen, text, font, color, pos):
    text = font.render(text, 1, color)
    screen.blit(text, (pos[0]-text.get_rect()[2]/2, pos[1]))
    return text.get_rect()[3]

if __name__ == '__main__':
    screen = display()
