import { app } from "../../../scripts/app.js";
import { LoraInfoDialog } from "../../ComfyUI-Custom-Scripts/js/modelInfo.js";

const infoHandlers = {
    "LoraLoaderVanilla":true,
    "LoraLoaderStackedVanilla":true,
    "LoraLoaderAdvanced":true,
    "LoraLoaderStackedAdvanced":true
}

app.registerExtension({
    name: "autotrigger.LoraInfo",
    beforeRegisterNodeDef(nodeType) {
        if (! infoHandlers[nodeType.comfyClass]) {
            return;
        }
        const getExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;
        nodeType.prototype.getExtraMenuOptions = function (_, options) {
            let value = this.widgets[0].value;
            if (!value) {
                return;
            }
            if (value.content) {
                value = value.content;
            }
            options.unshift({
                content: "View info...",
                callback: async () => {
                    new LoraInfoDialog(value).show("loras", value);
                },
            });

            return getExtraMenuOptions?.apply(this, arguments);
        };
    }
});