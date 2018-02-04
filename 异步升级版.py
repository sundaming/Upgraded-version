
#coding:utf-8
import time
import thread

gen = None


def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        global gen
        gen = f()
        gen.next()
    return wrapper


def long_io():
    def fun():
        print('开始执行io操作')
        global gen
        time.sleep(5)
        try:
            print('完成io操作，send结果唤醒程序继续执行')
            gen.send('io----结果---')
        except StopAsyncIteration:
            pass
        thread.start_new_thread(fun,())


@gen_coroutine
def req_a():
    print('开始执行请求req_a')
    ret = yield long_io()
    print('ret:%s' % ret)
    print('完成处理请求req_b')


def req_b():
    print('开始执行请求req_b')
    time.sleep(2)
    print('完成请求处理req_b')


def main():
    req_a()
    req_b()


if __name__ == '__main__':
    main()