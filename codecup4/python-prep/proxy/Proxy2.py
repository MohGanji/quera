class ProxiedCall:
    def __init__(self, proxy, method_name):
        self.proxy = proxy
        self.method_name = method_name

    def __call__(self, *args, **kwargs):

        obj = self.proxy._obj

        return getattr(obj, self.method_name)(*args, **kwargs)
        

class Proxy(object):
    __slots__ = ["_obj", "__weakref__", "last_invoked", "calls"]
    def __init__(self, obj):
        object.__setattr__(self, "_obj", obj)
        self.last_invoked = ""
        self.calls = dict()
    

    # def __getattr__(self, name):
    #     # print('name: ', name)
    #     # if name in ["was_called", "count_of_calls", "last_invoked_method"]:
    #     #     return object.__getattribute__(self, name)
    #     try:
    #         attr = getattr(self._obj, name)
    #         if callable(attr):
    #             self.last_invoked = name
    #             self.calls[name] = self.calls.get(name, 0) + 1
    #             return ProxiedCall(self, name)
    #         else: return attr
    #     except AttributeError:
    #         raise Exception('No Such Method')

    def last_invoked_method(self):
        if(self.last_invoked == ""):
            raise Exception("No Method Is Invoked")
        return self.last_invoked

    def count_of_calls(self, method_name):
        return self.calls.get(method_name, 0)

    def was_called(self, method_name):
        return method_name in list(self.calls.keys())        
    #
    # proxying (special cases)
    #
    def __getattribute__(self, name):
        attr = None
        flag = False
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            try:
                attr = getattr(object.__getattribute__(self, "_obj"), name)
                flag = True
            except AttributeError:
                raise Exception('No Such Method')
        if callable(attr):
            if(flag):
                self.last_invoked = name
            self.calls[name] = self.calls.get(name, 0) + 1
        return attr
    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "_obj"), name)
    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_obj"), name, value)
    
    def __nonzero__(self):
        return bool(object.__getattribute__(self, "_obj"))
    def __str__(self):
        return str(object.__getattribute__(self, "_obj"))
    def __repr__(self):
        return repr(object.__getattribute__(self, "_obj"))
    
    #
    # factories
    #
    _special_names = [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__', 
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__', 
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__', 
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__', 
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__', 
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__', 
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', 
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__', 
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__', 
        '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__', 
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', 
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__', 
        '__truediv__', '__xor__', 'next',
    ]
    
    @classmethod
    def _create_class_proxy(cls, theclass):
        """creates a proxy for the given class"""
        
        def make_method(name):
            def method(self, *args, **kw):
                return getattr(object.__getattribute__(self, "_obj"), name)(*args, **kw)
            return method
        
        namespace = {}
        for name in cls._special_names:
            if hasattr(theclass, name):
                namespace[name] = make_method(name)
        return type("%s(%s)" % (cls.__name__, theclass.__name__), (cls,), namespace)
    
    def __new__(cls, obj, *args, **kwargs):
        """
        creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an 
        __init__ method of their own.
        note: _class_proxy_cache is unique per deriving class (each deriving
        class must hold its own cache)
        """
        try:
            cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            theclass = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = theclass = cls._create_class_proxy(obj.__class__)
        ins = object.__new__(theclass)
        theclass.__init__(ins, obj, *args, **kwargs)
        return ins


class Radio():
    def __init__(self):
        self._channel = None
        self.is_on = False
        self.volume = 0

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    def power(self):
        self.is_on = not self.is_on
        
    def pwr(self):
        return self.is_on

radio = Radio()
p = Proxy(radio)
# print(p.last_invoked_method())
p.channel = 95 
# print(p.last_invoked_method())

print(p.volume)
p.power()
p.power()
# print(p.pwr())
# p.sjs()

print(p.was_called('power'))
print(p.was_called('pwr'))
print(p.count_of_calls('power'))
print(p.count_of_calls('pwr'))
print(p.count_of_calls('count_of_calls'))
print(p.last_invoked_method())