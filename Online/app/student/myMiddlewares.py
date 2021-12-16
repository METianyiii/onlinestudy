from django.db.models import Q
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from app.teacher.utils import GetTime
from app.user.models import LearningBehavior, Student


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path

        if path.startswith('/student/'):
            user = request.session.get("username", None)
            if user:
                student = Student.objects.filter(Q(username=user) | Q(email=user)).first()
                time = GetTime().getTime()
                urlList = ['videoDetail', 'submitVideo', 'VideoCollectNum', 'article', 'articleCommentSubmit', 'editArticle', 'assignments', 'videoDetail', 'videoDetail', ]
                if path.split('/')[2] in urlList:
                    learningBehavior = LearningBehavior.objects.filter(stu=student, loginTime__contains=time).first()
                    if learningBehavior:
                        learningBehavior.clickNum += 1
                        learningBehavior.save()
                    else:
                        LearningBehavior.objects.create(remoteID=request.META['REMOTE_ADDR'],
                                                        loginTime=time,
                                                        stu=student,
                                                        clickNum=1,
                                                        )


                pass
            else:
                return redirect("user:studentLogin")
        elif path.startswith('/teacher/'):
            if request.session.get("teacherUsername", None):
                pass
            else:
                return redirect("user:studentLogin")
        pass