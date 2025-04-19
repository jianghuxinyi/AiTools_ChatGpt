#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import time
import openai
import threading
from tkinter.messagebox import *
import tkinter.ttk
import base64
from icon import Icon
import os

LOG_LINE_NUM = 0


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.CHOOSE_MODE = IntVar()
        self.CHOOSE_MODE.set(1)

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("AI文本生成工具_leo · lee")  # 窗口名
        width = 1068
        height = 681
        screen_width = self.init_window_name.winfo_screenwidth()
        screen_height = self.init_window_name.winfo_screenheight()
        x = int(screen_width / 2 - width / 2)
        y = int(screen_height / 2 - height / 2)
        size = '{}x{}+{}+{}'.format(width, height, x, y)
        self.init_window_name.geometry(size)
        self.init_window_name.resizable(height=False, width=False)
        with open('tmp.ico', 'wb') as tmp:
            tmp.write(base64.b64decode(Icon().img))
        self.init_window_name.iconbitmap('tmp.ico')
        os.remove('tmp.ico')

        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        #self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=46)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        self.btn_radio_mode_common = Radiobutton(self.init_window_name, text="通用模式", bg="lightblue", width=10, variable=self.CHOOSE_MODE, value=1)
        self.btn_radio_mode_common.grid(row=1, column=11)
        self.btn_radio_mode_polish = Radiobutton(self.init_window_name, text="中文模式", bg="lightblue", width=10, variable=self.CHOOSE_MODE, value=2)
        self.btn_radio_mode_polish.grid(row=2, column=11)

        self.btn_radio_mode_polish = Radiobutton(self.init_window_name, text="英文模式", bg="lightblue", width=10,
                                                 variable=self.CHOOSE_MODE, value=3)
        self.btn_radio_mode_polish.grid(row=3, column=11)

        # 按钮
        self.bar_progress = tkinter.ttk.Progressbar(self.init_window_name, length=100, mode='indeterminate', orient=tkinter.HORIZONTAL)
        self.bar_progress.grid(row=4, column=11)

        # 按钮
        self.btn_generate = Button(self.init_window_name, text="文本生成>>", bg="lightblue", width=10,
                                              command=self.txt_ai_mode)  # 调用内部方法  加()为直接调用
        self.btn_generate.grid(row=5, column=11)

        # 按钮
        self.btn_continue_generate= Button(self.init_window_name, text="继续生成", bg="lightblue", width=10,
                                              command=self.ai_continue_generate_txt)  # 调用内部方法  加()为直接调用
        self.btn_continue_generate.grid(row=16, column=16)

    # 开启线程
    def thread_it(self, fc, *args):
        self.t = threading.Thread(target=fc, args=args)
        self.t.setDaemon(True)
        self.t.start()

    # 功能函数
    def txt_ai_mode(self):
        if self.init_data_Text.get(1.0, END).strip() == "":
            return

        # 判断时间
        print(int(time.time()))
        if int(time.time()) > int(1677680542):
            showerror("提示！", "账号已过期，请重新激活")
            return
        self.result_data_Text.delete(1.0, END)
        if self.CHOOSE_MODE.get() == 1:
            self.thread_it(self.ai_generate_txt)
            return
        if self.CHOOSE_MODE.get() == 2:
            self.thread_it(self.ai_polish_txt_zh)
            return
        if self.CHOOSE_MODE.get() == 3:
            self.thread_it(self.ai_polish_txt_en)
            return

    def ai_generate_txt(self):
        self.btn_continue_generate['state'] = DISABLED
        self.btn_generate['state'] = DISABLED
        self.bar_progress.start(5)
        try:
            self.write_log_to_Text("INFO:AI 文本生成中...")
            print(threading.current_thread().name)
            # openai.api_key = ""
            openai.api_key = ""
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.init_data_Text.get(1.0, END).strip(),
                temperature=0.3,
                max_tokens=200,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response)
            self.result_data_Text.delete(1.0, END)
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.result_data_Text.insert(1.0, self.init_data_Text.get(1.0, END).strip() + response.choices[0].text)
            self.bar_progress.stop()
            self.write_log_to_Text("SUCC:AI 文本生成完成...")
        except:
            self.bar_progress.stop()
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.write_log_to_Text("ERROR:AI 文本生成失败...")
            showerror('错误！', '生成错误，请重新生成...')

    def ai_continue_generate_txt(self):
        # 判断时间
        print(int(time.time()))
        if int(time.time()) > int(1677680542):
            showerror("提示！", "账号已过期，请重新激活")
            return
        self.thread_it(self.ai_continue_generate_request)

    def ai_continue_generate_request(self):
        if self.result_data_Text.get(1.0, END).strip() == "":
            return
        self.bar_progress.start(5)
        self.btn_continue_generate['state'] = DISABLED
        self.btn_generate['state'] = DISABLED
        try:
            self.write_log_to_Text("INFO:AI 文本续写中...")
            print(threading.current_thread().name)
            openai.api_key = ""
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.result_data_Text.get(1.0, END).strip(),
                temperature=0.3,
                max_tokens=200,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response)
            self.result_data_Text.insert(END, response.choices[0].text)
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.bar_progress.stop()
            self.write_log_to_Text("SUCC:AI 文本续写完成...")
        except:
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.bar_progress.stop()
            self.write_log_to_Text("ERROR:AI 文本续写失败...")
            showerror('错误！', '生成错误，请重新生成...')


    def ai_polish_txt_zh(self):
        try:
            self.bar_progress.start(5)
            self.btn_continue_generate['state'] = DISABLED
            self.btn_generate['state'] = DISABLED
            self.write_log_to_Text("INFO:AI 中文文本生成中...")
            print(threading.current_thread().name)
            openai.api_key = ""
            response = openai.Completion.create(
                model="text-davinci-003",
                # prompt="Correct this to standard English:\n\n" + self.init_data_Text.get(1.0, END).strip(),
                prompt="Correct this to standard Chinese:\n\n"+self.init_data_Text.get(1.0, END).strip(),
                temperature=0.3,
                max_tokens=1500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response)
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, response.choices[0].text)
            self.bar_progress.stop()
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.write_log_to_Text("SUCC:AI 中文文本生成完成...")
        except:
            self.bar_progress.stop()
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.write_log_to_Text("ERROR:AI 中文文本生成失败...")
            showerror('错误！', '生成错误，请重新生成...')

    def ai_polish_txt_en(self):
        try:
            self.bar_progress.start(5)
            self.btn_continue_generate['state'] = DISABLED
            self.btn_generate['state'] = DISABLED
            self.write_log_to_Text("INFO:AI 英文文本生成中...")
            openai.api_key = ""
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Correct this to standard English:\n\n" + self.init_data_Text.get(1.0, END).strip(),
                #prompt="Correct this to standard Chinese:\n\n"+self.init_data_Text.get(1.0, END).strip(),
                temperature=0.3,
                max_tokens=1500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response)
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, response.choices[0].text)
            self.bar_progress.stop()
            self.write_log_to_Text("SUCC:AI 英文文本生成完成...")
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
        except:
            self.bar_progress.stop()
            self.btn_continue_generate['state'] = NORMAL
            self.btn_generate['state'] = NORMAL
            self.write_log_to_Text("ERROR:AI 英文文本生成失败...")
            showerror('错误！', '生成错误，请重新生成...')

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
