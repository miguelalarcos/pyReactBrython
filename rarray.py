class DOM(object):
    def __init__(self, id):
        self.id = id


class Model(object):
    def __init__(self, id, x):
        self.id = id
        self.x = x

    def __repr__(self):
        return '(id:'+str(self.id) + ', x:' + str(self.x)+')'


class Controller(object):
    def __init__(self, key, filter):
        self.lista = []
        self.key = key
        self.filter = filter

    def test(self, model):
        if model.id in [x.id for x in self.lista]:
            print 'esta dentro'
            if self.filter(model):
                print 'y permance dentro', 'MODIFY'
                self.modify(model)
            else:
                print 'y sale', 'OUT'
                self.out(model)
        else:
            print 'esta fuera'
            if self.filter(model):
                print 'y entra', 'NEW'
                self.new(model)
            else:
                print 'y permanece fuera'

    def new(self, model):
        tupla = self.indexInList(model)
        index = tupla[0]
        self.lista.insert(index, model)
        print('new: ', model, tupla)

    def out(self, model):
        index = self.indexById(model.id)
        del self.lista[index]
        print ('out: ', model)

    def modify(self, model):
        index = self.indexById(model.id)
        del self.lista[index]
        tupla = self.indexInList(model)
        if index == tupla[0]:
            print 'ocupa misma posicion'
        else:
            print 'move to ', model, tupla
        self.lista.insert(tupla[0], model)

    def indexById(self, id):
        index = 0
        for item in self.lista:
            if item.id == id:
                break
            index += 1
        return index

    def indexInList(self, model):
        if self.lista == []:
            return (0, 'append')
        v = getattr(model, self.key)
        index = 0
        for item in self.lista:
            if v <= getattr(item, self.key):
                break
            index += 1
        if index == 0:
            return (index, 'before', self.lista[0].id)
        else:
            return (index, 'after', self.lista[index-1].id)


def filter(model):
    return model.x > 2

controller = Controller(key='x', filter=filter)
controller.test(Model(id='0', x=0))
controller.test(Model(id='1', x=2))
controller.test(Model(id='2', x=1))
m = Model(id='3', x=3)
controller.test(m)

m.x = -1
controller.test(m)
print controller.lista

controller.test(m)
m = Model(id='4', x=300)
controller.test(m)
m.x = 301
controller.test(m)
print controller.lista