# -*- coding: utf-8 -*-
import sys, os, pyglet, time, datetime, random
from pyglet.gl import *
from collections import deque
import pandas as pd
import numpy as np

# Prefernce
# ------------------------------------------------------------------------
use_scr = 1
rept = 1
test_x = -1  # If test_x = 1, rds have uncross disparity
exclude_mousePointer = False
# ------------------------------------------------------------------------

# Get display informations
display = pyglet.canvas.get_display()
screens = display.get_screens()
win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
win.set_fullscreen(fullscreen=True, screen=screens[use_scr])  # Present secondary display
win.set_exclusive_mouse(exclude_mousePointer)  # Exclude mouse pointer
key = pyglet.window.key

# Load variable conditions
dat = pd.DataFrame()
deg1 = 43.0  # 1 deg = 43 pix at LEDCinemaDisplay made by Apple
am42 = 30.0  # 42 arcmin = 30 pix
iso = 7.0
cntx = screens[use_scr].width / 2  # Store center of screen about x positon
cnty = screens[use_scr].height / 3  # Store center of screen about y position
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

# Load sound resource
p_sound = pyglet.resource.media("button57.mp3", streaming=False)
beep_sound = pyglet.resource.media("p01.mp3", streaming=False)
fixation = pyglet.image.load("fixationPoint.png")
fixr = pyglet.sprite.Sprite(fixation, x=cntx+iso*deg1-fixation.width/2.0+2, y=cnty-fixation.height/2.0-50)
fixl = pyglet.sprite.Sprite(fixation, x=cntx-iso*deg1-fixation.width/2.0+2, y=cnty-fixation.height/2.0-50)

files = next(os.walk("material"))[2]
file_num = int((len(files) - 1) / 2)
ran_num = random.sample(list(range(0, file_num)), file_num)
print(ran_num)


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
            pyglet.clock.schedule_once(Get_results, 31.0)
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
    draw_objects.append(R)
    draw_objects.append(L)
    fixer()


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
    global n, dl, trial_end
    del draw_objects[:]
    p_sound.play()
    n += 1
    pyglet.clock.schedule_once(exit_routine, 30.0)
    trial_end = time.time()


def Get_results(dt):
    global ku, kud, kd, kud_list, mdt, dtstd, n, tc, tcs, trial_end, trial_start, ran_num, file_num
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
    print("--------------------------------------------------")
    print("trial: " + str(n) + "/" + str(file_num))
    print("start: " + str(trial_start))
    print("end: " + str(trial_end))
    print("key_pressed: " + str(kud))
    print("transient counts: " + str(tc))
    print("cdt: " + str(c))
    print("mdt: " + str(m))
    print("dtstd: " + str(d))
    print("condition: " + str(ran_num[n - 1]))
    print("--------------------------------------------------")
    # Check the experiment continue or break
    if n == file_num:
        pyglet.app.exit()


def prepare_routine():
    global n, dat, R, L, ran_num, file_num
    if n < file_num:
        # Set up polygon for stimulus
        R = pyglet.resource.image("material/rds" + str(ran_num[n]) + "R.jpg")
        R = pyglet.sprite.Sprite(R)
        R.x = cntx + deg1 * iso - R.width / 2.0
        R.y = cnty - R.height / 2.0
        L = pyglet.resource.image("material/rds" + str(ran_num[n]) + "L.jpg")
        L = pyglet.sprite.Sprite(L)
        L.x = cntx - deg1 * iso - L.width / 2.0
        L.y = cnty - L.height / 2.0
        fixer()
    else:
        pass


# Store the start time
start = time.time()
win.push_handlers(resp_handler)

# Set up polygon for stimulus
R = pyglet.resource.image("material/rds" + str(ran_num[n]) + "R.jpg")
R = pyglet.sprite.Sprite(R)
R.x = cntx + deg1 * iso - R.width / 2.0
R.y = cnty - R.height / 2.0
L = pyglet.resource.image("material/rds" + str(ran_num[n]) + "L.jpg")
L = pyglet.sprite.Sprite(L)
L.x = cntx - deg1 * iso - L.width / 2.0
L.y = cnty - L.height / 2.0

for i in range(file_num):
    tc = 0  # Count transients
    ku = deque([])  # Store unix time when key up
    kd = deque([])  # Store unix time when key down
    kud = []  # Differences between kd and ku

    fixer()

    pyglet.app.run()

# -------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({"trial": ran_num,  # Store variance_A conditions
                        "transient_counts": tcs,  # Store transient_counts
                        "cdt": cdt,  # Store cdt(target values) and input number of trials
                        "mdt": mdt,
                        "dtstd": dtstd,
                        "key_press_list": kud_list})  # Store the key_press_duration list

os.makedirs("data", exist_ok=True)

name = str(daten)
name = name.replace(":", "'")
results.to_csv(path_or_buf="./data/DATE" + name + ".csv", index=False)  # Output experimental data

# Output following to shell, check this experiment
print(u"開始日時: " + str(start))
print(u"終了日時: " + str(end_time))
print(u"経過時間: " + str(end_time - start))