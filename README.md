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

## Examples
* Micro:bit example without reusing task classes
* Micro:bit example usage with reusing task class


## Credits
Inspiration was taken from the StateMachine found in [MyQueen.py](https://github.com/HccPythonRobotics/MaqueenPlus/blob/4b6518f61194a610a1954bdfced58ab0563d8c3c/Workshop2/MyQueen.py).
Started from that functionality, but felt the need to reuse state definitions with different configurations, resulting in an object based implementation. 
