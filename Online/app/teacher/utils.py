import os
import re
import queue
import threading
import time

import cv2 as cv
import subprocess as sp
from pydocx import PyDocX


class Utils:
    def __init__(self, file):
        self.file = file

    def docxToHtml(self):
        template = """
                        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Title</title>
    <script src="../../static/plugin/jquery-1.11.0.min.js"></script>
    <link href="../../static/plugin/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/plugin/bootstrap/js/bootstrap.min.js"></script>
    <link href="../../static/css/student/community.css" rel="stylesheet">
    <script type="text/javascript">
        function autoHeight() {
            var h = $(window).height().toFixed(2);
            var bottom = $(".bottom").height();
            var auto = $("#auto").height();
            if ((bottom + auto) < h) {
                $("#auto").css({'height': h - bottom, 'overflow': 'none'});
            } else {
                return false;
            }
        }

        function getTime() {
            var myDate = new Date;
            var year = myDate.getFullYear(); //获取当前年
            var mon = myDate.getMonth() + 1; //获取当前月
            var date = myDate.getDate(); //获取当前日
            var h = myDate.getHours();//获取当前小时数(0-23)
            var m = myDate.getMinutes();//获取当前分钟数(0-59)
            var s = myDate.getSeconds();//获取当前秒
            if (mon < 10) {
                mon = "0" + mon
            }
            if (date < 10) {
                date = "0" + date
            }
            if (h < 10) {
                h = "0" + h
            }
            if (m < 10) {
                m = "0" + m
            }
            if (s < 10) {
                s = "0" + s
            }

            return year + "-" + mon + "-" + date + " " + h + ":" + m + ":" + s
        }

        $(function () {
            autoHeight();
            $(window).resize(autoHeight);

            $(".bianjiwenzhang").click(function () {
                $("#testSubmit").click()
            });
        });


    </script>
    <isThisStyle>
        </head>
<body>
<div id="auto" style='background: url("/static/img/bg_dark.gif");    overflow:hidden;'>
    <div class="bianjiwenzhang" style="    border-radius: 40px;line-height: 64px;text-align: center;background: black;cursor:pointer;color: white;box-shadow: 0 0 4px 2px #d16106;">提交</div>
    <ul class="nav nav-pills" style="display: flex;    justify-content: center;">

        <li class="nav-item">
            <div style="background: url('/static/img/logo.png');    float: left;width: 100px;height: 36px;/* border: 1px solid; */background-size: 100px 36px;margin-right: 26px;"></div>
        </li>

        <li class="nav-item">
            <a class="nav-link my " href="/student/index">首页</a>
        </li>
        <li class="nav-item">
            <a class="nav-link my" href="/student/course">课程</a>
        </li>
        <li class="nav-item">
            <a class="nav-link my myactive" href="/student/assignments">随堂作业</a>
        </li>
        <li class="nav-item">
            <a class="nav-link my" href="/student/community">社区</a>
        </li>
        <li class="nav-item">
            <a class="nav-link my" href="/student/personal">个人中心</a>
        </li>
        <li class="nav-item">
            <a class="nav-link my" href="/user/logout">退出登录</a>
        </li>
    </ul>

    <div class="homeWorkList">
        <isThisHtml>
            <form action="/student/test/" method="post"><textarea name="content" id="" cols="30" rows="10" placeholder="在这里答题"style="width: 100%;height: 500px;margin-bottom: 50px;outline: none;"></textarea><input id="testSubmit" type="submit" hidden><input name="homeWorkID" type="text" value="{homeWorkID}" hidden><input name="videoID" type="text" value="{videoID}" hidden></form>
            
    </div>


</div>
<div class="bottom">
    © Copyright 2021 www.example.com | All rights reserved.More Templates 学习 - Collect from 学习
</div>
</body>
</html>
                        """
        html = PyDocX.to_html(r'static/word/' + self.file)
        # print(html)
        # print(re.findall(r'(<style>.*?</style>)', html))
        style = re.findall(r'(<style>.*?</style>)', html)[0]
        style = re.sub(r'body\s*{(.*?})', '.homeWorkList p, .homeWorkList span{color: #ddd;}', style)
        style = re.sub(r'style="color:#333333"', 'style="color:#ddd"', style)
        template = template.replace('<isThisStyle>', style)
        body = re.findall(r'<body>(.*?)</body>', html)[0]
        template = template.replace('<isThisHtml>', body)

        return template


# a = Utils(r't1000011628675820.7804015京东教育-小米运维面试题目.docx')
# print(a.d)




class Live(object):
    def __init__(self):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtmpUrl = ""
        self.camera_path = ""

    def read_frame(self):
        print("开启推流")
        cap = cv.VideoCapture(self.camera_path)

        # Get video information
        fps = int(cap.get(cv.CAP_PROP_FPS))
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmpUrl]

        # read webcamera
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                print("Opening camera is failed")
                break

            # put frame into queue
            self.frame_queue.put(frame)

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, stdin=sp.PIPE)
                break

        while True:
            if self.frame_queue.empty() != True:
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                # write to pipe
                p.stdin.write(frame.tostring())

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]


class GetTime():
    def getTime(self):
        return time.strftime("%Y-%m-%d", time.localtime())

