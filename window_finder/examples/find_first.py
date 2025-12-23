from window_finder import create_window_finder

finder = create_window_finder()

win = finder.find_first("BlueStacks")
if not win:
    print("Not found")
    raise SystemExit

print("Title:", win.title)
print("LT:", win.left_top)                       # (left, top)
print("LTWH:", win.left_top_width_height)        # (left, top, width, height)
print("LTRB:", win.rect_ltrb)                    # (left, top, right, bottom)
print("PID:", win.pid)
print("native_id:", win.native_id)
