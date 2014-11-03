__author__ = 'lamter'


class Init(object):

    def __call__(self, *args, **kwargs):

        print 'class->', self.__class__.__name__



i = Init()


class A(object):
    def __init__(self, a):
        self.a = a

    def gan(self):
        if hasattr(self.a, '__call__'):
            self.a()


if __name__ == "__main__":
    a = A(i)
    a.gan()