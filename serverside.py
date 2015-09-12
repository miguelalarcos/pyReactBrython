import random


class Controller(object):
    def __init__(self, filter):
        self.filter = filter # filters

    def test(self, model):
        before = random.choice(['IN', 'OUT'])
        print 'before:', before
        print 'update model'
        if before == 'OUT':
            after = random.choice(['IN', 'OUT'])
            print 'after:', after
            if after == 'IN':
                print 'send'
        else:
            print 'send'


controller = Controller(filter=None)
controller.test(None)
