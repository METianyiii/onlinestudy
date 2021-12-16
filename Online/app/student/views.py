import json
import time

from weibopy.weibo import WeiboClient


from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.teacher.utils import GetTime
from app.user.models import Video, Student, VideoComment, StudentInfo, Article, ArticleComment, VideoHistory, Teacher, \
    HomeWork, Answer, LearningBehavior, Score, StartLive


def index(request):
    return render(request, 'student/index.html', locals())


def course(request):
    page = int(request.GET.get("page", 1))
    sreachKey = request.GET.get('sreachKey', '').strip()
    if sreachKey:
        videoList = Video.objects.filter(Q(name__contains=sreachKey) | Q(produce__contains=sreachKey))
    else:
        videoList = Video.objects.all()
    # 初始化分页器，每页十个
    paginator = Paginator(videoList, 4)
    # 对页码进行处理
    # if paginator.num_pages > 10:
    #     # 判断页码大于5且小于总页码减3时
    #     if 5 < page < paginator.num_pages - 3:
    #         # 从总页码列表里取当前页码前三个和后三个和最后三个
    #         page_range = list(paginator.page_range[page - 3:page + 3]) + list(["···", ]) + list(
    #             paginator.page_range[-3:-1])
    #     # 当页码小于5时
    #     elif page <= 5:
    #         # 判断总页码数小于等于5时取所有页码列表
    #         if len(paginator.page_range) <= 5:
    #             page_range = list(paginator.page_range)
    #         # 取总页码前五个，和后三个
    #         else:
    #             page_range = list(paginator.page_range[0:5]) + list(["···", ]) + list(paginator.page_range[-3:-1])
    #     # 取总页码前三个和后四个
    #     else:
    #         page_range = list(paginator.page_range[0:3]) + list(["···", ]) + list(paginator.page_range[-4:-1])
    #     # 判断页码列表最后一个不是...时，取页码列表最后一个加一再追加进去
    #     if page_range[-1] != '···':
    #         page_range.append(int(page_range[-1]) + 1)
    # else:
    #     page_range = paginator.page_range
        # 获取对应页码的资源
    videoList = paginator.page(page)


    return render(request, 'student/course.html', locals())


def videoDetail(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    if not video:
        return redirect("student:course")
    videoCommentList = video.videocomment_set.all().order_by("-dateTime")

    username = request.session.get("username")
    # 获取收藏数量
    collectNum = len(Teacher.objects.all().filter(video=video)) + len(Student.objects.all().filter(video=video))
    # Student.objects.all().filter(video__collectNum__video=video)
    # print(collectNum)
    # 判断是否收藏
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    isCollect = Video.objects.filter(collectNum=student, videoID=videoID)

    # 判断是否完成测试
    # isComplete = Answer.objects.filter(homeWorkID=video.homework.homeWorkID, studentID=student).first()
    isComplete = video.homework.answer_set.all().filter(studentID=student).first()
    # print(isComplete.score.score, video.homework.homeWorkID)
    return render(request, 'student/videoDetail.html', locals())


@csrf_exempt
def submitVideo(request):
    videoComment = request.POST.get("videoComment")
    videoID = request.POST.get("videoID")
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    video = Video.objects.filter(videoID=videoID).first()

    # print(student.username, video.videoID)
    VideoComment.objects.create(student=student, content=videoComment, Video=video)
    # return redirect("/student/videoDetail?videoID=" + videoID)
    name = username
    if student.studentinfo.name:
        name = student.studentinfo.name
    data = {
        "success": "success",
        "name": name
    }
    student.studentinfo.interactive += 1
    student.studentinfo.save()
    return JsonResponse(data)


def VideoLookNum(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    video.lookNum += 1
    video.save()



    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    time = GetTime().getTime()
    learningBehavior = LearningBehavior.objects.filter(stu=student, loginTime__contains=time).first()
    learningBehavior.courseDay = 1
    learningBehavior.save()
    VideoHistory.objects.create(student=student, video=video)
    return HttpResponse("success")


def VideoCollectNum(request):
    videoID = request.GET.get('videoID')
    video = Video.objects.filter(videoID=videoID).first()
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    video.collectNum.add(student)
    if video and student:
        video.collectNum.add(student)
        student.studentinfo.collectNum += 1
        student.studentinfo.save()
        return HttpResponse("success")
    else:
        return HttpResponse("fail")


def VideoCollectNumCancel(request):
    videoID = request.GET.get('videoID')
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    student.video_set.remove(videoID)
    student.studentinfo.collectNum -= 1
    student.studentinfo.save()
    return HttpResponse("success")


def community(request):
    page = int(request.GET.get("page", 1))
    searchContent = request.GET.get("searchContent", '').strip()
    username = request.session.get("username")
    if searchContent:
        articleList = Article.objects.filter(Q(title__contains=searchContent) | Q(content__contains=searchContent)).order_by("-dateTime")
    else:
        articleList = Article.objects.all().order_by("-dateTime")

    paginator = Paginator(articleList, 4)

    articleList = paginator.page(page)
    return render(request, 'student/community.html', locals())


def article(request):
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    articleID = request.GET.get("articleID")
    article = Article.objects.filter(articleID=articleID).first()
    article.readNum += 1
    article.save()
    articleCommentList = article.articlecomment_set.all().order_by("-dateTime")
    return render(request, 'student/article.html', locals())


@csrf_exempt
def editArticle(request):
    if request.method == "GET":
        return render(request, 'student/editArticle.html', locals())
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        username = request.session.get("username")
        student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
        Article.objects.create(title=title, content=content, student=student)
        student.studentinfo.createNum += 1
        student.studentinfo.save()
        return redirect("student:community")


@csrf_exempt
def articleCommentSubmit(request):
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    articleComment = request.POST.get("articleComment")
    articleID = request.POST.get("articleID")
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    article = Article.objects.filter(articleID=articleID).first()
    ArticleComment.objects.create(student=student, content=articleComment, article=article)
    name = username
    if student.studentinfo.name:
        name = student.studentinfo.name
    data = {
        "success": "success",
        "name": name
    }
    student.studentinfo.interactive += 1
    student.studentinfo.save()
    return JsonResponse(data)


def personal(request):
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    return render(request, 'student/personal.html', locals())


@csrf_exempt
def editPersonalInfo(request):
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    # print(student)
    if request.method == "GET":
        return render(request, 'student/editPersonalInfo.html', locals())
    elif request.method == "POST":
        name = request.POST.get("name")
        nickname = request.POST.get("nickname")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        student.studentinfo.name = name
        student.studentinfo.nickname = nickname
        student.studentinfo.age = age
        student.studentinfo.sex = sex
        student.studentinfo.save()
        return redirect("student:personal")


@csrf_exempt
def editAvatar(request):
    if request.method == "POST":
        # 1.获取上传的图片文件
        imgfile = request.FILES.get('photo')
        size = imgfile.size  # 文件大小    做文件上传大小限制
        content_type = imgfile.content_type  # 文件类型  做文件上传类型限制
        name = imgfile.name  # 文件名称
        username = request.session.get("username")
        student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
        student.studentinfo.avatar = imgfile
        student.studentinfo.save()
        return HttpResponse("success")


def courseCollectS(request):
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    collectList = Video.objects.filter(collectNum=student)
    return render(request, 'student/courseCollectS.html', locals())


def WatchTheHistory(request):
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    historyList = VideoHistory.objects.filter(student=student)
    return render(request, 'student/WatchTheHistory.html', locals())


def assignments(request):

    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    return render(request, 'student/assignments.html', locals())


@csrf_exempt
def test(request):
    if request.method == "GET":
        testID = request.GET.get("testID")
        videoID = request.GET.get("videoID")
        homeWork = HomeWork.objects.filter(homeWorkID=testID).first()
        template = homeWork.content.replace('{homeWorkID}', str(homeWork.homeWorkID))
        template = template.replace('{videoID}', str(videoID))
        return HttpResponse(template)
    if request.method == "POST":
        content = request.POST.get("content")
        homeWorkID = request.POST.get("homeWorkID")
        videoID = request.POST.get("videoID")
        username = request.session.get("username")
        student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
        if not student:
            return redirect("student:test")
        Answer.objects.get_or_create(content=content, homeWorkID_id=homeWorkID, studentID=student)
        return redirect("/student/videoDetail?videoID={}".format(videoID))


def abilityToLearn(request):
    username = request.session.get("username")
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

    result = Score.objects.values('studentID').annotate(avg=Avg('score'))
    avgList = [[Student.objects.filter(studentID=i['studentID']).first().studentinfo.name if Student.objects.filter(studentID=i['studentID']).first().studentinfo.name else Student.objects.filter(studentID=i['studentID']).first().username, i['avg']] for i in result]
    avgList.sort(key=lambda x: x[0])
    # print(result, avgList)
    return render(request, 'student/abilityToLearn.html', locals())


def getGenderCount(request):
    male = StudentInfo.objects.filter(sex='男').values_list('sex')
    female = StudentInfo.objects.filter(sex='女').values_list('sex')
    data = {
        'male': len(male),
        'female': len(female),
        'percent1': '{:.2%}'.format(len(male) / (len(male) + len(female))),
        'percent2': '{:.2%}'.format(len(female) / (len(male) + len(female)))
    }
    return JsonResponse(data)


def getCourseScore(request):
    username = request.session.get("username")
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
    username = request.session.get("username")
    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
    result = LearningBehavior.objects.filter(stu=student).order_by('loginTime')
    if result.count() >= 10:
        result = result[:10]
    data = {
        'label': [i[0].split(" ")[0].split("-", 1)[1] for i in result.values_list('loginTime')],
        'click': [i[0] for i in result.values_list('clickNum')],
    }
    # print(data)
    return JsonResponse(data)


def getMain2(request):
    username = request.session.get("username")
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
        enthusiasm = round(student.studentinfo.collectNum/videoNum, 2)
    # 影响力
    if createList[lastIndex].get('createNum') - createList[0].get('createNum') == 0:
        influence = 0
    else:
        influence = round((student.studentinfo.createNum - createList[0].get('createNum')) / (createList[lastIndex].get('createNum') - createList[0].get('createNum')), 2)
    # 规律性
    if videoNum == 0:
        regularity = 0
    else:
        regularity = round(student.studentinfo.interactive / (videoNum + createNum), 2)
        if (regularity) >= 1:
            regularity = 1
    # 达标率
    SuccessRate = round(scoreAvg/100, 2)
    data = {
        'participation': participation,
        'enthusiasm': enthusiasm,
        'influence': influence,
        'regularity': regularity,
        'SuccessRate': SuccessRate,
    }
    return JsonResponse(data)


def liveList(request):
    liveList = StartLive.objects.filter(status=1)
    return render(request, 'student/liveList.html', locals())


def intoLive(request):
    username = request.GET.get("teacher")
    teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
    if teacher.startlive.status == 0:
        return redirect("student:liveList")

    return render(request, 'student/living.html', locals())


def share(request):

    return None