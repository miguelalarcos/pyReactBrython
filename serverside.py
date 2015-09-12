def pass_filter(filter, model):
    for key, value in filter.items():
        if type(value) == 'int' or type(value) == 'string':
            if model[key] != value:
                return False
        else:
            for op, val in value.items():
                if op == '$gt':
                    if model[key] <= val:
                        return False
                elif op == '$lt':
                    if model[key] > val:
                        return False
    return True


class Controller(object):
    def __init__(self):
        self.filters = [('ClientId', {'x': {"$gt": 7, "$lt": 10}}),]

    def test(self, model):
        print 'get model id:', model['id']
        model_before = {'id': '0', 'x': 50}
        print 'update model'
        for client, filt in self.filters:
            print('filter:', filt)
            before = pass_filter(filt, model_before)
            print 'before:', before

            if not before:
                after = pass_filter(filt, model)
                print 'after:', after
                if after:
                    print 'send', client, model
            else:
                print 'send', client, model


controller = Controller()
controller.test({'id': '0', 'x': 80})
