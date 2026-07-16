name: Build Sandy BG APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libltdl-dev libffi-dev libssl-dev autoconf automake libtool pkg-config cmake git openjdk-17-jdk freeglut3-dev
        pip install --upgrade pip
        pip install buildozer cython==0.29.33 kivy

    - name: Set up Android SDK Licenses
      run: |
        mkdir -p ~/.android
        touch ~/.android/repositories.cfg
        mkdir -p "$ANDROID_HOME/licenses" || true
        echo -e "\n893a3165745b630fa68b3de239a28e873a240f22\nd56f5187479451755a6fb2258d789080c3827eb1\nd36435b92d69b32a63e946175528c54e36817f93" > "$ANDROID_HOME/licenses/android-sdk-license" || true
        echo -e "\n84831b9409646a918e30573bab4c9c91346d8abd" > "$ANDROID_HOME/licenses/android-sdk-preview-license" || true

    - name: Build APK with Buildozer
      run: |
        buildozer -v android debug

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: Sandy-BG-APK
        path: bin/*.apk
