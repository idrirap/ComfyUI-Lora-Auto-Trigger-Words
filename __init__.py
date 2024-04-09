#from .nodes_autotrigger import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as na_NCM, na_NDNM
#from .nodes_utils import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as nu_NCM, nu_NDNM
from .nodes_autotrigger import NODE_CLASS_MAPPINGS as na_NCM
from .nodes_utils import NODE_CLASS_MAPPINGS as nu_NCM

NODE_CLASS_MAPPINGS = dict(na_NCM, **nu_NCM)
#NODE_DISPLAY_NAME_MAPPINGS = dict(na_NDNM, **nu_NDNM)
WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]#, "NODE_DISPLAY_NAME_MAPPINGS"]
