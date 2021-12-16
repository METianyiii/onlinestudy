from django.urls import path

from app.teacher import views

urlpatterns = [
    path('course/', views.course, name='course'),
    path('courseManage/', views.courseManage, name='courseManage'),
    path('myUploadcourseManage/', views.myUploadcourseManage, name='myUploadcourseManage'),
    path('uploadMp4/', views.uploadMp4, name='uploadMp4'),
    path('videoDetail/', views.videoDetail, name='videoDetail'),
    path('LiveMp4/', views.LiveMp4, name='LiveMp4'),
    path('reply/', views.reply, name='reply'),
    path('lookChooseVideoStudentInfo/', views.lookChooseVideoStudentInfo, name='lookChooseVideoStudentInfo'),
    path('lookStudentInfo/', views.lookStudentInfo, name='lookStudentInfo'),
    path('lookStudentAbility/', views.lookStudentAbility, name='lookStudentAbility'),
    path('checkHomeWorkResult/', views.checkHomeWorkResult, name='checkHomeWorkResult'),
    path('VideoLookNum/', views.VideoLookNum, name='VideoLookNum'),
    path('VideoCollectNum/', views.VideoCollectNum, name='VideoCollectNum'),
    path('VideoCollectNumCancel/', views.VideoCollectNumCancel, name='VideoCollectNumCancel'),
    path('deleteVideo/', views.deleteVideo, name='deleteVideo'),
    path('liveStreaming/', views.liveStreaming, name='liveStreaming'),
    path('startLive/', views.startLive, name='startLive'),
    path('community/', views.community, name='community'),
    # path('editArticle/', views.editArticle, name='editArticle'),
    path('personal/', views.personal, name='personal'),  # 个人中心
    path('editAvatar/', views.editAvatar, name='editAvatar'),  #
    path('editPersonalInfo/', views.editPersonalInfo, name='editPersonalInfo'),  #
    path('courseCollectS/', views.courseCollectS, name='courseCollectS'),  #
    path('WatchTheHistory/', views.WatchTheHistory, name='WatchTheHistory'),  #
    path('article/', views.article, name='article'),  #
    path('articleReply/', views.articleReply, name='articleReply'),  #


    path('getGenderCount/', views.getGenderCount, name='getGenderCount'),  #
    path('getCourseScore/', views.getCourseScore, name='getCourseScore'),  #
    path('getClick/', views.getClick, name='getClick'),  #
    path('getMain2/', views.getMain2, name='getMain2'),  #
]
