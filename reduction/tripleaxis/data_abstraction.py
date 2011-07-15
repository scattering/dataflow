import numpy as np
import uncertainty, err1d
#import readice
import readncnr4 as readncnr
from formatnum import format_uncertainty
import copy
from mpfit import mpfit
#from ...dataflow import wireit
eps=1e-8

"""
Current notes:
My current thoughts are to have one giant table so that we can do sorting
easily.

For some motors such as filter_translation, flipper_state, collimator, they have values such as 
"ON/OFF", "A,B,C", "50Min", etc.  we either need to mark these as unplottable, or rather, have a "mapper" which takes these values
to something plottable

"""





class Lattice(object):
        def __init__(self,a=None,b=None,c=None,alpha=None,beta=None,gamma=None):
                self.a=a
                self.b=b
                self.c=c
                self.alpha=alpha #stored in radians
                self.beta=beta
                self.gamma=gamma

class Orientation(object):
        def __init__(self,orient1=None,orient2=None):
                self.orient1=orient1  #these are vectors
                self.orient2=orient2

class Sample(object):
        def __init__(self):
                self.lattice=Lattice()
                self.mosaic=Mosaic()
                self.orientation=Orientation()

class Meta_tag(object):
        def __init__(self,name=None,value=None,isDistinct=False):
                self.name=name
                self.value=value
                self.isDistinct=isDistinct
                
                
class MetaData(object):
        def __init__(self,comment=None,filename=None, instrument_name=None,
                     epoch=None,experiment_name=None, experiment_id=None,
                     experiment_participants=None,date=None, filebase=None,
                     fileseq_number=None, scan_type=None, scanned_variables=None,
                     fixed_motors=None, fixed_energy=None, fixed_eief=None,
                     counting_standard=None, desired_detector=None
                     ):
                self.comment=Meta_tag('comment',comment)
                self.filename=Meta_tag('filename',filename)
                self.instrument_name=Meta_tag('instrument_name',instrument_name)
                self.epoch=Meta_tag('epoch',epoch)
                self.experiment_name=Meta_tag('experiment_name',experiment_name)
                self.experiment_id=Meta_tag('experiment_id',experiment_id)
                self.experiment_participants=Meta_tag('experiment_participants',experiment_participants)
                self.date=Meta_tag('date',date)
                self.filebase=Meta_tag('filebase',filebase)
                self.fileseq_number=Meta_tag('fileseq_number',filebase)
                self.scan_type=Meta_tag('scan_type',scan_type) #EX MOTOR, VECTOR, etc.
                self.scanned_variables=Meta_tag('scanned_variables',scanned_variables,isDistinct=True) #What the user wanted to scan
                self.fixed_motors=Meta_tag('fixed_motors',fixed_motors) #which motors are fixed
                self.fixed_energy=Meta_tag('fixed_energy',fixed_energy,isDistinct=True)
                self.fixed_eief=Meta_tag('fixed_eief',fixed_eief,isDistinct=True) #either ei or ef
                self.counting_standard=Meta_tag('counting_standard',counting_standard,isDistinct=True) # this is either monitor or time
                self.desired_detector=Meta_tag('desired_detector',desired_detector,isDistinct=True) #detector, sd, psddet, etc.
                
class IceMetaData(MetaData):
        def __init__(self, ice_version=None, ice_repository_info=None, experimental_details=None,
                     experiment_comment=None, desired_npoints=None, user=None, ranges=None,scan_description=None):
                super(IceMetaData,self).__init__()
                self.ice_version=Meta_tag('ice_version',ice_version)
                self.ice_repository_info=Meta_tag('ice_repository_info',ice_repository_info)
                self.experiment_details=Meta_tag('experiment_details',experimental_details)
                self.experiment_comment=Meta_tag('experiment_comment',experiment_comment)
                self.desired_npoints=Meta_tag('npoints',desired_npoints)
                self.user=Meta_tag('user',user)
                self.ranges=Meta_tag('ranges',ranges)
                self.scan_description=Meta_tag('scan_description',scan_description)



class Component(object):
        """This is the Component class.  A Component must have a name, for example, 'a1'
        Furthermore, it is given a set of values and stderr for initialization.
        units are optional.  Internally, we store a "measurement".  This can be
        accessed from measurement.x, measurement.dx
        """

        def _getx(self): return self.measurement.x
        def _setx(self,x): 
                self.measurement.x=x
        def _get_variance(self): return self.measurement.variance
        def _set_variance(self,variance):
                self.measurement.variance=variance
        def _getdx(self): 
                if self.variance==None:
                        return self.variance
                return np.sqrt(self.variance)                
        def _setdx(self,dx):
                # Direct operation
                #    variance = dx**2
                # Indirect operation to avoid temporaries
                self.variance[:] = dx
                self.variance **= 2
        x=property(_getx,_setx,doc='value')
        variance=property(_get_variance,_set_variance,doc='variance')
        dx = property(_getdx,_setdx,doc="standard deviation")

        #Out of laziness, I am defining properties of x, variance, and dx, but these only effect
        #the measurement objects attributes.  However, people should do operations on the motor object
        #NOT on these components, otherwise errors will not propagate correctly!!!
        def __init__(self, name,values,err, units=None,aliases=None):
                self.name=name
                self.aliases=aliases
                self.units=units
                #self.values=data
                #self.err=err
                self.measurement=uncertainty.Measurement(values,err**2)
        # np array slicing operations
        def __len__(self):
                return len(self.x)
        def __getitem__(self,key):
                if self.variance:
                        return uncertainty.Measurement(self.x[key],self.variance[key])
                else:
                        return uncertainty.Measurement(self.x[key],None)
                        
        def __setitem__(self,key,value):
                self.x[key] = value.x
                self.variance[key] = value.variance
        def __delitem__(self, key):
                del self.x[key]
                del self.variance[key]
        #def __iter__(self): pass # Not sure we need iter

        # Normal operations: may be of mixed type
        #def __add__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #return uncertainty.Measurement(*err1d.add(self.x,self.variance,other.x,other.variance))
                #else:
                        #return uncertainty.Measurement(self.x+other, self.variance+0) # Force copy
        #def __sub__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #return uncertainty.Measurement(*err1d.sub(self.x,self.variance,other.x,other.variance))
                #else:
                        #return uncertainty.Measurement(self.x-other, self.variance+0) # Force copy
        #def __mul__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #if (not self.variance is None) and not (other.variance is None):
                                #return uncertainty.Measurement(*err1d.mul(self.x,self.variance,other.x,other.variance))
                        #else:
                                #return uncertainty.Measurement(self.x*other.x,None)
                #else:
                        #if (not self.variance is None) and not (other.variance is None):
                                #return uncertainty.Measurement(self.x*other, self.variance*other**2)
                        #else:
                                #return uncertainty.Measurement(self.x*other.x,None)
        #def __truediv__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #if (not self.variance is None) and not (other.variance is None):
                                #return uncertainty.Measurement(*err1d.div(self.x,self.variance,other.x,other.variance))
                        #else:
                                #return uncertainty.Measurement(self.x/other.x,None)
                #else:
                        #if (not self.variance is None) and not (other.variance is None):
                                #return uncertainty.Measurement(self.x/other, self.variance/other**2)
                        #else:
                                #return uncertainty.Measurement(self.x/other, None)
                                
        #def __pow__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        ## Haven't calcuated variance in (a+/-da) ** (b+/-db)
                        #return NotImplemented
                #else:
                        #if (not self.variance is None) and not (other.variance is None):
                                #return uncertainty.Measurement(*err1d.pow(self.x,self.variance,other))
                        #else:
                                #return uncertainty.Measurement(self.x**other,None)

        ## Reverse operations
        #def __radd__(self, other):
                #return uncertainty.Measurement(self.x+other, self.variance+0) # Force copy
        #def __rsub__(self, other):
                #return uncertainty.Measurement(other-self.x, self.variance+0)
        #def __rmul__(self, other):
                #if (not self.variance is None) and not (other.variance is None):
                        #return uncertainty.Measurement(self.x*other, self.variance*other**2)
                #else:
                        #return uncertainty.Measurement(self.x*other, None)
        #def __rtruediv__(self, other):
                #x,variance = err1d.pow(self.x,self.variance,-1)
                #return uncertainty.Measurement(x*other,variance*other**2)
        #def __rpow__(self, other): return NotImplemented

        ## In-place operations: may be of mixed type
        #def __iadd__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #self.x,self.variance \
                            #= err1d.add_inplace(self.x,self.variance,other.x,other.variance)
                #else:
                        #self.x+=other
                #return self
        #def __isub__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #self.x,self.variance \
                            #= err1d.sub_inplace(self.x,self.variance,other.x,other.variance)
                #else:
                        #self.x-=other
                #return self
        #def __imul__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #self.x, self.variance \
                            #= err1d.mul_inplace(self.x,self.variance,other.x,other.variance)
                #else:
                        #self.x *= other
                        #self.variance *= other**2
                #return self
        #def __itruediv__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        #self.x,self.variance \
                            #= err1d.div_inplace(self.x,self.variance,other.x,other.variance)
                #else:
                        #self.x /= other
                        #self.variance /= other**2
                #return self
        #def __ipow__(self, other):
                #if isinstance(other,uncertainty.Measurement):
                        ## Haven't calcuated variance in (a+/-da) ** (b+/-db)
                        #return NotImplemented
                #else:
                        #self.x,self.variance = err1d.pow_inplace(self.x, self.variance, other)
                #return self

        ## Use true division instead of integer division
        #def __div__(self, other): return self.__truediv__(other)
        #def __rdiv__(self, other): return self.__rtruediv__(other)
        #def __idiv__(self, other): return self.__itruediv__(other)


        ## Unary ops
        #def __neg__(self):
                #return uncertainty.Measurement(-self.x,self.variance)
        #def __pos__(self):
                #return self
        #def __abs__(self):
                #return uncertainty.Measurement(np.abs(self.x),self.variance)

        def __str__(self):
                #return str(self.x)+" +/- "+str(np.sqrt(self.variance))
                if np.isscalar(self.x):
                        return format_uncertainty(self.x,np.sqrt(self.variance))
                else:
                        Nx=self.x.shape[0]
                        try:
                                Ny=self.x.shape[1]
                        except IndexError:
                                Ny=1
                        res=[]
                        if len(self.x.shape)==3:
                                for ny in range(Ny):
                                        for nx in range(Nx):
                                                res.append([format_uncertainty(v,dv) for v,dv in zip(self.x[:,nx,ny],np.sqrt(self.variance[:,nx,ny]))])
                        else:
                                for nx in range(Nx):
                                        if not self.variance is None:
                                                res.append([format_uncertainty(v,dv) for v,dv in zip(self.x,None)])
                                        else:
                                                for nx in range(Nx):
                                                        res.append(format_uncertainty(self.x[nx],None))                                                
                                                
                        return np.array(res).T.__repr__()
        def __repr__(self):
                return "Measurement(%s,%s)"%(str(self.x),str(self.variance))

        # Not implemented
        def __floordiv__(self, other): return NotImplemented
        def __mod__(self, other): return NotImplemented
        def __divmod__(self, other): return NotImplemented
        def __mod__(self, other): return NotImplemented
        def __lshift__(self, other): return NotImplemented
        def __rshift__(self, other): return NotImplemented
        def __and__(self, other): return NotImplemented
        def __xor__(self, other): return NotImplemented
        def __or__(self, other): return NotImplemented

        def __rfloordiv__(self, other): return NotImplemented
        def __rmod__(self, other): return NotImplemented
        def __rdivmod__(self, other): return NotImplemented
        def __rmod__(self, other): return NotImplemented
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

        def __invert__(self): return NotImplmented  # For ~x
        def __complex__(self): return NotImplmented
        def __int__(self): return NotImplmented
        def __long__(self): return NotImplmented
        def __float__(self): return NotImplmented
        def __oct__(self): return NotImplmented
        def __hex__(self): return NotImplmented
        def __index__(self): return NotImplmented
        def __coerce__(self): return NotImplmented

        def log(self):
                return uncertainty.Measurement(*err1d.log(self.x,self.variance))

        def exp(self):
                return uncertainty.Measurement(*err1d.exp(self.x,self.variance))

        def log(val): return self.log()
        def exp(val): return self.exp()


def err_check(values,err):
        if err==None:
                measurement=uncertainty.Measurement(values, err)
        else:
                measurement=uncertainty.Measurement(values, err**2)
        return measurement
        
        
class Motor(Component):
        """This is the motor class.  A Motor must have a name, for example, 'a1'
        Furthermore, it is given a set of values and stderr for initialization.
        units are optional.  Internally, we store a "measurement".  This can be
        accesed from measurement.x, measurement.dx
        """


        def __init__(self,name,values=None,err=None,units='degrees',isDistinct=True, 
                     window=eps,aliases=None,friends=None,spectator=False,
                     isInterpolatable=False):
                self.name=name
                self.units=units
                self.measurement=err_check(values,err)
                self.aliases=aliases
                self.isDistinct=isDistinct
                self.isInterpolatable=isInterpolatable
                self.spectator=spectator
                #The spectator flag says if I was moving or not during a scan.
                self.window=window #The window in which values are to be deemed equal, it assumes that the isDistinct flag is set 
                self.friends=friends  
                #If I am updated, then my friends might need to be updated, for example, hkl-> a3,a4, etc.


class SampleEnvironment(Component):
        """This is the SampleEnvironment class.  SampleEnvironment must have a name, for example, 'Temperature'
        Furthermore, it is given a set of values and stderr for initialization.
        units are optional.  Internally, we store a "measurement".  This can be
        accesed from measurement.x, measurement.dx
        """


        def __init__(self,name=None,values=None,err=None,units='degrees',isDistinct=True, 
                     window=eps,aliases=None,friends=None,spectator=False,
                     isInterpolatable=False):
                self.name=name
                self.units=units
                self.measurement=err_check(values,err)
                self.aliases=aliases
                self.isDistinct=isDistinct
                self.isInterpolatable=isInterpolatable
                self.spectator=spectator
                #The spectator flag says if I was moving or not during a scan.
                self.window=window #The window in which values are to be deemed equal, it assumes that the isDistinct flag is set 
                self.friends=friends  
                #If I am updated, then my friends might need to be updated, for example, hkl-> a3,a4, etc.

                

class Detector(Component):
        """This is the detector class.  A detector must have a name, for example, 'psd'
        Furthermore, it is given a set of values and stderr for initialization.
        units are optional.  Internally, we store a "measurement".  This can be
        accesed from measurement.x, measurement.dx
        """


        def __init__(self,name,dimension=None,values=None,err=None,units='counts', 
                     aliases=None,friends=None, isInterpolatable=True,isDistinct=None, efficiencies=None):
                self.name=name
                self.units=units
                self.measurement=err_check(values,err)
                self.aliases=aliases
                self.isDistinct=isDistinct
                self.isInterpolatable=isInterpolatable
                self.friends=friends  
		self.efficiencies=efficiencies
                #If I am updated, then my friends might need to be updated
                self.dimension=dimension
                #Internally, I imagine that we should internally store the detector a multidimensional array.
                # Each point is an array that is nxm pixels and then we have k points.  So, for a 2D psd for example,
                # we would have kpoints x (n x m) array where n and m define the dimensions of the 2D psd
        
        def correct_efficiencies(self,efficiencies):
                """This function will correct the detector for efficiencies, in place"""
                pass
        def correct_offsets(self, offsets):
                """This function will transform from a central a4, to the actual a4 """
                pass
        def sum(self,axis=0):
                """This function will find the total counts on the detector along a given axis, similar to np.sum(axis=1).  This should be for Measurement objects, so we can propagate errors as well.
                """
                pass

#class DetectorSet(object):
#        def __init__(self):
#                self.name=name
#        def __getitem__(self, key): return self.__dict__[key]
#        def __setitem__(self, key, item): self.__dict__[key] = item
 
class DetectorSet(object):
        """This defines a group of detectors"""
        def __init__(self):
                self.primary_detector=Detector('primary_detector',dimension=None,values=None,err=None,units='counts', 
                     aliases=None,friends=None, isInterpolatable=True)
                self.detector_mode=None
                        
        def __iter__(self):
                #temp_dict=copy.deepcopy(self.__dict__)
                #temp_dict.__delitem__('detector_mode')
                
                #temp_dict.__delitem__('primary_detector')
                #for key,value in temp_dict.iteritems():
                for key,value in self.__dict__.iteritems():
                        if not key=='detector_mode':
                                yield value

        #def next(self):
        #        for key, value in self.__dict__.iteritems():
        #                yield value
                


                          
class Mosaic(object):
        def __init__(self,horizontal=None, vertical=None):
                self.horizontal=horizontal
                self.vertical=vertical

class Monochromator(object):
        """A monochromator"""
        def __init__(self, name='Monochromator', 
                     vertical_focus=None,
                     horizontal_focus=None,
                     monochromator_translation=None,
                     blades=None,
                     mosaic=None,
                     dspacing=None  #dspacing of the monochromator
                     ):
                self.name=name
                self.vertical_focus=vertical_focus
                self.horizontal_focus=horizontal_focus
                self.blades=blades #this is an array of the monochromator blades
                self.mosaic=mosaic
                self.dspacing=dspacing
                self.focus_cu=Motor('focus_cu',values=None,err=None,units='degrees',isDistinct=True,
                                    isInterpolatable=True)
                self.focus_pg=Motor('focus_pg',values=None,err=None,units='degrees',isDistinct=True,
                                    isInterpolatable=True)
                self.translation=Motor('translation',values=None,err=None,units='degrees',isDistinct=False,
                                    isInterpolatable=True)
                self.elevation=Motor('elevation',values=None,err=None,units='degrees',isDistinct=False,
                                    isInterpolatable=True)

class Filters(object):
        """Filters"""
        def __init__(self):
                self.filter_rotation=Motor('filter_rotation',values=None,err=None,units='degrees',isDistinct=False,
                                           isInterpolatable=False)
                self.filter_tilt=Motor('filter_tilt',values=None,err=None,units='degrees',isDistinct=False,
                                       isInterpolatable=False)
                self.filter_translation=Motor('filter_translation',values=None,err=None,units='',isDistinct=True,
                                              isInterpolatable=False)
                #filter translation has values of "IN" and "OUT" 

class Apertures(object):
        def __init__(self):
                self.aperture_horizontal=Motor('aperture_horizontal',values=None,err=None,units='degrees',isDistinct=False,
                                               isInterpolatable=False)
                self.aperture_vertical=Motor('aperture_vertical',values=None,err=None,units='degrees',isDistinct=False,
                                             isInterpolatable=False)

class Time(object):
        def __init__(self):
                self.duration=Motor('duration',values=None,err=None,units='seconds',isDistinct=True,
                                                       isInterpolatable=True)
                self.timestamp=Motor('timestamp',values=None,err=None,units='seconds',isDistinct=False,
                                                       isInterpolatable=True)
                #We should decide if we ignore timestamps, for now let's do so....
                self.monitor=Motor('monitor',values=None,err=None,units='neutrons',isDistinct=False,
                                                       isInterpolatable=True)
                self.monitor2=Motor('monitor2',values=None,err=None,units='neutrons',isDistinct=False,
                                                       isInterpolatable=True)

class Temperature(object):                
        def __init__(self):
                self.temperature=SampleEnvironment('temperature',values=None,err=None,units='K',isDistinct=True,
                                               isInterpolatable=True)
                self.temperature_control_reading=SampleEnvironment('temperature_control_reading',values=None,err=None,units='K',isDistinct=False,
                                               isInterpolatable=True)
                self.temperature_heater_power=SampleEnvironment('temperature_heater_power',values=None,err=None,units='percentage',isDistinct=False,
                                               isInterpolatable=True) #usuallly a percentage for most controllers...
                self.temperature_setpoint=SampleEnvironment('temperature_setpoint',values=None,err=None,units='K',isDistinct=False,
                                               isInterpolatable=True)
                

class MagneticField(object):                
        def __init__(self):
                self.magnetic_field=SampleEnvironment('magnetic_field',values=None,err=None,units='Tesla',isDistinct=True,
                                               isInterpolatable=True)

  
        
                
                
class Analyzer(object):
        """An analyzer"""
        def __init__(self, name='Analyzer',
                     vertical_focus=None,
                     horizontal_focus=None,
                     blades=None,
                     mosaic=None,
                     dspacing=None,  #dspacing of the monochromator
                     focus_mode=None,
                     detector_mode=None
                     ):
                self.name=name
                self.blades=blades
                self.mosaic=mosaic
                self.detector_mode=detector_mode #DiffDet, SinglDetFlat,SinglDetHFoc,PSDDiff,PSDFlat,Undefined
                self.focus_mode=focus_mode
                self.dspacing=dspacing
                
                




class Primary_Motors(object):
        def __init__(self):
                """These are a1, which defines the focusing convention and is equal to "dfm" in files
                a5 also defines the focusing condition.  Instead, use analyzer_rotation and dfm_rotation
                when present to do calculations.
                
                """
                self.a1=Motor('a1',values=None,err=None,units='degrees',isDistinct=True, isInterpolatable=True)
                self.a2=Motor('a2',values=None,err=None,units='degrees',isDistinct=True, isInterpolatable=True)
                self.a3=Motor('a3',values=None,err=None,units='degrees',isDistinct=True, isInterpolatable=True)
                self.a4=Motor('a4',values=None,err=None,units='degrees',isDistinct=True, isInterpolatable=True)
                self.a5=Motor('a5',values=None,err=None,units='degrees',isDistinct=True, isInterpolatable=True)
                self.a6=Motor('a6',values=None,err=None,units='degrees',isDistinct=True, isInterpolatable=True)
                self.sample_elevator=Motor('sample_elevator',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True)
                self.sample_upper_tilt=Motor('sample_upper_tilt',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True) #note, needs to be changed in UB Mode
                self.sample_lower_tilt=Motor('sample_lower_tilt',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True) #note, needs to be changed in UB Mode
                self.sample_upper_translation=Motor('sample_upper_translation',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True)
                self.sample_lower_translation=Motor('sample_lower_translation',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True) #note, needs to be changed in UB Mode
                self.dfm_rotation=Motor('dfm_rotation',values=None,err=None,units='degrees',isDistinct=True
                                        , isInterpolatable=True)
                self.analyzer_rotation=Motor('analyzer_rotation',values=None,err=None,units='degrees',isDistinct=True
                                             , isInterpolatable=True)
                #self.aperture_horizontal=Motor('aperture_horizontal',values=None,err=None,units='degrees',isDistinct=True
                #                               , isInterpolatable=True)
                #self.aperture_vertical=Motor('aperture_vertical',values=None,err=None,units='degrees',isDistinct=True
                #                             , isInterpolatable=True)


class Physical_Motors(object):
        def __init__(self):
                self.h=Motor('h',values=None,err=None,units='rlu',isDistinct=True,
                             isInterpolatable=True)
                self.k=Motor('k',values=None,err=None,units='rlu',isDistinct=True,
                             isInterpolatable=True)
                self.l=Motor('l',values=None,err=None,units='rlu',isDistinct=True,
                             isInterpolatable=True)
                self.e=Motor('e',values=None,err=None,units='meV',isDistinct=True,
                             isInterpolatable=True)
                self.ei=Motor('ei',values=None,err=None,units='meV',isDistinct=True,
                             isInterpolatable=True)
                self.ef=Motor('ef',values=None,err=None,units='meV',isDistinct=True,
                             isInterpolatable=True)
                self.q=Motor('q',values=None,err=None,units='angstrom_inverse',isDistinct=True,
                             isInterpolatable=True)
		self.orient1=Motor('orient1',values=None,err=None,units='rlu',isDistinct=True,
                             isInterpolatable=True)
		self.orient2=Motor('orient2',values=None,err=None,units='rlu',isDistinct=True,
                             isInterpolatable=True)
		self.orient3=Motor('orient3',values=None,err=None,units='rlu',isDistinct=True,
                             isInterpolatable=True)
                #self.qx=Motor('qx',values=None,err=None,units='rlu',isDistinct=True,
                #              isInterpolatable=True)
                #self.qy=Motor('qy',values=None,err=None,units='rlu',isDistinct=True,
                #              isInterpolatable=True)
                #self.qz=Motor('qz',values=None,err=None,units='rlu',isDistinct=True,
                #              isInterpolatable=True)
                #self.hkl=Motor('hkl',values=None,err=None,units='rlu',isDistinct=True,
                #               isInterpolatable=True) #is this a tuple???

class Collimators(object):
        """Our collimators:  
        post_analyzer_collimator:user_defined
        post_monochromator_collimator:user_defined
        pre_analyzer_collimator:user_defined
        pre_monochromator_collimator:measured
        For the radial and soller collimators, these are angles on the track.  Others
        self.radial_collimator:  For horizontal focusing mode, rc=a6
        self.soller_collimator:  When in flat mode, the 50 minute collimator=a6, 
        others have a fixed offset relative to this one.  Within some window, these
        are likely to remain constant.  Thus, from the angle on the track, we could probably
        determine what the likely collimation status is.  This may be a candidate for a 
        "slowly varying" property.  For now, we will treat these as nonDistict

        """
        def __init__(self):
                self.post_analyzer_collimator=Motor('post_analyzer_collimator',values=None,err=None,units='minutes',isDistinct=False)
                self.post_monochromator_collimator=Motor('post_monochromator_collimator',values=None,err=None,units='minutes',isDistinct=False)
                self.pre_analyzer_collimator=Motor('pre_analyzer_collimator',values=None,err=None,units='minutes',isDistinct=False)
                self.pre_monochromator_collimator=Motor('post_monochromator_collimator',values=None,err=None,units='minutes',isDistinct=True)
                self.radial_collimator=Motor('radial_collimator',values=None,err=None,units='degrees',isDistinct=True, window=2.0)
                self.soller_collimator=Motor('soller_collimator',values=None,err=None,units='degrees',isDistinct=False, window=2.0)

                
class Blades(object):
        def __init__(self,title='',nblades=7):
                self.blades=[]
                for i in range(nblades):
                        self.blades.append(Motor(title+'_blade_'+str(i),values=None,err=None,units='degrees',isDistinct=False))

                
                
class PolarizedBeam(object):
        def __init__(self):
                self.ei_flip=Motor('ei_flip',values=None,err=None,units='amps',isDistinct=False) #used to determine if the flipper is on
                self.ef_flip=Motor('ef_flip',values=None,err=None,units='amps',isDistinct=False)
                self.ef_guide=Motor('ef_guide',values=None,err=None,units='amps',isDistinct=False) #guide field
                self.ei_guide=Motor('ei_guide',values=None,err=None,units='amps',isDistinct=False)
                self.ei_cancel=Motor('ei_cancel',values=None,err=None,units='amps',isDistinct=False)
                self.ef_cancel=Motor('ei_flip',values=None,err=None,units='amps',isDistinct=False)
                self.hsample=Motor('ei_flip',values=None,err=None,units='amps',isDistinct=False) #horizontal current
                self.vsample=Motor('ei_flip',values=None,err=None,units='amps',isDistinct=False) #vertical current
                self.sample_guide_field_rotatation=Motor('sample_guide_field_rotation',values=None,err=None,units='degrees',isDistinct=False)
                self.flipper_state=Motor('flipper_state',values=None,err=None,units='',isDistinct=False) #short hand, can be A,B,C, etc.


class Slits(object):
        def __init__(self):
                self.back_slit_height=Motor('back_slit_height',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True) 
                self.back_slit_width=Motor('back_slit_width',values=None,err=None,units='degrees',isDistinct=False
                                           , isInterpolatable=True) 
                



class TripleAxis(object):
        def __init__(self):
		self.data=[] #large nd array of all data columns
                self.monochromator=Monochromator()
                self.analyzer=Analyzer()
                self.sample=Sample()
                self.detectors=DetectorSet()
                self.filters=Filters()
                self.slits=Slits()
                self.polarized_beam=PolarizedBeam()
                self.collimators=Collimators()
                self.primary_motors=Primary_Motors()
                self.physical_motors=Physical_Motors()
                self.time=Time()
                self.sample_environment=SampleEnvironment()
                self.meta_data=IceMetaData()
                self.apertures=Apertures()
                self.temperature=Temperature()
                
                self.analyzer_blades=Blades(title='analyzer',nblades=8)
        def detailed_balance(self):
                beta_times_temp = 11.6
                beta = beta_times_temp /self.temperature.temperature
                E=self.physical_motors.e
                for detector in self.detectors:
                        detector.measurement=detector.measurement*np.exp(-beta*E/2)
                return
        def normalize_monitor(self,monitor):
                # Turns out iterating through self.detectors makes detector a copy,
                # and doesn't actually modify self.detectors -> could be the 'yield'
                # statement producing a generator...
                mon0=self.time.monitor.measurement 
                for detector in self.detectors:
                        detector.measurement=detector.measurement*(mon0/monitor)
                        print 'hi'
                        #for i in range(0,len(detector.measurement.x)):
                        #        detector.measurement[i]=detector.measurement[i]*mon0[i]/monitor
                return
        def harmonic_monitor_correction(self, instrument_name):
                """Multiplies the monitor correction through all of the detectors in the Detector_Sets."""
                #Use for constant-Q scans with fixed scattering energy, Ef.
                #CURRENTLY: Assumes Ef is fixed under constant-Q scan; could implement check later
        
                coefficients = establish_correction_coefficients('monitor_correction_coordinates.txt')
                M = coefficients[instrument_name]
                for i in range(0, len(M)):
                        M[i]=float(M[i])
                #TODO - Throw error if there's an improper instrument_name given
                for detector in self.detectors:
                        Eii=self.physical_motors.ei.measurement
                        detector.measurement=detector.measurement*(M[0] + M[1]*Eii + M[2]*Eii**2 + M[3]*Eii**3 + M[4]*Eii**4)
                return
                        
        def resolution_volume_correction(self):
                """Correct constant Q-scans with fixed incident energy, Ei, for the fact that the resolution volume changes
                as Ef changes"""
                # Requires constant-Q scan with fixed incident energy, Ei
                # theta_analyzer is occasionally producing a Measurement of Nan's only because
                #    it is taking the arcsin of a value > 1
                wavelength_analyzer=np.sqrt(81.80425/self.physical_motors.ef.measurement) #determine the wavelength based on the analyzer
                theta_analyzer=np.arcsin(wavelength_analyzer/2/self.analyzer.dspacing)  #This is what things should be 
                #alternatively, we could do theta_analyzer=np.radians(self.primary_motors.a6.measurement/2)
                argument=np.arcsin(np.pi/(.69472*self.analyzer.dspacing*np.sqrt(self.physical_motors.ei.measurement)))
                norm=(self.physical_motors.ei.measurement**1.5)/np.tan(argument)
                rescor=norm*np.tan(theta_analyzer)/self.physical_motors.ef.measurement**1.5
                for detector in bt7.detectors:
                        detector.measurement=detector.measurement*rescor
                return
	
	#def calc_plane(self, h, k, l):

		##o1=np.array([1,-1,0])
		##o2=np.array([1,1,-2])
		#o1,o2,o3=self.calc_basis()
		#A=np.array([o1,o2,o3]).T #now o1, o2, o3 form an orthonormal basis
		
		#a_arr=[]
		#b_arr=[]
		#c_arr=[]
		#h=self.physical_motors.h.measurement.x
		#k=self.physical_motors.k.measurement.x
		#l=self.physical_motors.l.measurement.x
		#res=0
		
		#for i in range(len(h)):
			#hkl=np.array([h[i],k[i],l[i]])
			#sol=np.linalg.solve(A,hkl)
			#a=sol[0]
			#b=sol[1]
			#c=sol[2]
			#a_arr.append(a)
			#b_arr.append(b)
			#c_arr.append(c)
		#return a_arr,b_arr,c_arr
	
	#def calc_basis(self, orient1, orient2):
		#"""Constructs the orothonormal bases for a TripleAxis object that has
		#two orientation vectors, orient1 and orient2."""
		#orient3 = np.cross(orient1,orient2)
		#A = np.array([orient1,orient2,orient3]).T
		#a_arr = []
		#b_arr = []
		#c_arr = []

		##Now, let's remap h,k,l into a linear combination of o1,o2,o3 s.t. for any point (h,k,l)
		##(h,k,l)=a*o1+b*o2+c*o3
		#for i in range(len(h)):
			#hkl=np.array([h[i],k[i],l[i]])
			#sol=np.linalg.solve(A,hkl);
			#[a,b,c]=sol
			##we use a solver because it is more numerically stable than simply taking the inverse
			#a_arr.append(a)
			#b_arr.append(b)
			#c_arr.append(c)		
		
		##need to use setattr?
		#self.physical_motors.orient1=a_rr
		#self.physical_motors.orient2=b_rr
		#self.physical_motors.orient3=c_rr
		
        def get_plottable(self):
        	#if self.detectors.primary_detector.dx==None:
			
                plottable_data = {
                        'type': 'nd',
                        'title': 'Triple Axis Plot',
                        'clear_existing': False,
                        'orderx': ['h', 'k', 'l'],
                        'ordery': ['primary_detector'],
                        'series': [{
                                'label': 'File 1',
                                'data': {
                                        'h': {
                                                'label': 'h',
                                                'values': self.physical_motors.h.x.tolist(),
                                                'errors': None,
                                                },
                                        'k': {
                                                'label': 'k',
                                                'values': self.physical_motors.k.x.tolist(),
                                                'errors': None,
                                                },
                                        'l': {
                                                'label': 'l',
                                                'values': self.physical_motors.l.x.tolist(),
                                                'errors': None,
                                                },
                                        'primary_detector': {
                                                'label': 'Primary Detector',
                                                'values': self.detectors.primary_detector.x.tolist(),
                                                'errors': None,
                                                },
                                        },
                                'color': 'Red',
                                'style': 'line',
                                },
                        ],
                }
                return plottable_data


# ****************************************************************************************************************************************************
# ***************************************************************** TRANSLATION METHODS **************************************************************
# ****************************************************************************************************************************************************
def translate(bt7,dataset):
        translate_monochromator(bt7,dataset)
        translate_analyzer(bt7,dataset)
        translate_collimator(bt7,dataset)
	translate_sample(bt7,dataset) #sample must be done before physical motors to calculate orient1,2,3 from dataset
        translate_primary_motors(bt7,dataset) #primary motors must be done before physical motors for Q calc.
        translate_physical_motors(bt7,dataset)
        translate_filters(bt7,dataset)
        translate_apertures(bt7,dataset)
        #translate_polarized_beam(bt7,dataset)
        translate_slits(bt7,dataset)
        translate_temperature(bt7,dataset)
        translate_time(bt7,dataset)
        translate_metadata(bt7,dataset)
        translate_detectors(bt7,dataset)


def translate_monochromator(bt7,dataset):
	#TODO:
	#append data from dataset to bt7.data (nd list) then set bt7.monochromator.field=bt7[val]
        translate_dict={}
        #key--> on bt7
        #value -> input, i.e. the field in dataset.data or dataset.metadata
        translate_dict['focus_cu']='focuscu'
        translate_dict['focus_pg']='focuspg'
        translate_dict['horizontal_focus']='monohorizfocus'
        translate_dict['vertical_focus']='monovertifocus'
        translate_dict['translation']='monotrans'
        translate_dict['elevation']='monoelev'
        translate_dict['dspacing']='monochromator_dspacing'
        map_motors(translate_dict, bt7.monochromator, dataset)
        
        #for key,value in translate_dict.iteritems():
        #        if dataset.data.has_key(value):
        #                setattr(bt7.monochromator,key,dataset.data[value])
        #        if dataset.metadata.has_key(value):
        #                setattr(bt7.monochromator,key,dataset.metadata[value])
                
        #bt7.monochromator.focus_cu=dataset.data['focuscu']
        #bt7.monochromator.focus_pg=dataset.data['focuspg']
        #bt7.monochromator.horizontal_focus=dataset.metadata['monohorizfocus']
        #bt7.monochromator.vertical_focus=dataset.metadata['monovertifocus']
        #bt7.monochromator.translation=dataset.data['monotrans']
        #bt7.monochromator.elevation=dataset.data.monoelev
        #bt7.monochromator.dspacing=dataset.metadata.monochromator_dspacing
        monochromator_blades=Blades(title='monochromator',nblades=10)
        for i in range(10):
                if i<9:
                        key='monoblade0'+str(i+1)
                else:
                        key='monoblade'+str(i+1)
                if dataset.data.has_key(key):
                        monochromator_blades.blades[i]=dataset.data[key]
        #monochromator_blades.blades[0]=dataset.data['monoblade01
        #monochromator_blades.blades[1]=dataset.data['monoblade02
        #monochromator_blades.blades[2]=dataset.data['monoblade03
        #monochromator_blades.blades[3]=dataset.data['monoblade04
        #monochromator_blades.blades[4]=dataset.data['monoblade05
        #monochromator_blades.blades[5]=dataset.data['monoblade06
        #monochromator_blades.blades[6]=dataset.data.monoblade07
        #monochromator_blades.blades[7]=dataset.data.monoblade08
        #monochromator_blades.blades[8]=dataset.data.monoblade09
        #monochromator_blades.blades[9]=dataset.data.monoblade10
        bt7.monochromator.blades=monochromator_blades
       
        
        
def translate_analyzer(bt7,dataset):
        bt7.analyzer.dspacing=dataset.metadata['analyzer_dspacing']
        if dataset.metadata.has_key('analyzerfocusmode'):
                bt7.analyzer.focus_mode=dataset.metadata['analyzerfocusmode']
        analyzer_blades=Blades(title='analyzer',nblades=13)
        for i in range(13):
                if i<9:
                        key='analyzerblade0'+str(i+1)
                else:
                        key='analyzerblade'+str(i+1)
                if dataset.data.has_key(key):
                        analyzer_blades.blades[i]=dataset.data[key]
        #analyzer_blades.blades[0]=dataset.data.analyzerblade01
        #analyzer_blades.blades[1]=dataset.data.analyzerblade02
        #analyzer_blades.blades[2]=dataset.data.analyzerblade03
        #analyzer_blades.blades[3]=dataset.data.analyzerblade04
        #analyzer_blades.blades[4]=dataset.data.analyzerblade05
        #analyzer_blades.blades[5]=dataset.data.analyzerblade06
        #analyzer_blades.blades[6]=dataset.data.analyzerblade07
        #analyzer_blades.blades[7]=dataset.data.analyzerblade08
        #analyzer_blades.blades[8]=dataset.data.analyzerblade09
        #analyzer_blades.blades[9]=dataset.data.analyzerblade10
        #analyzer_blades.blades[10]=dataset.data.analyzerblade11
        #analyzer_blades.blades[11]=dataset.data.analyzerblade12
        #analyzer_blades.blades[12]=dataset.data.analyzerblade13
        bt7.analyzer.blades=analyzer_blades
        

      
def translate_collimator(bt7,dataset):
        bt7.collimators.pre_monochromator_collimator=dataset.data['premonocoll']
        bt7.collimators.post_monochromator_collimator =dataset.data['postmonocoll']
        bt7.collimators.pre_analyzer_collimator=dataset.data['preanacoll']
        bt7.collimators.post_analyzer_collimator=dataset.data['postanacoll']
        
        if dataset.data.has_key('rc'):
                bt7.collimators.radial_collimator=dataset.data['rc']
        if dataset.data.has_key('sc'):
                bt7.collimators.soller_collimator=dataset.data['sc']
        
def translate_apertures(bt7,dataset):
        translate_dict={}
        translate_dict['aperture_horizontal']='aperthori'
        translate_dict['aperture_vertical']='apertvert'
        map_motors(translate_dict, bt7.apertures, dataset)

        #bt7.apertures.aperture_horizontal=dataset.aperthori
        #bt7.apertures.aperture_vertical=dataset.apertvert
            
def translate_polarized_beam(bt7,dataset):
        translate_dict={}
        translate_dict['ei_flip']='eiflip'
        translate_dict['ef_flip']='efflip'
        translate_dict['ei_guide']='eiguide'
        translate_dict['ef_guide']='efguide'
        translate_dict['ei_cancel']='eicancel'
        translate_dict['ef_cancel']='efcancel'
        translate_dict['sample_guide_field_rotatation']='smplgfrot'
        translate_dict['flipper_state']='flip'
        translate_dict['hsample']='hsample'
        translate_dict['vsample']='vsample'

        map_motors(translate_dict, bt7.polarized_beam, dataset)

        #bt7.polarized_beam.ei_flip=dataset.eiflip
        #bt7.polarized_beam.ef_flip=dataset.efflip
        #bt7.polarized_beam.ei_guide=dataset.eiguide
        #bt7.polarized_beam.ef_cancel=dataset.efcancel
        #bt7.polarized_beam.sample_guide_field_rotatation=dataset.smplgfrot
        #bt7.polarized_beam.flipper_state=dataset.flip
        #bt7.polarized_beam.hsample=dataset.hsample
        #bt7.polarized_beam.vsample=dataset.vsample
        #bt7.polarized_beam.ef_guide=dataset.efguide
        #bt7.polarized_beam.ei_cancel=dataset.data.eicancel
 
def translate_primary_motors(bt7,dataset):
        translate_dict={}
        translate_dict['sample_upper_tilt']='smplutilt'
        translate_dict['sample_lower_tilt']='smplltilt'
        translate_dict['sample_elevator']='smplelev'
        translate_dict['sample_upper_translation']='smplutrn'
        translate_dict['sample_lower_translation']='smplltrn'
        translate_dict['monochromator_theta']='a1'
        translate_dict['monochromator_two_theta']='a2'
        translate_dict['sample_theta']='a3'
        translate_dict['sample_two_theta']='a4'
        translate_dict['analyzer_theta']='a5'
        translate_dict['analyzer_two_theta']='a6'
        translate_dict['analyzer_rotation']='analyzerrotation'
        translate_dict['dfm_rotation']='dfmrot'
        translate_dict['dfm']='dfm'
        
        map_motors(translate_dict, bt7.primary_motors,dataset)
        
        #for key,value in translate_dict.iteritems():
        #        if dataset.data.has_key(value):
        #                setattr(bt7.primary_motors,key,dataset.data[value])
        #        if dataset.metadata.has_key(value):
        #                setattr(bt7.primary_motors,key,dataset.metadata[value])
        #self.primary_motors.sample_upper_tilt=dataset.data.smplutilt
        #self.primary_motors.sample_lower_tilt=dataset.data.smplltilt
        #self.primary_motors.sample_elevator=dataset.data.smplelev
        #self.primary_motors.sample_upper_translation=dataset.data.smplutrn
        #self.primary_motors.sample_lower_translation=dataset.data.smplltrn
        #self.primary_motors.a1=dataset.data.a1
        #self.primary_motors.a2=dataset.data.a2
        #self.primary_motors.a3=dataset.data.a3
        #self.primary_motors.a4=dataset.data.a4
        #self.primary_motors.a5=dataset.data.a5
        #self.primary_motors.a6=dataset.data.a6
        #self.primary_motors.dfm=dataset.data.dfm
        #self.primary_motors.analyzer_rotation=dataset.data.analyzerrotation
        #self.primary_motors.dfm_rotation=dataset.data.dfmrot


                                
def translate_physical_motors(bt7,dataset):
        translate_dict={}
        #key--> on bt7
        #value -> input, i.e. the field in dataset.data or dataset.metadata
        #translate_dict['hkl']='hkl'
        #In older versions, we cannot trust h,k,l, hkl, etc. because we don't know if we went where we wanted. 
        #Should translate to magnitude of q before hand
        translate_dict['h']='qx'
        translate_dict['k']='qy'
        translate_dict['l']='qz'
        translate_dict['e']='e'
        #translate_dict['q']='q'  #need to implement this
        #self.meta_data.fixed_eief=dataset.metadata.efixed
        #self.meta_data.fixed_energy=dataset.metadata.ef
        map_motors(translate_dict,bt7.physical_motors,dataset)
        if dataset.metadata['efixed']=='ei':
                bt7.physical_motors.ei.measurement.x=np.ones(np.array(dataset.data['e']).shape)*dataset.metadata['ei']
                bt7.physical_motors.ei.measurement.variance=None
                bt7.physical_motors.ef=bt7.physical_motors.ei.measurement-bt7.physical_motors.e.measurement
                #our convention is that Ei=Ef+delta_E (aka omega)
        else:
                bt7.physical_motors.ef.measurement.x=np.ones(np.array(dataset.data['e']).shape)*dataset.metadata['ef']
                bt7.physical_motors.ef.measurement.variance=None
                bt7.physical_motors.ei.measurement.x=bt7.physical_motors.ef.measurement.x+bt7.physical_motors.e.measurement.x  #punt for now, later should figure out what to do if variance is None
        
	Ei = bt7.physical_motors.ei.measurement
	Ef = bt7.physical_motors.ef.measurement
	A4 = bt7.primary_motors.sample_two_theta.measurement
        Qsquared = (Ei + Ef - 2*np.sqrt(Ei*Ef)*np.cos(A4/2))/2.072
	Q = np.sqrt(Qsquared)
	bt7.physical_motors.q.measurement=Q
	
	try:
		o1temp=bt7.sample.orientation.orient1
		o2temp=bt7.sample.orientation.orient2
		o1=np.array([o1temp['h'], o1temp['k'], o1temp['l']])
		o2=np.array([o2temp['h'], o2temp['k'], o2temp['l']])
		
		o1=o1/np.linalg.norm(o1) #normalize o1
		o2=o2/np.linalg.norm(o2) #normalize o2, not necessary?
		o3=np.cross(o1,o2)       #construct o3
		o3=o3/np.linalg.norm(o3) #normalize o3, though should already be normalized
		o2=np.cross(o3,o1)       #conctruct unit vector o2
		
		setattr(bt7.physical_motors.orient1, 'value', o1)
		setattr(bt7.physical_motors.orient2, 'value', o2)
		setattr(bt7.physical_motors.orient3, 'value', o3)
		#TODO - make 'fancy' names for these?
		#setattr(bt7.physical_motors.orient3, 'name', '110')
	except:
		pass
        #translate_dict['h']='h'
        #translate_dict['k']='k'
        #translate_dict['l']='l'
        #self.physical_motors.hkl=dataset.data.hkl
        #self.physical_motors.qx=dataset.data.qx
        #self.physical_motors.qy=dataset.data.qy
        #self.physical_motors.qz=dataset.data.qz
        #self.physical_motors.e=dataset.data.e
        
        
def translate_filters(bt7,dataset):
        translate_dict={}
        #key--> on bt7
        #value -> input, i.e. the field in dataset.data or dataset.metadata
        #translate_dict['hkl']='hkl'
        #In older versions, we cannot trust h,k,l, hkl, etc. because we don't know if we went where we wanted. 
        #Should translate to magnitude of q before hand
        translate_dict['filter_tilt']='temp'
        translate_dict['filter_translation']='temperaturesensor1'
        translate_dict['filter_rotation']='temperaturesensor2'
        map_motors(translate_dict,bt7.filters,dataset)
        #self.filters.filter_tilt=dataset.filtilt
        #self.filters.filter_translation=dataset.filtran
        #self.filters.filter_rotation=dataset.filrot


def translate_time(bt7, dataset):
        translate_dict={}
        translate_dict['month']='month'
        translate_dict['day']='day'
        translate_dict['year']='year'
        translate_dict['start_time']='start_time'
        translate_dict['epoch']='epoch'
        translate_dict['duration']='time'
        translate_dict['monitor']='monitor'
        translate_dict['monitor2']='monitor2'
        map_motors(translate_dict,bt7.time,dataset)

        #self.time.timestamp=dataset.timestamp
        #self.time.duration=dataset.data.time
        #self.time.monitor=dataset.data.monitor
        #self.time.monitor2=dataset.data.monitor2

def translate_temperature(bt7,dataset):
        translate_dict={}
        #key--> on bt7
        #value -> input, i.e. the field in dataset.data or dataset.metadata
        #translate_dict['hkl']='hkl'
        #In older versions, we cannot trust h,k,l, hkl, etc. because we don't know if we went where we wanted. 
        #Should translate to magnitude of q before hand
        translate_dict['temperature']='temp'
        translate_dict['temperature_sensor1']='temperaturesensor1'
        translate_dict['tempetature_sensor2']='temperaturesensor2'
        translate_dict['temperature_sensor3']='temperaturesensor3'
        translate_dict['temperature_heater_power']='temperatureheatorpower'
        translate_dict['temperature_control_reading']='temperaturecontrolreading'
        translate_dict['temperature_setpoint']='temperaturesetpoint'
        map_motors(translate_dict,bt7.temperature,dataset)
        if dataset.metadata.has_key('temperature_units'):
                bt7.temperature.temperature.units=dataset.metadata['temperature_units']
        #self.temperature.temperature=dataset.temp
        #self.temperature.temperature.units=dataset.metadata.temperature_units
        #self.temperature.temperaturesensor1=dataset.temperaturesensor1
        #self.temperature.temperaturesensor2=dataset.temperaturesensor2
        #self.temperature.temperaturesensor3=dataset.temperaturesensor3
        #self.temperature.temperature_heater_power=dataset.temperatureheaterpower
        #self.temperature.temperature_control_reading =dataset.temperaturecontrolreading
        #self.temperature.temperature_setpoint =dataset.temperaturesetpoint


def translate_slits(bt7,dataset):
        translate_dict={}
        #key--> on bt7
        #value -> input, i.e. the field in dataset.data or dataset.metadata
        #translate_dict['hkl']='hkl'
        #In older versions, we cannot trust h,k,l, hkl, etc. because we don't know if we went where we wanted. 
        #Should translate to magnitude of q before hand
        translate_dict['back_slit_width']='bksltwdth'
        translate_dict['back_slit_height']='bkslthght'
        map_motors(translate_dict,bt7.slits,dataset)
        #self.slits.back_slit_width =dataset.data.bksltwdth
        #self.slits.back_slit_height =dataset.data.bkslthght
        
        
        
def translate_sample(bt7,dataset):
        translate_dict = {}
        translate_dict['orientation']='orientation'
        translate_dict['lattice']='lattice'
        map_motors(translate_dict,bt7.sample,dataset)
        
	if bt7.sample.orientation.orient1==None:
		#if the dataset has labels 'orient1' and 'orient2' but not 'orientation'
		translate_dict = {}
		translate_dict['orient1']='orient1'
		translate_dict['orient2']='orient2'
		map_motors(translate_dict, bt7.sample.orientation,dataset)
        #bt7.sample.orientation =dataset.metadata.orientation
        #bt7.sample.mosaic=dataset.metadata.?
        #bt7.sample.lattice=dataset.metadata.lattice
        
        
        
def translate_metadata(bt7,dataset):
        translate_dict = {}
        translate_dict['epoch']='epoch'
        translate_dict['counting_standard']='count_type'
        translate_dict['filename']='filename'
        translate_dict['fixed_eief']='efixed'
        translate_dict['fixed_energy']='ef'
        translate_dict['experiment_comment']='exptcomment'
        translate_dict['comment']='comment'
        translate_dict['experiment_id']='experiment_id'
        translate_dict['fixed_devices']='fixed_devices'
        translate_dict['scanned_variables']='varying'
        translate_dict['ice_version']='ice'
        translate_dict['instrument_name']='instrument'
        translate_dict['filebase']='filebase'
        translate_dict['fileseq_number']='fileseq_number'
        translate_dict['experiment_name']='exptname'
        translate_dict['experiment_participants']='exptparticipants'
        translate_dict['experiment_details']='exptdetails'
        translate_dict['desired_detector']='signal'
        translate_dict['ranges']='ranges'
        translate_dict['user']='user'
        translate_dict['scan_description']='scan_description'
        translate_dict['desired_npoints']='npoints'

        map_motors(translate_dict,bt7.meta_data,dataset)

        #self.meta_data.epoch=dataset.metadata.epoch
        #self.meta_data.counting_standard=dataset.metadata.count_type
        #self.meta_data.filename=dataset.metadata.filename
        #self.meta_data.fixed_eief=dataset.metadata.efixed
        #self.meta_data.fixed_energy=dataset.metadata.ef
        #self.meta_data.experiment_comment=dataset.metadata.exptcomment
        #self.meta_data.comment=dataset.metadata.comment
        #self.meta_data.date=dataset.metadata.?
        #self.meta_data.experiment_id=dataset.metadata.experiment_id
        #self.meta_data.fixed_devices=dataset.metadata.fixed_devices
        #self.meta_data.scanned_variables=dataset.metadata.varying
        #self.meta_data.ice_version=dataset.metadata.ice
        #self.meta_data.ice_repository_info=dataset.metadata.?
        #self.meta_data.instrument_name=dataset.metadata.instrument
        #self.meta_data.filebase =dataset.metadata.filebase
        #self.meta_data.fileseq_number=dataset.metadata.fileseq_number
        #self.meta_data.experiment_name=dataset.metadata.exptname
        #self.meta_data.experiment_participants=dataset.metadata.exptparticipants
        #self.meta_data.experiment_details=dataset.metadata.exptdetails
        #self.meta_data.desired_detector=dataset.metadata.signal
        #self.meta_data.ranges=dataset.metadata.ranges
        #self.meta_data.user=dataset.metadata.user
        #self.meta_data.scan_description=dataset.metadata.scan_description
        #self.meta_data.desired_npoints=dataset.metadata.npoints
        
def translate_detectors(bt7,dataset):
        bt7.detectors.primary_detector.measurement.x=np.array(dataset.data['detector'],'Float64')
        bt7.detectors.primary_detector.measurement.variance=np.array(dataset.data['detector'],'Float64')
        bt7.detectors.detector_mode=dataset.metadata['analyzerdetectormode']
        #later, I should do something clever to determine how many detectors are in the file,
        #or better yet, lobby to have the information in the ice file
        #but for now, let's just get something that works
        
        
        #detectors do NOT have a 'summed_counts' attribute currently.
        if dataset.metadata.has_key('analyzersdgroup'):
                set_detector(bt7,dataset,'single_detector','analyzersdgroup')
                #bt7.detectors.single_detector.summed_counts.measurement.x=dataset.data['singledet']
                #bt7.detectors.single_detector.summed_counts.measurement.variance=dataset.data['singledet']
                
        if dataset.metadata.has_key('analyzerdoordetectorgroup'):
                set_detector(bt7,dataset,'door_detector','analyzerdoordetectorgroup')
                #bt7.detectors.single_detector.summed_counts.measurement.x=bt7.detectors.door_detector.x.sum(axis=1)#None #dataset.data['doordet']  #Not sure why this one doesn't show up???
                #bt7.detectors.single_detector.summed_counts.measurement.variance=bt7.detectors.door_detector.x.sum(axis=1)#None #dataset.data['doordet']  #Not sure why this one doesn't show up???
              
        if dataset.metadata.has_key('analyzerddgroup'):
                set_detector(bt7,dataset,'diffraction_detector','analyzerddgroup')
                #bt7.detectors.diffraction_detector.summed_counts.measurement.x=dataset.data['diffdet']
                #bt7.detectors.diffraction_detector.summed_counts.measurement.variance=dataset.data['diffdet']
          
        if dataset.metadata.has_key('analyzerpsdgroup'):
                set_detector(bt7,dataset,'position_sensitive_detector','analyzerpsdgroup')
                #if hasattr(bt7.detectors,'position_sensitive_detector'):
                        #bt7.detectors.position_sensitive_detector.summed_counts.measurement.x=dataset.data['psdet']
                        #bt7.detectors.position_sensitive_detector.summed_counts.measurement.variance=dataset.data['psdet']
               
                
                        
                        
def set_detector(bt7,dataset,detector_name,data_name):                        
        analyzergroup=dataset.metadata[data_name]
        setattr(bt7.detectors,detector_name,Detector(detector_name))
        
        setattr(getattr(bt7.detectors,detector_name),'dimension',[len(dataset.metadata['analyzersdgroup']),1])
        Nx=getattr(getattr(bt7.detectors,detector_name),'dimension')[0]
        Ny=getattr(getattr(bt7.detectors,detector_name),'dimension')[1]
        npts=len(dataset.data[dataset.metadata['analyzersdgroup'][0]])  #I choose this one because the sd group SHOULD always be present.
        data=np.empty((npts,Nx,Ny),'Float64')
        #put all the data in data array which is npts x Nx x Ny, in this case, Ny=1 since our detectors are 1D
        #We have to do some defensive programming here.  It turns out that even though the metadata states that the PSD may be present,
        #There may be no data associated with it.....
        if dataset.data.has_key(dataset.metadata[data_name][0]):
                for nx in range(Nx):
                        curr_detector=dataset.metadata[data_name][nx]
                        data[:,nx,0]=np.array(dataset.data[curr_detector],'Float64')
                
                setattr(getattr(bt7.detectors,detector_name).measurement,'x',np.copy(data))
                setattr(getattr(bt7.detectors,detector_name).measurement,'variance',np.copy(data))
        else:
                delattr(bt7.detectors,detector_name)  #We were lied to by ICE and this detector isn't really present...


		
#Originally working map_motors:
#def map_motors(translate_dict,target_field,dataset):
        ##key --> on bt7
        ##value --> input, i.e. the field in dataset.data or dataset.metadata
        #for key,value in translate_dict.iteritems():
                #'''
                #afield = None
                #try:
                        #afield = getattr(target_field, key)
                #except:
                        #pass
                #'''
                #if dataset.metadata.has_key(value):
                        #if hasattr(target_field, key) and isinstance(getattr(target_field, key),Motor):
                                #getattr(target_field,key).measurement.x=dataset.metadata[value] #do we need try escape logic here?
                                #getattr(target_field,key).measurement.variance=None
                        #else:
                                #setattr(target_field,key,dataset.metadata[value])
                #if dataset.data.has_key(value):
                        #if hasattr(target_field, key) and isinstance(getattr(target_field, key),Motor):
                                #try:
                                        #getattr(target_field,key).measurement.x=np.array(dataset.data[value],'Float64')
                                        #getattr(target_field,key).measurement.variance=None
                                #except:
                                        #getattr(target_field,key).measurement.x=np.array(dataset.data[value])  #These may be "IN", or "OUT", or "N/A"
                                        #getattr(target_field,key).measurement.variance=None
                        #else:
                                #try:
                                        #setattr(target_field,key,Motor(key,values=np.array(dataset.data[value],'Float64'),
                                                                       #err=None,
                                                                       #units=None,
                                                                       #isDistinct=True,
                                                                       #isInterpolatable=True))
                                                                       ##Not sure how I should really be handling this--> this is for the case where the field doesn't already exist
                                #except:
                                        #setattr(target_field,key,Motor(key,values=dataset.data[value],
                                                                       #err=None,
                                                                       #units=None,
                                                                       #isDistinct=True,
                                                                       #isInterpolatable=True))


def map_motors(translate_dict,tas,target_field,dataset):
        #key --> on bt7
        #value --> input, i.e. the field in dataset.data or dataset.metadata
        for key,value in translate_dict.iteritems():
		if dataset.data.has_key(value):
                        if hasattr(target_field, key) and isinstance(getattr(target_field, key),Motor):
                                try:
                                        getattr(target_field,key).measurement.x=np.array(dataset.data[value],'Float64')
                                        getattr(target_field,key).measurement.variance=None
                                except:
                                        getattr(target_field,key).measurement.x=np.array(dataset.data[value])  #These may be "IN", or "OUT", or "N/A"
                                        getattr(target_field,key).measurement.variance=None
                        else:
                                try:
                                        setattr(target_field,key,Motor(key,values=np.array(dataset.data[value],'Float64'),
                                                                       err=None,
                                                                       units=None,
                                                                       isDistinct=True,
                                                                       isInterpolatable=True))
                                                                       #Not sure how I should really be handling this--> this is for the case where the field doesn't already exist
                                except:
                                        setattr(target_field,key,Motor(key,values=dataset.data[value],
                                                                       err=None,
                                                                       units=None,
                                                                       isDistinct=True,
                                                                       isInterpolatable=True))
                elif dataset.metadata.has_key(value):
                        if hasattr(target_field, key) and isinstance(getattr(target_field, key),Motor):
                                getattr(target_field,key).measurement.x=dataset.metadata[value] #do we need try escape logic here?
                                getattr(target_field,key).measurement.variance=None
				tas.data.append(getattr(target_field,key))
                        else:
                                setattr(target_field,key,dataset.metadata[value])
                
                


def establish_correction_coefficients(filename):
        "Obtains the instrument-dependent correction coefficients from a given file and \
         returns them in the dictionary called coefficients"
        datafile = open(filename)

        coefficients = {} # Dictionary of instrument name mapping to its array of M0 through M4
        while 1:
                line = datafile.readline().strip()
                if not line:
                        break
                elif len(line) != 0:
                        #if it's not an empty line, thus one with data
                        if not line.startswith("#"):
                                #if it's not a comment/headers, i.e. actual data
                                linedata = line.split()
                                instrument = linedata.pop(0)
                                coefficients[instrument] = linedata

        return coefficients   


def make_orthonormal(o1,o2):
	"""Given two vectors, creates an orthonormal set of three vectors. 
	Maintains the direction of o1 and the coplanarity of o1 and o2"""
	o1=o1/N.linalg.norm(o1)
	o2=o2/N.linalg.norm(o2)
	o3=N.cross(o1,o2)
	o3=o3/N.linalg.norm(o3)
	o2=N.cross(o3,o1)
	return o1,o2,o3

def calc_plane(p,h,k,l,normalize=True):
	o1=N.array([p[0],p[1],p[2]])
	o2=N.array([p[3],p[4],p[5]])
	if normalize:
		o1,o2,o3=make_orthonormal(o1,o2)
	else:
		o3 = np.cross(o1,o2)
	A=N.array([o1,o2,o3]).T
	a_arr=[]
	b_arr=[]
	c_arr=[]

	for i in range(len(h)):
		hkl=N.array([h[i],k[i],l[i]])
		sol=N.linalg.solve(A,hkl)
		a=sol[0]
		b=sol[1]
		c=sol[2]
		a_arr.append(a)
		b_arr.append(b)
		c_arr.append(c)
	return a_arr,b_arr,c_arr


def cost_func(p,h,k,l):
	a_arr, b_arr, c_arr = calc_plane(p,h,k,l)
	c = N.array(c_arr)
	res = (c-c.mean())**2
	#dof=len(I)-len(p)
	#fake_dof=len(I)
	#print 'chi',(y-ycalc)/err
	return res#/Ierr#/N.sqrt(fake_dof)



def myfunctlin(p, fjac=None,h=None,k=None,l=None):
	# Parameter values are passed in "p"
	# If fjac==None then partial derivatives should not be
	# computed.  It will always be None if MPFIT is called with default
	# flag.
	# Non-negative status value means MPFIT should continue, negative means
	# stop the calculation.
	status = 0
	return [status, cost_func(p,h,k,l)]

def fit_plane(h,k,l,p0=None):
	if p0==None:
		p0=[1./N.sqrt(5),-1./N.sqrt(2),0,0,0,1] #a guess...
	parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
	parinfo=[]
	for i in range(len(p0)):
		parinfo.append(copy.deepcopy(parbase))
	for i in range(len(p0)): 
		parinfo[i]['value']=p0[i]
	if 0:
		for i in range(len(p0)): 
			parinfo[i]['limited']=[1,1]
			parinfo[i]['limits']=[-1,1]
	fa = {'h':h, 'k':k,'l':l}
	print 'linearizing'
	m = mpfit(myfunctlin, p0, parinfo=parinfo,functkw=fa)
	p = m.params
	print 'status = ', m.status
	print 'params = ', m.params
	#your parameters define two noncollinear vectors that will form the basis for your space
	o1=N.array([p[0],p[1],p[2]])
	o2=N.array([p[3],p[4],p[5]])
	o1,o2,o3=make_orthonormal(o1,o2)
	return o1,o2,o3

 

def join(tas1, tas2):
	"""Joins two TripleAxis objects"""
	#average all similar points
	#put all detectors on the same monitor, assumed that the first monitor is desired throughout
	pass #TODO




def filereader(filename):
        filestr=filename
        mydatareader=readncnr.datareader()
        mydata=mydatareader.readbuffer(filestr)
        instrument = TripleAxis()
        translate(instrument, mydata)
        return instrument

if __name__=="__main__":
        #myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\mesh53439.bt7'
        #myfilestr=r'EscanQQ7HorNSF91831.bt7'
        #print 'hi'
        #mydatareader=readncnr.datareader()
        #mydata=mydatareader.readbuffer(myfilestr)
        #print mydata.metadata.varying
        #mydata = filereader('EscanQQ7HorNSF91831.bt7') #NOTE: include the r in the beginning!
        #bt7=TripleAxis()
        #translate(bt7,mydata)
        
        bt7 = filereader('EscanQQ7HorNSF91831.bt7')
        print 'translations done'
	aarr,barr,carr=bt7.calc_plane()
        bt7.normalize_monitor(90000)
        #print 'detailed balance done'
        bt7.harmonic_monitor_correction('BT7')
        bt7.resolution_volume_correction()
        print 'bye'
        


