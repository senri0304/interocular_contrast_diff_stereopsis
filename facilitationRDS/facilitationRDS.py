# -*- coding: utf-8 -*-
import os, pyglet, time, datetime, random, copy, math
from pyglet.gl import *
from pyglet.image import AbstractImage
from collections import deque
import pandas as pd
import numpy as np
import display_info

# Prefernce
# ------------------------------------------------------------------------
rept = 5
exclude_mousePointer = False
# ------------------------------------------------------------------------

# Get display information
display = pyglet.canvas.get_display()
screens = display.get_screens()
win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
win.set_fullscreen(fullscreen=True, screen=screens[len(screens)-1])  # Present secondary display
win.set_exclusive_mouse(exclude_mousePointer)  # Exclude mouse pointer
key = pyglet.window.key

# Load variable conditions
deg1 = display_info.deg1
cntx = screens[len(screens)-1].width / 2  # Store center of screen about x position
cnty = screens[len(screens)-1].height / 3  # Store center of screen about y position
dat = pd.DataFrame()
iso = 8
draw_objects = []  # 描画対象リスト
end_routine = False  # Routine status to be exitable or not
tc = 0  # Count transients
tcs = []  # Store transients per trials
kud_list = []  # Store durations of key pressed
cdt = []  # Store sum(kud), cumulative reaction time on a trial.
mdt = []
dtstd = []
exitance = True
n = 0

# Load resources
p_sound = pyglet.resource.media('materials/840Hz.wav', streaming=False)
beep_sound = pyglet.resource.media('materials/460Hz.wav', streaming=False)
pedestal: AbstractImage = pyglet.image.load('materials/pedestal.png')
fixr = pyglet.sprite.Sprite(pedestal, x=cntx+iso*deg1-pedestal.width/2.0, y=cnty-pedestal.height/2.0)
fixl = pyglet.sprite.Sprite(pedestal, x=cntx-iso*deg1-pedestal.width/2.0, y=cnty-pedestal.height/2.0)

file_names = copy.copy(display_info.variation)*rept*2
file_names.extend([200, 200])
r = random.randint(0, math.factorial(len(file_names)))
random.seed(r)
sequence = random.sample(file_names, len(file_names))


num = list(np.repeat(range(1, rept+1), len(display_info.variation)))*2
num.extend([1, 1])
random.seed(r)
sequence2 = random.sample(num, len(file_names))
print(sequence)
print(sequence2)

complementary = list(np.repeat([0, 1], len(display_info.variation)*rept))
complementary.extend([0, 1])
random.seed(r)
sequence3 = random.sample(complementary, len(file_names))
print(sequence3)

# ----------- Core program following ----------------------------

# A getting key response function
class key_resp(object):
    def on_key_press(self, symbol, modifiers):
        global tc, exitance, trial_start
        if exitance == False and symbol == key.DOWN:
            kd.append(time.time())
            tc = tc + 1
        if exitance == True and symbol == key.UP:
            p_sound.play()
            exitance = False
            pyglet.clock.schedule_once(delete, 30.0)
            replace()
            trial_start = time.time()
        if symbol == key.ESCAPE:
            win.close()
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        global tc
        if exitance == False and symbol == key.DOWN:
            ku.append(time.time())
            tc = tc + 1


resp_handler = key_resp()


# Store objects into draw_objects
def fixer():
    draw_objects.append(fixl)
    draw_objects.append(fixr)


def replace():
    del draw_objects[:]
    fixer()
    draw_objects.append(R)
    draw_objects.append(L)


# A end routine function
def exit_routine(dt):
    global exitance
    exitance = True
    beep_sound.play()
    prepare_routine()
    fixer()
    pyglet.app.exit()


@win.event
def on_draw():
    # Refresh window
    win.clear()
    # 描画対象のオブジェクトを描画する
    for draw_object in draw_objects:
        draw_object.draw()


# Remove stimulus
def delete(dt):
    global n, trial_end
    del draw_objects[:]
    p_sound.play()
    n += 1
    pyglet.clock.schedule_once(get_results, 1.0)
    trial_end = time.time()


def get_results(dt):
    global ku, kud, kd, kud_list, mdt, dtstd, n, tc, tcs, trial_end, trial_start, sequence, file_names
    ku.append(trial_start + 30.0)
    while len(kd) > 0:
        kud.append(ku.popleft() - kd.popleft() + 0)  # list up key_press_duration
    kud_list.append(str(kud))
    c = sum(kud)
    cdt.append(c)
    tcs.append(tc)
    if kud == []:
        kud.append(0)
    m = np.mean(kud)
    d = np.std(kud)
    mdt.append(m)
    dtstd.append(d)
    print('--------------------------------------------------')
    print('trial: ' + str(n) + '/' + str(len(file_names)))
    print('start: ' + str(trial_start))
    print('end: ' + str(trial_end))
    print('key_pressed: ' + str(kud))
    print('transient counts: ' + str(tc))
    print('cdt: ' + str(c))
    print('mdt: ' + str(m))
    print('dtstd: ' + str(d))
    print('condition: ' + str(sequence[n-1]) + ', ' + str(sequence3[n-1]))
    print('--------------------------------------------------')
    # Check the experiment continue or break
    if n != len(file_names):
        pyglet.clock.schedule_once(exit_routine, 29.0)
    else:
        p_sound.play()
        pyglet.app.exit()


def set_polygon():
    global L, R, sequence, n
    # Set up polygon for stimulus
    R = pyglet.resource.image('stereograms/' + str(sequence2[n]) +
                              'rds' + str(sequence[n]) + 'R' + str(sequence3[n]) + '.png')
    R = pyglet.sprite.Sprite(R)
    R.x = cntx + deg1 * iso - R.width / 2.0
    R.y = cnty - R.height / 2.0
    L = pyglet.resource.image('stereograms/' + str(sequence2[n]) +
                              'rds' + str(sequence[n]) + 'L' + str(sequence3[n]) + '.png')
    L = pyglet.sprite.Sprite(L)
    L.x = cntx - deg1 * iso - L.width / 2.0
    L.y = cnty - L.height / 2.0


def prepare_routine():
    global n, file_names
    if n < len(file_names):
        fixer()
        set_polygon()
    else:
        pass


# Store the start time
start = time.time()
win.push_handlers(resp_handler)

fixer()
set_polygon()


for i in sequence:
    tc = 0  # Count transients
    ku = deque([])  # Store unix time when key up
    kd = deque([])  # Store unix time when key down
    kud = []  # Differences between kd and ku

    pyglet.app.run()

# -------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({'trial': list(range(1, len(file_names)+1)),  # Store variance_A conditions
                        'luminance': sequence,
                        'repetition': sequence2,
                        'complementary': sequence3,
                        'transient_counts': tcs,  # Store transient_counts
                        'cdt': cdt,  # Store cdt(target values) and input number of trials
                        'mdt': mdt,
                        'dtstd': dtstd,
                        'key_press_list': kud_list})  # Store the key_press_duration list

os.makedirs('data', exist_ok=True)

name = str(daten)
name = name.replace(":", "'")
results.to_csv(path_or_buf='./data/DATE' + name + '.csv', index=False)  # Output experimental data

# Output following to shell, check this experiment
print(u'開始日時: ' + str(start))
print(u'終了日時: ' + str(end_time))
print(u'経過時間: ' + str(end_time - start))