from microbit import *
from taskmgr import TaskMgr, Task


class TaskYes(Task):
    def start(self):
        display.show(Image.YES)

    def beat(self):
        if self.duration_ms(2000):
            self._task_manager.next()


class TaskNo(Task):
    def start(self):
        display.show(Image.NO)

    def beat(self):
        if self.duration_ms(3000):
            self._task_manager.next()


tm = TaskMgr()
task_yes = TaskYes(p_task_manager=tm)
task_no = TaskNo(p_task_manager=tm)
tm.next(p_task_list=[task_no, task_yes])
tm.print_task_list()
while tm.beat():
    pass
