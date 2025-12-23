```
window_finder/
├── pyproject.toml                 # 后面发包用
├── README.md
└── src/
    └── window_finder/
        ├── __init__.py
        ├── models.py
        ├── protocol.py
        ├── errors.py
        ├── factory.py
        └── backends/
            ├── __init__.py
            └── win32.py
```

由于README.md里应该放最小示例。
所以给出如下代码作为用法参考。
```python
from window_finder import create_window_finder
finder = create_window_finder()
win = finder.find_first("BlueStacks")
```

这个包的设计就是未来要扩张成多系统下的。