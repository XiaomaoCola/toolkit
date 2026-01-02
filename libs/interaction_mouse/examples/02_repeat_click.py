from interaction_mouse import Clicker, Point, Button

if __name__ == "__main__":
    c = Clicker(click_delay=0.01, move_duration=(0.2 , 0.5))

    # Repeat click at fixed point
    c.clicks(
        Point(200, 200),
        count=10,
        interval=0.12,
        jitter_px=100,
        button=Button.LEFT,
    )
