class ProxiedCall:
    def __init__(self, proxy, method_name):
        self.proxy = proxy
        self.method_name = method_name

    def __call__(self, *args, **kwargs):

        obj = self.proxy._obj

        return getattr(obj, self.method_name)(*args, **kwargs)
        
class Proxy:
    def __init__(self, obj):
        self._obj = obj
        self.last_invoked = ""
        self.calls = dict()

    def __getattr__(self, name):
        # if(name == 'last_invoked_method' or name == 'was_called' or name == 'count_of_calls'):
        #     return self[name]
        self.last_invoked = name
        self.calls[name] = self.calls.get(name, 0) + 1
        try:
            attr = getattr(self._obj, name)
            if callable(attr):
                return ProxiedCall(self, name)
            else:
                return attr
        except AttributeError:
            raise Exception('No Such Method')
    

    def last_invoked_method(self):
        return self.last_invoked

    def count_of_calls(self, method_name):
        return self.calls.get(method_name, 0)

    def was_called(self, method_name):
        return method_name in list(self.calls.keys())

# class Radio():
#     def __init__(self):
#         self._channel = None
#         self.is_on = False
#         self.volume = 0

#     @property
#     def channel(self):
#         return self._channel

#     @channel.setter
#     def channel(self, value):
#         self._channel = value

#     def power(self):
#         self.is_on = not self.is_on
        
#     def pwr(self):
#         self.is_on = not self.is_on

# radio = Radio()
# p = Proxy(radio)
# p.channel = 95
# print(p.channel)
# p.power()
# p.power()

# print(p.was_called('power'))
# print(p.was_called('pwr'))
# print(p.count_of_calls('power'))
# print(p.last_invoked_method())