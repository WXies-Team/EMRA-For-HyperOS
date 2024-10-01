import os  # 引入OS模块，用于操作文件和目录
import glob  # 引入glob模块，用于搜索文件夹中的文件
import platform

# 获取当前脚本文件所在目录的绝对路径
src_dir = os.path.abspath(__file__)

# 在当前脚本文件所在目录下创建一个名为"output_apk"的子目录
dst_dir = os.path.join(src_dir, "output_apk")

# 在当前目录下搜索所有以".zip"为后缀的文件，并返回它们的文件路径
zip_files = glob.glob("*.zip")

# 在当前目录下搜索所有以".zip"为后缀的文件，并返回它们的文件路径
build_prop_path = glob.glob("build.prop")

# 创建名为"output_apk"的目录（如果它不存在）
output_dir = 'output_apk'

update_apk_folder = "update_apk"

update_apk_name_folder = "update_name_apk"

if not os.path.exists(update_apk_folder):
    os.makedirs(update_apk_folder)

if not os.path.exists(update_apk_name_folder):
    os.makedirs(update_apk_name_folder)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取名为"output_apk"目录中所有以".apk"为后缀的文件列表
apk_files = [f for f in os.listdir(output_dir) if f.endswith('.apk')]

# 外部工具路径
tools_path_mapping = {('Windows', 'AMD64'): './tools/Windows/AMD64/',('Linux', 'x86_64'): './tools/Linux/x86_64/',('Linux', 'arm64'): './tools/Linux/arm64/',('Darwin', 'x86_64'): './tools/Darwin/x86_64/',('Darwin', 'arm64'): './tools/Darwin/arm64/',}
tools_path = tools_path_mapping.get((platform.system(), platform.machine()))

# 定义了两个字符串常量，分别用于指定排除 APK 的文件路径和 APK 版本号和名称的 JSON 文件路径
EXCLUDE_APK_PATH = 'exclude_apk.txt'
APK_VERSION = 'app_version.json'
APK_CODE = 'app_code.json'
APK_APP_NAME = 'app_name.json'
APK_APP_NAME_PAD = 'app_name_pad.json'
# 定义一个临时字典，用于存储版本名相同但版本号有所变更的 APK
APK_CODE_NAME = 'app_code_name.json'
# 定义字典类型
JSON_V = 'app_json.txt'
# 相关分区
partitions = ["product"]
# 设备种类识别
is_fold = {"cetus", "zizhan", "babylon", "goku"}
is_pad = {"nabu", "elish", "enuma", "dagu", "pipa", "liuqin", "yudi", "yunluo", "xun", "sheng", "dizi", "ruan"}
is_flip = {"ruyi"}
# 需要删除的文件夹
files_to_delete = ["payload.bin", "product.img", "app_code_name.json"]
folders_to_delete = ["output_apk", "update_apk", "update_name_apk", "product"]
# 获取信息
properties = {"ro.product.product.name": "设备名","ro.product.build.version.incremental": "软件版本号","ro.product.build.date": "编译时间","ro.product.build.id": "基线","ro.product.build.fingerprint": "指纹"}
