import time


class TaskMgr:
    def __init__(self, p_beat_duration_ms=0, p_task_list=None):
        # Actual initialization of the instance attributes is done in reset funtion.
        self._rev_task_list = None  # List of tasks to execute in reverse order.
        self._start_task = None  # True if a new task is about to be started.
        self.reset(p_beat_duration_ms, p_task_list)
        self._beat_duration_ms = None  # Defines the rythm of the beat in milliseconds per beat (0 = no wait).
        self._last_beat_ticks_ms = None  # Time in milliseconds when the next beat is due.

    def reset(self, p_beat_duration_ms=0, p_task_list=None):
        self._rev_task_list = []  # Initialize the list of tasks as empty.
        # self._start_task will be set in next function.
        self.next(p_task_list)  # Add the provided list of tasks.
        self._beat_duration_ms = p_beat_duration_ms  # Store the value provided.
        self._last_beat_ticks_ms = time.ticks_ms()  # Next beat may start any time from now.

    def next(self, p_task_list=None):
        # Meant to be called from a beat funtion in a Task object to indicate to go to the next task.
        # Optionally one or more tasks can be provided to be executed before the current next task.
        # Can also be called outside a beat function for initially populating the task list.
        if len(self._rev_task_list) > 0:
            self._rev_task_list.pop()  # Remove the current task from the list.
        if p_task_list is not None:
            for task_object in reversed(p_task_list):  # Add the provided tasks to the task list.
                self._rev_task_list.append(task_object)
        self._start_task = True  # Indicate a new task is about to be started.

    def beat(self):
        # To be called from outside the task manager, over and over again, to keep the state machine going.
        # Will return false when no tasks are left, otherwise true.
        # Will abort immediately if the next beat is not due.
        # If the current task is new, it will call the start function of this task.
        # Will call the beat function of the current task.
        if time.ticks_diff(time.ticks_ms(), self._last_beat_ticks_ms) > self._beat_duration_ms:
            return True  # Abort if next beat is not due yet.
        self._last_beat_ticks_ms = time.ticks_ms()
        
        if self._start_task:
            if len(self._rev_task_list) == 0:
                return False  # No more task to execute.
            self._start_task = False  # Reset flag.
            self._rev_task_list[-1].start()  # Call the start function of the current, last in list, task.

        self._rev_task_list[-1].beat()  # Call the beat function of the current, last in list, task.
        return True
    
    def print_task_list(self):
        print("task list")
        for task_object in reversed(self._rev_task_list):
            print(task_object.__dict__)
    
    
class Task:
    def __init__(self, p_task_manager: TaskMgr, p_label=""):
        self._task_manager = p_task_manager
        self._label = p_label
        self._start_ticks_ms = None

    def duration_ms(self, p_duration_ms):
        return time.ticks_diff(time.ticks_ms(), self._start_ticks_ms) > p_duration_ms

    def start(self):
        self._start_ticks_ms = time.ticks_ms()

    def beat(self):
        self._task_manager.next()
    