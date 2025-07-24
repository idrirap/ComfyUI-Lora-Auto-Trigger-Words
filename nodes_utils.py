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
               "text_2":("STRING", {"forceInput": True} ), 
               "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "lora_1":("LORA_STACK", ), 
                "lora_2":("LORA_STACK", ), 
            }
        }

    RETURN_TYPES = ("STRING", "LORA_STACK")
    RETURN_NAMES = ("text", "lora stack")
    FUNCTION = "randomize"

    #OUTPUT_NODE = False

    CATEGORY = "autotrigger"

    def randomize(self, text_1, text_2, seed, lora_1=[], lora_2=[]):
        if seed %2 == 0:
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
    

# 定义一个标签选择器类
# Define a tag selector class
class TagsSelector:
    
    # 定义输入类型信息（ComfyUI 或类似框架的自定义节点接口）
    # Define the input types for the node (used by ComfyUI or similar frameworks)
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {  # 必填项 / Required fields
                "tags_list": ("LIST", {"default": []}),  # 标签列表，预期是字符串组成的列表 / List of tags (e.g., ["sunlight", "fog"])
                "selector": ("STRING", {"default": ":"}),  # 选择器表达式，用于组合标签 / Selector expression to combine tags
                "weight": ("FLOAT", {
                    "default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01
                }),  # 标签权重 / Tag weight
                "ensure_comma": ("BOOLEAN", {"default": True})  # 是否确保末尾加逗号 / Whether to append a comma at the end
            },
            "optional": {  # 可选项 / Optional fields
                "prefix":("STRING", {"default":"", "forceInput": True}),  # 前缀字符串 / Optional prefix string
                "suffix":("STRING", {"default":"", "forceInput": True}),  # 后缀字符串 / Optional suffix string
            }
        }

    # 返回类型为字符串 / This node returns a single string
    RETURN_TYPES = ("STRING",)
    
    # 该节点执行的函数名 / Function to call when this node is executed
    FUNCTION = "select_tags"
    
    # 所属分类，用于在 UI 中组织节点 / Category used in UI organization
    CATEGORY = "autotrigger"

    # 标签选择与格式化主逻辑函数
    # Main logic for selecting and formatting tags
    def select_tags(self, tags_list, selector, weight, ensure_comma, prefix="", suffix=""):
        
        # 如果权重不是 1.0，则将每个标签包装为 (tag:weight) 格式
        # Format each tag as (tag:weight) if weight is not 1.0
        if weight != 1.0:
            tags_list = [f"({tag}:{weight})" for tag in tags_list]

        # 使用选择器语法处理标签组合（需自定义 parse_selector 函数）
        # Use the selector expression to combine tags (parse_selector is assumed to be defined elsewhere)
        output = parse_selector(selector, tags_list)

        # 防止输出为空或为 None 时返回 None
        # Avoid returning None if output is empty or invalid
        if output is None:
            output = ""

        # 如果启用了 ensure_comma，且输出非空且未以逗号结尾，则添加逗号
        # Append comma if ensure_comma is True and output is non-empty and not ending with comma
        if ensure_comma and output != "" and not output.endswith(","):
            output += ","

        # 拼接前缀 + 输出 + 后缀，返回字符串元组
        # Return the final string with prefix and suffix wrapped as a tuple
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

class LoraListNames:
    @classmethod
    def INPUT_TYPES(s):
        LORA_LIST = sorted(folder_paths.get_filename_list("loras"), key=str.lower)
        return {
            "required": { 
                "lora_name": (LORA_LIST,),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("lora_name",)
    FUNCTION = "output_selected"
    CATEGORY = "autotrigger"

    def output_selected(self, lora_name):
        name = lora_name
        return (name,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Randomizer": Randomizer,
    "FusionText": FusionText,
    "TextInputBasic": TextInputBasic,
    "TagsSelector": TagsSelector,
    "TagsFormater": TagsFormater,
    "LoraListNames": LoraListNames,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Randomizer": "Randomizer",
    "FusionText": "FusionText",
    "TextInputBasic": "TextInputBasic",
    "TagsSelector": "TagsSelector",
    "TagsFormater": "TagsFormater",
    "LoraListNames": "LoraListNames",
}