# -*- coding: utf-8 -*-
# author: kiven

from apps.worktickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType
from rest_framework import serializers
from apps.users.models import User, Group
from apps.tools.models import Upload


class WorkTicketSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=TicketType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    edit_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', allow_null=True)
    create_group = serializers.SlugRelatedField(many=True, queryset=Group.objects.all(), slug_field='name',
                                                allow_null=True)

    class Meta:
        model = WorkTicket
        fields = (
            'url', 'id', 'pid', 'name', 'type', 'content', 'create_user', 'action_user', 'edit_user',
            'create_group', 'level', 'ticket_status', 'create_time', 'update_time')


class TicketCommentSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = TicketComment
        fields = ('url', 'id', 'ticket', 'content', 'create_user', 'create_time')


class TicketEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = TicketEnclosure
        fields = ('url', 'id', 'ticket', 'file', 'create_user', 'create_time')


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('url', 'id', 'name', 'desc')
