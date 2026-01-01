# interaction-mouse

A small, reusable Python package for mouse interactions:
- click
- repeat click
- random click in a rectangle
- drag

This package is designed to be **a clean interaction layer**:
- ✅ mouse actions + target sampling
- ❌ NOT window finding / coordinate mapping
- ❌ NOT OCR/CV detection
- ❌ NOT workflow/state machine

## Install (dev)

```bash
pip install -e .
## Flexible inputs

`Clicker` accepts both dataclasses and simple tuples/lists:

- Point: `Point(x, y)` or `(x, y)` or `[x, y]`
- Rect: `Rect(l, t, r, b)` or `(l, t, r, b)` or `[l, t, r, b]`
- Button: `Button.LEFT/RIGHT/MIDDLE` or `"left"/"right"/"middle"` (also `"l"`, `"r"`, `"m"`)

Example:

```python
from interaction_mouse import Clicker

c = Clicker()
c.click((100, 200), button="left")
c.rand_click((10, 20, 200, 260), count=5, button="right")
c.drag([300, 400], [700, 420], duration=0.6, steps=30)
```

问：为什么要单独给一个 drivers/ 目录？
答：driver 只有两个 ≠ driver 很简单， driver 是“变化最快、风险最高、最容易被平台/环境推翻的一层”， 
所以哪怕现在只有两个，也必须单独关起来。

问：drives的功能具体是啥？
答：driver 是给鼠标提供最基础操作的一层。driver 的功能 = 把“抽象的鼠标动作”翻译成“某个具体库/系统能执行的真实操作”。