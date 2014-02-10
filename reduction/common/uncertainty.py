"""

Measurement propagation class, and log() and exp() functions.

Based on scalars or numpy vectors, this class allows you to store and
manipulate values+uncertainties, with propagation of gaussian error for
addition, subtraction, multiplication, division, power, exp() and log().

Storage properties are determined by the numbers used to set the value
and uncertainty.  Be sure to use floating point uncertainty vectors
for inplace operations since numpy does not do automatic type conversion.
Normal operations can use mixed integer and floating point.  In place
operations (a *= b, etc.) create at most one extra copy for each operation.
c = a*b by contrast uses four intermediate vectors, so shouldn't be used
for huge arrays.
"""

from __future__ import division

import numpy as np
from . import err1d
from .formatnum import format_uncertainty

__all__ = ['Measurement']

# TODO: rename to Measurement and add support for units?
# TODO: C implementation of *,/,**?
class Measurement(object):
    # Make standard deviation available
    def hstack(self,other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        if np.isscalar(v2) and not np.isscalar(x2):
            v2 = np.ones_like(x2)*v2
        self.x = np.hstack((x1,x2))
        self.variance = np.hstack((v1,v2))
    def vstack(self,other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        if np.isscalar(v2) and not np.isscalar(x2):
            v2 = np.ones_like(x2)*v2
        self.x = np.vstack((x1,x2))
        self.variance = np.hstack((v1,v2))
    def _getdx(self):
        return np.sqrt(self.variance)
    def _setdx(self,dx):
        # Direct operation
        #    variance = dx**2
        # Indirect operation to avoid temporaries
        self.variance[:] = dx
        self.variance **= 2
    dx = property(_getdx,_setdx,doc="standard deviation")

    # Constructor
    def __init__(self, x, variance=0):
        if np.isscalar(variance) and not np.isscalar(x):
            temporary = variance
            variance = np.empty_like(x)
            variance[:] = temporary
        self.x, self.variance = x, variance

    # Numpy array slicing operations
    def __len__(self):
        return len(self.x)
    def __getitem__(self, key):
        return Measurement(self.x[key], self.variance[key])
    def __setitem__(self, key, value):
        self.x[key] = value.x
        self.variance[key] = value.variance
    def __delitem__(self, key):
        self.x=np.delete(self.x,key,0)
        self.variance=np.delete(self.variance,key,0)
    #def __iter__(self): pass # Not sure we need iter

    # Normal operations: may be of mixed type
    def __add__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        return Measurement(*err1d.add(x1,v1,x2,v2))
    def __sub__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        return Measurement(*err1d.sub(x1,v1,x2,v2))
    def __mul__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        return Measurement(*err1d.mul(x1,v1,x2,v2))
    def __truediv__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        return Measurement(*err1d.div(x1,v1,x2,v2))
    def __pow__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        return Measurement(*err1d.pow(x1,v1,x2,v2))

   # Reverse operations
    def __radd__(self, other):
        x1,v1 = _valvar(other)
        x2,v2 = _valvar(self)
        return Measurement(*err1d.add(x1,v1,x2,v2))
    def __rsub__(self, other):
        x1,v1 = _valvar(other)
        x2,v2 = _valvar(self)
        return Measurement(*err1d.sub(x1,v1,x2,v2))
    def __rmul__(self, other):
        x1,v1 = _valvar(other)
        x2,v2 = _valvar(self)
        return Measurement(*err1d.mul(x1,v1,x2,v2))
    def __rtruediv__(self, other):
        x1,v1 = _valvar(other)
        x2,v2 = _valvar(self)
        return Measurement(*err1d.div(x1,v1,x2,v2))
    def __rpow__(self, other):
        x1,v1 = _valvar(other)
        x2,v2 = _valvar(self)
        return Measurement(*err1d.pow(x1,v1,x2,v2))

    # In-place operations: may be of mixed type
    def __iadd__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        self.x,self.variance = err1d.add_inplace(x1,v1, x2,v2)
        return self
    def __isub__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        self.x,self.variance = err1d.sub_inplace(x1,v1, x2,v2)
        return self
    def __imul__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        self.x,self.variance = err1d.mul_inplace(x1,v1, x2,v2)
        return self
    def __itruediv__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        self.x,self.variance = err1d.div_inplace(x1,v1, x2,v2)
        return self
    def __ipow__(self, other):
        x1,v1 = _valvar(self)
        x2,v2 = _valvar(other)
        self.x,self.variance = err1d.pow_inplace(x1,v1, x2,v2)

    # Use true division instead of integer division
    def __div__(self, other): return self.__truediv__(other)
    def __rdiv__(self, other): return self.__rtruediv__(other)
    def __idiv__(self, other): return self.__itruediv__(other)


    # Unary ops
    def __neg__(self):
        return Measurement(-self.x,self.variance)
    def __pos__(self):
        return self
    def __abs__(self):
        return Measurement(abs(self.x),self.variance)

    def __str__(self):
        #return str(self.x)+" +/- "+str(np.sqrt(self.variance))
        if np.isscalar(self.x):
            return format_uncertainty(self.x,np.sqrt(self.variance))
        else:
            return [format_uncertainty(v,dv) for v,dv in zip(self.x,np.sqrt(self.variance))]
    def __repr__(self):
        return "Measurement(%s,%s)"%(str(self.x),str(self.variance))

    # Not implemented
    def __floordiv__(self, other): return NotImplemented
    def __mod__(self, other): return NotImplemented
    def __divmod__(self, other): return NotImplemented
    def __lshift__(self, other): return NotImplemented
    def __rshift__(self, other): return NotImplemented
    def __and__(self, other): return NotImplemented
    def __xor__(self, other): return NotImplemented
    def __or__(self, other): return NotImplemented

    def __rfloordiv__(self, other): return NotImplemented
    def __rmod__(self, other): return NotImplemented
    def __rdivmod__(self, other): return NotImplemented
    def __rlshift__(self, other): return NotImplemented
    def __rrshift__(self, other): return NotImplemented
    def __rand__(self, other): return NotImplemented
    def __rxor__(self, other): return NotImplemented
    def __ror__(self, other): return NotImplemented

    def __ifloordiv__(self, other): return NotImplemented
    def __imod__(self, other): return NotImplemented
    def __idivmod__(self, other): return NotImplemented
    def __imod__(self, other): return NotImplemented
    def __ilshift__(self, other): return NotImplemented
    def __irshift__(self, other): return NotImplemented
    def __iand__(self, other): return NotImplemented
    def __ixor__(self, other): return NotImplemented
    def __ior__(self, other): return NotImplemented

    def __invert__(self): return NotImplemented  # For ~x
    def __complex__(self): return NotImplemented
    def __int__(self): return NotImplemented
    def __long__(self): return NotImplemented
    def __float__(self): return NotImplemented
    def __oct__(self): return NotImplemented
    def __hex__(self): return NotImplemented
    def __index__(self): return NotImplemented
    def __coerce__(self,other): return NotImplemented

    def log(self):
        return Measurement(*err1d.log(self.x,self.variance))
    def sqrt(self):
        return Measurement(*err1d.sqrt(self.x,self.variance))
    def exp(self):
        return Measurement(*err1d.exp(self.x,self.variance))
    def arcsin(self):
        return Measurement(*err1d.arcsin(self.x,self.variance))
    def arccos(self):
        return Measurement(*err1d.arcsin(self.x,self.variance))
    def arctan(self):
        return Measurement(*err1d.arctan(self.x,self.variance))
    def sin(self):
        return Measurement(*err1d.sin(self.x,self.variance))
    def tan(self):
        return Measurement(*err1d.tan(self.x,self.variance))
    def cos(self):
        return Measurement(*err1d.cos(self.x,self.variance))


def _valvar(obj):
    try:
        return obj.x, getattr(obj, 'variance', 0)
    except KeyError:
        return obj, 0

def test():
    a = Measurement(5,3)
    b = Measurement(4,2)

    # Scalar operations
    z = a+4
    print z,z.variance
    assert z.x == 5+4 and z.variance == 3
    z = a-4
    assert z.x == 5-4 and z.variance == 3
    z = a*4
    assert z.x == 5*4 and z.variance == 3*4**2
    z = a/4
    assert z.x == 5./4 and z.variance == 3./4**2

    # Reverse scalar operations
    z = 4+a
    assert z.x == 4+5 and z.variance == 3
    z = 4-a
    assert z.x == 4-5 and z.variance == 3
    z = 4*a
    assert z.x == 4*5 and z.variance == 3*4**2
    z = 4/a
    assert z.x == 4./5 and abs(z.variance - 3./5**4 * 4**2) < 1e-15

    # Power operations
    z = a**2
    assert z.x == 5**2 and z.variance == 4*3*5**2
    z = a**1
    assert z.x == 5**1 and z.variance == 3
    z = a**0
    assert z.x == 5**0 and z.variance == 0
    z = a**-1
    assert z.x == 5**-1 and abs(z.variance - 3./5**4) < 1e-15

    # Binary operations
    z = a+b
    assert z.x == 5+4 and z.variance == 3+2
    z = a-b
    assert z.x == 5-4 and z.variance == 3+2
    z = a*b
    assert z.x == 5*4 and z.variance == (5**2*2 + 4**2*3)
    z = a/b
    assert z.x == 5./4 and abs(z.variance - (3./5**2 + 2./4**2)*(5./4)**2) < 1e-15

    # ===== Inplace operations =====
    # Scalar operations
    y = a+0; y += 4
    z = a+4
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15
    y = a+0; y -= 4
    z = a-4
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15
    y = a+0; y *= 4
    z = a*4
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15
    y = a+0; y /= 4
    z = a/4
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15

    # Power operations
    y = a+0; y **= 4
    z = a**4
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15

    # Binary operations
    y = a+0; y += b
    z = a+b
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15
    y = a+0; y -= b
    z = a-b
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15
    y = a+0; y *= b
    z = a*b
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15
    y = a+0; y /= b
    z = a/b
    assert y.x == z.x and abs(y.variance-z.variance) < 1e-15


    # =============== vector operations ================
    # Slicing
    z = Measurement(np.array([1,2,3,4,5]),np.array([2,1,2,3,2]))
    assert z[2].x == 3 and z[2].variance == 2
    assert (z[2:4].x == [3,4]).all()
    assert (z[2:4].variance == [2,3]).all()
    z[2:4] = Measurement(np.array([8,7]),np.array([4,5]))
    assert z[2].x == 8 and z[2].variance == 4
    A = Measurement(np.array([a.x]*2),np.array([a.variance]*2))
    B = Measurement(np.array([b.x]*2),np.array([b.variance]*2))

    # TODO complete tests of copy and inplace operations for vectors and slices.

    # Binary operations
    z = A+B
    assert (z.x == 5+4).all() and (z.variance == 3+2).all()
    z = A-B
    assert (z.x == 5-4).all() and (z.variance == 3+2).all()
    z = A*B
    assert (z.x == 5*4).all() and (z.variance == (5**2*2 + 4**2*3)).all()
    z = A/B
    assert (z.x == 5./4).all()
    assert (abs(z.variance - (3./5**2 + 2./4**2)*(5./4)**2) < 1e-15).all()

    # printing; note that sqrt(3) ~ 1.7
    assert str(Measurement(5,3)) == "5.0(17)"
    assert str(Measurement(15,3)) == "15.0(17)"
    assert str(Measurement(151.23356,0.324185**2)) == "151.23(32)"

if __name__ == "__main__": test()
