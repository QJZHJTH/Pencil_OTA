# -*-coding:utf-8 -*-
import os

from time import sleep


# 获取安卓版本
def android_version(device):
    ver = os.popen("adb -s {} shell getprop ro.build.version.release".format(device))
    return ver.readline()


# 获取某个路径下的文件
def file_list(device):
    list_files = os.popen("adb -s {} shell ls /sdcard/OTA".format(device))
    print(list_files.readlines())


# 传文件到手机
def tra_file(device, pc_file):
    data = os.popen("adb -s {} push {} /sdcard/OTA/".format(device, pc_file))
    print(data.read())


# 获取手机系统时间
def get_phone_time(device):
    data = os.popen("adb -s {} shell date".format(device)).read()
    data = data.strip("\n")
    return data


# 获取所有连接的设备
def get_devices():
    ret = os.popen('adb devices').readlines()

    device_lists = []
    for item in ret:
        if '\tdevice\n' in item:
            device_lists.append(item[:item.index('\t')])
    return device_lists


# 判断apk是否安装
def apkIsInstall(device, apkPackage=None):
    return os.popen(
        'adb -s {} shell pm list packages | find "com.keyboardapp.firmwaredownload.lxI2c"'.format(device)).readlines()


# 安装apk
def installApk(path):
    os.system("adb install {}".format(path))


# 获取当前运行apk的包名
def currentRunPackage(device):
    return os.popen("adb -s {} shell dumpsys window | findstr mCurrentFocus".format(device)).read()


# 启动app
def startApp(device, appPackageName, appPackageActive):
    os.popen("adb -s {} root".format(device))
    res = os.popen("adb -s {} shell am start -n {}/{}".format(device, appPackageName, appPackageActive))
    return res.readlines()


# 启动设置
def startSet(device, appPackageName):
    res = os.popen("adb -s {} shell am start {}".format(device, appPackageName))
    return res.readlines()


# 关闭app
def stopApp(device, packageName):
    os.system("adb -s {} shell am force-stop {}".format(device, packageName))


# 上下滑动
def slipFun(device):
    os.popen("adb -s " + device + " shell input swipe 1500 960 1500 450")


# 左右滑动
def RightSlipFun(device):
    os.popen("adb -s " + device + " shell input swipe 0 800 200 800")


def slipFac(device, ora=[]):
    s = " ".join(ora)
    print(s)
    os.popen("adb -s {} shell input swipe {}".format(device, s))


def clickTap(device, ora=[]):
    s = " ".join(ora)
    os.popen("adb -s {} shell input tap {}".format(device, s))


# 判断屏幕亮灭状态
def is_screenState(device):
    try:
        cmd = 'adb -s ' + device + ' shell dumpsys power | findstr "Display Power: state="'
        res = os.popen(cmd).read()
        if "mHoldingDisplaySuspendBlocker=true" in res:
            return True
        else:
            return False
    except Exception as e:
        print('获取手机屏幕点亮状态异常', e)
        return False


# 判断横竖屏状态adb shell dumpsys input | findstr orientation=
def screen_status(device):
    res = os.popen("adb -s {} shell dumpsys input | findstr orientation=".format(device))
    data = res.read()
    if "orientation=0" in data:
        return 0
    else:
        return 1


# 亮屏进入主页面
def lightScreen(device):
    os.popen("adb -s " + device + " shell input keyevent 224")
    sleep(1)
    slipFun(device)


def screen_cut_fun(device, path):
    data = get_phone_time(device)
    data_list = data.split(" ")
    temp = data_list[3].replace(":", "-")
    data_list[3] = temp
    pic_name = data_list[3]
    print(pic_name)
    # 进行截图
    cut_cmd = "adb -s " + device + " shell screencap -p /sdcard/" + pic_name + ".png"
    os.system(cut_cmd)
    # 获取截图照片
    get_cmd = "adb -s " + device + " pull /sdcard/" + pic_name + ".png " + path
    res = os.popen(get_cmd).read()
    if "1 file pulled" in res:
        return True
    else:
        return False


# 获取蓝牙状态并打开
def start_bluetooth(device):
    is_open = os.popen("adb -s {} shell settings get global bluetooth_on".format(device))
    data = is_open.read()
    if data == "0":
        os.system("adb -s {} shell svc bluetooth enable".format(device))


if __name__ == '__main__':
    # flag = screen_cut_fun(device="01234ABC", path=r"D:\result")

    ret = get_devices()
    print(ret)
    # startSet("AMABUN3A17G00223", appPackageName="com.android.settings")
    clickTap(device="AMABUN3A17G00223", ora=['300', '2080'])
