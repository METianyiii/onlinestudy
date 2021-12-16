from django.urls import path

from app.student import views

urlpatterns = [
    path('index/', views.index, name='index'),  # 主页
    path('course/', views.course, name='course'),  # 课程
    path('videoDetail/', views.videoDetail, name='videoDetail'),  # 课程详情
    path('submitVideo/', views.submitVideo, name='submitVideo'),  # 课程评论
    path('VideoLookNum/', views.VideoLookNum, name='VideoLookNum'),  # 计算课程观看数
    path('VideoCollectNum/', views.VideoCollectNum, name='VideoCollectNum'),  # 计算课程收藏数
    path('VideoCollectNumCancel/', views.VideoCollectNumCancel, name='VideoCollectNumCancel'),  # 取消藏数
    path('community/', views.community, name='community'),  # 社区
    path('article/', views.article, name='article'),  # 文章
    path('articleCommentSubmit/', views.articleCommentSubmit, name='articleCommentSubmit'),  # 文章评论
    path('editArticle/', views.editArticle, name='editArticle'),  # 文章编辑
    path('personal/', views.personal, name='personal'),  # 个人中心
    path('editPersonalInfo/', views.editPersonalInfo, name='editPersonalInfo'),  # 个人信息修改
    path('editAvatar/', views.editAvatar, name='editAvatar'),  # 个人信息修改
    path('courseCollectS/', views.courseCollectS, name='courseCollectS'),  # 课程收藏
    path('WatchTheHistory/', views.WatchTheHistory, name='WatchTheHistory'),  # 课程记录
    # path('recordHistory/', views.recordHistory, name='recordHistory'),  # 添加课程记录

    path('assignments/', views.assignments, name='assignments'),  # 随堂作业
    path('test/', views.test, name='test'),  # 随堂作业
    path('abilityToLearn/', views.abilityToLearn, name='abilityToLearn'),  #
    path('getGenderCount/', views.getGenderCount, name='getGenderCount'),  #
    path('getCourseScore/', views.getCourseScore, name='getCourseScore'),  #
    path('getClick/', views.getClick, name='getClick'),  #
    path('getMain2/', views.getMain2, name='getMain2'),  #

    path('liveList/', views.liveList, name='liveList'),  # 直播
    path('intoLive/', views.intoLive, name='intoLive'),  # 直播


    path('share/', views.share, name='share'),  # 直播



]
