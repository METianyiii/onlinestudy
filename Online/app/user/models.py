from django.db import models


class Student(models.Model):
    studentID = models.AutoField(primary_key=True, verbose_name="主键")
    username = models.CharField(max_length=20, unique=True, verbose_name="用户名")
    email = models.CharField(max_length=20, unique=True, verbose_name="邮箱")
    password = models.CharField(max_length=20, verbose_name="密码")

    class Meta:
        db_table = "Student"
        verbose_name = "学生表"


class StudentInfo(models.Model):
    studentInfoID = models.AutoField(primary_key=True, verbose_name="主键")
    name = models.CharField(max_length=10, verbose_name="名字", default='')
    nickname = models.CharField(max_length=10, verbose_name="昵称", default='')
    sex = models.CharField(max_length=2, verbose_name="性别", default='男')
    age = models.IntegerField(verbose_name="年龄", default=0)
    collectNum = models.IntegerField(verbose_name="收藏数", default=0)
    createNum = models.IntegerField(verbose_name="原创数", default=0)
    interactive = models.IntegerField(verbose_name="互动数", default=0)
    avatar = models.ImageField(upload_to='avatar', default="avatar/头像.png", verbose_name="头像")
    student = models.OneToOneField(Student, on_delete=models.CASCADE, verbose_name="学生")

    class Meta:
        db_table = "StudentInfo"
        verbose_name = "学生信息表"


class Teacher(models.Model):
    studentID = models.AutoField(primary_key=True, verbose_name="主键")
    username = models.CharField(max_length=20, unique=True, verbose_name="用户名")
    email = models.CharField(max_length=20, unique=True, verbose_name="邮箱")
    password = models.CharField(max_length=20, verbose_name="密码")
    name = models.CharField(max_length=10, verbose_name="名字", default='')
    nickname = models.CharField(max_length=10, verbose_name="昵称", default='')
    sex = models.CharField(max_length=2, verbose_name="性别", default='')
    age = models.IntegerField(verbose_name="年龄", default=0)
    collectNum = models.IntegerField(verbose_name="收藏数", default=0)
    avatar = models.ImageField(upload_to='avatar', default="avatar/头像.png", verbose_name="头像")

    class Meta:
        db_table = "Teacher"
        verbose_name = "教师表"


class Video(models.Model):
    videoID = models.AutoField(primary_key=True, verbose_name="主键")
    name = models.CharField(max_length=200, verbose_name="名字/题目")
    produce = models.TextField(max_length=500, verbose_name="视频介绍")
    interfacePath = models.CharField(max_length=200, verbose_name="界面路径")
    path = models.CharField(max_length=200, verbose_name="视频路径")
    praiseNum = models.IntegerField(verbose_name="赞数", default=0)
    lookNum = models.IntegerField(verbose_name="观看数", default=0)
    commentNum = models.IntegerField(verbose_name="评论数", default=0)
    collectNum = models.ManyToManyField(Student, verbose_name="收藏(学生)")
    teacherCollect = models.ManyToManyField(Teacher, verbose_name="收藏(教师)")
    author = models.ForeignKey(Teacher, related_name='uploader', on_delete=models.CASCADE, verbose_name='上传者')

    class Meta:
        db_table = "Video"
        verbose_name = "课程表"


class HomeWork(models.Model):
    homeWorkID = models.AutoField(primary_key=True, verbose_name="主键")
    name = models.CharField(max_length=100, verbose_name="试题名称", default='')
    fileName = models.CharField(max_length=100, verbose_name="试题文件名称", default='')
    content = models.TextField(verbose_name="试题内容")
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='上传者')
    video = models.OneToOneField(Video, on_delete=models.CASCADE, verbose_name='指定课程')

    class Meta:
        db_table = "HomeWork"
        verbose_name = "随堂作业"


class Answer(models.Model):
    answerID = models.AutoField(primary_key=True, verbose_name="主键")
    content = models.TextField(verbose_name="答案")
    homeWorkID = models.ForeignKey(HomeWork, on_delete=models.CASCADE, verbose_name='测试题')
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='答题学生')

    class Meta:
        db_table = 'Answer'
        verbose_name = "学生提交作业"


class Score(models.Model):
    ScoreID = models.AutoField(primary_key=True)
    homeWorkID = models.IntegerField(verbose_name="测试ID")
    studentID = models.IntegerField(verbose_name="学生ID")
    score = models.IntegerField(verbose_name="分数")
    teacherID = models.IntegerField(verbose_name="教师ID")
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, verbose_name='学生答案')


    class Meta:
        db_table = "Score"
        verbose_name = "学生测试成绩"


class VideoHistory(models.Model):
    VideoHistoryID = models.AutoField(primary_key=True, verbose_name="主键")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="观看时间")
    Period = models.CharField(max_length=20, verbose_name="视频时间点", default="0")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        db_table = "VideoHistory"
        verbose_name = "学习浏览记录"


class VideoHistoryTeacher(models.Model):
    VideoHistoryID = models.AutoField(primary_key=True, verbose_name="主键")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="观看时间")
    Period = models.CharField(max_length=20, verbose_name="视频时间点", default="0")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="课程")
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="教师")

    class Meta:
        db_table = "VideoHistoryTeacher"
        verbose_name = "教师浏览记录"


class VideoComment(models.Model):
    VideoCommentID = models.AutoField(primary_key=True, verbose_name="主键")
    content = models.TextField(max_length=1000, verbose_name="评论")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")
    praiseNum = models.IntegerField(verbose_name="赞数", default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    Video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        db_table = 'VideoComment'
        verbose_name = "课程评论"


class VideoCommentAnswer(models.Model):
    VideoCommentAnswerID = models.AutoField(primary_key=True, verbose_name="主键")
    content = models.TextField(max_length=1000, verbose_name="评论")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")
    praiseNum = models.IntegerField(verbose_name="赞数", default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="教师")
    VComment = models.ForeignKey(VideoComment, on_delete=models.CASCADE, verbose_name="课程评论")

    class Meta:
        db_table = 'VideoCommentAnswer'
        verbose_name = "课程评论回复"


class Article(models.Model):
    articleID = models.AutoField(primary_key=True, verbose_name="主键")
    title = models.CharField(max_length=150, verbose_name="文章标题")
    content = models.TextField(max_length=10000, verbose_name="文章内容")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")
    praiseNum = models.IntegerField(verbose_name="赞数", default=0)
    commentNum = models.IntegerField(verbose_name="评论数", default=0)
    readNum = models.IntegerField(verbose_name="阅读数", default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")

    class Meta:
        db_table = 'Article'
        verbose_name = "社区文章表"


class ArticleComment(models.Model):
    ArticleCommentID = models.AutoField(primary_key=True, verbose_name="主键")
    content = models.TextField(max_length=1000, verbose_name="评论")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")
    praiseNum = models.IntegerField(verbose_name="赞数", default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")

    class Meta:
        db_table = "ArticleComment"
        verbose_name = "社区文章评论"


class ArticleCommentReply(models.Model):
    ArticleCommenReplytID = models.AutoField(primary_key=True, verbose_name="主键")
    content = models.TextField(max_length=1000, verbose_name="评论")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")
    praiseNum = models.IntegerField(verbose_name="赞数", default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="教师")
    articleComment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, verbose_name="文章评论")

    class Meta:
        db_table = "ArticleCommentReply"
        verbose_name = "社区文章评论回复"


class LearningBehavior(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="主键")
    remoteID = models.CharField(max_length=30, verbose_name="IP")
    loginTime = models.CharField(max_length=40, verbose_name="登陆时间")
    clickNum = models.IntegerField(default=0, verbose_name='当天点击量')
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    # videoCount = models.IntegerField(verbose_name="观看视频数", default=1)
    courseDay = models.IntegerField(verbose_name='当天是否学习课程', default=0)

    class Meta:
        db_table = "LearningBehavior"
        verbose_name = "行为数据"


class StartLive(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="主键")
    status = models.IntegerField(default=0)
    tea = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'StartLive'