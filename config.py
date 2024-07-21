import os
import shutil
import subprocess
import json
import fnmatch
import glob
import apkfile
import platform

src_dir = os.path.abspath(__file__)
dst_dir = os.path.join(src_dir, "output_apk")
zip_files = glob.glob("*.zip")
output_dir = 'output_apk'
update_apk_folder = "update_apk"
update_apk_name_folder = "update_name_apk"

if not os.path.exists(update_apk_folder):
    os.makedirs(update_apk_folder)

if not os.path.exists(update_apk_name_folder):
    os.makedirs(update_apk_name_folder)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

apk_files = [f for f in os.listdir(output_dir) if f.endswith('.apk')]
EXCLUDE_APK_PATH = 'exclude_apk.txt'
APK_VERSION = 'app_version.json'
APK_CODE = 'app_code.json'
APK_APP_NAME = 'app_name.json'
APK_APP_NAME_PAD = 'app_name_pad.json'
APK_CODE_NAME = 'app_code_name.json'
JSON_V = 'app_json.txt'
type_map = {"ph": ("./phone", "Phone"),"f": ("./fold", "Fold"),"p": ("./pad", "Pad"),"fp": ("./flip", "Flip")}
partition = "product"
device_types = {"Fold": {"cetus", "zizhan", "babylon", "goku"},"Pad": {"nabu", "elish", "enuma", "dagu", "pipa", "liuqin", "yudi", "yunluo", "xun", "sheng", "dizi", "ruan"},"Flip": {"ruyi"}}
prop_name = "./product/etc/build.prop"
ro_device_name = "ro.product.product.name"
ro_info ={"ro.product.product.name": "设备名","ro.product.build.version.incremental": "软件版本号","ro.product.build.date": "编译时间","ro.product.build.id": "基线","ro.product.build.fingerprint": "指纹"}
name_use = {"Fold": "","Flip": "","Phone": "","Pad": "_pad",}
files_to_delete = ["payload.bin", "product.img", "app_code_name.json"]
folders_to_delete = ["output_apk", "update_apk", "update_name_apk", "product"]
