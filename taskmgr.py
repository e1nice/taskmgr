from time import ticks_ms, ticks_diff


class TaskMgr:
    def __init__(self, beat_ms=0, task_list=None):
        self._rev_task_list = None
        self._start = None
        self._beat_ms = None
        self._last_beat_ticks_ms = None
        self.reset(beat_ms, task_list)

    def reset(self, beat_ms=0, task_list=None):
        self._rev_task_list = []
        self.next(task_list)
        self._beat_ms = beat_ms
        self._last_beat_ticks_ms = ticks_ms()

    def next(self, task_list=None):
        if len(self._rev_task_list) > 0:
            self._rev_task_list.pop()
        if task_list is not None:
            for task_object in reversed(task_list):
                self._rev_task_list.append(task_object)
        self._start = True

    def beat(self):
        if ticks_diff(ticks_ms(), self._last_beat_ticks_ms) < self._beat_ms:
            return True
        self._last_beat_ticks_ms = ticks_ms()
        
        if self._start:
            if len(self._rev_task_list) == 0:
                return False
            self._start = False
            self._rev_task_list[-1].start()

        self._rev_task_list[-1].beat()
        return True
    
    def print_task_list(self):
        print("task list")
        for task_object in reversed(self._rev_task_list):
            print(task_object.__dict__)
    
    
class Task:
    def __init__(self, task_manager, label=""):
        self._task_manager = task_manager
        self._label = label
        self._start_ticks_ms = None

    def duration_ms(self, duration_ms):
        return ticks_diff(ticks_ms(), self._start_ticks_ms) >= duration_ms

    def start(self):
        self._start_ticks_ms = ticks_ms()

    def beat(self):
        self._task_manager.next()
