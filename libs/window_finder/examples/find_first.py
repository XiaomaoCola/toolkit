from libs.window_finder import create_window_finder

finder = create_window_finder()

win = finder.find_first("BlueStacks")
if not win:
    print("Not found")
    raise SystemExit

print("Title:", win.title)
print("LT:", win.window_left_top)                       # (left, top)
print("LTWH:", win.window_left_top_width_height)        # (left, top, width, height)
print("LTRB:", win.window_rect_ltrb)                    # (left, top, right, bottom)
print("PID:", win.pid)
print("native_id:", win.native_id)
