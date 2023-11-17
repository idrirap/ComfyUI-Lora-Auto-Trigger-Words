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
                "clip": ("CLIP", ),
                "lora_name": (LORA_LIST, ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "force_fetch": ("BOOLEAN", {"default": False}),
                "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "LIST", "LIST")
    RETURN_NAMES = ("MODEL", "CLIP", "civitai_tags_list", "meta_tags_list")
    FUNCTION = "load_lora"
    CATEGORY = "autotrigger"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip, force_fetch, append_loraname_if_empty):
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
  
        return (model_lora, clip_lora, civitai_tags_list, meta_tags_list)

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
            }
        }

    RETURN_TYPES = ("LIST", "LIST", "LORA_STACK",)
    RETURN_NAMES = ("civitai_tags_list", "meta_tags_list", "LORA_STACK",)
    FUNCTION = "set_stack"
    #OUTPUT_NODE = False
    CATEGORY = "autotrigger"

    def set_stack(self, lora_name, lora_weight, force_fetch, append_loraname_if_empty, lora_stack=None):
        civitai_tags_list = load_and_save_tags(lora_name, force_fetch)

        meta_tags = get_metadata(lora_name, "loras")
        meta_tags_list = sort_tags_by_frequency(meta_tags)

        civitai_tags_list = append_lora_name_if_empty(civitai_tags_list, lora_name, append_loraname_if_empty)
        meta_tags_list = append_lora_name_if_empty(meta_tags_list, lora_name, append_loraname_if_empty)

        loras = [(lora_name,lora_weight,lora_weight,)]
        if lora_stack is not None:
            loras.extend(lora_stack)

        return (civitai_tags_list, meta_tags_list, loras)

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
                "clip": ("CLIP", ),
                "lora_name": (LORA_LIST, ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "force_fetch": ("BOOLEAN", {"default": False}),
                "enable_preview": ("BOOLEAN", {"default": False}),
                "append_loraname_if_empty": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "LIST", "LIST")
    RETURN_NAMES = ("MODEL", "CLIP", "civitai_tags_list", "meta_tags_list")
    FUNCTION = "load_lora"
    CATEGORY = "autotrigger"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip, force_fetch, enable_preview, append_loraname_if_empty):
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
                return {"ui": {"images": [preview_output]}, "result": (model_lora, clip_lora, civitai_tags_list, meta_tags_list)}


        return (model_lora, clip_lora, civitai_tags_list, meta_tags_list)

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
            }
        }

    RETURN_TYPES = ("LIST", "LIST", "LORA_STACK",)
    RETURN_NAMES = ("civitai_tags_list", "meta_tags_list", "LORA_STACK",)
    FUNCTION = "set_stack"
    #OUTPUT_NODE = False
    CATEGORY = "autotrigger"

    def set_stack(self, lora_name, lora_weight, force_fetch, enable_preview, append_loraname_if_empty, lora_stack=None):
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
                return {"ui": {"images": [preview_output]}, "result": (civitai_tags_list, meta_tags_list, loras)}
        
        return {"result": (civitai_tags_list, meta_tags_list, loras)}


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoraLoaderVanilla": LoraLoaderVanilla,
    "LoraLoaderStackedVanilla": LoraLoaderStackedVanilla,
    "LoraLoaderAdvanced": LoraLoaderAdvanced,
    "LoraLoaderStackedAdvanced": LoraLoaderStackedAdvanced,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraLoaderVanilla": "LoraLoaderVanilla",
    "LoraLoaderStackedVanilla": "LoraLoaderStackedVanilla",
    "LoraLoaderAdvanced": "LoraLoaderAdvanced",
    "LoraLoaderStackedAdvanced": "LoraLoaderStackedAdvanced",
}
