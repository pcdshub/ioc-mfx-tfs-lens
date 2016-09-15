import logging
import itertools
import numpy as np

from blbase import epicsdevice
from lens import LensArray,Lens

log = logging.getLogger(__name__)


class LensSystem(epicsdevice.Device):
    """
    An object to represent a system of Beryllium lenses
    """
    _records = {'beam_energy'      : 'ENERGY',
                'requested_energy' : 'REQ_ENERGY',
                'current_limit'    : 'LIMIT',
                'current_focus'    : 'FOCUS',
                'focal_length'     : 'FOCAL_LENGTH'
               }

    def __init__(self,base,sample=None):
        super(LensSystem,self).__init__(prefix=base,delim=':') 
        
        self.sample_position = sample
        self._lenses = []

   
    @property
    def shape(self):
        """
        Return the shape of the lens array

        The shape is determined by sorting the leneses in the system by
        beamline position. If multiple lenses are found with identical
        coordinates, they are assumed to belong to a lens stack and therefore
        their in posiitons are assumed to be mutually exclusive. The None
        values are place holders for the option of removing the lens from the
        beam path. 
        """
        index = 0
        prev_lens = None
        
        shape = []
        lens_sequence = sorted(self._lenses,key=lambda x : x.beamline_position)  
        
        for lens in lens_sequence:
            if prev_lens and prev_lens.beamline_position == lens.beamline_position:
                shape[index-1].append(lens)
            else:
                shape.append([None,lens])
                index+= 1

            prev_lens = lens
                
        return shape
  

    @property
    def combinations(self):
        """
        Return a list with all possible lens combinations as determined by the
        :attr:`.shape`array. Each combination is represented as a
        :class'`.LensArray` object
        """
        return [LensArray(*l) for l in itertools.product(*self.shape)]


    def focus_at(self,z,energy=None):
        """
        Focus the lenses at a beamline position.

        This uses the :meth:`.config_focused_at` to determine the most suitable
        lens configuration for the requested focus which is then applied. 
        
        :param z: The beamline position to focus the lens system at in meters
        :type  z: float

        :param energy: (optional) The energy to evaluate the array at in eV
        :type  energy: float
        """
        array = self.config_focused_at(z,energy=energy)
        log.info(array)
        self._apply_array(array)

    
    def create_spot(self,z,size,convergent=True,divergent=True,energy=None):
        """
        Focus the lenses at a point such that a unfocused image of a specific
        size is created at a beamline position.
        
        :param z: The beamline position to create the image at in meters
        :type  z: float

        :param size: The size of the spot in microns
        :type  size: float
        
        :param convergent: Allow convergent solutions
        :type  convergent: bool

        :param divergent:  Allow divergent solutions
        :type  divergent:  bool

        :param energy: (optional) The energy to evaluate the array at in eV
        :type  energy: float
        """
        array = self.config_with_spot(z,size,convergent=convergent,
                                      divergent=divergent,energy=energy)
        log.info(array)
        self._apply_array(array)


    def config_focused_at(self,z,energy=None):
        """
        Find the configuration that focuses the beam at a specific beamline
        coordinate. The function :meth:`.LensArray.focus_displacement` is
        calculated for each array, the mininimum being treated as the most
        optimal conifguration. 
        
        :param z: The beamline position to focus the lens system at in meters
        :type  z: float

        :param energy: (optional) The energy to evaluate the array at in eV
        :type  energy: float
        """
        if energy:
            self.requested_energy = energy

        return self._minimize(LensArray.focus_displacement,z,energy=energy)
   

    def config_with_spot(self,z,size,convergent=True,divergent=True,energy=None):
        """
        Find the configuration with a given spot size and Z position
        
        :param z: The beamline position to create the image at in meters
        :type  z: float

        :param size: The size of the spot in microns
        :type  size: float
        
        :param convergent: Allow convergent solutions
        :type  convergent: bool

        :param divergent:  Allow divergent solutions
        :type  divergent:  bool

        :param energy: (optional) The energy to evaluate the array at in eV
        :type  energy: float
        """
        if energy:
            self.requested_energy = energy
   
        return self._minimize(LensArray._spot_size_diff,z,size,
                              convergent=convergent,divergent=divergent,
                              energy=energy)


    def _add_lens(self,base):
        """
        Add a Lens to the system by providing the channel access base for all
        of the associated records.
        """
        self._lenses.append(Lens(base))


    def _apply_array(self,array):
        """
        Apply a configuration contained in a Lens Array object. All of the
        lenses are removed, then the lenses in the specified configuration are
        inserted.
        """
        for lens in self._lenses:
            lens.remove()

        for lens in array.inserted_lenses:
            lens.insert()
    
    
    def _minimize(self,eval_func,*args,**kwargs):
        """
        Find the combination that minimizes a calculation with the current
        available lenses.

        This function allows us to minimize any calculation available from the
        :class`.LensArray` object. Every combination of the lens system is
        analyzed, the minimum of which is returned by the function. If multiple
        solutions are found to have the same result, the lens system with the
        least number of lenses will be included.  
        """
        vector = np.vectorize(lambda array : eval_func(array,*args,**kwargs)) 
        combos = np.asarray(self.combinations)
        values = vector(combos)

        min_value  = np.min(values)
        min_arrays = combos[np.where(values==min_value)]

        log.info('Found {:} solution/s'.format(len(min_arrays)))

        if len(min_arrays) == 1:
            return min_arrays[0]

        log.info('Picking solution based on number of lenses')
        return sorted(min_arrays,key=lambda array: array.size)[0]
