import random

from .utils import *

class FusionText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text_1": ("STRING", {"default": "", "forceInput": True}), "text_2": ("STRING", {"default": "", "forceInput": True})}}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "combine"
    CATEGORY = "autotrigger"

    def combine(self, text_1, text_2):
        return (text_1 + text_2, )


class Randomizer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
               "text_1":("STRING", {"forceInput": True}), 
               "lora_1":("LORA_STACK", ), 
               "text_2":("STRING", {"forceInput": True} ), 
               "lora_2":("LORA_STACK", ), 
               "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "LORA_STACK")
    RETURN_NAMES = ("text", "lora stack")
    FUNCTION = "randomize"

    #OUTPUT_NODE = False

    CATEGORY = "autotrigger"

    def randomize(self, text_1, lora_1, text_2, lora_2, seed):
        random.seed(seed)
        if random.random() < .5:
            return (text_1, lora_1)
        return (text_2, lora_2)
    
class TextInputBasic:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
               "text":("STRING", {"default":"", "multiline":True}), 
            },
            "optional": {
                "prefix":("STRING", {"default":"", "forceInput": True}), 
                "suffix":("STRING", {"default":"", "forceInput": True}), 
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text", )
    FUNCTION = "get_text"

    #OUTPUT_NODE = False

    CATEGORY = "autotrigger"

    def get_text(self, text, prefix="", suffix=""):
        return (prefix + text + suffix, )
    

class TagsSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "tags_list": ("LIST", {"default": []}),
                "selector": ("STRING", {"default": ":"}),
                "weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "ensure_coma": ("BOOLEAN", {"default": True})
            },
            "optional": {
                "prefix":("STRING", {"default":"", "forceInput": True}), 
                "suffix":("STRING", {"default":"", "forceInput": True}), 
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "select_tags"
    CATEGORY = "autotrigger"

    def select_tags(self, tags_list, selector, weight, ensure_coma, prefix="", suffix=""):
        if weight != 1.0:
            tags_list = [f"({tag}:{weight})" for tag in tags_list]
        output = parse_selector(selector, tags_list)
        if ensure_coma:
            striped_prefix = prefix.strip()
            striped_suffix = suffix.strip()
            if striped_prefix != "" and not striped_prefix.endswith(",") and output != "" and not output.startswith(","):
                prefix = striped_prefix + ", "
            if output != "" and not output.endswith(",") and striped_suffix != "" and not striped_suffix.startswith(","):
                suffix = ", " + striped_suffix
        return (prefix + output + suffix, )

class TagsFormater:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "tags_list": ("LIST", {"default": []}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_tags"
    CATEGORY = "autotrigger"

    def format_tags(self, tags_list):
        output = ""
        i = 0
        for tag in tags_list:
            output += f'{i} : "{tag}"\n'
            i+=1

        return (output,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Randomizer": Randomizer,
    "FusionText": FusionText,
    "TextInputBasic": TextInputBasic,
    "TagsSelector": TagsSelector,
    "TagsFormater": TagsFormater,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Randomizer": "Randomizer",
    "FusionText": "FusionText",
    "TextInputBasic": "TextInputBasic",
    "TagsSelector": "TagsSelector",
    "TagsFormater": "TagsFormater",
}
