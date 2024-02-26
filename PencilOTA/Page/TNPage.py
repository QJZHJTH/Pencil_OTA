# -*-coding:utf-8 -*-
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy

from PencilOTA.Base.BasePage import BasePage
from PencilOTA.Common.utils import startApp, is_screenState, lightScreen, android_version, screen_cut_fun, startSet, \
    slipFac, clickTap
from PencilOTA.Common.utils import start_bluetooth, screen_status


class TNPage(BasePage):

    # 初始化
    def __init__(self, device, screenPath):
        super().__init__()
        # com.tinno.app.pc006.tool/com.tinno.app.MainActivity
        self.pc006_package = "com.tinno.app.pc006.tool"
        self.pc006_activity = "com.tinno.app.MainActivity"
        self.device = device

        self.screenPath = screenPath

        self.pc006_blue_icon = (AppiumBy.XPATH,
                                '//android.view.View[@content-desc="Send"]')

    # 获取driver
    def tn_start_driver(self):
        self.driver = self.start_driver(android_version(self.device))

    # 启动app,跳转到指定界面
    def startTNApk(self):
        if not is_screenState(self.device):
            print("屏幕灭")
            # 屏幕亮屏
            lightScreen(self.device)
        # 打开蓝牙
        start_bluetooth(self.device)
        # 打开app
        startApp(self.device, appPackageName=self.pc006_package, appPackageActive=self.pc006_activity)
        return {'res': True, 'msg': "打开app成功"}

    # 连接蓝牙
    def connect_bluetooth(self, bluetooth_mac):
        # 点击蓝牙连接
        el = self.get_ele(self.pc006_blue_icon)
        if el:
            el.click()
        else:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '未找到搜索蓝牙按钮'}
        conn_times = 0
        while True:
            target_bluetooth = self.get_ele((
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format(bluetooth_mac)))
            if target_bluetooth:
                target_bluetooth.click()
                self.resolve_windows()
                break
            if conn_times > 2:
                screen_cut_fun(self.device, path=self.screenPath)
                return {'res': False, 'msg': '15秒内未找到目标蓝牙'}
            conn_times += 1

        while True:
            clear_btn = self.get_ele((AppiumBy.XPATH, '//android.view.View[@content-desc="Clear"]'))
            if clear_btn:
                break
        return {'res': True, 'msg': '蓝牙连接成功'}

    def update_type_select(self, up_t="DFU"):
        # 选择升级方式
        up_btn = self.get_ele((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format(up_t)))
        if up_btn:
            up_btn.click()
        else:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '未找到目标蓝牙'}

    # 升级
    def update_ver(self, pack):
        # 获取当前版本
        current_ver_el = self.get_ele((AppiumBy.XPATH,
                                       "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android"
                                       ".widget.FrameLayout/androidx.compose.ui.platform.z0/android.view.View/android"
                                       ".view.View/android.view.View/android.view.View[2]/android.widget.TextView[2]"))
        if current_ver_el.text == "null":
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': "配对连接失败！"}

        clear_btn = self.get_ele((AppiumBy.XPATH, '//android.view.View[@content-desc="Delete description"]'))
        clear_btn.click()

        sleep(2)

        select_btn = self.get_ele((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget"
                                                   ".LinearLayout/android.widget.FrameLayout/androidx.compose"
                                                   ".ui.platform.z0/android.view.View/android.view.View/android"
                                                   ".view.View/android.view.View[2]/android.view.View[1]"))

        if not select_btn:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '未点击到Select按钮'}
        select_btn.click()

        target_ver = self.get_ele((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format(pack)))
        if not target_ver:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '未找到目标版本，确认目标版本'}
        target_ver.click()

        # 开始升级
        update_btn = self.get_ele((AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android'
                                                   '.widget.LinearLayout/android.widget.FrameLayout'
                                                   '/androidx.compose.ui.platform.z0/android.view.View'
                                                   '/android.view.View/android.view.View/android.view'
                                                   '.View[2]/android.view.View[2]'))
        update_btn.click()

        # 判断是否升级完成
        while True:
            tar_per = self.get_ele((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("%")))
            if not tar_per:
                break

        sleep(1)

        target_success = self.get_ele(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("success")))
        if not target_success:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '升级失败'}

        return {'res': True, 'msg': "升级成功"}

    # 在线升级
    def udp_online(self):
        # 进入设置
        startSet(device=self.device, appPackageName="com.android.settings")
        # 判断是否在辅助

        target_lf = self.get_ele(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("手写笔")))
        while not target_lf:
            slipFac(device=self.device, ora=["300", "800", "300", "500"])
            sleep(1)
            clickTap(device=self.device, ora=['500', '1120'])
            target_lf = self.get_ele(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("手写笔")))
        target_lf.click()
        target = self.get_ele(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("产品信息")))
        target.click()
        target = self.get_ele(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("固件更新")))
        target.click()
        target = self.get_ele(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("下载并安装")))
        while not target:
            target = self.get_ele(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("下载并安装")))
        target.click()
        target = self.get_ele(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("完成")))
        # 判断升级成功
        while not target:
            target = self.get_ele(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("完成")))
        target.click()

    # 升级成功，取消配对
    def update_cancel_pair(self):
        exit_btn = self.get_ele((AppiumBy.XPATH, '//android.view.View[@content-desc="ArrowBack"]'))
        if not exit_btn:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '退出DFU界面失败'}
        exit_btn.click()

        cancel_pair = self.get_ele((AppiumBy.XPATH, '//android.view.View[@content-desc="Clear"]'))
        if not cancel_pair:
            screen_cut_fun(self.device, path=self.screenPath)
            return {'res': False, 'msg': '未退出到配对界面'}
        cancel_pair.click()

    #  处理弹窗
    def resolve_windows(self):
        sys_el = self.get_ele((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{}")'.format("配对与连接")))
        if sys_el:
            sys_el.click()
        els = self.get_eles((AppiumBy.CLASS_NAME, "android.widget.Button"))
        if els:
            for el in els:
                if el.text == u"确定":
                    el.click()
                elif el.text == u'允许':
                    el.click()
                elif el.text == u'配对':
                    el.click()
                elif el.text == u'配对与连接':
                    el.click()
                else:
                    continue
            return True
        else:
            print("未检测到弹窗")
            return False


if __name__ == '__main__':
    tp = TNPage(device="AMABUN3A17G00223", screenPath="D:\\")
    tp.tn_start_driver()
    # flag = tp.startTNApk()
    tp.udp_online()
