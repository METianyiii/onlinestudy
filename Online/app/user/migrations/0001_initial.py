# Generated by Django 2.0 on 2021-08-26 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answerID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('content', models.TextField(verbose_name='答案')),
            ],
            options={
                'verbose_name': '学生提交作业',
                'db_table': 'Answer',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('articleID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(max_length=150, verbose_name='文章标题')),
                ('content', models.TextField(max_length=10000, verbose_name='文章内容')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='日期时间')),
                ('praiseNum', models.IntegerField(default=0, verbose_name='赞数')),
                ('commentNum', models.IntegerField(default=0, verbose_name='评论数')),
                ('readNum', models.IntegerField(default=0, verbose_name='阅读数')),
            ],
            options={
                'verbose_name': '社区文章表',
                'db_table': 'Article',
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('ArticleCommentID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('content', models.TextField(max_length=1000, verbose_name='评论')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='日期时间')),
                ('praiseNum', models.IntegerField(default=0, verbose_name='赞数')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Article', verbose_name='文章')),
            ],
            options={
                'verbose_name': '社区文章评论',
                'db_table': 'ArticleComment',
            },
        ),
        migrations.CreateModel(
            name='ArticleCommentReply',
            fields=[
                ('ArticleCommenReplytID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('content', models.TextField(max_length=1000, verbose_name='评论')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='日期时间')),
                ('praiseNum', models.IntegerField(default=0, verbose_name='赞数')),
                ('articleComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ArticleComment', verbose_name='文章评论')),
            ],
            options={
                'verbose_name': '社区文章评论回复',
                'db_table': 'ArticleCommentReply',
            },
        ),
        migrations.CreateModel(
            name='HomeWork',
            fields=[
                ('homeWorkID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(default='', max_length=100, verbose_name='试题名称')),
                ('fileName', models.CharField(default='', max_length=100, verbose_name='试题文件名称')),
                ('content', models.TextField(verbose_name='试题内容')),
            ],
            options={
                'verbose_name': '随堂作业',
                'db_table': 'HomeWork',
            },
        ),
        migrations.CreateModel(
            name='LearningBehavior',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('remoteID', models.CharField(max_length=30, verbose_name='IP')),
                ('loginTime', models.CharField(max_length=40, verbose_name='登陆时间')),
                ('clickNum', models.IntegerField(default=0, verbose_name='当天点击量')),
                ('courseDay', models.IntegerField(default=0, verbose_name='当天是否学习课程')),
            ],
            options={
                'verbose_name': '行为数据',
                'db_table': 'LearningBehavior',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('ScoreID', models.AutoField(primary_key=True, serialize=False)),
                ('homeWorkID', models.IntegerField(verbose_name='测试ID')),
                ('studentID', models.IntegerField(verbose_name='学生ID')),
                ('score', models.IntegerField(verbose_name='分数')),
                ('teacherID', models.IntegerField(verbose_name='教师ID')),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.Answer', verbose_name='学生答案')),
            ],
            options={
                'verbose_name': '学生测试成绩',
                'db_table': 'Score',
            },
        ),
        migrations.CreateModel(
            name='StartLive',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'StartLive',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('email', models.CharField(max_length=20, unique=True, verbose_name='邮箱')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
            ],
            options={
                'verbose_name': '学生表',
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('studentInfoID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(default='', max_length=10, verbose_name='名字')),
                ('nickname', models.CharField(default='', max_length=10, verbose_name='昵称')),
                ('sex', models.CharField(default='', max_length=2, verbose_name='性别')),
                ('age', models.IntegerField(default=0, verbose_name='年龄')),
                ('collectNum', models.IntegerField(default=0, verbose_name='收藏数')),
                ('createNum', models.IntegerField(default=0, verbose_name='原创数')),
                ('interactive', models.IntegerField(default=0, verbose_name='互动数')),
                ('avatar', models.ImageField(default='avatar/头像.png', upload_to='avatar', verbose_name='头像')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.Student', verbose_name='学生')),
            ],
            options={
                'verbose_name': '学生信息表',
                'db_table': 'StudentInfo',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('email', models.CharField(max_length=20, unique=True, verbose_name='邮箱')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('name', models.CharField(default='', max_length=10, verbose_name='名字')),
                ('nickname', models.CharField(default='', max_length=10, verbose_name='昵称')),
                ('sex', models.CharField(default='', max_length=2, verbose_name='性别')),
                ('age', models.IntegerField(default=0, verbose_name='年龄')),
                ('collectNum', models.IntegerField(default=0, verbose_name='收藏数')),
                ('avatar', models.ImageField(default='头像.png', upload_to='avatar', verbose_name='头像')),
            ],
            options={
                'verbose_name': '教师表',
                'db_table': 'Teacher',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('videoID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(max_length=200, verbose_name='名字/题目')),
                ('produce', models.TextField(max_length=500, verbose_name='视频介绍')),
                ('interfacePath', models.CharField(max_length=200, verbose_name='界面路径')),
                ('path', models.CharField(max_length=200, verbose_name='视频路径')),
                ('praiseNum', models.IntegerField(default=0, verbose_name='赞数')),
                ('lookNum', models.IntegerField(default=0, verbose_name='观看数')),
                ('commentNum', models.IntegerField(default=0, verbose_name='评论数')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to='user.Teacher', verbose_name='上传者')),
                ('collectNum', models.ManyToManyField(to='user.Student', verbose_name='收藏(学生)')),
                ('teacherCollect', models.ManyToManyField(to='user.Teacher', verbose_name='收藏(教师)')),
            ],
            options={
                'verbose_name': '课程表',
                'db_table': 'Video',
            },
        ),
        migrations.CreateModel(
            name='VideoComment',
            fields=[
                ('VideoCommentID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('content', models.TextField(max_length=1000, verbose_name='评论')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='日期时间')),
                ('praiseNum', models.IntegerField(default=0, verbose_name='赞数')),
                ('Video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Video', verbose_name='课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student', verbose_name='学生')),
            ],
            options={
                'verbose_name': '课程评论',
                'db_table': 'VideoComment',
            },
        ),
        migrations.CreateModel(
            name='VideoCommentAnswer',
            fields=[
                ('VideoCommentAnswerID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('content', models.TextField(max_length=1000, verbose_name='评论')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='日期时间')),
                ('praiseNum', models.IntegerField(default=0, verbose_name='赞数')),
                ('VComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.VideoComment', verbose_name='课程评论')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher', verbose_name='教师')),
            ],
            options={
                'verbose_name': '课程评论回复',
                'db_table': 'VideoCommentAnswer',
            },
        ),
        migrations.CreateModel(
            name='VideoHistory',
            fields=[
                ('VideoHistoryID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='观看时间')),
                ('Period', models.CharField(default='0', max_length=20, verbose_name='视频时间点')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student', verbose_name='学生')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Video', verbose_name='课程')),
            ],
            options={
                'verbose_name': '学习浏览记录',
                'db_table': 'VideoHistory',
            },
        ),
        migrations.CreateModel(
            name='VideoHistoryTeacher',
            fields=[
                ('VideoHistoryID', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('dateTime', models.DateTimeField(auto_now_add=True, verbose_name='观看时间')),
                ('Period', models.CharField(default='0', max_length=20, verbose_name='视频时间点')),
                ('Teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher', verbose_name='教师')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Video', verbose_name='课程')),
            ],
            options={
                'verbose_name': '教师浏览记录',
                'db_table': 'VideoHistoryTeacher',
            },
        ),
        migrations.AddField(
            model_name='startlive',
            name='tea',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher'),
        ),
        migrations.AddField(
            model_name='learningbehavior',
            name='stu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student'),
        ),
        migrations.AddField(
            model_name='homework',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher', verbose_name='上传者'),
        ),
        migrations.AddField(
            model_name='homework',
            name='video',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.Video', verbose_name='指定课程'),
        ),
        migrations.AddField(
            model_name='articlecommentreply',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher', verbose_name='教师'),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student', verbose_name='学生'),
        ),
        migrations.AddField(
            model_name='article',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student', verbose_name='学生'),
        ),
        migrations.AddField(
            model_name='answer',
            name='homeWorkID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.HomeWork', verbose_name='测试题'),
        ),
        migrations.AddField(
            model_name='answer',
            name='studentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student', verbose_name='答题学生'),
        ),
    ]
