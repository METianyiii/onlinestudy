import os
import re
import threading
import time

from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from pydocx import PyDocX

from Online.settings import BASE_DIR
from app.teacher.utils import Utils
from app.user.models import Video, Teacher, Student, VideoHistoryTeacher, HomeWork, VideoHistory, Answer, Score, \
    VideoCommentAnswer, Article, ArticleCommentReply, StudentInfo, LearningBehavior, StartLive


def course(request):
    return render(request, 'teacher/course.html', locals())


def courseManage(request):
    page = int(request.GET.get("page", 1))
    sreachKey = request.GET.get('sreachKey', '').strip()
    if sreachKey:
        videoList = Video.objects.filter(Q(name__contains=sreachKey) | Q(produce__contains=sreachKey))
    else:
        videoList = Video.objects.all()
    paginator = Paginator(videoList, 4)
    videoList = paginator.page(page)
    return render(request, 'teacher/courseManage.html', locals())


def myUploadcourseManage(request):
    page = int(request.GET.get("page", 1))
    sreachKey = request.GET.get('sreachKey', '').strip()
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    if sreachKey:
        videoList = Video.objects.filter(Q(name__contains=sreachKey) | Q(produce__contains=sreachKey), author=teacher)
    else:
        videoList = Video.objects.filter(author=teacher)
    paginator = Paginator(videoList, 4)
    videoList = paginator.page(page)
    return render(request, 'teacher/myUploadcourseManage.html', locals())


def deleteVideo(request):
    videoID = request.GET.get('videoID')
    Video.objects.filter(videoID=videoID).delete()
    return redirect('teacher:myUploadcourseManage')


@csrf_exempt
def uploadMp4(request):
    username = request.session.get("teacherUsername")
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        produce = request.POST.get("produce")
        mp4 = request.FILES.get("Mp4")
        interface = request.FILES.get("interface")
        test = request.FILES.get("test")
        filename = username + str(time.time()) + mp4.name
        filenameImg = username + str(time.time()) + interface.name
        filenameWord = username + str(time.time()) + test.name
        # print(test.read())
        if mp4:
            dir = os.path.join(BASE_DIR, 'static/video/video')
            destination = open(os.path.join(dir, filename), 'wb+')
            for chunk in mp4.chunks():
                destination.write(chunk)
            destination.close()

            if produce:
                dir = os.path.join(BASE_DIR, 'static/video/img')
                destination = open(os.path.join(dir, filenameImg), 'wb+')
                for chunk in interface.chunks():
                    destination.write(chunk)
                destination.close()
            teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
            video = Video.objects.create(name=name, produce=produce, interfacePath=filenameImg, path=filename, author=teacher)

            if test:
                dir = os.path.join(BASE_DIR, 'static/word')

                with open(os.path.join(dir, filenameWord), 'wb+') as f:
                    f.write(test.read())
                # template = Utils.docxToHtml(filenameWord)
                utils = Utils(filenameWord)
                template = utils.docxToHtml()
                HomeWork.objects.create(name=test.name.split(".")[0], content=template, author=teacher, video=video)
        return redirect("teacher:myUploadcourseManage")
    else:
        return render(request, 'teacher/uploadMp4.html', locals())


@csrf_exempt
def LiveMp4(request):
    username = request.session.get("teacherUsername")
    mp4 = request.FILES.get("file")
    filename = username + str(time.time()) + mp4.name
    dir = os.path.join(BASE_DIR, 'static/video/live')
    destination = open(os.path.join(dir, filename), 'wb+')
    for chunk in mp4.chunks():
        destination.write(chunk)
    destination.close()
    data = {
        'status': 'ok',
        'path': filename
    }
    t1 = threading.Thread(target=putStream, args=(os.path.join(dir, filename), username,))

    t1.start()
    return JsonResponse(data)


def videoDetail(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    if not video:
        return redirect("teacher:myUploadcourseManage")
    videoCommentList = video.videocomment_set.all().order_by("-dateTime")

    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    # 获取收藏数量
    collectNum = len(Teacher.objects.all().filter(video=video)) + len(Student.objects.all().filter(video=video))

    # Student.objects.all().filter(video__collectNum__video=video)
    # print(collectNum)
    # 判断是否收藏
    isCollect = Video.objects.filter(teacherCollect=teacher, videoID=videoID)

    # 作业
    answerList = HomeWork.objects.filter(author=teacher, video=video).first()
    return render(request, 'teacher/videoDetail.html', locals())


@csrf_exempt
def reply(request):
    videoID = request.POST.get('videoID')
    videoCommentID = request.POST.get('videoCommentID')
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    content = request.POST.get('videoComment')
    VideoCommentAnswer.objects.create(content=content, teacher=teacher, VComment_id=videoCommentID)
    return redirect("/teacher/videoDetail/?videoID={}".format(videoID))


def VideoLookNum(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    video.lookNum += 1
    video.save()

    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    VideoHistoryTeacher.objects.create(Teacher=teacher, video=video)
    return HttpResponse("success")


def VideoCollectNum(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    username = request.session.get("teacherUsername")
    print(username, video)
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    if video and teacher:
        video.teacherCollect.add(teacher)

        return HttpResponse("success")
    else:
        return HttpResponse("fail")


def VideoCollectNumCancel(request):
    videoID = request.GET.get('videoID')
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    teacher.video_set.remove(videoID)
    return HttpResponse("success")


def liveStreaming(request):

    return render(request, 'teacher/liveStreaming.html', locals())


def lookChooseVideoStudentInfo(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    studentList = Student.objects.all().filter(video=video)
    isComplete = []
    answerID = []
    n = 0
    for student in studentList:
        answer = Answer.objects.filter(studentID=student, homeWorkID=video.homework).first()
        if answer:
            answerID.append(answer.answerID)
            try :
                isComplete.append(f"分数：{answer.score.score}")
            except Exception as e:
                isComplete.append(n)
        else:
            answerID.append(-1)
            isComplete.append(-1)
        n += 1
    # print(isComplete)
    return render(request, 'teacher/lookChooseVideoStudentInfo.html', locals())


def lookStudentInfo(request):
    studentID = request.GET.get('studentID')
    videoID = request.GET.get('videoID')
    student = Student.objects.filter(studentID=studentID).first()
    return render(request, 'teacher/lookStudentInfo.html', locals())


@csrf_exempt
def checkHomeWorkResult(request):
    if request.method == "GET":
        answerID = request.GET.get('answerID')
        answer = Answer.objects.filter(answerID=answerID).first()
        rePl = """<form action="/student/test/" method="post"><textarea name="content" id="" cols="30" rows="10" placeholder="在这里答题"style="width: 100%;height: 500px;margin-bottom: 50px;outline: none;"></textarea><input id="testSubmit" type="submit" hidden><input name="homeWorkID" type="text" value="{homeWorkID}" hidden></form>"""
        compile = re.compile(r'<form.*</form>', re.S)
        # print(re.findall(r'<form.*</form>', answer.homeWorkID.content))
        cont = "<div style='color:white'>学生答案</div><pre style='width: 98%;white-space: pre-wrap;word-wrap: break-word;border-top: 1px solid #ddd;color: white;'>" + answer.content + "</pre><div style='color:white'>评分：" \
                                                                                                                                                                                     "<form action='/teacher/checkHomeWorkResult/' method='POSt'><input type='number' name='score' placeholder='分数' required>" \
                                                                                                                                                                                     "<input type='text' name='answerID' value='{}' hidden>" \
                                                                                                                                                                                     "<input type='submit' value='确定'></form>" \
                                                                                                                                                                                     "</div>".format(
            answerID)
        content = re.sub(r'<form.*</form>', cont, answer.homeWorkID.content, flags=re.M)
        content = re.sub(
            r'<div class="bianjiwenzhang" style="    border-radius: 40px;line-height: 64px;text-align: center;background: black;cursor:pointer;color: white;box-shadow: 0 0 4px 2px #d16106;">提交</div>',
            '', content, flags=re.M)
        # content = answer.homeWorkID.content.replace(rePl, '')
        # print(compile.findall(r'(<form.*?</form>)', answer.homeWorkID.content))
        # if answer:
        #     topic = HomeWork.objects.filter(homeWorkID=answer.homeWorkID).first()
        return HttpResponse(content)
    elif request.method == "POST":
        username = request.session.get("teacherUsername")
        teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
        answerID = request.POST.get("answerID")
        score = request.POST.get("score")
        answer = Answer.objects.filter(answerID=answerID).first()
        videoID = answer.homeWorkID.video.videoID
        Score.objects.get_or_create(answer=answer, score=score, teacherID=teacher.studentID, homeWorkID=answer.homeWorkID.homeWorkID, studentID=answer.studentID.studentID)
        return redirect("/teacher/lookChooseVideoStudentInfo/?videoID={}".format(videoID))
    # return render(request, 'teacher/checkHomeWorkResult.html', locals())


def community(request):
    page = int(request.GET.get("page", 1))
    searchContent = request.GET.get("searchContent", '').strip()
    username = request.session.get("teacherUsername")
    if searchContent:
        articleList = Article.objects.filter(Q(title__contains=searchContent) | Q(content__contains=searchContent)).order_by("-dateTime")
    else:
        articleList = Article.objects.all().order_by("-dateTime")

    paginator = Paginator(articleList, 4)

    articleList = paginator.page(page)
    return render(request, 'teacher/community.html', locals())

#
# @csrf_exempt
# def editArticle(request):
#     if request.method == "GET":
#         return render(request, 'teacher/editArticle.html', locals())
#     elif request.method == "POST":
#         title = request.POST.get("title")
#         content = request.POST.get("content")
#         username = request.session.get("teacherUsername")
#         teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
#         Article.objects.create(title=title, content=content, student=student)
#
#         return redirect("teacher:community")


def personal(request):
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    return render(request, 'teacher/personal.html', locals())


@csrf_exempt
def editAvatar(request):
    if request.method == "POST":
        # 1.获取上传的图片文件
        imgfile = request.FILES.get('photo')
        size = imgfile.size  # 文件大小    做文件上传大小限制
        content_type = imgfile.content_type  # 文件类型  做文件上传类型限制
        name = imgfile.name  # 文件名称
        username = request.session.get("teacherUsername")
        teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
        teacher.avatar = imgfile
        teacher.save()
        return HttpResponse("success")


@csrf_exempt
def editPersonalInfo(request):
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    if request.method == "GET":
        return render(request, 'teacher/editPersonalInfo.html', locals())
    elif request.method == "POST":
        name = request.POST.get("name")
        nickname = request.POST.get("nickname")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        teacher.name = name
        teacher.nickname = nickname
        teacher.age = age
        teacher.sex = sex
        teacher.save()
        return redirect("teacher:personal")


def courseCollectS(request):
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    collectList = Video.objects.filter(teacherCollect=teacher)
    return render(request, 'teacher/courseCollectS.html', locals())


def WatchTheHistory(request):
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    historyList = VideoHistoryTeacher.objects.filter(Teacher=teacher)
    return render(request, 'teacher/WatchTheHistory.html', locals())


def article(request):
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    articleID = request.GET.get("articleID")
    article = Article.objects.filter(articleID=articleID).first()
    article.readNum += 1
    article.save()
    articleCommentList = article.articlecomment_set.all().order_by("-dateTime")
    return render(request, 'teacher/article.html', locals())


@csrf_exempt
def articleReply(request):
    articleID = request.POST.get('articleID')
    ArticleCommentID = request.POST.get('ArticleCommentID')
    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    content = request.POST.get('articleComment')
    ArticleCommentReply.objects.create(content=content, teacher=teacher, articleComment_id=ArticleCommentID)
    return redirect("/teacher/article/?articleID={}".format(articleID))


def putStream(path, username):
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    teacher.startlive.status = 1
    teacher.startlive.save()
    src = "ffmpeg  -re -i {} -vcodec libx264 -vprofile baseline -acodec libmp3lame -ar 44100 -ac 1 -f flv rtmp://127.0.0.1:1935/live/{}".format(path, username)
    os.system(src)
    teacher.startlive.status = 0
    teacher.startlive.save()


def startLive(request):

    username = request.session.get("teacherUsername")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    return HttpResponse("ok")


def lookStudentAbility(request):
    username = request.GET.get("username")
    videoID = request.GET.get("videoID")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    studentID = student.studentID
    scoreList = []
    courseComplete = 0
    for item in student.answer_set.all():
        try:
            scoreList.append(item.score.score)
            courseComplete += 1
        except Exception as e:
            continue
    if len(scoreList) == 0:
        scoreAvg = 0
    else:
        scoreAvg = sum(scoreList) / len(scoreList)

    result = Score.objects.values('studentID').annotate(avg=Avg('score'))
    avgList = [[Student.objects.filter(studentID=i['studentID']).first().studentinfo.name if Student.objects.filter(
        studentID=i['studentID']).first().studentinfo.name else Student.objects.filter(
        studentID=i['studentID']).first().username, i['avg']] for i in result]
    avgList.sort(key=lambda x: x[0])
    return render(request, 'teacher/lookStudentAbility.html', locals())


def getGenderCount(request):
    male = StudentInfo.objects.filter(sex='男').values_list('sex')
    female = StudentInfo.objects.filter(sex='女').values_list('sex')

    return JsonResponse({'male': len(male), 'female': len(female), 'percent1': '{:.2%}'.format(len(male) / (len(male) + len(female))), 'percent2': '{:.2%}'.format(len(female) / (len(male) + len(female)))})


def getCourseScore(request):
    username = request.GET.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    answerList = student.answer_set.all()
    title = []
    score = []
    for item in answerList:
        try:
            score.append(item.score.score)
            title.append(item.homeWorkID.video.name)
        except Exception as e:
            continue
    data = {
        'title': title,
        'score': score,
    }
    # print(data)
    return JsonResponse(data)


def getClick(request):
    username = request.GET.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    result = LearningBehavior.objects.filter(stu=student).order_by('loginTime')
    if result.count() >= 10:
        result = result[:10]
    data = {
        'label': [i[0].split(" ")[0].split("-", 1)[1] for i in result.values_list('loginTime')],
        'click': [i[0] for i in result.values_list('clickNum')],
    }
    # print(data.get('label'))
    return JsonResponse(data)


def getMain2(request):
    username = request.GET.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    scoreList = []
    courseComplete = 0
    for item in student.answer_set.all():
        try:
            scoreList.append(item.score.score)
            courseComplete += 1
        except Exception as e:
            continue
    if len(scoreList) == 0:
        scoreAvg = 0
    else:
        scoreAvg = sum(scoreList) / len(scoreList)
    videoNum = Video.objects.all().count()
    createNum = Article.objects.all().count()
    createList = StudentInfo.objects.all().order_by('createNum').values('createNum')
    lastIndex = len(createList) - 1
    # 参与度
    if videoNum == 0:
        participation = 0
    else:
        participation = round(LearningBehavior.objects.filter(stu=student, courseDay=1).count() / videoNum, 2)
        if (participation) >= 1:
            participation = 1
    # 积极性
    if videoNum == 0:
        enthusiasm = 0
    else:
        enthusiasm = round(student.studentinfo.collectNum / videoNum, 2)
    # 影响力
    if createList[lastIndex].get('createNum') - createList[0].get('createNum') == 0:
        influence = 0
    else:
        influence = round((student.studentinfo.createNum - createList[0].get('createNum')) / (
                    createList[lastIndex].get('createNum') - createList[0].get('createNum')), 2)
    # 规律性
    if videoNum == 0:
        regularity = 0
    else:
        regularity = round(student.studentinfo.interactive / (videoNum + createNum), 2)
        if (regularity) >= 1:
            regularity = 1
    # 达标率
    SuccessRate = round(scoreAvg / 100, 2)
    data = {
        'participation': participation,
        'enthusiasm': enthusiasm,
        'influence': influence,
        'regularity': regularity,
        'SuccessRate': SuccessRate,
    }
    return JsonResponse(data)
