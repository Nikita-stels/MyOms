# -*- coding: utf-8 -*-
# author: huashaw

from rest_framework import viewsets
from apps.perms.models import UserMenuPerms, UserHostPerms, UserWikiPerms
from apps.perms.serializers import UserMenuPermsSerializer, UserHostPermsSerializer, UserWikiPermsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.users.models import User, Group
from apps.users.serializers import UserSerializer, RoleSerializer, GroupSerializer
from apps.perms.filters import UserMenuPermsFilter


class UserMenuPermsViewSet(viewsets.ModelViewSet):
    queryset = UserMenuPerms.objects.all()
    serializer_class = UserMenuPermsSerializer
    filter_class = UserMenuPermsFilter


@api_view()
def routers(request):
    username = request.GET['username']
    userqueryset = User.objects.get(username=username)
    userserializer = UserSerializer(userqueryset, context={'request': request}).data
    groups = userserializer['groups']
    menus = []
    elements = []
    for group in groups:
        try:
            menuqueryset = UserMenuPerms.objects.get(group=group)
            menuserializer = UserMenuPermsSerializer(menuqueryset, context={'request': request}).data
            menus = menuserializer["firstmenus"] + menuserializer["secondmenus"] + menus
            elements = menuserializer["elements"] + elements
        except Exception as e:
            pass
    menus = set(menus)
    elements = set(elements)
    return Response({"groups": groups, "menus": menus, "elements": elements})


class UserHostPermsViewSet(viewsets.ModelViewSet):
    queryset = UserHostPerms.objects.all().order_by('id')
    serializer_class = UserHostPermsSerializer


class UserWikiPermsViewSet(viewsets.ModelViewSet):
    queryset = UserWikiPerms.objects.all().order_by('id')
    serializer_class = UserWikiPermsSerializer