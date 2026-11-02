from controller import Robot, Keyboard

robot = Robot()
timestep = int(robot.getBasicTimeStep())

keyboard = robot.getKeyboard()
keyboard.enable(timestep)

UP_DELTA   = 1.0
DOWN_DELTA = 1.0
TURN_STEP  = 0.25
MAX_SPEED  = 6.28
MAX_DIFF   = 2.0

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = (
    Keyboard.UP, Keyboard.DOWN, Keyboard.LEFT, Keyboard.RIGHT, ord(' ')
)

lm = robot.getDevice('left wheel motor')
rm = robot.getDevice('right wheel motor')
lm.setPosition(float('inf'))
rm.setPosition(float('inf'))

ls = rs = 0.0

while robot.step(timestep) != -1:
    key = keyboard.getKey()
    while key != -1:
        if   key == KEY_UP:
            ls += UP_DELTA
            rs += UP_DELTA
        elif key == KEY_DOWN:
            ls -= DOWN_DELTA
            rs -= DOWN_DELTA
        elif key == KEY_RIGHT:
            if ls + TURN_STEP <= MAX_SPEED:
                ls += TURN_STEP
            else:
                rs = max(-MAX_SPEED, rs - TURN_STEP)
        elif key == KEY_LEFT:
            if rs + TURN_STEP <= MAX_SPEED:
                rs += TURN_STEP
            else:
                ls = max(-MAX_SPEED, ls - TURN_STEP)
        elif key == KEY_SPACE:
            ls = rs = 0.0
        key = keyboard.getKey()

    ls = max(-MAX_SPEED, min(MAX_SPEED, ls))
    rs = max(-MAX_SPEED, min(MAX_SPEED, rs))
    d = ls - rs
    if   d >  MAX_DIFF: ls = rs + MAX_DIFF
    elif d < -MAX_DIFF: ls = rs - MAX_DIFF

    lm.setVelocity(ls)
    rm.setVelocity(rs)