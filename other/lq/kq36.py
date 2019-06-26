def foo(num):
    print("starting...")
    while num<10:
        num=num+1
        yield num

def start():
    g= foo(0)
    print("sdsdasd")

start()