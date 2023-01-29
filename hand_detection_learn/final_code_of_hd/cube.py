from ursina import *
import random


def camera_mov():
    if held_keys['q']:
        camera.position += (0, time.dt, 0)
    if held_keys['w']:
        camera.position -= (0, time.dt, 0)


random_ganaretor = random.Random()
print(str(random_ganaretor), random_ganaretor.random())
app = Ursina()

window.title = "Havit Game"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enable = True


def update():
    cube.rotation_y += time.dt * 100
    camera_mov()

    if held_keys['z']:
        cube.rotation_z += time.dt * 50
    if held_keys['x']:
        cube.rotation_x += time.dt * 50

    if held_keys['t']:
        red = random_ganaretor.random() * 255
        blue = random_ganaretor.random() * 255
        green = random_ganaretor.random() * 255
        cube.color = color.rgb(red, green, blue)


def input(key):
    if key == 'space':
        red = random_ganaretor.random() * 255
        blue = random_ganaretor.random() * 255
        green = random_ganaretor.random() * 255
        cube.color = color.rgb(red, green, blue)
    if held_keys['a']:
        cube.scale = cube.scale.x + 1
        print(cube.scale.x)


camera.rotation_x = 5
cube = Entity(model='cube', color=color.orange, scale=(2, 2, 2), texture='cube_texture')

app.run()
