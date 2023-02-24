# Task Manager

Implementation of a Finite State Machine framework targeted at robotics using MicroPython.

## Concept
NOTE: Terminology used is different from the common terminology used in Finite State Machine theory.

The robot is expected to excute a list of tasks in a specific order (Task List), e.g. [Task1, Task2, Task3].
It will execute the first task in the list (Current Task) e.g. Task1.

When the Current Task indicates the robot can move on to the next task (Next), the Current Task is removed from the list and the next task becomes the Current Task.
However, when indicating to go to the next task, optionally a list of additional tasks can be provided to insert in the task list to replace the current task, thus to be executed before the current next task in the list.
E.g. Task1 indicates 'next' with additional tasks [Task1a, Task1b], results in the new list [Task1a, Task1b, Task2, Task3] and Task1a becoming the new current task.

The Task Manager maintains the Task List and makes sure the Current Task is executed.

A Task needs to provide two functions: Start and Beat.
When the Task Manager switches to a new Task, it will call the Start function.
After that, the Task Manager will call the Beat function over and over again until the Task indicates Next.

The Start function is meant to initialize the Task.

The Beat function is meant to process events and thus react to those.
To allow a fixed interval between beat executions the option is available to configure that.

Tasks are implemented as objects instead of functions, allowing the reuse of a task definition, implemented as a class, with different configuration.

## Provided examples
* Micro:bit example without reusing task classes
* Micro:bit example usage with reusing task class


## Credits
Inspiration was taken from the StateMachine found in [MyQueen.py](https://github.com/HccPythonRobotics/MaqueenPlus/blob/4b6518f61194a610a1954bdfced58ab0563d8c3c/Workshop2/MyQueen.py).
Started from that functionality, but felt the need to reuse state definitions with different configurations, resulting in an object based implementation. 

---
# Implementation documentation

## Module: taskmgr
Finite State Machine framework targeted at robotics using MicroPython.  
Managing a list of tasks to be excuted in sequence and execute those in sequence.

Allowing each task to provide two non-blocking methods that will be called by the framework:
* start - will be called once when the task is about to be executed for the first time.
* beat - will be called over and over again to process events and thus react on those.  

Offering the ability to:
* Replace the current task with a sequence of other tasks.
* Have the beat function called at a regular interval.
* Have a task check if execution time exceeded a specific time.


### Class: TaskMgr
Task Manager manages the task list and takes care of calling the start and beat functions of the current task.  
Each task in the task list must be an object of a Task subclass.

Private attributes:
* _rev_task_list: List of tasks to execute in reverse order.
* _start:True if a new task is about to be started.
* _beat_ms: Defines the rythm of the beat in milliseconds per beat (0 = no wait).
* _last_beat_ticks_ms: Timestamp indicating when the last beat started.

#### Method: \_\_init\_\_
Create a task manager object.

Parameters:
* beat_ms: The minimum time between calls to task beat functions in milliseconds (default: 0).
* task_list: A list of tasks (object from a Task subclass) to be used as task list (default: no task).

Calls 'reset' method.

#### Method: reset
Deletes the current task list and reinitializes the task manager object.

Parameters:
* beat_ms: The minimum time between calls to task beat functions in milliseconds (default: 0).
* task_list: A list of tasks (object from a Task subclass) to be used as task list (default: no task).

Resets private attributes: _beat_ms, _last_beat_ticks_ms.  
Empties _rev_task_list and calls 'next' method to reset _start and set _rev_task_list.

#### Method: next
Move to the next task from the task list, optionally replacing the current task with the task list provided.

Parameters:
* task_list: A list of tasks to replace the current task in the task list (default: no task).

Meant to be called from a beat method in a Task object to indicate to go to the next task.  
Current task will be removed from _rev_task_list.  
If provided task_list will be appended to _rev_task_list to be executed before the current next task.  
Can also be called outside a beat function for initially populating the task list.

#### Method: beat
To be called from outside the task manager, over and over again, to keep the state machine going.

Returns:
* boolean: False when no tasks are left, otherwise true.

Will abort immediately if the next beat is not due.  
If the current task is new (_start=True), it will:
* Reset _start to False.
* Call the start function of the current task.

Will call the beat function of the current task.

#### Method: print_task_list
Prints for each Task object in the task list its properties.  
Meant to be used as a poor man's debug function.

### Class: Task
Abstract class to be used to create subclasses that can be used for task objects.

Private attributes:
* _task_manager: The task manager object this task object is linked to.
* _label: A label to give the task object (default: empty). Meant to be helpful for debugging.
* _start_ticks_ms: Timestamp indicating when the task started.

#### Abstract method: \_\_init\_\_
Create a task object.

Parameters:
* _task_manager: The task manager object this task object is linked to.
* _label: A label to give the task object (default: empty). Meant to be helpful for debugging.

Sets _task_manager and _label.  
Initializes start_ticks_ms to None.

#### Regular method: duration_ms
Check if the task was started more than the given duration, in milliseconds, ago.

Parameters:
* duration_ms: The duration, in milliseconds.

Returns:
* boolean: False if the task is running less than duration_ms, otherwise true.

#### Abstract method: start
Will be called once by the Task Manager when the task is starting.

Resets private attribute _start_ticks_ms.  
Has to be overridden in the subclass and should be called from that subclass.

#### Abstract method: beat
Will be called over and over by the Task Manager as long as the task is running.

Has to be overridden in the subclass.
