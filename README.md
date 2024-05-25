# EMRA For HyperOS

用于提取、修改和重命名 HyperOS 中的 APK 文件的 Python 脚本。它可以帮助开发者和用户轻松地获取 APK 文件及比对更新，并根据需要对其进行定制。

## 功能

- 从 ROM 下载链接下载 ROM
- 从 ZIP 文件中提取 payload.bin
- 从 payload.bin 文件中提取指定镜像文件
- 提取镜像
- 删除指定的 APK
- 重命名 APK 文件
- 更新 APK 版本
- 更新 APK 文件名
- 删除多余文件

## 如何使用

1. 克隆此仓库或下载脚本文件：

   ```
   https://github.com/WXies-Team/EMRA-For-RedMagicOS.git
   ```

2. 确保已安装 Python 3.x, aria2c, 7z 并配置好环境变量后(具体方法可百度 Windows/Linux/macOS 如何安装 xxx 并配置环境变量)安装以下依赖库和 Android 的 `aapt`：

   ```
   pip install -r requirements.txt
   ```

   注意：Windows 用户还需安装 cygwin 并在安装后将 `安装目录/bin` 添加到环境变量中

3. 从以下仓库中下载并解压得到 `extract.erofs` 和 `payload-dumper-go` 文件，并将文件移动到脚本目录下

   - [extract.erofs（Windows 选 cygwin）](https://github.com/sekaiacg/erofs-utils/releases)
   - [payload-dumper-go](https://github.com/ssut/payload-dumper-go/releases)

4. 运行脚本：
   ```
   python main.py [-h] [-d URL] [-p] [-i] [-f] [-t] [-a] [-n] [-u] [-m] [-c]
   ```

按照提示选择相应的操作。

```bash
    -h, --help            显示此帮助消息并退出
    -d URL, --download URL
                          从指定 URL 下载 ROM
    -p, --extract-payload
                          从 zip 文件中提取 payload.bin
    -i, --img             从 payload.bin 中提取指定镜像
    -f, --files           从镜像中提取文件
    -t  --devicetype      修改字典设备类型 (需要2个参数), 0/1 => 不备份/备份, ph/f/p => phone/fold/pad
    -a, --apk             删除指定的 APK
    -n, --rename          重命名 APK 文件
    -u, --update-version  更新 APK 版本
    -m, --update-name     更新 APK 名称
    -c, --clean           删除不需要的文件和文件夹
```

## 相关项目

[EMRA For Flyme](https://github.com/WXies-Team/EMRA-For-Flyme)

[EMRA For ColorOS](https://github.com/WXies-Team/EMRA-For-ColorOS)

[EMRA For OriginOS](https://github.com/WXies-Team/EMRA-For-OriginOS)

[EMRA For HyperOS](https://github.com/WXies-Team/EMRA-For-HyperOS)

[EMRA For RedMagicOS](https://github.com/WXies-Team/EMRA-For-RedMagicOS)
