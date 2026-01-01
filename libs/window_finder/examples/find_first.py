from window_finder import create_window_finder

finder = create_window_finder()

win = finder.find_first("BlueStacks")
if not win:
    print("Not found")
    raise SystemExit

print("Title:", win.title)
print("native_id:", win.native_id)
print("PID:", win.pid)

print("\n--- Window rect (外框 / GetWindowRect, screen coords) ---")
print("window LT:", win.window_left_top)                       # (left, top)
print("window LTWH:", win.window_left_top_width_height)        # (left, top, width, height)
print("window LTRB:", win.window_rect_ltrb)                    # (left, top, right, bottom)

print("\n--- Client rect (客户区 / GetClientRect+ClientToScreen, screen coords) ---")
print("client LT:", win.client_left_top)                       # (left, top)
print("client LTWH:", win.client_left_top_width_height)        # (left, top, width, height)
print("client LTRB:", win.client_rect_ltrb)                    # (left, top, right, bottom)
