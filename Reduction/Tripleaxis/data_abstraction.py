import numpy as N
import uncertainty
import readice
import copy
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
        accesed from measurement.x, measurement.dx
        """

        def _getx(self): return self.measurement.x
        def _setx(self,x): 
                self.measurement.x=x
        def _get_variance(self): return self.measurement.variance
        def _set_variance(self,variance):
                self.measurement.variance=variance
        def _getdx(self): return numpy.sqrt(self.variance)
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
        # Numpy array slicing operations
        def __len__(self):
                return len(self.x)
        def __getitem__(self,key):
                return Measurement(self.x[key],self.variance[key])
        def __setitem__(self,key,value):
                self.x[key] = value.x
                self.variance[key] = value.variance
        def __delitem__(self, key):
                del self.x[key]
                del self.variance[key]
        #def __iter__(self): pass # Not sure we need iter

        # Normal operations: may be of mixed type
        def __add__(self, other):
                if isinstance(other,Measurement):
                        return Measurement(*err1d.add(self.x,self.variance,other.x,other.variance))
                else:
                        return Measurement(self.x+other, self.variance+0) # Force copy
        def __sub__(self, other):
                if isinstance(other,Measurement):
                        return Measurement(*err1d.sub(self.x,self.variance,other.x,other.variance))
                else:
                        return Measurement(self.x-other, self.variance+0) # Force copy
        def __mul__(self, other):
                if isinstance(other,Measurement):
                        return Measurement(*err1d.mul(self.x,self.variance,other.x,other.variance))
                else:
                        return Measurement(self.x*other, self.variance*other**2)
        def __truediv__(self, other):
                if isinstance(other,Measurement):
                        return Measurement(*err1d.div(self.x,self.variance,other.x,other.variance))
                else:
                        return Measurement(self.x/other, self.variance/other**2)
        def __pow__(self, other):
                if isinstance(other,Measurement):
                        # Haven't calcuated variance in (a+/-da) ** (b+/-db)
                        return NotImplemented
                else:
                        return Measurement(*err1d.pow(self.x,self.variance,other))

        # Reverse operations
        def __radd__(self, other):
                return Measurement(self.x+other, self.variance+0) # Force copy
        def __rsub__(self, other):
                return Measurement(other-self.x, self.variance+0)
        def __rmul__(self, other):
                return Measurement(self.x*other, self.variance*other**2)
        def __rtruediv__(self, other):
                x,variance = err1d.pow(self.x,self.variance,-1)
                return Measurement(x*other,variance*other**2)
        def __rpow__(self, other): return NotImplemented

        # In-place operations: may be of mixed type
        def __iadd__(self, other):
                if isinstance(other,Measurement):
                        self.x,self.variance \
                            = err1d.add_inplace(self.x,self.variance,other.x,other.variance)
                else:
                        self.x+=other
                return self
        def __isub__(self, other):
                if isinstance(other,Measurement):
                        self.x,self.variance \
                            = err1d.sub_inplace(self.x,self.variance,other.x,other.variance)
                else:
                        self.x-=other
                return self
        def __imul__(self, other):
                if isinstance(other,Measurement):
                        self.x, self.variance \
                            = err1d.mul_inplace(self.x,self.variance,other.x,other.variance)
                else:
                        self.x *= other
                        self.variance *= other**2
                return self
        def __itruediv__(self, other):
                if isinstance(other,Measurement):
                        self.x,self.variance \
                            = err1d.div_inplace(self.x,self.variance,other.x,other.variance)
                else:
                        self.x /= other
                        self.variance /= other**2
                return self
        def __ipow__(self, other):
                if isinstance(other,Measurement):
                        # Haven't calcuated variance in (a+/-da) ** (b+/-db)
                        return NotImplemented
                else:
                        self.x,self.variance = err1d.pow_inplace(self.x, self.variance, other)
                return self

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
                return Measurement(numpy.abs(self.x),self.variance)

        def __str__(self):
                #return str(self.x)+" +/- "+str(numpy.sqrt(self.variance))
                if numpy.isscalar(self.x):
                        return format_uncertainty(self.x,numpy.sqrt(self.variance))
                else:
                        return [format_uncertainty(v,dv)
                                for v,dv in zip(self.x,numpy.sqrt(self.variance))]
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
                return Measurement(*err1d.log(self.x,self.variance))

        def exp(self):
                return Measurement(*err1d.exp(self.x,self.variance))

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
                     aliases=None,friends=None, isInterpolatable=True,isDistinct=None):
                self.name=name
                self.units=units
                self.measurement=err_check(values,err)
                self.aliases=aliases
                self.isDistinct=isDistinct
                self.isInterpolatable=isInterpolatable
                self.friends=friends  
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

class DetectorSet(object):
        def __init__(self):
                self.name=name
        def __getitem__(self, key): return self.__dict__[key]
        def __setitem__(self, key, item): self.__dict__[key] = item
 
                


                          
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
                self.qx=Motor('qx',values=None,err=None,units='rlu',isDistinct=True,
                              isInterpolatable=True)
                self.qy=Motor('qy',values=None,err=None,units='rlu',isDistinct=True,
                              isInterpolatable=True)
                self.qz=Motor('qz',values=None,err=None,units='rlu',isDistinct=True,
                              isInterpolatable=True)
                self.hkl=Motor('hkl',values=None,err=None,units='rlu',isDistinct=True,
                               isInterpolatable=True) #is this a tuple???

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
                

class DetectorSet(object):
        """This defines a group of detectors"""
        def __init__(self):
                self.primary_detector=Detector('primary_detector',dimension=None,values=None,err=None,units='counts', 
                     aliases=None,friends=None, isInterpolatable=True)
                self.detector_mode=None
                        
        def __iter__(self):
                for key,value in self.__dict__:
                        return value
        def next(self):
                for key, value in self.__dict__:
                        yield value


class TripleAxis(object):
        def __init__(self):
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
                
                
                
        def translate(self,dataset):
                self.translate_monochromator(dataset)
        
        def translate_monochromator(self,dataset):
                self.monochromator.focus_cu=dataset.data.focuscu
                self.monochromator.focus_pg=dataset.data.focuspg
                self.monochromator.horizontal_focus=dataset.metadata.monohorizfocus
                self.monochromator.vertical_focus=dataset.metadata.monovertifocus
                self.monochromator.translation=dataset.data.monotrans
                self.monochromator.elevation=dataset.data.monoelev
                self.monochromator.dspacing=dataset.metadata.monochromator_dspacing
                monochromator_blades=Blades(title='monochromator',nblades=10)
                monochromator_blades.blades[0]=dataset.data.monoblade01
                monochromator_blades.blades[1]=dataset.data.monoblade02
                monochromator_blades.blades[2]=dataset.data.monoblade03
                monochromator_blades.blades[3]=dataset.data.monoblade04
                monochromator_blades.blades[4]=dataset.data.monoblade05
                monochromator_blades.blades[5]=dataset.data.monoblade06
                monochromator_blades.blades[6]=dataset.data.monoblade07
                monochromator_blades.blades[7]=dataset.data.monoblade08
                monochromator_blades.blades[8]=dataset.data.monoblade09
                monochromator_blades.blades[9]=dataset.data.monoblade10
                self.monochromator.blades=monochromator_blades
               
                
                
        def translate_analyzer(self,dataset):
                self.analyzer.dspacing=dataset.metadata.analyzer_dspacing
                self.analyzer.focus_mode=dataset.metadata.analyzerfocusmode
                analyzer_blades=Blades(title='analyzer',nblades=13)
                analyzer_blades[0]=dataset.data.analyzerblade01
                analyzer_blades[1]=dataset.data.analyzerblade02
                analyzer_blades[2]=dataset.data.analyzerblade03
                analyzer_blades[3]=dataset.data.analyzerblade04
                analyzer_blades[4]=dataset.data.analyzerblade05
                analyzer_blades[5]=dataset.data.analyzerblade06
                analyzer_blades[6]=dataset.data.analyzerblade07
                analyzer_blades[7]=dataset.data.analyzerblade08
                analyzer_blades[8]=dataset.data.analyzerblade09
                analyzer_blades[9]=dataset.data.analyzerblade10
                analyzer_blades[10]=dataset.data.analyzerblade11
                analyzer_blades[11]=dataset.data.analyzerblade12
                analyzer_blades[12]=dataset.data.analyzerblade13
                self.analyzer.blades=analyzer_blades
                

              
        def translate_collimator(self,dataset):
                self.collimators.pre_analyzer_collimator=dataset.preanacoll
                self.collimators.post_analyzer_collimator=datset.postanacoll
                self.collimators.post_monochromator_collimator =dataset.postmonocoll
                self.collimators.pre_monochromator_collimator=dataset.data.premonocoll
                self.collimators.radial_collimator=dataset.data.rc
                self.collimators.soller_collimator=dataset.data.sc
                
        def translate_apertures(self,dataset):
                self.apertures.aperture_horizontal=dataset.aperthori
                self.apertures.aperture_vertical=dataset.apertvert
                
        def translate_polarized_beam(self,dataset):
                self.polarized_beam.ei_flip=dataset.eiflip
                self.polarized_beam.ef_flip=dataset.efflip
                self.polarized_beam.ei_guide=dataset.eiguide
                self.polarized_beam.ef_cancel=dataset.efcancel
                self.polarized_beam.sample_guide_field_rotatation=dataset.smplgfrot
                self.polarized_beam.flipper_state=dataset.flip
                self.polarized_beam.hsample=dataset.hsample
                self.polarized_beam.vsample=dataset.vsample
                self.polarized_beam.ef_guide=dataset.efguide
                self.polarized_beam.ei_cancel=dataset.data.eicancel
         
        def translate_primary_motors(self,dataset):
                self.primary_motors.sample_upper_tilt=dataset.data.smplutilt
                self.primary_motors.sample_lower_tilt=dataset.data.smplltilt
                self.primary_motors.sample_elevator=dataset.data.smplelev
                self.primary_motors.sample_upper_translation=dataset.data.smplutrn
                self.primary_motors.sample_lower_translation=dataset.data.smplltrn
                self.primary_motors.a1=dataset.data.a1
                self.primary_motors.a2=dataset.data.a2
                self.primary_motors.a3=dataset.data.a3
                self.primary_motors.a4=dataset.data.a4
                self.primary_motors.a5=dataset.data.a5
                self.primary_motors.a6=dataset.data.a6
                self.primary_motors.dfm=dataset.data.dfm
                self.primary_motors.analyzer_rotation=dataset.data.analyzerrotation
                self.primary_motors.dfm_rotation=dataset.data.dfmrot
                
                
        def translate_physical_motors(self,dataset):
                self.physical_motors.h=dataset.data.h
                self.physical_motors.k=dataset.data.k
                self.physical_motors.l=dataset.data.l
                self.physical_motors.hkl=dataset.data.hkl
                self.physical_motors.qx=dataset.data.qx
                self.physical_motors.qy=dataset.data.qy
                self.physical_motors.qz=dataset.data.qz
                self.physical_motors.e=dataset.data.e
                
        def translate_filters(self,dataset):
                self.filters.filter_tilt=dataset.filtilt
                self.filters.filter_translation=dataset.filtran
                self.filters.filter_rotation=dataset.filrot

        def translate_timestamp(self,dataset):
                self.time.timestamp=dataset.timestamp
                self.time.duration=dataset.data.time
                

        def translate_temperature(self,dataset):
                self.temperature.temperature=dataset.temp
                self.temperature.temperature.units=dataset.metadata.temperature_units
                self.temperature.temperaturesensor1=dataset.temperaturesensor1
                self.temperature.temperaturesensor2=dataset.temperaturesensor2
                self.temperature.temperaturesensor3=dataset.temperaturesensor3
                self.temperature.temperature_heater_power=dataset.temperatureheaterpower
                self.temperature.temperature_control_reading =dataset.temperaturecontrolreading
                self.temperature.temperature_setpoint =dataset.temperaturesetpoint
        
        def translate_slits(self,dataset):
                self.slits.back_slit_width =dataset.data.bksltwdth
                self.slits.back_slit_height =dataset.data.bkslthght
                
        
                
                
        def translate_sample(self,dataset):
                self.sample.orientation =dataset.metadata.orientation
               #self.sample.mosaic=dataset.metadata.?
                self.sample.lattice=dataset.metadata.lattice
                
                
                
        def translate_metadata(self,dataset):
                self.meta_data.epoch=dataset.metadata.epoch
                self.meta_data.counting_standard=dataset.metadata.count_type
                self.meta_data.filename=dataset.metadata.filename
                self.meta_data.fixed_eief=dataset.metadata.efixed
                self.meta_data.fixed_energy=dataset.metadata.ef
                self.meta_data.experiment_comment=dataset.metadata.exptcomment
                self.meta_data.comment=dataset.metadata.comment
                #self.meta_data.date=dataset.metadata.
                self.meta_data.experiment_id=dataset.metadata.experiment_id
                self.meta_data.fixed_devices=dataset.metadata.fixed_devices
                self.meta_data.scanned_variables=dataset.metadata.varying
                self.meta_data.ice_version=dataset.metadata.ice
                #self.meta_data.ice_repository_info=dataset.metadata.?
                self.meta_data.instrument_name=dataset.metadata.instrument
                self.meta_data.filebase =dataset.metadata.filebase
                self.meta_data.fileseq_number=dataset.metadata.fileseq_number
                self.meta_data.experiment_name=dataset.metadata.exptname
                self.meta_data.experiment_participants=dataset.metadata.exptparticipants
                self.meta_data.experiment_details=dataset.metadata.exptdetails
                self.meta_data.desired_detector=dataset.metadata.signal
                self.meta_data.ranges=dataset.metadata.ranges
                self.meta_data.user=dataset.metadata.user
                self.meta_data.scan_description=dataset.metadata.scan_description
                self.meta_data.desired_npoints=dataset.metadata.npoints
                
        def translate_detectors(self,dataset):
                self.detectors.primary_detector=dataset.data.detector
                self.detectors.detector_mode=dataset.metadata.analyzerdetectormode
                #later, I should do something clever to determine how many detectors are in the file,
                #or better yet, lobby to have the information in the ice file
                #but for now, let's just get something that works
                
                
                        
                if hasattr(dataset.metadata,'analyzersdgroup'):
                        self.set_detector(dataset,'single_detector','analyzersdgroup')
                        self.detectors.single_detector.summed_counts=dataset.data.singledet
                        
                if hasattr(dataset.metadata,'analyzerdoordetectorgroup'):
                        self.set_detector(dataset,'door_detector','analyzerdoordetectorgroup')
                        self.detectors.single_detector.summed_counts=dataset.data.singledet
                        
                if hasattr(dataset.metadata,'analyzerddgroup'):
                        self.set_detector(dataset,'diffraction_detector','analyzerddgroup')
                        self.detectors.single_detector.summed_counts=dataset.data.diffdet
                        
                if hasattr(dataset.metadata,'analyzerpsdgroup'):
                        self.set_detector(dataset,'position_sensitive_detector','analyzerpsdgroup')
                        self.detectors.single_detector.summed_counts=dataset.data.psdet
                        
                
                        
                        
                def set_detector(self,dataset,detector_name,data_name):                        
                        analyzergroup=getattr(data.metadata,data_name)
                        setattr(self.detectors,detector_name,Detector(detector_name))
                        setattr(self.detectors,detector_name,'dimension=',[len(dataset.metadata.analyzersdgroup),1])
                        Nx=getattr(self.detectors,detector_name,dimension[0])
                        Ny=getattr(self.detectors,detector_name,dimension[1])
                        npts=len(getattr(dataset.data,dataset.metadata.analyzersdgroup[0]))
                        data=N.empty((npts,Nx,Ny),'Float64')
                        #put all the data in data array which is npts x Nx x Ny, in this case, Ny=1 since our detectors are 1D
                        for nx in range(Nx):
                                curr_detector=getattr(dataset.metadata,data_name)[nx]
                                data[:,nx,1]=getattr(dataset.data,curr_detector)
                                
                        setattr(getattr(self.detectors,detector_name),'x',N.copy.deepcopy(data))
                        setattr(getattr(self.detectors,detector_name),'variance',N.copy.deepcopy(data))
                
               

                
                
                
               
                
                


 





if __name__=="__main__":
        myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\mesh53439.bt7'
        print 'hi'
        mydatareader=readice.datareader()
        mydata=mydatareader.readbuffer(myfilestr)
        print mydata.metadata.varying
        bt7=TripleAxis()
        bt7.translate(mydata)
        print 'hi'
        


