
import turtle
import math
import random
import time
from collections import deque

# ----------------------------
# Helper functions & settings
# ----------------------------
WIDTH, HEIGHT = 1000, 700
BG_COLOR = "black"
FPS_BASE = 60

def hsv_to_rgb(h, s, v):
    """Return (r,g,b) in 0..1 for turtle.color usage; h in [0,1]."""
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return (r, g, b)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(max(0, min(1, c)) * 255) for c in rgb)

# ----------------------------
# Setup screen & global state
# ----------------------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor(BG_COLOR)
screen.title("Spectacle — Turtle Animation")
screen.tracer(0, 0)  # manage updates manually for smooth animation

# control state
paused = False
speed_multiplier = 1.0

def toggle_pause():
    global paused
    paused = not paused

def speed_up():
    global speed_multiplier
    speed_multiplier = min(4.0, speed_multiplier * 1.25)

def slow_down():
    global speed_multiplier
    speed_multiplier = max(0.1, speed_multiplier / 1.25)

def restart():
    global paused, speed_multiplier
    paused = False
    speed_multiplier = 1.0
    for t in all_turtles:
        t.clear()
    particle_system.clear()
    setup_scene()

def quit_program():
    turtle.bye()

# keyboard bindings
screen.listen()
screen.onkey(toggle_pause, "space")
screen.onkey(speed_up, "Up")
screen.onkey(slow_down, "Down")
screen.onkey(restart, "r")
screen.onkey(quit_program, "q")
screen.onkey(quit_program, "Escape")

# ----------------------------
# Create drawing turtles
# ----------------------------
all_turtles = []

def make_turtle(visible=False, speed=0):
    t = turtle.Turtle(visible)
    t.hideturtle()
    t.speed(speed)
    t.penup()
    all_turtles.append(t)
    return t

spiro_t = make_turtle()
mandala_t = make_turtle()
tree_t = make_turtle()
fire_t = make_turtle()

# ----------------------------
# Spirograph / Kaleidoscope
# ----------------------------
class Spiro:
    def __init__(self, t, cx, cy):
        self.t = t
        self.cx = cx
        self.cy = cy
        self.phase = random.random() * 2 * math.pi
        self.rotation = random.uniform(-0.002, 0.002)
        self.a = random.randint(40, 140)   # circle size param
        self.b = random.randint(10, 120)   # circle size param
        self.k = random.uniform(0.2, 0.9)  # ratio
        self.hue = random.random()
        self.line_width = random.randint(1, 3)
        self.angle = 0

    def step(self, dt):
        self.angle += 0.8 * dt
        r = self.a * (1 - self.k) / (1 + self.k) + self.b * math.cos(self.angle)
        x = self.cx + r * math.cos(self.angle + self.phase)
        y = self.cy + r * math.sin(self.angle + self.phase)
        # dynamic color using hue shift
        hue = (self.hue + 0.08 * math.sin(self.angle * 0.07) + 0.5 * dt) % 1.0
        color = rgb_to_hex(hsv_to_rgb(hue, 0.9, 0.95))
        self.t.goto(x, y)
        self.t.pendown()
        self.t.pensize(self.line_width)
        self.t.pencolor(color)
        # draw a short motion line for trailing effect
        self.t.forward(2 + math.sin(self.angle * 0.3) * 1.5)
        self.t.penup()

# ----------------------------
# Rotating mandala reflections
# ----------------------------
class Mandala:
    def __init__(self, t, cx=0, cy=0, petals=8):
        self.t = t
        self.cx = cx
        self.cy = cy
        self.petals = petals
        self.time = 0
        self.hue = random.random()

    def step(self, dt):
        self.time += dt * 0.6
        R = 200 + 60 * math.sin(self.time * 0.12)
        pet = self.petals
        for i in range(pet):
            angle = self.time + (2 * math.pi / pet) * i
            x = self.cx + R * math.cos(angle)
            y = self.cy + R * math.sin(angle)
            subr = 40 + 20 * math.sin(self.time * 0.6 + i)
            # color per petal
            hue = (self.hue + i / pet + 0.1 * math.sin(self.time * 0.3)) % 1.0
            color = rgb_to_hex(hsv_to_rgb(hue, 0.8, 0.95))
            self.t.goto(self.cx, self.cy)
            self.t.pendown()
            self.t.pensize(2)
            self.t.pencolor(color)
            # petal as an arch
            for s in range(12):
                a = angle + (s / 12.0 - 0.5) * 0.8
                px = self.cx + (R + subr * math.cos(s * 0.6)) * math.cos(a)
                py = self.cy + (R + subr * math.cos(s * 0.6)) * math.sin(a)
                self.t.goto(px, py)
            self.t.penup()

# ----------------------------
# Recursive glowing tree
# ----------------------------
def draw_glowing_branch(t, x, y, angle, length, level, hue):
    if length < 6 or level <= 0:
        return
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.pendown()
    # color & width based on level
    width = max(1, level / 1.2)
    color = rgb_to_hex(hsv_to_rgb(hue % 1.0, 0.7, 0.92))
    t.pensize(width)
    t.pencolor(color)
    # draw trunk with small jitter for organic feel
    t.forward(length * (0.9 + 0.2 * random.random()))
    nx, ny = t.position()
    # recursive branching
    nlen = length * (0.62 + 0.06 * random.random())
    branch_count = 2 if level < 3 else 3
    for i in range(branch_count):
        na = angle + random.uniform(-35, 35) * (1.0 - level * 0.05)
        nhue = hue + 0.02 * random.random() + 0.01 * i
        draw_glowing_branch(t, nx, ny, na, nlen, level - 1, nhue)

def recursive_tree(t, cx, cy, time_offset):
    # "breathing" hue shift
    base_hue = (0.08 * math.sin(time_offset * 0.3) + 0.07) % 1.0
    # trunk start
    t.penup()
    t.goto(cx, cy - 60)
    t.setheading(90)
    t.pendown()
    t.pensize(6)
    t.pencolor(rgb_to_hex(hsv_to_rgb(base_hue, 0.6, 0.9)))
    t.forward(40)
    # start recursive branches
    draw_glowing_branch(t, t.xcor(), t.ycor(), 90, 80, 5, base_hue)

# ----------------------------
# Fireworks / Particle System
# ----------------------------
class Particle:
    def __init__(self, x, y, vx, vy, hue, lifespan=1.8):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.hue = hue
        self.age = 0.0
        self.lifespan = lifespan

    def alive(self):
        return self.age < self.lifespan

    def step(self, dt):
        # gravity & drag
        self.vy -= 160 * dt
        self.vx *= (1 - 0.02 * dt)
        self.vy *= (1 - 0.005 * dt)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.age += dt

class ParticleSystem:
    def __init__(self, t):
        self.t = t
        self.particles = []
        self.last_launch = 0.0

    def launch_firework(self, cx=0, cy=-200):
        # shoot up then explode (simulate by immediate explosion for visual)
        hue = random.random()
        count = random.randint(30, 90)
        speed = random.uniform(80, 260)
        for i in range(count):
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(0.2, 1.0) * speed
            vx = math.cos(a) * sp
            vy = math.sin(a) * sp
            self.particles.append(Particle(cx, cy + random.uniform(50, 200), vx, vy, (hue + random.uniform(-0.05, 0.05)) % 1.0, lifespan=1.4 + random.random()))
        self.last_launch = time.time()

    def step(self, dt):
        # occasionally launch fireworks
        now = time.time()
        if now - self.last_launch > random.uniform(0.6, 1.8):
            # random location across screen width
            lx = random.uniform(-WIDTH * 0.35, WIDTH * 0.35)
            self.launch_firework(lx, -180)
        # step particles
        alive = []
        for p in self.particles:
            p.step(dt)
            if p.alive() and -WIDTH < p.x < WIDTH and -HEIGHT < p.y < HEIGHT:
                alive.append(p)
        self.particles = alive

    def draw(self):
        # paint particles as small dots with fading
        t = self.t
        for p in self.particles:
            alpha = max(0.0, 1.0 - p.age / p.lifespan)
            bri = 0.6 + 0.4 * alpha
            col = rgb_to_hex(hsv_to_rgb(p.hue, 0.9, bri))
            t.goto(p.x, p.y)
            t.pencolor(col)
            t.dot(3 + 4 * alpha)

    def clear(self):
        self.particles.clear()

# ----------------------------
# Scene setup & main loop
# ----------------------------
spiro_list = []
mandala = None
particle_system = ParticleSystem(fire_t)

def setup_scene():
    global spiro_list, mandala
    # clear canvas
    for t in all_turtles:
        t.clear()
        t.penup()
    spiro_list = [Spiro(spiro_t, 0, 0) for _ in range(6)]
    mandala = Mandala(mandala_t, 0, 0, petals=12)
    # draw a faint central glow once
    mandala_t.goto(0, -10)
    mandala_t.dot(260, "#0a0a0a")
    # initial tree
    tree_t.clear()
    recursive_tree(tree_t, -320, -180, time.time() * 0.6)

setup_scene()

last_time = time.time()
frame = 0

def step():
    global last_time, frame
    now = time.time()
    dt = (now - last_time) * speed_multiplier
    last_time = now
    if paused:
        # still update the clock but do nothing visual
        screen.ontimer(step, 30)
        return

    # fade previous drawings slightly by overlaying translucent rectangles using dots
    # (use many dots to create a subtle trailing effect)
    # For performance: do a small partial fade each frame
    if frame % 3 == 0:
        # draw a faint black translucent rectangle with very low alpha effect
        # approximate by drawing many near-black dots across screen edges (cheap)
        fade = spiro_t
        fade.penup()
        for i in range(10):
            x = random.uniform(-WIDTH/2, WIDTH/2)
            y = random.uniform(-HEIGHT/2, HEIGHT/2)
            fade.goto(x, y)
            fade.dot(12, "#000000")

    # clear turtles' immediate drawings and redraw current frame elements
    spiro_t.clear()
    mandala_t.clear()
    tree_t.clear()
    fire_t.clear()

    # Spiro steps
    for sp in spiro_list:
        sp.phase += sp.rotation * dt * 60
        sp.step(dt)

    # Mandala
    mandala.step(dt)

    # Tree (recompute subtle changes to make it "breathe")
    recursive_tree(tree_t, -320, -160, now * 0.8)

    # Update particles
    particle_system.step(dt)
    particle_system.draw()

    # small central rotating mini-mandalas for extra pop
    for i in range(6):
        ang = now * (0.3 + 0.05 * i) + i
        x = 320 * math.cos(ang * 0.7) * 0.35
        y = 120 * math.sin(ang * 0.8) * 0.7 + 40 * math.sin(ang * 0.3)
        mandala_t.goto(x, y)
        hue = (0.55 + 0.1 * math.sin(now * 0.2 + i)) % 1.0
        mandala_t.dot(18, rgb_to_hex(hsv_to_rgb(hue, 0.9, 0.95)))

    # center pulsing signature
    spiro_t.goto(0, 0)
    pulse_color = rgb_to_hex(hsv_to_rgb((0.1 + 0.07 * math.sin(now * 0.8)) % 1.0, 0.9, 0.96))
    spiro_t.dot(48 + 20 * abs(math.sin(now * 0.9)), pulse_color)

    # final update
    screen.update()
    frame += 1
    # schedule next frame with interval depending on FPS_BASE and speed_multiplier
    interval = int(max(8, 1000 / (FPS_BASE * min(3.0, speed_multiplier))))  # ms
    screen.ontimer(step, interval)

# start
step()
screen.done()
