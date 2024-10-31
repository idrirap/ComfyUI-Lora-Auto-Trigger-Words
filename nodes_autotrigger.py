from comfy.sd import load_lora_for_models
from comfy.utils import load_torch_file
import folder_paths

from .utils import *

class LoraLoaderVanilla:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = sorted(folder_paths.get_filename_list("loras"), key=str.lower)
        return {
            "required": { 
                "model": ("MODEL",),
                "lora_name": (LORA_LIST, ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "force_fetch": ("BOOLEAN", {"default": False}),
                "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "clip": ("CLIP", ),
                "override_lora_name":("STRING", {"forceInput": True}), 
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "LIST", "LIST", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "civitai_tags_list", "meta_tags_list", "lora_name")
    FUNCTION = "load_lora"
    CATEGORY = "autotrigger"

    def load_lora(self, model, lora_name, strength_model, strength_clip, force_fetch, append_loraname_if_empty, clip=None, override_lora_name=""):
        if clip is None:
            strength_clip=0
        if override_lora_name != "":
            lora_name = override_lora_name
        meta_tags_list = sort_tags_by_frequency(get_metadata(lora_name, "loras"))
        civitai_tags_list = load_and_save_tags(lora_name, force_fetch)

        meta_tags_list = append_lora_name_if_empty(meta_tags_list, lora_name, append_loraname_if_empty)
        civitai_tags_list = append_lora_name_if_empty(civitai_tags_list, lora_name, append_loraname_if_empty)

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = load_lora_for_models(model, clip, lora, strength_model, strength_clip)
  
        return (model_lora, clip_lora, civitai_tags_list, meta_tags_list, lora_name)

class LoraLoaderStackedVanilla:
    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = folder_paths.get_filename_list("loras")
        return {
            "required": {
               "lora_name": (LORA_LIST,),
               "lora_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
               "force_fetch": ("BOOLEAN", {"default": False}),
               "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "lora_stack": ("LORA_STACK", ),
                "override_lora_name":("STRING", {"forceInput": True}), 
            }
        }

    RETURN_TYPES = ("LIST", "LIST", "LORA_STACK", "STRING")
    RETURN_NAMES = ("civitai_tags_list", "meta_tags_list", "LORA_STACK", "lora_name")
    FUNCTION = "set_stack"
    #OUTPUT_NODE = False
    CATEGORY = "autotrigger"

    def set_stack(self, lora_name, lora_weight, force_fetch, append_loraname_if_empty, lora_stack=None, override_lora_name=""):
        if override_lora_name != "":
            lora_name = override_lora_name
        civitai_tags_list = load_and_save_tags(lora_name, force_fetch)

        meta_tags = get_metadata(lora_name, "loras")
        meta_tags_list = sort_tags_by_frequency(meta_tags)

        civitai_tags_list = append_lora_name_if_empty(civitai_tags_list, lora_name, append_loraname_if_empty)
        meta_tags_list = append_lora_name_if_empty(meta_tags_list, lora_name, append_loraname_if_empty)

        loras = [(lora_name,lora_weight,lora_weight,)]
        if lora_stack is not None:
            loras.extend(lora_stack)

        return (civitai_tags_list, meta_tags_list, loras, lora_name)

class LoraLoaderAdvanced:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = sorted(folder_paths.get_filename_list("loras"), key=str.lower)
        populate_items(LORA_LIST, "loras")
        return {
            "required": { 
                "model": ("MODEL",),
                "lora_name": (LORA_LIST, ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "force_fetch": ("BOOLEAN", {"default": False}),
                "enable_preview": ("BOOLEAN", {"default": False}),
                "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "clip": ("CLIP", ),
                "override_lora_name":("STRING", {"forceInput": True}), 
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "LIST", "LIST", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "civitai_tags_list", "meta_tags_list", "lora_name")
    FUNCTION = "load_lora"
    CATEGORY = "autotrigger"

    def load_lora(self, model, lora_name, strength_model, strength_clip, force_fetch, enable_preview, append_loraname_if_empty, clip=None, override_lora_name=""):
        if clip is None:
            strength_clip=0
        if override_lora_name != "":
            has_preview, prev = get_preview_path(override_lora_name, "loras")
            prev = f"loras/{prev}" if has_preview else None
            lora_name = {"content": override_lora_name, "image": prev, "type": "loras"}
        
        meta_tags_list = sort_tags_by_frequency(get_metadata(lora_name["content"], "loras"))
        civitai_tags_list = load_and_save_tags(lora_name["content"], force_fetch)

        civitai_tags_list = append_lora_name_if_empty(civitai_tags_list, lora_name["content"], append_loraname_if_empty)
        meta_tags_list = append_lora_name_if_empty(meta_tags_list, lora_name["content"], append_loraname_if_empty)

        lora_path = folder_paths.get_full_path("loras", lora_name["content"])
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        if enable_preview:
            _, preview = copy_preview_to_temp(lora_name["image"])
            if preview is not None:
                preview_output = {
                    "filename": preview,
                    "subfolder": "lora_preview",
                    "type": "temp"
                }
                return {"ui": {"images": [preview_output]}, "result": (model_lora, clip_lora, civitai_tags_list, meta_tags_list, lora_name["content"])}


        return (model_lora, clip_lora, civitai_tags_list, meta_tags_list, lora_name["content"])

class LoraLoaderStackedAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = folder_paths.get_filename_list("loras")
        populate_items(LORA_LIST, "loras")
        return {
            "required": {
               "lora_name": (LORA_LIST,),
               "lora_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
               "force_fetch": ("BOOLEAN", {"default": False}),
               "enable_preview": ("BOOLEAN", {"default": False}),
               "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "lora_stack": ("LORA_STACK", ),
                "override_lora_name":("STRING", {"forceInput": True}), 
            }
        }

    RETURN_TYPES = ("LIST", "LIST", "LORA_STACK", "STRING")
    RETURN_NAMES = ("civitai_tags_list", "meta_tags_list", "LORA_STACK", "lora_name")
    FUNCTION = "set_stack"
    #OUTPUT_NODE = False
    CATEGORY = "autotrigger"

    def set_stack(self, lora_name, lora_weight, force_fetch, enable_preview, append_loraname_if_empty, lora_stack=None, override_lora_name=""):
        if override_lora_name != "":
            has_preview, prev = get_preview_path(override_lora_name, "loras")
            prev = f"loras/{prev}" if has_preview else None
            lora_name = {"content": override_lora_name, "image": prev, "type": "loras"}
        
        civitai_tags_list = load_and_save_tags(lora_name["content"], force_fetch)

        meta_tags = get_metadata(lora_name["content"], "loras")
        meta_tags_list = sort_tags_by_frequency(meta_tags)

        civitai_tags_list = append_lora_name_if_empty(civitai_tags_list, lora_name["content"], append_loraname_if_empty)
        meta_tags_list = append_lora_name_if_empty(meta_tags_list, lora_name["content"], append_loraname_if_empty)

        loras = [(lora_name["content"],lora_weight,lora_weight,)]
        if lora_stack is not None:
            loras.extend(lora_stack)

        if enable_preview:
            _, preview = copy_preview_to_temp(lora_name["image"])
            if preview is not None:
                preview_output = {
                    "filename": preview,
                    "subfolder": "lora_preview",
                    "type": "temp"
                }
                return {"ui": {"images": [preview_output]}, "result": (civitai_tags_list, meta_tags_list, loras, lora_name["content"])}
        
        return {"result": (civitai_tags_list, meta_tags_list, loras, lora_name["content"])}

class LoraTagsOnly:
    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = sorted(folder_paths.get_filename_list("loras"), key=str.lower)
        return {
            "required": { 
                "lora_name": (LORA_LIST,),
                "force_fetch": ("BOOLEAN", {"default": False}),
                "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "override_lora_name":("STRING", {"forceInput": True}), 
            }
        }

    RETURN_TYPES = ("LIST", "LIST")
    RETURN_NAMES = ("civitai_tags_list", "meta_tags_list")
    FUNCTION = "ask_lora"
    CATEGORY = "autotrigger"

    def ask_lora(self, lora_name, force_fetch, append_loraname_if_empty, override_lora_name=""):
        if override_lora_name != "":
            lora_name = override_lora_name
        meta_tags_list = sort_tags_by_frequency(get_metadata(lora_name, "loras"))
        civitai_tags_list = load_and_save_tags(lora_name, force_fetch)

        meta_tags_list = append_lora_name_if_empty(meta_tags_list, lora_name, append_loraname_if_empty)
        civitai_tags_list = append_lora_name_if_empty(civitai_tags_list, lora_name, append_loraname_if_empty)

        return (civitai_tags_list, meta_tags_list)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoraLoaderVanilla": LoraLoaderVanilla,
    "LoraLoaderStackedVanilla": LoraLoaderStackedVanilla,
    "LoraLoaderAdvanced": LoraLoaderAdvanced,
    "LoraLoaderStackedAdvanced": LoraLoaderStackedAdvanced,
    "LoraTagsOnly": LoraTagsOnly,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraLoaderVanilla": "LoraLoaderVanilla",
    "LoraLoaderStackedVanilla": "LoraLoaderStackedVanilla",
    "LoraLoaderAdvanced": "LoraLoaderAdvanced",
    "LoraLoaderStackedAdvanced": "LoraLoaderStackedAdvanced",
    "LoraTagsOnly": "LoraTagsOnly",
}
