from config import *

def move_json(backup, type_name):
    src_dir, new_content = type_map.get(type_name, ("", ""))
    if not src_dir:
        print("无效的类型名称")
        return
    
    try:
        shutil.copy2(os.path.join(src_dir, "app_version.json"), "app_version.json")
        shutil.copy2(os.path.join(src_dir, "app_code.json"), "app_code.json")
        with open(JSON_V, 'w') as file:
            file.write(new_content)
        print(f"字典库已变更为 {new_content}")
    except Exception as e:
        print(f"异常: {e}")
    
    if int(backup) == 1:
        sync_dir = os.path.join(".", f"{new_content.lower()}")
        if os.path.exists(sync_dir):
            for file_name in ["app_version.json", "app_code.json"]:
                src = os.path.join(".", file_name)
                dst = os.path.join(sync_dir, file_name)
                shutil.move(src, dst)
            print(f"字典库已同步到 {new_content} 目录，正在切换")
        else:
            print(f"{new_content} 目录不存在")

def init_folder():
    folders = ["output_apk", "update_apk", "update_name_apk", output_dir, update_apk_folder, update_apk_name_folder]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    if not os.path.exists(APK_CODE) or not os.path.exists(APK_VERSION):
        print("检测到根目录下没有字典库，正在初始化字典库为 Phone")
        move_json(0, "ph")
        print("如有更换字典库需要，请使用 -t 命令进行切换")

def init_json():
    """初始化排除APK列表和APK版本号字典"""
    exclude_apk = []
    apk_version = {}
    apk_code = {}
    apk_code_name = {}

    if os.path.exists(EXCLUDE_APK_PATH):
        with open(EXCLUDE_APK_PATH, 'r') as f:
            exclude_apk = [line.strip() for line in f]
    
    if os.path.exists(APK_VERSION):
        with open(APK_VERSION, 'r') as f:
            apk_version = json.load(f)
    
    if os.path.exists(APK_CODE):
        with open(APK_CODE, 'r') as f:
            apk_code = json.load(f)
    
    return exclude_apk, apk_version, apk_code, apk_code_name

def download_rom(url):
    """从给定的URL下载ROM"""
    subprocess.run(["aria2c", "-x16", "-s16", url])

def extract_payload_bin(zip_files):
    """从ZIP文件中提取payload.bin文件"""
    for f in zip_files:
        try:
            subprocess.run(["7z", "x", f, "payload.bin"])
        except Exception as e:
            print(f"异常，报错信息: {e}")

def extract_img():
    subprocess.run(["./payload-dumper-go", "-c", "8", "-o", "./", "-p", partition, "payload.bin"])

def extract_files():
    try:
        os_type = platform.system()
        if os_type == "Windows":
            option = "-T16"
        else:
            option = "-T8"
        
        partitions = partition.split(",")
        
        for part in partitions:
            img_file = f"{part}.img"
            subprocess.run(["./extract.erofs", "-i", img_file, "-x", option])
        
        with open(prop_name, "r") as file:
            for line in file:
                if line.startswith(ro_device_name):
                    device_name = line.split("=")[1].strip()
                    for dtype, names in device_types.items():
                        if device_name in names:
                            print(f"\n检测到包设备为 {dtype}，请使用 -t 参数切换字库")
                            get_info()
                    else:
                        print("\n检测到包设备为 Phone，请输入-t 参数切换字库")
                        get_info()
    except FileNotFoundError:
        print("无法获取设备名")

def remove_some_apk(exclude_apk):
    """移动APK文件并删除特定文件"""
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.apk') and file not in exclude_apk:
                src = os.path.join(root, file)
                dst = os.path.join(output_dir, file)
                try:
                    shutil.move(src, dst)
                except PermissionError:
                    print(f"无法移动文件 {src}，请检查你的文件权限或关闭占用该文件的程序。")

    for root, _, files in os.walk(output_dir):
        for filename in fnmatch.filter(files, "*.apk"):
            if "overlay" in filename.lower() or "_Sys" in filename:
                try:
                    os.remove(os.path.join(root, filename))
                except PermissionError:
                    print(f"无法删除文件 {filename}，请检查你的文件权限或关闭占用该文件的程序。")

def rename_apk(apk_files):
    """重命名APK文件"""
    for apk_file in apk_files:
        apk_path = os.path.join(output_dir, apk_file)
        try:
            apk = ApkFile(apk_path)
            package_name = apk.package_name
            version_name = apk.version_name
            version_code = apk.version_code
            new_name = f"{package_name}^{version_name}^{version_code}.apk"
            new_path = os.path.join(output_dir, new_name)
            if not os.path.exists(new_path):
                os.rename(apk_path, new_path)
        except Exception as e:
            print(f"异常，报错信息: {e}")

def update_apk_version(apk_version, apk_code, apk_code_name):
    """更新APK版本和本地字典"""
    for apk_file in os.listdir(output_dir):
        if apk_file.endswith('.apk'):
            try:
                x, y, z = os.path.splitext(apk_file)[0].split('^')
                if x in apk_code:
                    if apk_code[x] < int(z):
                        print(f'更新 {x}：{apk_code[x]} -> {z}')
                        if apk_version[x] == y:
                            apk_version[x] = y
                            apk_code[x] = apk_code_name[x] = int(z)
                            shutil.copy2(os.path.join(output_dir, apk_file), os.path.join(update_apk_folder, apk_file))
                        else:
                            apk_version[x] = y
                            apk_code[x] = int(z)
                            shutil.copy2(os.path.join(output_dir, apk_file), os.path.join(update_apk_folder, apk_file))
                    elif apk_code[x] == int(z) and apk_version[x] != y:
                        print(f'疑似更新 {x}：{apk_version[x]} -> {y}')
                        shutil.copy2(os.path.join(output_dir, apk_file), os.path.join(update_apk_name_folder, apk_file))
                else:
                    print(f'添加新应用 {x}:{y}({z})')
                    apk_version[x] = y
                    apk_code[x] = int(z)
            except Exception as e:
                print(f"异常，报错信息: {e}")
                return

    with open(APK_VERSION, 'w') as f:
        json.dump(apk_version, f)
    with open(APK_CODE, 'w') as f:
        json.dump(apk_code, f)
    with open(APK_CODE_NAME, 'w') as f:
        json.dump(apk_code_name, f)

def update_apk_name():
    """更新APK文件名"""
    with open(JSON_V, 'r', encoding='utf-8') as file:
        line = file.readline().strip()
    
    apk_name = {}
    for name, use in name_use.items():
        if line in name:
            apk_path = f"app_name{use}"
        else:
            apk_path = None

        if apk_path and os.path.exists(apk_path):
            with open(apk_path, 'r', encoding='utf-8') as f:
                apk_name = json.load(f)

        apk_code_name = {}
        if os.path.exists(APK_CODE_NAME):
            with open(APK_CODE_NAME, 'r', encoding='utf-8') as f:
                apk_code_name = json.load(f)

    def rename_files_in_folder(folder, name_dict, code_dict):
        for apk_file in os.listdir(folder):
            if apk_file.endswith('.apk'):
                x, y, z = os.path.splitext(apk_file)[0].split('^')
                if x in name_dict:
                    new_x = name_dict[x]
                    new_name = f'{new_x}_{y}({z}).apk'
                    os.rename(os.path.join(folder, apk_file), os.path.join(folder, new_name))
                    print(f'修改 {apk_file} -> {new_name}')

    rename_files_in_folder(output_dir, apk_name, apk_code_name)
    rename_files_in_folder(update_apk_folder, apk_name, apk_code_name)
    rename_files_in_folder(update_apk_name_folder, apk_name, apk_code_name)

def delete_files_and_folders():
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"{file} 删除成功")
            except OSError as e:
                print(f"无法删除 {file}: {e}")
        else:
            print(f"{file} 不存在")

    for folder in folders_to_delete:
        if os.path.exists(folder):
            if os.path.isdir(folder):
                try:
                    shutil.rmtree(folder)
                    print(f"{folder} 删除成功")
                except OSError as e:
                    print(f"无法删除 {folder}: {e}")
            else:
                print(f"{folder} 不是文件夹")
        else:
            print(f"{folder} 不存在")

def git_push():
    """推送更改到Git仓库"""
    device_name = input("机型：")
    os_version = input("版本号：")
    commit_text = "Database：Update"
    commit = f"{commit_text} {device_name} {os_version}"
    
    try:
        with open(JSON_V, 'r') as file:
            line = file.readline().strip()
            if line in ["Phone", "Pad", "Fold", "Flip"]:
                move_json(1, line.lower())
                subprocess.run(["git", "add", f"{line.lower()}/"])
            else:
                print("未检测到字库，无法上传")
    except Exception as e:
        print(f"异常，报错信息: {e}")

    subprocess.run(["git", "commit", "-m", commit])
    subprocess.run(["git", "push"])

def get_info():
        try:
            with open(prop_name, "r") as file:
                lines = file.readlines()
                for key, label in ro_info.items():
                    for line in lines:
                        if line.startswith(key):
                            value = line.split("=")[1].strip()
                            print(f"{label}: {value}")
        except FileNotFoundError:
            print("请在执行 -f 后执行此参数")
