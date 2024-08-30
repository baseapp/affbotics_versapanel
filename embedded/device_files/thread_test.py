import time
import _thread

counter_1 = 0
counter_2 = 1

def thread_0():
    global counter_1
    print("a:%d"%counter_1)
    counter_1 += 1
    time.sleep(1)


def thread_1():
    global counter_2
    print("b:%d"%counter_2)
    counter_2 += 1
    time.sleep(1)


task_module = ""

def loop_task():
    global task_module
    
    while(1):
        if(callable(task_module)):
            fung_name = task_module.__name__
            print("Calling %s"%fung_name)
            task_module()
        else:
            print("Function not callable")
        time.sleep_ms(50)

def task_switch():
    global task_module
    task_num = 0
    
    while True:
        print("Switching task:%d"%task_num)
        
        if(task_num):
            task_num = 0
            task_module = thread_0
        else:
            task_num = 1
            task_module = thread_1
        time.sleep(5)
        

loop_thread = _thread.start_new_thread(loop_task, ())

task_switch_thread =  _thread.start_new_thread(task_switch, ())



