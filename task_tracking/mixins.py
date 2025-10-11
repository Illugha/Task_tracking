from django.core.exceptions import PermissionDenied
from django.shortcuts import render

class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return render(request, 'tasks/403.html', status=403)
        return super().dispatch(request, *args, **kwargs)