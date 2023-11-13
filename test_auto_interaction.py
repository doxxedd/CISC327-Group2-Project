import curses
import threading
import time
import keyboard
import landingpage

def curses_main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'q' to quit")

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def keyboard_listener(stdscr):
    time.sleep(2)
    keyboard.write('test')
    time.sleep(2)
    keyboard.press_and_release("enter")


def main(stdscr):
    curses_thread = threading.Thread(target=landingpage.landing_page, args=(stdscr,))
    keyboard_thread = threading.Thread(target=keyboard_listener, args=(stdscr,))

    curses_thread.start()
    keyboard_thread.start()

    curses_thread.join()
    keyboard_thread.join()

if __name__ == "__main__":
    
    curses.wrapper(main)