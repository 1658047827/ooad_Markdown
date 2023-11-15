import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main
import unittest
from unittest.mock import patch
from io import StringIO


class TestCase1(unittest.TestCase):
    @patch(
        "builtins.input",
        side_effect=[
            "load test1.md",
            "insert ## 程序设计",
            "append-head # 我的资源",
            "append-tail ### 软件设计",
            "append-tail #### 设计模式",
            "append-tail 1. 观察者模式",
            "append-tail 3. 单例模式",
            "insert 6 2. 策略模式",
            "delete 单例模式",
            "append-tail 3. 组合模式",
            "list-tree",
            "append-tail ## ⼯具箱",
            "append-tail ### Adobe",
            "list-tree",
            "save",
            "exit",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        self.maxDiff = None
        main.client()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            output,
            "Command Line Markdown Editing Tool\n"
            + "└── 我的资源\n"
            + "    └── 程序设计\n"
            + "        └── 软件设计\n"
            + "            └── 设计模式\n"
            + "                ├── 1. 观察者模式\n"
            + "                ├── 2. 策略模式\n"
            + "                └── 3. 组合模式\n"
            + "└── 我的资源\n"
            + "    ├── 程序设计\n"
            + "    │   └── 软件设计\n"
            + "    │       └── 设计模式\n"
            + "    │           ├── 1. 观察者模式\n"
            + "    │           ├── 2. 策略模式\n"
            + "    │           └── 3. 组合模式\n"
            + "    └── ⼯具箱\n"
            + "        └── Adobe",
        )

        with open("test1.md", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(
            content,
            "# 我的资源\n"
            + "## 程序设计\n"
            + "### 软件设计\n"
            + "#### 设计模式\n"
            + "1. 观察者模式\n"
            + "2. 策略模式\n"
            + "3. 组合模式\n"
            + "## ⼯具箱\n"
            + "### Adobe\n",
        )


class TestCase2(unittest.TestCase):
    @patch(
        "builtins.input",
        side_effect=[
            "load test2.md",
            "append-head # 旅行清单",
            "append-tail ## 亚洲",
            "append-tail 1. 中国",
            "append-tail 2. 日本",
            "delete 亚洲",
            "undo",
            "redo",
            "list-tree",
            "save",
            "exit",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        self.maxDiff = None
        main.client()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            output,
            "Command Line Markdown Editing Tool\n"
            + "└── 旅行清单\n"
            + "    ├── 1. 中国\n"
            + "    └── 2. 日本",
        )

        with open("test2.md", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, "# 旅行清单\n1. 中国\n2. 日本\n")


class TestCase3(unittest.TestCase):
    @patch(
        "builtins.input",
        side_effect=[
            "load test3.md",
            "append-head # 书籍推荐",
            "append-tail * 《深入理解计算机系统》",
            "undo",
            "append-tail ## 编程",
            "append-tail * 《设计模式的艺术》",
            "redo",
            "list-tree",
            "append-tail * 《云原生：运用容器、函数计算和数据构建下一代应用》",
            "append-tail * 《深入理解Java虚拟机》",
            "undo",
            "redo",
            "list-tree",
            "save",
            "exit",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        self.maxDiff = None
        main.client()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            output,
            "Command Line Markdown Editing Tool\n"
            + "No command to redo.\n"
            + "└── 书籍推荐\n"
            + "    └── 编程\n"
            + "        └── · 《设计模式的艺术》\n"
            + "└── 书籍推荐\n"
            + "    └── 编程\n"
            + "        ├── · 《设计模式的艺术》\n"
            + "        ├── · 《云原生：运用容器、函数计算和数据构建下一代应用》\n"
            + "        └── · 《深入理解Java虚拟机》",
        )

        with open("test3.md", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(
            content,
            "# 书籍推荐\n"
            + "## 编程\n"
            + "* 《设计模式的艺术》\n"
            + "* 《云原生：运用容器、函数计算和数据构建下一代应用》\n"
            + "* 《深入理解Java虚拟机》\n",
        )


class TestCase4(unittest.TestCase):
    @patch(
        "builtins.input",
        side_effect=[
            "load test4.md",
            "append-head # 旅行清单",
            "append-tail ## 亚洲",
            "ws",
            "save",
            "append-tail 1. 中国",
            "load test3.md",
            "list-tree",
            "ws",
            "append-tail * 《软件工程》",
            "switch 1",
            "save",
            "switch 2",
            "close 2",
            "n",
            "ws",
            "exit",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        self.maxDiff = None
        main.client()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            output,
            "Command Line Markdown Editing Tool\n"
            + "1 test4.md*<\n"
            + "└── 书籍推荐\n"
            + "    └── 编程\n"
            + "        ├── · 《设计模式的艺术》\n"
            + "        ├── · 《云原生：运用容器、函数计算和数据构建下一代应用》\n"
            + "        └── · 《深入理解Java虚拟机》\n"
            + "1 test4.md*\n"
            + "2 test3.md<\n"
            + "1 test4.md<",
        )

        with open("test4.md", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, "# 旅行清单\n## 亚洲\n1. 中国\n")


class TestCase5(unittest.TestCase):
    @patch(
        "builtins.input",
        side_effect=[
            "load test5.md",
            "append-head # 旅行清单",
            "append-tail ## 欧洲",
            "insert 2 ## 亚洲",
            "insert 3 1. 中国",
            "insert 4 2. 日本",
            "save",
            "undo",
            "list-tree",
            "delete 亚洲",
            "list-tree",
            "history 2",
            "undo",
            "list-tree",
            "redo",
            "list-tree",
            "redo",
            "list-tree",
            "save",
            "exit",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        self.maxDiff = None
        main.client()
        output = mock_stdout.getvalue().strip()

        with open("history.log", "r", encoding="utf-8") as log:
            log_entries = log.readlines()

        self.assertEqual(
            output,
            "Command Line Markdown Editing Tool\n"
            + "No command to undo.\n"
            + "└── 旅行清单\n"
            + "    ├── 亚洲\n"
            + "    │   ├── 1. 中国\n"
            + "    │   └── 2. 日本\n"
            + "    └── 欧洲\n"
            + "└── 旅行清单\n"
            + "    ├── 1. 中国\n"
            + "    ├── 2. 日本\n"
            + "    └── 欧洲\n"
            + f"{log_entries[-9]}"
            + f"{log_entries[-10]}"
            + "└── 旅行清单\n"
            + "    ├── 亚洲\n"
            + "    │   ├── 1. 中国\n"
            + "    │   └── 2. 日本\n"
            + "    └── 欧洲\n"
            + "└── 旅行清单\n"
            + "    ├── 1. 中国\n"
            + "    ├── 2. 日本\n"
            + "    └── 欧洲\n"
            + "No command to redo.\n"
            + "└── 旅行清单\n"
            + "    ├── 1. 中国\n"
            + "    ├── 2. 日本\n"
            + "    └── 欧洲",
        )

        with open("test5.md", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, "# 旅行清单\n1. 中国\n2. 日本\n## 欧洲\n")


def clean():
    if os.path.exists("history.log"):
        os.remove("history.log")
    if os.path.exists("stats.log"):
        os.remove("stats.log")
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith(".md"):
            file_path = os.path.join(current_directory, filename)
            os.remove(file_path)


if __name__ == "__main__":
    clean()
    unittest.main()
