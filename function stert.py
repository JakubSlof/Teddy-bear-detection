#program that starts function after specific key is pressed 
import keyboard

def test():
  print('sucess')
keyboard.add_hotkey('s',test)
keyboard.wait('s')
