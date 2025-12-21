# toolkit

目前的文件结构
```
toolkit/
├── Renamer/
│   ├── renamer.py
│   └── renamer_gui.py
├── TreeDrawer/
│   ├── main.py
│   ├── README.md
│   ├── tree_generator.py
│   └── tree_gui.py
├── LICENSE
└── README.md
```


```
toolkit/
├── README.md
├── .gitignore
├── libs/
│   └── window_finder/
│       ├── pyproject.toml
│       └── src/window_finder/...
│   └── region_calculator/
├── apps/
│   ├── renamer/
│   ├── tree_drawer/
```

每个 app 自己是一个小项目，然后由于app可能会依赖libs里的库，所以跟libs分开，libs里面主要放我自己写的包。