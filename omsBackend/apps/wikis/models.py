# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from apps.users.models import User, Group
from apps.worktickets.models import TicketType

admin_groups = ['admin', 'OMS_Super_Admin']


class Wiki(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'类型')
    content = models.TextField(verbose_name=u'内容')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'wiki'
        verbose_name_plural = u'wiki'