from microbit import *
from taskmgr import TaskMgr, Task


class TaskDisplay(Task):
    def __init__(self, p_task_manager: TaskMgr, p_duration_ms=0, p_image=None, p_label=""):
        super().__init__(p_task_manager, p_label)
        self._duration_ms = p_duration_ms
        if p_image is None:
            self._image = Image.SURPRISED
        else:
            self._image = p_image

    def start(self):
        super().start()
        display.show(self._image)

    def beat(self):
        if self.duration_ms(self._duration_ms):
            self._task_manager.next()


tm = TaskMgr()
task_yes = TaskDisplay(p_task_manager=tm, p_duration_ms=4000, p_image=Image.YES, p_label="task_yes")
task_no = TaskDisplay(p_task_manager=tm, p_duration_ms=2000, p_image=Image.NO, p_label="task_no")
tm.next(p_task_list=[task_no, task_yes])
tm.print_task_list()
while tm.beat():
    pass
display.clear()
