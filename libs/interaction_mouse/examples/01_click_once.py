from interaction_mouse import Clicker, Point, Button

if __name__ == "__main__":
    c = Clicker(move_duration = (0.5 , 1))
    c.click(Point(200, 200), button=Button.LEFT, jitter_px=50)
