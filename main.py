import dashboard.py

def main(stdscr):
    dashboard.landing_page()


if __name__ == "__main__":
    curses.wrapper(main)
