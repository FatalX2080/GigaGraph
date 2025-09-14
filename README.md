# Giga Graph
[![Python Version](https://img.shields.io/badge/python-3.10%2B-brightgreen?logo=python)](https://www.python.org/)
![version](https://img.shields.io/badge/version-1.0.0-green)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Downloads](https://img.shields.io/github/downloads/FatalX2080/GigaGraph/total?logo=github&color=orange)

This tool assists with graph theory by helping you visualize structures and solve common problems. Also, if you find any error, write to her in the **issue** section. We will be supporting the project for a while. 

**Special thanks to [Vrudem](https://github.com/vrudem) - _creator of the core_ and [Zennerest](https://github.com/Zennerest) - _creator of the original idea_**

# ❗️Notification
 1. The program was created solely for familiarization with the topic "graphs"
 2. There may be errors in the program. We do not guarantee the correctness of the answers.
 3. Interface errors are also possible, so it's better to use the console version.

# 🚀Quick Start
Go to [release page](https://github.com/FatalX2080/GigaGraph/releases) and download last stable release.

# 🖥️Instalation 
### Poertry 
```
git clone https://github.com/FatalX2080/GigaGraph.git
poetry shell
poetry install
cd src
flet run main.py
```
### Pypi
```
git clone https://github.com/FatalX2080/GigaGraph.git
python3 -m venv .venv
source /.venv/bin/activate
pip install requirements.txt
cd src
python3 main.py
``` 
# 🌴 Project Tree
```
GigaGraph
├── config.py
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── gui
│   ├── __init__.py
│   ├── gui_cards.py
│   ├── gui.py
│   └── graph_draftsman.py
├── recognizer
│   ├── __init__.py
│   └── main.py
└── solvers
    ├── __init__.py
    ├── graph_gen.py
    ├── all_not_fixed.py
    ├── nx_core.py
    └── task_result_class.py

```

# 🌟 Features
| Feature          | Status  | Notes                        |
|------------------|:-------:|------------------------------|
| Image recognezing| ❄️      | I'm lazy. If you cv2 enjoyer send me note |
| Task 2 / 8       | ❄️      | Write to [Vrudem](https://github.com/vrudem) if you have any ideas|
| (non-) Python core | ❄️      | Сreate a fork and create new core |


