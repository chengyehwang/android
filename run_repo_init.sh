echo "repo branch ${TAG}"
git config --global color.ui true
repo init -u https://android.googlesource.com/platform/manifest -b ${TAG} --depth 1
