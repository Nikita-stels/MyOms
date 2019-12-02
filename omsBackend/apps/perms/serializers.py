# -*- coding: utf-8 -*-
# author: huashaw

from rest_framework import serializers

from apps.perms.models import UserMenuPerms, UserHostPerms, UserWikiPerms
from apps.menus.models import Firstmenu, Secondmenu, Element
from apps.users.models import Group
from apps.hosts.models import Host
from apps.wikis.models import Wiki


class UserMenuPermsSerializer(serializers.ModelSerializer):
    firstmenus = serializers.SlugRelatedField(many=True, queryset=Firstmenu.objects.all(), slug_field='title',
                                              allow_null=True)
    secondmenus = serializers.SlugRelatedField(many=True, queryset=Secondmenu.objects.all(), slug_field='title',
                                               allow_null=True)
    elements = serializers.SlugRelatedField(many=True, queryset=Element.objects.all(), slug_field='name',
                                            allow_null=True)

    class Meta:
        model = UserMenuPerms
        fields = ('url', 'id', 'group', 'firstmenus', 'secondmenus', 'elements')


class UserHostPermsSerializer(serializers.ModelSerializer):
    usergroups = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name')
    objs = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = UserHostPerms
        fields = ('url', 'id', 'name', 'usergroups', 'objs')


class UserWikiPermsSerializer(serializers.ModelSerializer):
    usergroups = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name')
    objs = serializers.SlugRelatedField(many=True, queryset=Wiki.objects.all(), slug_field='title')

    class Meta:
        model = UserWikiPerms
        fields = ('url', 'id', 'name', 'usergroups', 'objs')