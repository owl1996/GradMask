from .impl import load_unlearn_checkpoint, save_unlearn_checkpoint  # noqa: F401

from .retrain import retrain
from .FT import FT

from .fisher import fisher, fisher_new
from .Wfisher import Wfisher

from .NGPlus import NGPlus
from .NGSalUn import NGSalUn

from .NGradMask import NGradMask
from .NGradFocus import NGradFocus

from .SRL import SRL

from .SRGradFocus import SRGradFocus
from .SRGradMask import SRGradMask

from .SalUn import SalUn

from .SRL_OPT import SRL_OPT
from .NGPlus_OPT import NGPlus_OPT

from .SRGradFocusOPT import SRGradFocusOPT
from .NGradFocusOPT import NGradFocusOPT

from .SCRUB import SCRUB
from .SCRUBSalUn import SCRUBSalUn
from .SCRUBGradMask import SCRUBGradMask
from .SCRUBFocus import SCRUBFocus

from .MSG import MSG
from .CT import CT

def get_unlearn_method(name):
    """method usage:

    function(data_loaders, model, criterion, args)"""
    if name == "retrain":
        return retrain
    elif name == "FT":
        return FT

    elif name == "fisher":
        return fisher
    elif name == "fisher_new":
        return fisher_new
    elif name == "wfisher":
        return Wfisher
    
    elif name == "NGPlus":
        return NGPlus
    elif name == "NGradMask":
        return NGradMask
    elif name == "NGradFocus":
        return NGradFocus
    elif name == "NGSalUn":
        return NGSalUn
    
    elif name == "SRL":
        return SRL
    elif name == "SRGradFocus":
        return SRGradFocus
    elif name == "SRGradMask":
        return SRGradMask
    elif name == "SalUn":
        return SalUn
    
    elif name == "SRGradFocusOPT":
        return SRGradFocusOPT
    elif name == "NGradFocusOPT":
        return NGradFocusOPT
    
    elif name == "MSG":
        return MSG
    elif name == "CT":
        return CT
    
    elif name == "SRL_OPT":
        return SRL_OPT
    elif name == "NGPlus_OPT":
        return NGPlus_OPT
    
    elif name == "SCRUBFocus":
        return SCRUBFocus
    elif name == "SCRUBGradMask":
        return SCRUBGradMask
    elif name == "SCRUBSalUn":
        return SCRUBSalUn
    elif name == "SCRUB":
        return SCRUB

    else:
        raise NotImplementedError(f"Unlearn method {name} not implemented!")
