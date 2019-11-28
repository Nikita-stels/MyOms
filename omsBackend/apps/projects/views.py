# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from projects.models import Project, ProjectComment, ProjectEnclosure, ProjectType, BugManager, TestManager, \
    DemandManager, DemandEnclosure, ProjectComplete
from projects.serializers import (ProjectSerializer,
                                  ProjectCommentSerializer,
                                  ProjectEnclosureSerializer,
                                  ProjectTypeSerializer,
                                  BugManagerSerializer,
                                  TestManagerSerializer,
                                  DemandManagerSerializer,
                                  DemandEnclosureSerializer,
                                  ProjectCompleteSerializer)
from projects.filters import ProjectFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from projects.filters import ProjectFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('status', '-create_time')
    serializer_class = ProjectSerializer
    filter_backends = (ProjectFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ProjectFilter
    search_fields = ['pid', 'name', 'content', 'type__name']
    ordering_fields = ['level', 'task_complete', 'test_complete', 'create_time', 'update_time']


class ProjectCompleteViewSet(viewsets.ModelViewSet):
    queryset = ProjectComplete.objects.all().order_by('complete')
    serializer_class = ProjectCompleteSerializer
    filter_fields = ['project__id', 'user__username']


class ProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectComment.objects.all().order_by('create_time')
    serializer_class = ProjectCommentSerializer
    filter_fields = ['project__id']


class ProjectEnclosureViewSet(viewsets.ModelViewSet):
    queryset = ProjectEnclosure.objects.all()
    serializer_class = ProjectEnclosureSerializer
    filter_fields = ['project__id']


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class BugManagerViewSet(viewsets.ModelViewSet):
    queryset = BugManager.objects.all().order_by('create_time')
    serializer_class = BugManagerSerializer
    filter_fields = ['id', 'status', 'project__id', 'test_id']
    search_fields = ['name', 'project__pid']


class TestManagerViewSet(viewsets.ModelViewSet):
    queryset = TestManager.objects.all().order_by('create_time')
    serializer_class = TestManagerSerializer
    filter_fields = ['id', 'status', 'project__id', 'project__pid']
    search_fields = ['name', 'project__pid']


class DemandManagerViewSet(viewsets.ModelViewSet):
    queryset = DemandManager.objects.all().order_by('status', '-create_time')
    serializer_class = DemandManagerSerializer
    search_fields = ['name', 'content']
    ordering_fields = ['status', 'create_time']
    filter_fields = ['pid', 'status', 'create_user__username']


class DemandEnclosureViewSet(viewsets.ModelViewSet):
    queryset = DemandEnclosure.objects.all()
    serializer_class = DemandEnclosureSerializer
    filter_fields = ['project__id']