#!/usr/bin/env python
import sys, inspect, enum



class Cmcl(enum.EnumMeta):
  """This is the meta class for all sets of constants"""
  def __new__(mcs, name, bases, dict):
      print mcs, name, bases, dict
      C = enum.EnumMeta.__new__(mcs, name, bases, dict)
      if len(C) > 0:
        for i in C:
          i.__doc__ =  str(i.name) + ':\t' + str(i.value) + '\t' + (i.__doc__ or '')
        if not C.__doc__:
          pretty = map(lambda i: '\t' + str(i.__doc__), C.__members__.values())
          C.__doc__ = (
            "The following module constants are available:\n\tName\tValue\n"
            + "\n".join( pretty)
          )
        for i in C:
          i.__doc__ += " (module constant)"
      else: 
        C.__doc__ = """Base class for a set of module constants."""
      return C
    
  def __call__(self, *a, **k):
      if len(self) > 0:
        return super(Cmcl, self).__call__(*a)
      else:
        def call(names, module=None):
          print names, module
          if module is None:
            try:
              module = inspect.stack()[2][0].f_globals['__name__']
              print "Guessed module is ", module
            except:
              raise AttributeError('You must specify module=__name__ on this platform.')
          modobj = sys.modules[module]
          C = super(Cmcl, self).__call__('CONSTANTS', names=names, module=module)
          modobj.__dict__['CONSTANTS'] = C
          for i in C.__members__:
            #assert not (i in modobj.__dict__)
            modobj.__dict__[i] = C.__members__[i]
          return C
        return call(*a, **k)
        

class CONSTANTS(enum.IntEnum):
    """Base class for individual module constants."""
    __metaclass__=Cmcl
