{
    "name": "Product Image Zoom Viewer",
    "version": "18.0.1.0.0",
    "summary": "Zoom fullscreen para imagenes de producto en backend",
    "category": "Productivity",
    "author": "KEVIN CORDON",
    "license": "LGPL-3",
    "depends": ["web", "product"],
    "assets": {
        "web.assets_backend": [
            "product_image_zoom/static/src/js/image_zoom_patch.js",
            "product_image_zoom/static/src/xml/image_zoom_templates.xml",
            "product_image_zoom/static/src/scss/image_zoom.scss",
        ],
    },
    "installable": True,
    "application": False,
}
