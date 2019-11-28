# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from hosts.models import Host
from users.models import User
from tools.models import Upload

DEPLOY_STATUS = {
    "deploy": "发布中",
    "success": "发布成功",
    "failed": "发布失败"
}

admin_groups = ['admin', 'OMS_Super_Admin']
sql_admin_groups = ['admin', 'OMS_Super_Admin', 'OMS_Dev_Manager']


class Jobs(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=u'名称')
    version = models.CharField(max_length=20, default='HEAD', verbose_name=u'版本号')
    content = models.TextField(null=True, blank=True, verbose_name=u'更新内容')
    code_url = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'代码地址')
    deploy_path = models.CharField(max_length=250, null=True, blank=True, verbose_name=u'发布路径')
    cur_step = models.IntegerField(default=0, verbose_name=u'当前步骤')
    total_step = models.IntegerField(default=0, verbose_name=u'总步骤')
    showdev = models.BooleanField(default=False, verbose_name=u'研发可见')
    done = models.BooleanField(default=False, verbose_name=u'完成')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目或任务'
        verbose_name_plural = u'项目或任务'

    def save(self, *args, **kwargs):
        envs = Deployenv.objects.filter(job=self.id)
        self.total_step = len(envs)
        super(Jobs, self).save(*args, **kwargs)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        groups = User.objects.get(username=request.user).groups.all()
        admin_list = [group.name for group in groups]

        # 求交集
        is_admin = [i for i in admin_list if i in admin_groups]
        print(is_admin)
        if len(is_admin) > 0 or self.showdev:
            return True
        else:
            return False

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return True

    @staticmethod
    def has_update_permission(request):
        return True

    def has_object_update_permission(self, request):
        return True


class Deployenv(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'发布任务')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    level = models.IntegerField(default=1, verbose_name=u'顺序')
    deploy_hosts = models.ManyToManyField(Host, blank=True, verbose_name=u'发布主机')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'发布环境'
        verbose_name_plural = u'发布环境'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Deployenv, self).save(*args, **kwargs)


class Deploycmd(models.Model):
    env = models.ForeignKey(Deployenv, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'发布环境')
    name = models.CharField(max_length=20, verbose_name=u'名称')
    deploy_cmd = models.TextField(null=True, blank=True, verbose_name=u'发布命令')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'发布命令'
        verbose_name_plural = u'发布命令'


class DeployJobs(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'发布任务', related_name='deploy_job')
    j_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'任务ID')
    deploy_status = models.CharField(choices=tuple(DEPLOY_STATUS.items()), default="deploy", max_length=10,
                                     verbose_name=u'发布状态')
    deploy_hosts = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'发布主机')
    deploy_cmd_host = models.CharField(max_length=100, default='null', verbose_name=u'命令目标主机')
    env = models.CharField(max_length=10, verbose_name=u'发布环境')
    deploy_path = models.CharField(max_length=250, null=True, blank=True, verbose_name=u'发布路径')
    version = models.CharField(max_length=20, default='HEAD', verbose_name=u'版本号')
    content = models.TextField(verbose_name=u'更新内容')
    deploy_cmd = models.TextField(verbose_name=u'发布命令')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'操作人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.j_id

    class Meta:
        verbose_name = u'执行发布'
        verbose_name_plural = u'执行发布'


class DeployResults(models.Model):
    deployjob = models.ForeignKey(DeployJobs, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'发布任务', related_name='deployjob')
    result = models.TextField(null=True, blank=True, verbose_name=u'发布结果')

    class Meta:
        verbose_name = u'发布结果'
        verbose_name_plural = u'发布结果'


Status = {
    0: '待审核',
    1: '待上线',
    2: '未通过',
    3: '已上线',
}


class DeployTicket(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    version = models.TextField(default='HEAD', verbose_name=u'项目版本')
    content = models.TextField(verbose_name=u'上线内容')
    desc = models.TextField(null=True, blank=True, verbose_name=u'发布说明')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deployticket_create_user', verbose_name=u'创建者')
    status = models.CharField(max_length=3, choices=tuple(Status.items()), default=0, verbose_name=u'状态')
    skype_to = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'通知人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'上线工单'
        verbose_name_plural = u'上线工单'


class DeployTicketEnclosure(models.Model):
    ticket = models.ForeignKey(DeployTicket, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单')
    file = models.ForeignKey(Upload, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'工单附件'
        verbose_name_plural = u'工单附件'


SqlStatus = {
    0: '未执行',
    1: '已执行'
}


class SqlTicket(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    dbname = models.CharField(max_length=100, verbose_name=u'db')
    content = models.TextField(verbose_name=u'sql语句')
    desc = models.TextField(verbose_name=u'说明')
    status = models.CharField(max_length=3, choices=tuple(SqlStatus.items()), default=0, verbose_name=u'状态')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sqlticket_create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sqlticket_action_user', verbose_name=u'执行者')
    env = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'执行环境')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'sql工单'
        verbose_name_plural = u'sql工单'
