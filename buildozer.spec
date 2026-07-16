[app]
title = Sandy BG
package.name = sandybg
package.domain = org.sandy
source.dir = .
source.include_exts = py,png,jpg,onnx
version = 0.1
requirements = python3,kivy,opencv-python,numpy
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA
android.api = 33
android.minapi = 24
android.private_storage = True
orientation = portrait
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
