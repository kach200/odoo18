/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ImageField } from "@web/views/fields/image/image_field";
import { onWillUnmount, useState } from "@odoo/owl";

const ZOOM_STEP = 0.15;
const ZOOM_MIN = 0.5;
const ZOOM_MAX = 4;

function clampZoom(value) {
    return Math.min(Math.max(value, ZOOM_MIN), ZOOM_MAX);
}

patch(ImageField.prototype, {
    setup() {
        super.setup(...arguments);
        this.zoomViewer = useState({
            open: false,
            scale: 1,
        });

        this._onZoomKeydown = (ev) => {
            if (!this.zoomViewer.open) {
                return;
            }
            if (ev.key === "Escape") {
                this.closeZoomViewer();
            }
            if (ev.key === "+" || ev.key === "=") {
                this.zoomIn();
            }
            if (ev.key === "-") {
                this.zoomOut();
            }
            if (ev.key === "0") {
                this.resetZoom();
            }
        };

        onWillUnmount(() => {
            document.removeEventListener("keydown", this._onZoomKeydown);
        });
    },

    get canOpenZoomViewer() {
        return Boolean(this.props.record.data[this.props.name]) && this.state.isValid;
    },

    get zoomImageUrl() {
        return this.getUrl(this.zoomImageFieldName);
    },

    get zoomImageFieldName() {
        if (this.fieldType === "many2one") {
            return this.props.previewImage || this.props.name;
        }
        const preferredFields = ["image_1920", "image_1024", "image_512", "image_256", "image_128"];
        for (const fieldName of preferredFields) {
            if (this.props.record.fields[fieldName]?.type === "binary") {
                return fieldName;
            }
        }
        return this.props.previewImage || this.props.name;
    },

    onZoomOpen(ev) {
        if (!this.canOpenZoomViewer) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();
        this.zoomViewer.open = true;
        this.zoomViewer.scale = 1.6;
        document.addEventListener("keydown", this._onZoomKeydown);
    },

    onZoomBackdropClick(ev) {
        if (ev.target === ev.currentTarget) {
            this.closeZoomViewer();
        }
    },

    onZoomWheel(ev) {
        if (!this.zoomViewer.open) {
            return;
        }
        const nextScale = this.zoomViewer.scale + (ev.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP);
        this.zoomViewer.scale = clampZoom(nextScale);
    },

    closeZoomViewer() {
        this.zoomViewer.open = false;
        document.removeEventListener("keydown", this._onZoomKeydown);
    },

    zoomIn() {
        this.zoomViewer.scale = clampZoom(this.zoomViewer.scale + ZOOM_STEP);
    },

    zoomOut() {
        this.zoomViewer.scale = clampZoom(this.zoomViewer.scale - ZOOM_STEP);
    },

    resetZoom() {
        this.zoomViewer.scale = 1;
    },

    onZoomDownload() {
        const link = document.createElement("a");
        const modelName = (this.props.record.resModel || "product").replace(".", "_");
        const recordId = this.props.record.resId || "new";
        link.href = this.zoomImageUrl;
        link.download = `${modelName}_${recordId}_${this.props.name}.png`;
        document.body.appendChild(link);
        link.click();
        link.remove();
    },
});
