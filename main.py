import dashboard
import curses


def main(stdscr):
    dashboard.landing_page(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
