import turtle
import math
import random

# Setup
screen = turtle.Screen()
screen.setup(width=1000, height=1000)
screen.bgcolor("black")
screen.title("Cosmic Spiral Galaxy")
screen.tracer(0)

# Create multiple turtles for different effects
particles = []
for i in range(8):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(2)
    particles.append(t)

# Central star
star = turtle.Turtle()
star.hideturtle()
star.speed(0)

def draw_star(x, y, size, color):
    """Draw a glowing star"""
    star.penup()
    star.goto(x, y)
    star.pendown()
    
    # Outer glow
    for i in range(3):
        star.color(color)
        star.dot(size - i * (size // 4))

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB (h: 0-360, s: 0-1, v: 0-1)"""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (r + m, g + m, b + m)

def spiral_galaxy(frame):
    """Create animated spiral galaxy with particles"""
    screen.clear()
    screen.bgcolor("black")
    
    # Draw central glow
    draw_star(0, 0, 30, "#FFD700")
    draw_star(0, 0, 20, "#FFF8DC")
    
    # Parameters
    num_arms = 5
    particles_per_arm = 80
    rotation = frame * 0.5
    pulse = math.sin(frame * 0.05) * 0.2 + 1
    
    # Draw spiral arms
    for arm in range(num_arms):
        arm_angle = (360 / num_arms) * arm + rotation
        
        for i, particle in enumerate(range(particles_per_arm)):
            # Calculate position
            angle_offset = particle * 4
            angle = math.radians(arm_angle + angle_offset)
            
            # Fibonacci-like spiral
            radius = (particle * 5) * pulse
            
            # Add some randomness for organic feel
            radius += math.sin(frame * 0.1 + particle * 0.1) * 3
            
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            # Calculate color based on position
            hue = (arm_angle + angle_offset + frame * 2) % 360
            saturation = 0.8
            value = 1 - (particle / particles_per_arm) * 0.5
            
            r, g, b = hsv_to_rgb(hue, saturation, value)
            color = (r, g, b)
            
            # Draw particle with glow effect
            t = particles[arm % len(particles)]
            t.penup()
            t.goto(x, y)
            
            # Size based on distance from center
            size = max(2, 8 - (particle / particles_per_arm) * 6)
            
            # Glow effect
            t.color(color)
            t.dot(size + 2)
            
            # Add some stars in the background
            if particle % 10 == 0 and random.random() > 0.7:
                t.dot(2)
    
    # Add nebula clouds
    for _ in range(15):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(100, 400)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        hue = (frame * 3 + random.uniform(0, 60)) % 360
        r, g, b = hsv_to_rgb(hue, 0.4, 0.6)
        
        star.penup()
        star.goto(x, y)
        star.color(r, g, b)
        star.dot(random.randint(20, 40))
    
    # Add distant stars
    for _ in range(50):
        x = random.randint(-500, 500)
        y = random.randint(-500, 500)
        star.penup()
        star.goto(x, y)
        star.color("white")
        star.dot(random.choice([1, 1, 2]))
    
    screen.update()

# Animation loop
frame = 0
try:
    while True:
        spiral_galaxy(frame)
        frame += 1
        
        if frame > 360:
            frame = 0
            
except turtle.Terminator:
    pass