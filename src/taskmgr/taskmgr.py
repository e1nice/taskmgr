"""Finite State Machine framework targeted at robotics using MicroPython.

Managing a list of tasks to be excuted in sequence and execute those in sequence.

Allowing each task to provide two functions that will be called by the framework:
- start - will be called once when the task is about to be executed for the first time.
- beat - will be called over and over again to process events and thus react on those.
Both functions have to be non-blocking

Offering the ability to:
- Replace the current task with a sequence of other tasks.
- Have the beat function called at a regular interval.
- Have a task check if execution time exceeded a specific time.
"""
import time


class TaskMgr:
    """Task Manager manages the task list and takes care of calling the start and beat functions of the current task.

    Each task in the task list must be an object of a Task subclass.
    """
    def __init__(self, p_beat_duration_ms=0, p_task_list=None):
        """Create a task manager object.

        Args:
            p_beat_duration_ms: The minimum time between calls to task beat functions in milliseconds (default: 0).
            p_task_list: A list of tasks (object from a Task subclass) to be used as task list (default: no task).
        """
        # Actual initialization of the instance attributes is done in reset funtion.
        self._rev_task_list = None  # List of tasks to execute in reverse order.
        self._start_task = None  # True if a new task is about to be started.
        self._beat_duration_ms = None  # Defines the rythm of the beat in milliseconds per beat (0 = no wait).
        self._last_beat_ticks_ms = None  # Time in milliseconds when the next beat is due.
        self.reset(p_beat_duration_ms, p_task_list)

    def reset(self, p_beat_duration_ms=0, p_task_list=None):
        """Deletes the current task list and reinitializes the task manager object.

        Args:
            p_beat_duration_ms: The minimum time between calls to task beat functions in milliseconds (default: 0).
            p_task_list: A list of tasks (object from a Task subclass) to be used as task list (default: no task).
        """
        self._rev_task_list = []  # Initialize the list of tasks as empty.
        # self._start_task will be set in next function.
        self.next(p_task_list)  # Add the provided list of tasks.
        self._beat_duration_ms = p_beat_duration_ms  # Store the value provided.
        self._last_beat_ticks_ms = time.ticks_ms()  # Next beat may start any time from now.

    def next(self, p_task_list=None):
        """Move to the next task from the task list, optionally replacing the current task with the task list provided.

        Args:
            p_task_list: A list of tasks to replace the current task in the task list.

        Meant to be called from a beat funtion in a Task object to indicate to go to the next task.
        Optionally one or more tasks can be provided to be executed before the current next task.
        Can also be called outside a beat function for initially populating the task list.
        """
        if len(self._rev_task_list) > 0:
            self._rev_task_list.pop()  # Remove the current task from the list.
        if p_task_list is not None:
            for task_object in reversed(p_task_list):  # Add the provided tasks to the task list.
                self._rev_task_list.append(task_object)
        self._start_task = True  # Indicate a new task is about to be started.

    def beat(self):
        """To be called from outside the task manager, over and over again, to keep the state machine going.

        Returns false when no tasks are left, otherwise true.
        Will abort immediately if the next beat is not due.
        If the current task is new, it will call the start function of this task.
        Will call the beat function of the current task.
        """
        if time.ticks_diff(time.ticks_ms(), self._last_beat_ticks_ms) < self._beat_duration_ms:
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
        """Prints for each Task object in the task list its properties as a poor man's debug function.
        """
        print("task list")
        for task_object in reversed(self._rev_task_list):
            print(task_object.__dict__)
    
    
class Task:
    """Abstract class to be used to create subclasses that can be used for task objects.
    """
    def __init__(self, p_task_manager: TaskMgr, p_label=""):
        """Create a task object.

        Args:
            p_task_manager: The task manager object the task will be used with.
            p_label: A label to give the task object (default: empty). Meant to be helpful for debugging.
        """
        self._task_manager = p_task_manager
        self._label = p_label
        self._start_ticks_ms = None

    def duration_ms(self, p_duration_ms):
        """Check if the task was started more than the given duration, in milliseconds, ago.

        Args:
            p_duration_ms: The duration, in milliseconds.
        """
        return time.ticks_diff(time.ticks_ms(), self._start_ticks_ms) > p_duration_ms

    def start(self):
        """Will be called once by the Task Manager when the task is starting.
        """
        self._start_ticks_ms = time.ticks_ms()

    def beat(self):
        """Will be called over and over by the Task Manager as long as the task is running.
        """
        self._task_manager.next()
    