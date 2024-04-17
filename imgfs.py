import pytsk3

# 指定磁盘镜像文件的路径
image_path = "product.img"

# 打开磁盘镜像文件
img = pytsk3.Img_Info(image_path)

try:
    # 获取磁盘镜像文件中的文件系统信息
    fs_info = pytsk3.FS_Info(img)

    # 打印文件系统类型和大小
    print("File system type:", fs_info.info.ftype)
    print("File system size (in bytes):", fs_info.info.size)

except Exception as e:
    print("Error:", e)

finally:
    # 关闭磁盘镜像文件
    img.close()
