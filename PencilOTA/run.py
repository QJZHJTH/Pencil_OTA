# -*-coding:utf-8 -*-

from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog

from PencilOTA.Common.log import Logger
from PencilOTA.Common.utils import get_devices, screen_cut_fun, startApp, tra_file
from PencilOTA.Page.TNPage import TNPage


class OTAGui:

    def __init__(self):

        self.root = Tk()
        self.root.title("OTA升降级测试")
        self.root.geometry("530x280+750+250")
        self.root.resizable(width=False, height=False)
        self.btn_start = None
        # 操作的设备
        self.device = ""
        self.devices = []

        # 本地升级或在线升级
        self.up_type = ""
        self.up_typeVar = StringVar()
        self.up_types = ["本地", "在线"]

        # 操作的MCU
        self.mcu = ""
        # 结果保存的路径
        self.file_path = StringVar()
        # 失败截图保存路径
        self.screen_path = StringVar()
        # 电脑连接的所有设备
        self.deviceVar = StringVar()
        self.high_edition = StringVar()
        self.low_edition = StringVar()
        self.times = StringVar()
        self.time_value = StringVar()
        self.logger = ""
        self.status = StringVar()
        self.status.set("未开始")
        self.blue_name = StringVar()
        self.blue_name.set('6F:50')
        # 创建页面主体
        self.main_module()

    def main_module(self):
        top_frame = Frame(self.root, width=650)
        top_frame.grid(row=0, column=0, padx=15, pady=5)
        # 设备选择模块
        top_t = Frame(top_frame)
        top_t.grid(row=0, column=0)
        top_b = Frame(top_frame)
        top_b.grid(row=1, column=0)
        self.devices = get_devices()
        label_device = Label(top_t, text="选择设备：")
        label_device.grid(row=0, column=0, padx=5, pady=5)
        self.combox_devices = ttk.Combobox(top_t, textvariable=self.deviceVar, values=self.devices)
        self.combox_devices.grid(row=0, column=1, pady=5)
        self.combox_devices.bind('<<ComboboxSelected>>', self.select_device_event)
        self.combox_devices.bind('<Button-1>', self.click_device_event)
        # 结果存放路径
        label_resultPath = Label(top_t, text="log路径：")
        label_resultPath.grid(row=0, column=2, pady=5)
        entry_path = Entry(top_t, textvariable=self.file_path, state="readonly")
        entry_path.grid(row=0, column=3)
        btn_select_path = Button(top_t, text="选择", command=self.select_file_path)
        btn_select_path.grid(row=0, column=4, padx=5)

        label_type = Label(top_b, text="选择类型：")
        label_type.grid(row=0, column=0, padx=5, pady=5)
        combox_type = ttk.Combobox(top_b, textvariable=self.up_typeVar, values=self.up_types)
        combox_type.grid(row=0, column=1, pady=5)
        combox_type.bind('<<ComboboxSelected>>', self.select_type_event)

        # 截图存放路径
        label_screenPath = Label(top_b, text="截图路径：")
        label_screenPath.grid(row=0, column=2, pady=5)
        entry_screen = Entry(top_b, textvariable=self.screen_path, state="readonly")
        entry_screen.grid(row=0, column=3, pady=5)
        btn_select_screen = Button(top_b, text="选择", command=self.select_screen_path)
        btn_select_screen.grid(row=0, column=4, pady=5)

        # 底部参数模块
        bottom_frame = LabelFrame(self.root, text="操作设置")
        bottom_frame.grid(row=1, column=0, padx=5, pady=10)
        # 高版本选择
        label_high_edition = Label(bottom_frame, text="版本1：")
        label_high_edition.grid(row=0, column=0, pady=5)
        entry_high_edition = Entry(bottom_frame, textvariable=self.high_edition, state="readonly")
        entry_high_edition.grid(row=0, column=1, pady=5)
        btn_high_path = Button(bottom_frame, text="选择", command=self.select_high_file)
        btn_high_path.grid(row=0, column=2, padx=5)
        # 低版本
        label_low_edition = Label(bottom_frame, text="版本2：")
        label_low_edition.grid(row=0, column=3, pady=5)
        entry_low_edition = Entry(bottom_frame, textvariable=self.low_edition, state="readonly")
        entry_low_edition.grid(row=0, column=4, pady=5)
        btn_low_path = Button(bottom_frame, text="选择", command=self.select_low_file)
        btn_low_path.grid(row=0, column=5, padx=5, )
        # 验证次数
        label_times_edition = Label(bottom_frame, text="验证次数：")
        label_times_edition.grid(row=1, column=0, pady=15)
        entry_times = Entry(bottom_frame, textvariable=self.times)
        entry_times.grid(row=1, column=1, pady=15)

        # 蓝牙名
        label_blue_name = Label(bottom_frame, text="MAC地址：")
        label_blue_name.grid(row=1, column=3, pady=5)
        entry_blue_name = Entry(bottom_frame, textvariable=self.blue_name)
        entry_blue_name.grid(row=1, column=4, pady=5)

        # 状态
        label_status_tag = Label(bottom_frame, text="状态:")
        label_status_tag.grid(row=2, column=1)
        label_status = Label(bottom_frame, textvariable=self.status, fg="red")
        label_status.grid(row=2, column=2, columnspan=3, sticky='W')

        # 由低到高按钮
        bottom_frm = Frame(self.root)
        bottom_frm.grid(row=2, column=0)
        self.btn_start = Button(bottom_frm, text="开始", command=self.thread_start_fun, width=10)
        self.btn_start.grid(row=0, column=0, padx=10, pady=10)
        self.btn_exit = Button(bottom_frm, text="退出", command=self.thread_exit_fun, width=10)
        self.btn_exit.grid(row=0, column=1, padx=10, pady=10)

    # 下拉点击事件
    def click_device_event(self, event):
        self.devices = get_devices()
        self.combox_devices['value'] = self.devices

    # 选择文件路径事件
    def select_file_path(self):
        select_folder = filedialog.askdirectory()
        self.file_path.set(select_folder)

    # 选择截图路径事件
    def select_screen_path(self):
        screen_folder = filedialog.askdirectory()
        self.screen_path.set(screen_folder)

    def select_high_file(self):
        high_file = filedialog.askopenfilename(title=u'选择文件')
        tra_file(device=self.device, pc_file=high_file)
        high_file = high_file[-14:]
        high_file = high_file.replace('.zip', '')
        high_file = high_file.replace('/', '')
        self.high_edition.set(high_file)

    def select_low_file(self):
        low_file = filedialog.askopenfilename(title=u'选择文件')
        tra_file(device=self.device, pc_file=low_file)
        low_file = low_file[-14:]
        low_file = low_file.replace('.zip', '')
        low_file = low_file.replace('/', '')
        self.low_edition.set(low_file)

    # 选择设备事件
    def select_device_event(self, event):
        self.devices = get_devices()
        self.device = self.deviceVar.get()

    # 选择升级方式事件
    def select_type_event(self, event):
        self.up_type = self.up_typeVar.get()

    # 启动线程
    def thread_start_fun(self):
        thread_start = Thread(target=self.start_update)
        thread_start.start()

    # 退出界面
    def thread_exit_fun(self):
        thread_exit = Thread(target=self.ui_des)
        thread_exit.start()

    # 升降级
    def start_update(self):
        self.status.set(value="开始OTA")
        # 判断信息是否填写完整
        if not self.msg_write_is_complete():
            return False
        self.btn_start['state'] = 'disable'
        # 创建logger对象
        self.logger = Logger("result", self.file_path.get(), self.device)
        message = "选择的设备：" + self.device + ",版本1：" + self.high_edition.get() + ",版本2：" + self.low_edition.get() + \
                  "，验证次数：" + self.times.get() + "，连接蓝牙MAC" + self.blue_name.get()
        self.logger.info(msg=message)
        times = int(self.times.get())
        tp = TNPage(device=self.device, screenPath=self.screen_path.get())
        tp.tn_start_driver()
        ver = self.high_edition.get()
        # 启动app
        flag = tp.startTNApk()
        self.status.set(flag['msg'])
        t = 1
        while times != 0:
            if self.up_type == "本地":
                # 选择版本
                if ver == self.high_edition.get():
                    ver = self.low_edition.get()
                    self.status.set("高版本升级")
                else:
                    ver = self.high_edition.get()
                    self.status.set("低版本升级")
                times -= 1
                s = "第{}次升级".format(t)
                self.logger.info(msg=s)
                self.status.set(s)

                flag = tp.connect_bluetooth(bluetooth_mac=self.blue_name.get())
                if not self.resolve_res(flag):
                    self.btn_start['state'] = 'normal'
                    self.status.set('连接蓝牙失败')
                    self.logger.error(msg='连接蓝牙失败')
                    continue
                tp.update_type_select()
                self.status.set('开始进行选版本升级')
                flag = tp.update_ver(pack=ver)
                if not self.resolve_res(flag):
                    self.status.set('升级版本失败')
                    self.btn_start['state'] = 'normal'
                    self.logger.error(msg='升级版本失败')
                    self.logger.info(msg="第{}次执行结束，执行结果：success".format(t))
                    continue
                self.logger.info(msg="第{}次执行结束，执行结果：success".format(t))
                self.status.set("第{}次执行结束，执行结果：success".format(t))
                tp.update_cancel_pair()

            else:
                if t % 2 != 0:
                    s = "第{}次升级".format(t)
                    self.logger.info(msg=s)
                    self.status.set(s)
                    flag = tp.connect_bluetooth(bluetooth_mac=self.blue_name.get())
                    if not self.resolve_res(flag):
                        self.btn_start['state'] = 'normal'
                        self.status.set('连接蓝牙失败')
                        self.logger.error(msg='连接蓝牙失败')
                        continue
                    tp.update_type_select()
                    self.status.set('开始进行选版本升级')
                    flag = tp.update_ver(pack=ver)
                    if not self.resolve_res(flag):
                        self.status.set('升级版本失败')
                        self.btn_start['state'] = 'normal'
                        self.logger.error(msg='升级版本失败')
                        self.logger.info(msg="第{}次执行结束，执行结果：success".format(t))
                        continue

                else:
                    tp.udp_online()

            self.logger.info(msg="第{}次执行结束，执行结果：success".format(t))
            self.status.set("第{}次执行结束，执行结果：success".format(t))
            t += 1

        self.btn_start['state'] = 'normal'
        self.status.set(value="执行结束")
        messagebox.showinfo(title="提醒", message="执行结束")

    def resolve_res(self, flag):
        if not flag['res']:
            self.status.set(flag['msg'])
            self.logger.info(msg=flag['msg'])
            return False
        self.logger.info(msg=flag['msg'])
        self.status.set(flag['msg'])
        return True

    def ui_des(self):
        self.root.destroy()

    # 复选框验证
    def msg_write_is_complete(self):
        if self.device == "":
            messagebox.showwarning(title="警告", message="请选择测试设备")
            return False
        if self.up_type == "":
            messagebox.showwarning(title="警告", message="请选择升级方式")
            return False
        if self.file_path.get() == "":
            messagebox.showwarning(title="警告", message="请选择结果路径")
            return False
        if self.screen_path.get() == "":
            messagebox.showwarning(title="警告", message="请选择截图路径")
            return False
        if self.high_edition.get() == "":
            messagebox.showwarning(title="警告", message="请选择版本1路径")
            return False
        if self.up_type == "本地":
            if self.low_edition.get() == "":
                messagebox.showwarning(title="警告", message="请选择版本2路径")
                return False
        if self.times.get() == "":
            messagebox.showwarning(title="警告", message="请填写验证次数")
            return False
        if self.times.get() != "":
            if not self.times.get().isdigit():
                messagebox.showwarning(title="警告", message="验证次数请填写数字")
                return False
        if self.blue_name.get() == "":
            messagebox.showwarning(title="警告", message="请填写名称")
            return False
        return True


if __name__ == '__main__':
    ota = OTAGui()
    ota.root.mainloop()
