from microbit import *
from taskmgr import TaskMgr, Task


class TaskDisplay(Task):
    def __init__(self, task_manager: TaskMgr, duration_ms=0, image=None, label=""):
        super().__init__(task_manager, label)
        self._duration_ms = duration_ms
        if image is None:
            self._image = Image.SURPRISED
        else:
            self._image = image

    def start(self):
        super().start()
        display.show(self._image)

    def beat(self):
        if self.duration_ms(self._duration_ms):
            self._task_manager.next()


tm = TaskMgr()
task_yes = TaskDisplay(task_manager=tm, duration_ms=4000, image=Image.YES, label="task_yes")
task_no = TaskDisplay(task_manager=tm, duration_ms=2000, image=Image.NO, label="task_no")
tm.next(task_list=[task_no, task_yes])
tm.print_task_list()
while tm.beat():
    pass
display.clear()
