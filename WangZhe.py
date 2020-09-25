# -*- coding: utf-8 -*-
import os
import time
from time import sleep
import random
import cv2

repeat_times = 600
包名 = 'com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity'


def 随机延迟(秒数):
    """
    随机延迟，时间在输入的秒数以内
    :param 秒数: 延迟的时间，秒
    :return: 无
    """
    sleep(random.random() * 秒数)


def 长随机延迟(秒数):
    """
    随机给延迟增加0~1秒，适合长延迟
    :param 秒数: 延迟的时间，秒
    :return: 无
    """
    sleep(random.random() + 秒数)


def 模拟点击(点击位置):
    """
    模拟点击触屏，会在点击前后随机延迟，延迟小于0.1秒
    :param 点击位置: 输入表示点击位置的元组
    :return: 无返回值，执行点击
    """
    x, y = 点击位置
    x += random.randint(-5, 5)
    y += random.randint(-3, 3)
    随机延迟(0.1)
    os.system('adb shell input tap {} {}'.format(x, y))
    随机延迟(0.1)


def 截屏():
    """
    安卓截屏
    :return: 无返回值，在根目录下生成screen.png
    """
    os.system('adb shell screencap -p sdcard/screen.png')
    os.system('adb pull /sdcard/screen.png')


def 找图(模板, 截屏='screen.png'):
    """
    找到模板图像在截屏中的位置
    :param 模板: 模板名字，字符串格式
    :param 截屏: 截屏的名字，字符串格式
    :return: 匹配到的位置，输出元组为(横坐标、纵坐标)；如果没匹配到返回
    """
    # tem = cv2.imread(模板)
    # height, width, depth = tem.shape
    # scr_shot = cv2.imread(截屏)
    # res = cv2.matchTemplate(image=scr_shot, templ=tem, method=cv2.TM_SQDIFF)
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # if min_val <= max_val / 256:
    #     return min_loc[0] + int(width / 2), min_loc[1] + int(height / 2)
    # else:
    #     return -1
    min_val, max_val, min_loc, max_loc = 找图匹配度(模板, 截屏)
    return 找图后处理(模板, min_val, max_val, min_loc, max_loc)


def 找图匹配度(模板, 截屏='screen.png'):
    tem = cv2.imread(模板)
    height, width, depth = tem.shape
    scr_shot = cv2.imread(截屏)
    res = cv2.matchTemplate(image=scr_shot, templ=tem, method=cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return min_val, max_val, min_loc, max_loc


def 找图后处理(模板, min_val, max_val, min_loc, max_loc):
    """
    找图后判断点击并确定图的中点
    :param min_val:
    :param max_val:
    :param min_loc:
    :param max_loc:
    :return:
    """
    tem = cv2.imread(模板)
    height, width, depth = tem.shape
    if min_val <= max_val / 100:
        return min_loc[0] + int(width / 2), min_loc[1] + int(height / 2)
    else:
        return -1


def 点击按钮(按钮模板):
    """
    点击已经截图了的按钮
    :param 按钮模板: 就是按钮的截图
    :return: 返回0表示点了，返回-1表示没点到
    """
    截屏()
    随机延迟(0.5)
    按钮中点坐标 = 找图(模板=按钮模板)
    if 按钮中点坐标 != -1:
        模拟点击(按钮中点坐标)
        return 0
    else:
        print('未找到按钮！')
        return -1


def 获取当前应用():
    """
    用adb获取当前活动应用
    :return: 当前应用名
    """
    当前应用 = os.popen('adb shell dumpsys window | findstr mCurrentFocus')
    当前应用名 = 当前应用.read()
    return 当前应用名


def 启动游戏(包名):
    """
    用adb启动所需的应用
    :param 包名: 待启动的应用包名
    :return: 无
    """
    os.system('adb shell am start ' + 包名)


def 检验是否运行并启动(包名):
    """
    先检验是否启动，如果没启动就现在启动
    :param 包名: 待启动的应用包名
    :return: 无
    """
    当前应用名 = 获取当前应用()
    if 当前应用名.find(包名) != -1:
        print('游戏已启动！')
    else:
        print('游戏尚未启动！')
        启动游戏(包名)


def 等待至点击一次(按钮模板):
    """
    如果按键没刷出来，就等一会儿；如果刷出来了，就点一下按键
    :param 按钮模板: 要点击的按键截图文件位置
    :return: 无
    """
    等待轮次 = 0
    while 1:
        点击结果 = 点击按钮(按钮模板)  # 开始游戏
        if 点击结果 != -1:
            break
        else:
            随机延迟(1)
            等待轮次 += 1


def 点掉所有按钮(按钮模板):
    """
    连续点某个按键（主要是点掉叉叉），直到该按键都被点没了
    :param 按钮模板: 要点击的按键截图文件位置
    :return: 无
    """
    while 1:
        随机延迟(1)
        点击结果 = 点击按钮(按钮模板)
        if 点击结果 == -1:
            break


def 调节开关型按钮(关型模板, 开型模板, 调节目标=True):
    关型模板方差 = 找图匹配度(关型模板)
    开型模板方差 = 找图匹配度(开型模板)
    if 调节目标:
        if 开型模板方差 > 关型模板方差:
            点击按钮(关型模板)
            return
    else:
        if 开型模板方差 < 关型模板方差:
            点击按钮(开型模板)
            return


################################
#  状态机部分
def 初始状态():
    当前应用名 = 获取当前应用()
    if 当前应用名.find(包名) == -1:
        print('游戏尚未启动！')
        启动游戏(包名)
        return 开始游戏
    else:
        截屏()
        if 找图(模板=r'tem/kaishiyouxi.jpg') != -1:
            return 开始游戏
        elif 找图(模板=r'tem/chacha.jpg') != -1:
            return 点掉叉叉
        elif 找图(模板=r'tem/wanxiang.jpg') != -1:
            return 点击万象天工
        elif 找图(模板=r'tem/maoxian.jpg') != -1:
            return 点击冒险玩法
        elif 找图(模板=r'tem/tiaozhan.jpg') != -1:
            return 点击挑战
        elif 找图(模板=r'tem/xiayibu.jpg') != -1:
            return 点击下一步
        elif 找图(模板=r'tem/chuangguan.jpg') != -1:
            return 点击闯关
        elif 找图(模板=r'tem/zidongguan.jpg') != -1 or 找图(模板=r'tem/zidongkai.jpg') != -1:
            return 点击自动开关
        elif 找图(模板=r'tem/jixu.jpg') != -1:
            return 点击屏幕继续
        elif 找图(模板=r'tem/zaicitiaozhan.jpg') != -1:
            return 点击再次挑战
        else:
            return 初始状态


def 开始游戏():
    等待至点击一次(r'tem/kaishiyouxi.jpg')
    长随机延迟(5)
    return 点掉叉叉


def 点掉叉叉():
    等待至点击一次(r'tem/chacha.jpg')
    点掉所有按钮(r'tem/chacha.jpg')
    return 点击万象天工


def 点击万象天工():
    等待至点击一次(r'tem/wanxiang.jpg')
    return 点击冒险玩法


def 点击冒险玩法():
    等待至点击一次(r'tem/maoxian.jpg')
    return 点击挑战


def 点击挑战():
    等待至点击一次(r'tem/tiaozhan.jpg')
    return 点击下一步


def 点击下一步():
    等待至点击一次(r'tem/xiayibu.jpg')
    return 点击闯关


def 点击闯关():
    等待至点击一次(r'tem/chuangguan.jpg')
    return 点击自动开关


def 点击自动开关():
    调节开关型按钮(r'tem/zidongguan.jpg', r'tem/zidongkai.jpg')
    长随机延迟(30)
    return 点击屏幕继续

def 点击屏幕继续():
    等待至点击一次(r'tem/jixu.jpg')
    return 点击再次挑战


def 点击再次挑战():
    等待至点击一次(r'tem/zaicitiaozhan.jpg')
    return 点击闯关


################################


if __name__ == '__main__':
    状态机函数 = 初始状态()
    while 1:
        状态机函数 = 状态机函数()

    # sleep(30)
    # 点击按钮(r'tem/chacha.jpg') #游戏内的叉叉
    #  mCurrentFocus=Window{d7734f8 u0 com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity}
    # if 当前应用 != '  mCurrentFocus=Window{3148ce u0 com.android.launcher3/com.android.launcher3.Launcher}':
    #     os.system('adb shell am start com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity')
    # 截屏()
    # 开始游戏 = 找图(tem_in=r"tem/muban.png", scr_in='screen.png')
    # if
    # elif 开始游戏 != -1:
    #     模拟点击(开始游戏)
    # elif
    # screen()
    # a = time.time()
    # i = cv2.imread("screen.png")
    # ii = i[:170, :170]
    # find_filter()
    # print(a)

    # tap_screen(pos)

    # for i in range(repeat_times):
    #     if i > 0:
    #         tap_screen((814, 498))  # 再次挑战
    #         print("再次挑战开始")
    #         sleep(3)
    #     tap_screen((726, 440))  # 闯关
    #     print("开始闯关")
    #     sleep(10)
    #     # tap_screen((890, 25))  # 自动
    #     # print("自动按钮点击")
    #     sleep(85)
    #     tap_screen((400, 275))  # 点击屏幕继续
    #     print("点击屏幕继续")
    #     sleep(5)
    #     tap_screen((814, 498))  # 再次挑战
    #     sleep(1)
