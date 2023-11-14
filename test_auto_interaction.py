import curses
import threading
import time
import keyboard
import landingpage




def keyboard_listener():
    time.sleep(2)
    keyboard.write('test')
    # time.sleep(2)
    keyboard.press_and_release("enter")
    keyboard.write('test')
    time.sleep(2)
    keyboard.press_and_release("enter")
    keyboard.press_and_release("enter")
    keyboard.write("test")
    keyboard.press_and_release("enter")
    keyboard.write("test")
    keyboard.press_and_release("enter")
    keyboard.press_and_release("enter")


def main(stdscr):
    # curses_thread = threading.Thread(landingpage.landing_page(stdscr))
    keyboard_thread = threading.Thread(target=keyboard_listener)
    # curses_thread.start()
    keyboard_thread.start()

    # curses_thread.join()
    keyboard_thread.join()
    landingpage.landing_page(stdscr)
    

if __name__ == "__main__":

    curses.wrapper(main)