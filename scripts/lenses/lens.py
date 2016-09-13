import math
import logging
import numpy as np

from blbase import epicsdevice

log = logging.getLogger(__name__)

class Lens(epicsdevice.Device):
    """
    A Python interface to wrap the PVs created by a Beryllium IOC
    
    The methods related to the calculation of the focal plane have two major
    modes determined by the :param:`.use_beam`. If set to True, the current
    beam energy will be used to calculate the focal plane of the lens. This is
    the default mode of operation. However, if there is a need to calculate
    beam parameters in an offline mode, you can set this to False, and the
    requested beam energy as specified by the IOC will be used. 
    """
    _records = {'radius'             : 'RADIUS',
                'current_focus'      : 'FOCUS',
                'requested_focus'    : 'REQ_FOCUS',
                'beamline_position'  : 'Z',
                '_state'             : 'STATE',
                '_insert'            : 'INSERT',
                '_remove'            : 'REMOVE'}


    def __init__(self,base):
        self.base = base
        self._shift = 0.0
        self.use_beam = True
        super(Lens,self).__init__(prefix=base,delim=':')
  

    @property
    def inserted(self):
        """
        Whether lens is in the beam as determined by the STATE PV
        """
        return self._state == 1


    @property
    def removed(self):
        """
        Whether lens is out of the beam as determined by the STATE PV
        """
        return self._state == 0
 

    def insert(self):
        """
        Place the lens in the beam path
        """
        if not self.inserted:
            self._insert = 1


    def remove(self):
        """
        Remove the lens from the beam path
        """
        if not self.removed:
            self._remove = 1


    @property
    def focus(self):
        """
        Return the focal length based on the use_beam parameter
        """
        if not self.use_beam:
            return self.requested_focus
        
        return self.current_focus
    
    
    @property
    def ray_transfer(self):
        """
        The thin lens ray transfer matrix based on the focal length of the lens
        
        The matrix take the form :
        
        .. math::
            &[   1      0  ]\\
            &[ -1/f     1  ]
            :label: thins_lens
        """
        return np.array([[1,0],[-1/self.focus,1]])


    def propagation_from(self,z):
        """
        Return the ray transfer matrix corresponding to light travelling from a
        beamline position, z, to the surface of the lens  
        
        The matrix takes the form :

        .. math::
            &[  1   d  ]\\
            &[  0   1  ]
            :label: propagation
        
        :param z: The origin of the light ray along the beamline in meters
        :type  z: float
        """
        d = z - self.beamline_position
        
        return np.array([[1,d],[0,1]])
    
    
    def focused_from(self,z):
        """
        Return the ray transfer matrix for for a beam of light originating from
        a beamline position, z, which is then focused by the lens. This is
        simply the matrix created by the cross product of
        :param:`.ray_transfer` and the :method:`.propagation_from`   
        
        :param z: The origin of the light ray along the beamline in meters
        :type  z: float
        """
        return np.dot(self.ray_transfer,self.propagation_from(z))
   

    def __repr__(self):
        return '< LENS object with focus {:}, radius {:}'.format(self.focus,
                                                                 self.radius)


class LensArray(object):
    """
    An object to represent an array of Lenses
    
    The array is initalized by passing each :class:`.Lens` object as a
    arguement. 
    
    The methods related to the calculation of the focal plane have two major
    modes determined by the :param:`.use_beam`. If set to True, the current
    beam energy will be used to calculate the focal plane of the lens. This is
    the default mode of operation. However, if there is a need to calculate
    beam parameters in an offline mode, you can set this to False, and the
    requested beam energy as specified by the IOC will be used. 
    """
    def __init__(self,*lenses):
        self.lenses   = lenses
        self.use_beam = True
        

    @property
    def size(self):
        """
        Number of lenses in the array
        """
        return len(self.inserted_lenses)


    @property
    def inserted_lenses(self):
        """
        A list of all the lenses in the array organized by beamline position
        """
        lenses = [l for l in self.lenses if l]
        return sorted(lenses,key=lambda lens: lens.beamline_position)


    @property
    def use_beam(self):
        """
        The choice to use the current beam energy for focus calculations or the
        requested energy stored in the IOC 
        """
        return self._use_beam


    @use_beam.setter
    def use_beam(self,beam_usage):
        for lens in self.inserted_lenses:
            lens.use_beam = beam_usage
        
        self._use_beam = beam_usage


    @property
    def ray_transfer_matrix(self):
        """
        The ray transfer matrix of all the inserted lenses

        This is the matrix formed by tracing a ray originating at the LCLS
        Undulator (z=0) through each inserted lens in the array      
        """
        if not all([lens.use_beam == self.use_beam 
                    for lens in self.inserted_lenses]):
            log.warn('Not all lenses are using the same beam energy parameter, '\
                     'set use_beam to True/False')


        for i,lens in enumerate(self.inserted_lenses):
            if i == 0:
                transfer = lens.focused_from(0.0)
            else:
                transfer = np.dot(lens.focused_from(prev_lens.beamline_position),
                                                    transfer)
            prev_lens = lens
        
        return transfer


    @property
    def focus(self):
        """
        Calculate the focal plane in beamline coordinates of the Lens Array

        This solution is derived from the coefficients found in the ray transfer
        matrix
        """
        transfer       = self.ray_transfer_matrix
        focal_distance =  -transfer[0][1]/transfer[1][1]
        
        focal_distance += self.inserted_lenses[-1].beamline_position
        return focal_distance


    def focus_displacement(self,z,energy=None):
        """
        Return the absolute distance from the focal plane to a point on the
        beamline
        
        :param z: The beamline position of reference mark in meters
        :type  z: float

        :param energy: (optional) The energy to evaluate the array at in eV
        :type  energy: float
        """
        if energy:
            self.use_beam = False

        if not self.inserted_lenses:
            return np.inf
        
        return math.fabs(z - self.focus)
   

    def __str__(self):
        """
        String description of Lens Array
        """
        s = ''
        s+= 'Lens Array with focus at {:}\n'.format(self.focus)
        s+= '-'*79+'\n'
        s+= '{:20} {:15} {:15}\n'.format('Name','Focal Length','Position')
        for lens in (self.inserted_lenses):
            s+= '{:20} {:15.2f} {:15.2f}\n'.format(lens.base,
                                             lens.focus,
                                             lens.beamline_position)
        return s


    def __repr__(self):
        return self.__str__()
