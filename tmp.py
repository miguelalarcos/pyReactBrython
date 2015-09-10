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
    helper()
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

# ########

from browser import document, html

def value_string(obj, attr):
    def helper(ev):
        setattr(obj, attr, ev.target.value)
        while execute:
            call = execute.pop()
            call()
    return helper

class A(Model):
    def __init__(self):
        super().__init__()
        self.a = ''

# the model
obj = A()

# <input id='input' value_string=${obj.a}>
document['main'] <= html.INPUT(Id="input")
document['input'].bind('keyup', value_string(obj, 'a'))
@reactive
def input():
    document['input'].value = obj.a

# <input id='input2' value_string=${obj.a}>
document['main'] <= html.INPUT(Id="input2")
document['input2'].bind('keyup', value_string(obj, 'a'))
@reactive
def input2():
    document['input2'].value = obj.a

# <div id='output'>${obj.a}</div>
document['main'] <= html.DIV(Id='output')
@reactive
def output():
    document['output'].html = obj.a
    

    