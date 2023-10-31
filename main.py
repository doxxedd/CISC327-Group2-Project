import landingpage
import curses





def main(stdscr):   
    landingpage.landing_page(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
