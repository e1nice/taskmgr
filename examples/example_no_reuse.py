from microbit import *
from taskmgr import TaskMgr, Task


class TaskYes(Task):
    def start(self):
        super().start()
        display.show(Image.YES)

    def beat(self):
        if self.duration_ms(4000):
            self._task_manager.next()


class TaskNo(Task):
    def start(self):
        super().start()
        display.show(Image.NO)

    def beat(self):
        if self.duration_ms(2000):
            self._task_manager.next()


tm = TaskMgr()
task_yes = TaskYes(p_task_manager=tm, p_label="task_yes")
task_no = TaskNo(p_task_manager=tm, p_label="task_no")
tm.next(p_task_list=[task_no, task_yes])
tm.print_task_list()
while tm.beat():
    pass
display.clear()
