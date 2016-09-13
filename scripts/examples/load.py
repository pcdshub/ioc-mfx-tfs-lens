import sys
import logging
from os import path

if __name__ == '__main__':
    sys.path.append(path.dirname(path.dirname((path.abspath(__file__)))))
    
    import lenses 
    l = logging.getLogger('lenses')
    l.addHandler(logging.StreamHandler())
    l.setLevel(logging.DEBUG)

    tfs = lenses.LensSystem('MFX:LENS:BEAM',sample=378.686)
    tfs._add_lens('MFX:LENS:DIA:01')
    tfs._add_lens('MFX:LENS:DIA:02')
    tfs._add_lens('MFX:LENS:DIA:03')
    tfs._add_lens('MFX:LENS:TFS:02')
    tfs._add_lens('MFX:LENS:TFS:03')
    tfs._add_lens('MFX:LENS:TFS:04')
    tfs._add_lens('MFX:LENS:TFS:05')
    tfs._add_lens('MFX:LENS:TFS:06')
    tfs._add_lens('MFX:LENS:TFS:07')
    tfs._add_lens('MFX:LENS:TFS:08')
    tfs._add_lens('MFX:LENS:TFS:09')
    tfs._add_lens('MFX:LENS:TFS:10')

