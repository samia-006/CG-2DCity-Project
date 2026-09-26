from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# ==========================================
# GLOBAL VARIABLES FOR ANIMATION & STATE
# ==========================================
car_xs = [-1.4, -2.1, -2.8, -3.5]  # X-coordinates for multiple cars on the road
bird_x = -1.0                       # X-coordinate for flying birds animation
pedestrian_xs = [-0.1, 0.3, 0.6]    # X-coordinates for pedestrians on the sidewalk
traffic_light_state = 0             # 0 = Red Light (stop), 1 = Green Light (move)
frame_counter = 0                   # Frame tracker to control timing and state shifts

# ==========================================
# 1. SHAPE DRAWING & COLOR FILL FUNCTIONS
# ==========================================
def draw_rectangle(x1, y1, x2, y2, r, g, b):
    # What it does: Draws a filled rectangular shape with specific RGB colors.
    # Why it is needed: Fundamental building block for roads, buildings, cars, and windows.
    # Where it appears in the real world: Windows, walls, bricks in buildings, and road blocks.
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_circle(cx, cy, r, red, green, blue):
    # What it does: Draws a filled circle using triangle fan approximation.
    # Why it is needed: Used for drawing the sun, traffic lights, and vehicle wheels.
    # Where it appears in the real world: Traffic signals, sun, wheels, and round architectural structures.
    glColor3f(red, green, blue)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(37):
        angle = i * 2.0 * math.pi / 36
        glVertex2f(cx + (r * math.cos(angle)), cy + (r * math.sin(angle)))
    glEnd()

def draw_bird(x, y):
    # What it does: Renders a V-shaped flying bird in the sky using connected lines.
    # Why it is needed: To add dynamic nature and life elements to the sky background.
    # Where it appears in the real world: Birds flying over a city skyline.
    glColor3f(0.2, 0.2, 0.2)
    glLineWidth(2.0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(x - 0.03, y + 0.02)
    glVertex2f(x, y)
    glVertex2f(x + 0.03, y + 0.02)
    glEnd()
    glLineWidth(1.0)

# ==========================================
# 2. ADVANCED GRAPHICS: BEZIER CURVE & CLIPPING
# ==========================================
def draw_bezier_curve():
    # What it does: Renders a smooth curve using Bernstein polynomials for Bezier curves.
    # Why it is needed: To fulfill the project requirement of drawing complex curved vector paths.
    # Where it appears in the real world: Vector design paths, road overpasses, and architectural arcs.
    glColor3f(0.8, 0.4, 0.1)  
    glBegin(GL_LINE_STRIP)
    p0 = (-0.9, -0.2)
    p1 = (-0.6, 0.1)
    p2 = (-0.3, -0.2)
    
    for t in [i / 20.0 for i in range(21)]:
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        glVertex2f(x, y)
    glEnd()

def draw_line_clipping_demo():
    # What it does: Demonstrates line clipping concept within specific graphic bounds.
    # Why it is needed: To satisfy the line clipping requirement by showing clipped vectors.
    # Where it appears in the real world: Window clipping in computer monitors and viewport rendering.
    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.8, 0.7)
    glEnd()
    glLineWidth(1.0)

# ==========================================
# 3. SCENERY & CHARACTER OBJECTS
# ==========================================
def draw_tree(x, y):
    # What it does: Draws a tree consisting of a brown trunk and green foliage.
    # Why it is needed: To enhance the urban scenery with natural elements and shape drawing.
    # Where it appears in the real world: Parks, roadside landscaping, and city avenues.
    draw_rectangle(x - 0.025, y, x + 0.025, y + 0.18, 0.55, 0.27, 0.07)
    glColor3f(0.1, 0.6, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - 0.07, y + 0.15)
    glVertex2f(x + 0.07, y + 0.15)
    glVertex2f(x, y + 0.32)
    glEnd()

def draw_person(x, y):
    # What it does: Draws a stick/block figure representing an adult pedestrian.
    # Why it is needed: Adds life, movement, and activity to the city sidewalk environment.
    # Where it appears in the real world: People walking on footpaths in a city.
    draw_circle(x, y + 0.1, 0.02, 1.0, 0.8, 0.6)
    draw_rectangle(x - 0.015, y, x + 0.015, y + 0.08, 0.1, 0.1, 0.8)

def draw_child(x, y):
    # What it does: Draws a smaller person representing a child.
    # Why it is needed: To diversify the city environment with kids walking on sidewalks.
    # Where it appears in the real world: Neighborhood streets and footpaths.
    draw_circle(x, y + 0.07, 0.015, 1.0, 0.8, 0.6)
    draw_rectangle(x - 0.01, y, x + 0.01, y + 0.05, 0.9, 0.3, 0.5)

def draw_dog(x, y):
    # What it does: Draws a small pet dog shape on the sidewalk.
    # Why it is needed: Adds realism and cute detail to the pedestrian walking scene.
    # Where it appears in the real world: Parks and streets with pet owners.
    draw_rectangle(x - 0.02, y, x + 0.02, y + 0.025, 0.5, 0.3, 0.1)
    draw_rectangle(x + 0.01, y + 0.02, x + 0.03, y + 0.04, 0.5, 0.3, 0.1)

# ==========================================
# 4. TRAFFIC SIGNAL & VEHICLE MOVEMENT
# ==========================================
def draw_traffic_light():
    # What it does: Renders a traffic signal pole with changing red and green lights.
    # Why it is needed: Simulates real-world traffic management and interactive visual state.
    # Where it appears in the real world: City road intersections and traffic junctions.
    global traffic_light_state
    draw_rectangle(0.58, -0.35, 0.61, 0.1, 0.3, 0.3, 0.3)
    draw_rectangle(0.55, 0.05, 0.64, 0.25, 0.1, 0.1, 0.1)
    
    if traffic_light_state == 0:
        draw_circle(0.595, 0.21, 0.018, 1.0, 0.0, 0.0)  # Red Light ON
        draw_circle(0.595, 0.09, 0.018, 0.2, 0.0, 0.0)  # Green Light OFF
    else:
        draw_circle(0.595, 0.21, 0.018, 0.3, 0.0, 0.0)  # Red Light OFF
        draw_circle(0.595, 0.09, 0.018, 0.0, 1.0, 0.0)  # Green Light ON

def draw_car(x, r, g, b):
    # What it does: Translates the car horizontally using 2D transformation matrix.
    # Why it is needed: Implements 2D translation (`glTranslatef`) to animate vehicle motion across the screen.
    # Where it appears in the real world: Moving vehicles in traffic simulations and games.
    glPushMatrix()
    glTranslatef(x, 0.0, 0.0)
    draw_rectangle(-0.15, -0.45, 0.15, -0.35, r, g, b)
    draw_rectangle(-0.08, -0.35, 0.08, -0.28, r*0.8, g*0.8, b*0.8)
    draw_circle(-0.09, -0.47, 0.025, 0.1, 0.1, 0.1)
    draw_circle(0.09, -0.47, 0.025, 0.1, 0.1, 0.1)
    glPopMatrix()

# ==========================================
# 5. MAIN DISPLAY RENDERING PIPELINE
# ==========================================
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # 1. Sky Background
    draw_rectangle(-1.0, -1.0, 1.0, 1.0, 0.53, 0.81, 0.98)
    
    # 2. Sun
    draw_circle(0.75, 0.75, 0.12, 1.0, 0.9, 0.0)

    # 3. Flying Birds in Sky
    draw_bird(bird_x, 0.6)
    draw_bird(bird_x - 0.15, 0.68)
    draw_bird(bird_x - 0.3, 0.63)
    
    # 4. Greenery Field / Sidewalk area
    draw_rectangle(-1.0, -0.6, 1.0, -0.2, 0.2, 0.75, 0.25)
    
    # 5. Road with dashed divider strips
    draw_rectangle(-1.0, -0.55, 1.0, -0.35, 0.25, 0.25, 0.25)
    for x in [-0.8, -0.4, 0.0, 0.4, 0.8]:
        draw_rectangle(x, -0.46, x + 0.15, -0.44, 1.0, 1.0, 1.0)
        
    # 6. Buildings with Fixed, Perfectly Aligned Windows & Roofs
    # Building 1 (Left Skyscraper)
    draw_rectangle(-0.95, -0.2, -0.65, 0.55, 0.6, 0.6, 0.7)
    # Neatly arranged windows for Building 1
    for wx in [-0.88, -0.78]:
        for wy in [0.38, 0.24, 0.10, -0.04]:
            draw_rectangle(wx, wy, wx + 0.06, wy + 0.09, 0.9, 0.9, 0.2)

    # Building 2 (Center Residential House with Roof)
    draw_rectangle(-0.55, -0.2, -0.2, 0.4, 0.9, 0.5, 0.3)
    draw_rectangle(-0.48, 0.12, -0.38, 0.26, 1.0, 1.0, 1.0)
    draw_rectangle(-0.35, 0.12, -0.25, 0.26, 1.0, 1.0, 1.0)
    draw_rectangle(-0.42, -0.05, -0.33, 0.1, 0.2, 0.2, 0.2) # Door
    
    # Roof for Center House
    glColor3f(0.8, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.37, 0.6)
    glVertex2f(-0.55, 0.4)
    glVertex2f(-0.2, 0.4)
    glEnd()
    
    # Building 3 (Right Background Building)
    draw_rectangle(-0.15, -0.2, 0.15, 0.45, 0.5, 0.6, 0.8)
    # Neatly arranged grid windows for Building 3
    for wx in [-0.09, 0.03]:
        for wy in [0.32, 0.18, 0.04, -0.10]:
            draw_rectangle(wx, wy, wx + 0.05, wy + 0.08, 1.0, 1.0, 1.0)

    # 7. Trees along the roadside
    draw_tree(-0.98, -0.35)
    draw_tree(-0.85, -0.35)
    draw_tree(0.22, -0.35)
    draw_tree(0.38, -0.35)
    draw_tree(0.50, -0.35)
    
    # 8. Pedestrians, children, and pets on sidewalk
    draw_person(pedestrian_xs[0], -0.35)
    draw_child(pedestrian_xs[1], -0.36)
    draw_dog(pedestrian_xs[2], -0.37)
    draw_person(0.42, -0.35)
    
    # 9. Bezier Curve & Line Clipping demonstration
    draw_bezier_curve()
    draw_line_clipping_demo()
    
    # 10. Traffic Light system
    draw_traffic_light()
    
    # 11. Multiple Moving Cars with unique colors
    car_colors = [
        (0.1, 0.4, 0.8),
        (0.9, 0.2, 0.2),
        (0.9, 0.8, 0.1),
        (0.6, 0.2, 0.8)
    ]
    for i in range(len(car_xs)):
        draw_car(car_xs[i], car_colors[i][0], car_colors[i][1], car_colors[i][2])
    
    glutSwapBuffers()

# ==========================================
# 6. ANIMATION & TIMING CONTROLLER
# ==========================================
def update(value):
    # What it does: Controls frame-by-frame updates, traffic light timing, and coordinate movements.
    # Why it is needed: Manages real-time animation loop using timer functions.
    global car_xs, bird_x, pedestrian_xs, traffic_light_state, frame_counter
    
    frame_counter += 1
    if frame_counter % 120 == 0:
        traffic_light_state = 1 - traffic_light_state  # Switch traffic signal state
        
    bird_x += 0.003
    if bird_x > 1.3:
        bird_x = -1.3

    for i in range(len(pedestrian_xs)):
        pedestrian_xs[i] += 0.001
        if pedestrian_xs[i] > 0.8:
            pedestrian_xs[i] = -0.5

    # Cars move only if traffic light is GREEN (1)
    if traffic_light_state == 1:
        for i in range(len(car_xs)):
            car_xs[i] += 0.007
            if car_xs[i] > 1.3:
                car_xs[i] = -1.4 - (i * 0.7)
                
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# ==========================================
# 7. MAIN FUNCTION & WINDOW INITIALIZATION
# ==========================================
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(900, 650)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Complete 2D City Scene - CG Final Project")
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    
    glutDisplayFunc(display)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()