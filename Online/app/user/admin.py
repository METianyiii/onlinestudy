
from django.contrib import admin

from app.user.models import Student, StudentInfo, Teacher, Video, HomeWork, Answer, Score, VideoHistory, \
    VideoHistoryTeacher, VideoComment, VideoCommentAnswer, Article, ArticleComment, ArticleCommentReply

admin.site.site_header = '塞科学习平台管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '塞科学习平台管理'


class StudentXadmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    show_bookmarks = False
    list_display = ('studentID', 'username', 'email', 'password')
    list_filter = ('username', 'email', 'password')
    list_editable = ('username', 'email', 'password')
    search_fields = ('name',)

class StudentInfoXadmin(admin.ModelAdmin):
    list_display = ('studentInfoID', 'name', 'nickname', 'sex', 'age', 'collectNum', 'avatar', 'student')
    list_filter = ('name', 'nickname', 'sex', 'age', 'collectNum', 'avatar', 'student')
    list_editable = ('name', 'nickname', 'sex', 'age', 'collectNum', 'avatar', 'student')
    search_fields = ('name',)
    #list_display_links = ('name',)
    show_bookmarks = False



class TeacherXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('studentID', 'username', 'email', 'password', 'name', 'nickname', 'sex', 'age', 'collectNum', 'avatar')
    list_editable = ('username', 'email', 'password', 'name', 'nickname', 'sex', 'age', 'collectNum', 'avatar')
    search_fields = ('name',)


class VideoXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('videoID', 'name', 'produce', 'interfacePath', 'path', 'praiseNum', 'lookNum', 'commentNum', 'author')
    list_editable = ('name', 'produce', 'interfacePath', 'path', 'praiseNum', 'lookNum', 'commentNum', 'author')
    search_fields = ('name',)
    # raw_id_fields = ('author',)
    filter_horizontal = ('collectNum',)
    filter_vertical = ('collectNum',)


class HomeWorkXadmin(admin.ModelAdmin):
    list_display = ('homeWorkID', 'name', 'fileName', 'content', 'author', 'video')
    list_editable = ('name', 'fileName', 'content', 'author', 'video')
    search_fields = ('name',)


class AnswerXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('answerID', 'content', 'homeWorkID', 'studentID')
    list_editable = ('content', 'homeWorkID', 'studentID')
    search_fields = ('content',)


class ScoreXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('ScoreID', 'homeWorkID', 'studentID', 'score', 'teacherID', 'answer')
    list_editable = ('homeWorkID', 'studentID', 'score', 'teacherID', 'answer')
    search_fields = ('homeWorkID',)


class VideoHistoryXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('VideoHistoryID', 'Period', 'student', 'video')
    list_editable = ('Period', 'student', 'video')
    # search_fields = ('homeWorkID',)


class VideoHistoryTeacherXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('VideoHistoryID', 'Period', 'video', 'Teacher')
    list_editable = ('Period', 'video', 'Teacher')


class VideoCommentXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('VideoCommentID', 'content', 'praiseNum', 'student', 'Video')
    list_editable = ('content', 'praiseNum', 'student', 'Video')
    search_fields = ('content',)


class VideoCommentAnswerXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('VideoCommentAnswerID', 'content', 'praiseNum', 'teacher', 'VComment')
    list_editable = ('content', 'praiseNum', 'teacher', 'VComment')
    search_fields = ('content',)


class ArticleXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('articleID', 'title', 'content', 'praiseNum', 'commentNum', 'readNum', 'student')
    list_editable = ('title', 'content', 'praiseNum', 'commentNum', 'readNum', 'student')
    search_fields = ('title',)


class ArticleCommentXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('ArticleCommentID', 'content', 'praiseNum', 'student', 'article')
    list_editable = ('content', 'praiseNum', 'student', 'article')
    search_fields = ('content',)


class ArticleCommentReplyXadmin(admin.ModelAdmin):
    show_bookmarks = False
    list_display = ('ArticleCommenReplytID', 'content', 'praiseNum', 'teacher', 'articleComment')
    list_editable = ('content', 'praiseNum', 'teacher', 'articleComment')
    search_fields = ('content',)


admin.site.register(Student, StudentXadmin)
admin.site.register(StudentInfo, StudentInfoXadmin)
admin.site.register(Teacher, TeacherXadmin)
admin.site.register(Video, VideoXadmin)
admin.site.register(HomeWork, HomeWorkXadmin)
admin.site.register(Answer, AnswerXadmin)
admin.site.register(Score, ScoreXadmin)
admin.site.register(VideoHistory, VideoHistoryXadmin)
admin.site.register(VideoHistoryTeacher, VideoHistoryTeacherXadmin)
admin.site.register(VideoComment, VideoCommentXadmin)
admin.site.register(VideoCommentAnswer, VideoCommentAnswerXadmin)
admin.site.register(Article, ArticleXadmin)
admin.site.register(ArticleComment, ArticleCommentXadmin)
admin.site.register(ArticleCommentReply, ArticleCommentReplyXadmin)