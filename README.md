# Command Line Markdown Editing Tool

## 项目说明

2023年秋复旦大学《面向对象分析和设计》课程项目。

## 运行环境

使用 Python 3.9 环境运行，没有使用第三方库，只使用了 Python 标准库中的一些模块。

## 启动步骤

1. 安装 Python 3.9 环境，以 `conda` 为例：

   ```shell
   conda create -n ooad_Markdown python=3.9
   ```

2. 激活对应 Python 环境，并将工作路径切换至项目主目录下。

3. 使用 Python 运行 `main.py` 即可启动项目。

4. 将工作路径切换至 test 文件夹下，使用 Python 运行 `test.py` 即可进行自动化测试。

## 设计模式

### 命令模式

定义了 `Command` 基类，`Command` 是不能忽略，无法撤销重做的命令。同时有 `CanIgnoreCommand` 和 `CanUndoCommand` 类继承自 `Command` ，表示可被忽略的命令和可被撤销与重做的命令，其中仅有 `CanUndoCommand` 类需要实现 `undo` 方法。

具体的命令类全部继承自这三个类：

+ `LoadCommand`、`SaveCommand`、`SwitchCommand` 等具体命令继承自 `Command` ，是无法撤销也不应被忽略的命令。
+ `InsertCommand`、`DeleteCommand`、`AppendTailCommand` 等具体命令继承自 `CanUndoCommand` ，是不应被忽略且可以撤销重做的命令。
+ `ListCommand`、`ListTreeCommand`、`DirTreeCommand` 等具体命令继承自 `CanIgnoreCommand` ，是与撤销重做无关，可以被忽略的命令。

每个具体命令的 `execute` 方法会调用命令接收者的对应动作。

在 `main.py` 中，`client` 函数获取各个模块的实例，并组织起模块之间的关系，然后将各个模块传入 `Parse` 解析器。`Parse` 解析器的 `parse_input` 方法负责解析用户命令行输入，使用分发器将命令行输入分发到对应的 `Command` 构造器，`Command` 构造器将设置命令接收者和参数，最后返回对应的命令。如 `Parse.insert` 方法会将 `Editor` 实例设置为 `InsertCommand` 的接收者，并设置好 `InsertCommand` 的相关行号、内容，最后返回这个 `InsertCommand` 。

`client` 中得到解析出来的命令对象后，委托 `Invoker` 执行。`Invoker` 的 `execute_command` 方法会调用命令的 `execute` 方法，此时命令的接收者真正执行相关操作。然后 `Invoker` 也会使用持有的 `Logger` 实例进行命令的日志记录。同时，`Invoker` 还会根据命令的 `can_undo` 和 `can_ignore` 对需要撤销或重做命令进行保存管理。

比较特别的是，在这里为了统一形式，`Invoker` 也可以是接收者。比如 `UndoCommand` 的接收者会被设置为 `Invoker` ，`UndoCommand.execute` 方法内调用其持有的 `Invoker` 实例的 `undo` 方法，最终 `Invoker.undo` 调用其持有的将被撤销的那个命令的 `undo` 方法，真正完成撤销操作。

### 观察者模式

为了实现 `stats` 指令，这里使用了观察者模式。`Stats` 类继承自 `Observer` 类，并要求实现一个 `update` 方法。在具体的 `Stats` 类中，其 `update` 方法接受文件路径、时间间隔作为参数，更新相关的时间统计数据。`FileManager` 类中的 `attach` 方法可以用于添加观察者，`notify` 方法可以进行更新的发布，调用其持有的 `Stats` 实例的 `update` 方法，更新当前打开的文件的工作总时间。

`FileManager.notify` 方法在文件加载、切换、关闭的时候被调用，以及在 `StatsCommand.execute` 中会被调用。使用观察者模式，能比较好地将 `FileManager` 和 `Stats` 解耦。

### 单例模式

在这里 `Logger`、`Stats`、`FileManager` 等类在整个程序的生命周期中只会有唯一一个实例。利用 Python 模块级变量的特点可以很好地实现单例模式。Python 中模块天然就是单例的，因为模块只会被加载一次，所以在对应模块初始化目标单例，之后只导入和调用这个单例，就满足了单例模式。对于 `Logger`、`Stats` 和 `FileManager` 这样的和资源管理相关的类，单例模式能提供唯一的入口，更好地保证资源被正确管理。