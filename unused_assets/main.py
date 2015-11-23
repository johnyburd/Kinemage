# Python Cocos2d Game Development
# Part 1: Getting Started

# Tutorial: http://jpwright.net/writing/python-cocos2d-game-1/
# Github: http://github.com/jpwright/cocos2d-python-tutorials

# Jason Wright (jpwright0@gmail.com)


# Imports

import pyglet
from pyglet.window import key

import cocos
from cocos import actions, layer, sprite, scene
from cocos.director import director


# Player class
direction = 0 
class Me(actions.Move):

  
  # step() is called every frame.
  # dt is the number of seconds elapsed since the last call.
  def step(self, dt):
    
    super(Me, self).step(dt) # Run step function on the parent class.
    
    # Determine velocity based on keyboard inputs.
    if keyboard[key.RIGHT] > keyboard[key.LEFT]:
      direction = 0
      print("up here dummy")
    else:
      direction = 1

    velocity_x = 100 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
    velocity_y = 100 * (keyboard[key.UP] - keyboard[key.DOWN])
    
    # Set the object's velocity.
    self.target.velocity = (velocity_x, velocity_y)

    player_layer = layer.Layer()
    if direction == 0:
      print("0")
      me = sprite.Sprite('standing.png', scale=1.0)
    else:
      print('1')
      me = sprite.Sprite('standingleft.png', scale=2.0)
    player_layer.add(me)
    
# Main class

def main():
  global keyboard # Declare this as global so it can be accessed within class methods.
  
  # Initialize the window.
  director.init(width=500, height=300, resizable=True)
  
  # Create a layer and add a sprite to it.
  player_layer = layer.Layer()
  if direction == 0:
    print("0")
    me = sprite.Sprite('standing.png', scale=1.0)
  else:
    print('1')
    me = sprite.Sprite('standingleft.png', scale=1.0)
  player_layer.add(me)
  
  # Set initial position and velocity.
  me.position = (100, 100)
  me.velocity = (0, 0)
  
  # Set the sprite's movement class.
  me.do(Me())

  # Create a scene and set its initial layer.
  main_scene = scene.Scene(player_layer)

  # Attach a KeyStateHandler to the keyboard object.
  keyboard = key.KeyStateHandler()
  director.window.push_handlers(keyboard)

  # Play the scene in the window.
  director.run(main_scene)



if __name__ == '__main__':
    main()
