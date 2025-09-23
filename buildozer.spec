[app]
title = MonCalculateur
package.name = moncalculateur
package.domain = org.hassane
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
osx.python_version = 3
android.api = 33
android.minapi = 21
android.sdk = 33.0.2
android.ndk = 25b
android.ndk_api = 21
android.build_tools = 33.0.2
android.arch = armeabi-v7a
android.allow_backup = False
android.logcat_filters = *:S python:D
android.enable_androidx = True
android.gradle_version = 7.4
android.target_sdk = 33
android.private_storage = True
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
