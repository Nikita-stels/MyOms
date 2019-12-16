# -*- coding: utf-8 -*-
# author: huashaw

from apps.hosts.models import Host, admin_groups
from apps.users.models import User, Group
from apps.perms.models import UserHostPerms
from dry_rest_permissions.generics import DRYPermissionFiltersBase


class ComputerRoomFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the create_groups.
        admin groups can get all().
        """
        groups = User.objects.get(username=request.user).groups.all()
        admin_list = [group.name for group in groups]

        # 求交集
        is_admin = [i for i in admin_list if i in admin_groups]
        if len(is_admin) > 0:
            return queryset
        else:
            # .distinct()去重
            print("not admin")
            objs = []
            for group in groups:
                try:
                    objperm = UserHostPerms.objects.get(usergroups__name=group.name).objs.all()
                    for obj in objperm:
                        objs.append(obj.hostname)
                except:
                    pass
            return queryset.filter(hostname__in=set(objs)).distinct()