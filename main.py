current_name = None
current_call = None
execute = []
map_ = {}


def reactive(func):

    def helper():
        global current_call, current_name
        current_name = func.__name__
        objects = map_.get(func.__name__, set())
        for obj in objects:
            obj.reset(func.__name__)
        map_[func.__name__] = set()
        current_call = helper
        return func()

    return helper


class Model(object):
    def __init__(self):
        self.__dict__['_map'] = []

    def reset(self, name):
        print ('reset', name)
        self.__dict__['_map'] = [item for item in self._map if item['name'] != name]

    def __getattr__(self, name):
        map_[current_name].add(self)
        self._map.append({'name': current_name, 'call': current_call, 'attr': name})
        return self.__dict__['_'+name]

    def __setattr__(self, key, value):
        if '_'+key not in self.__dict__.keys():
            self.__dict__['_'+key] = value
            return

        if value != self.__dict__['_'+key]:
            self.__dict__['_'+key] = value
            global execute
            for item in self._map:
                if item['attr'] == key and item['call'] not in execute:
                    execute.append(item['call'])


class Car(Model):
    def __init__(self, x, y):
        super(self.__class__, self).__init__()
        self.x = x
        self.y = y

car = Car(x=8, y=9)

@reactive
def f():
    if car.x > 50:
        print(car.x)
    else:
        print(car.y)

f()

car.y = 10
while execute:
    call = execute.pop()
    call()

car.x = 99
while execute:
    call = execute.pop()
    call()

car.y = 11
while execute:
    call = execute.pop()
    call()
