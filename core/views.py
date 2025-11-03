from django.shortcuts import render
from django.db.models import Q

from lists.models import List

LIST_PREVIEW_MAX_COUNT = 20


def get_list_previews(user, limit=3, max_rows=LIST_PREVIEW_MAX_COUNT):
    previews = (
            List.objects.filter(Q(owner=user) | Q(contributors=user))
            .distinct()
            .order_by('-date_updated')[:limit]
    )
    return map(lambda p:
               {
                   'id': p.id,
                   'name': p.name,
                   'serialized': p.serialize_rows()[:max_rows]
                },
               previews)


def index(request):
    previews = []
    if request.user.is_authenticated:
        previews = get_list_previews(request.user)
    return render(request, 'core/index.html', {'previews': previews})
