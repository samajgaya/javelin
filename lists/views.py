from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone

from .models import List, MediaListRow
from .forms import ListForm, MediaListRowForm


@login_required
def create_list(request):
    form = ListForm(request.POST or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            lst = form.save(commit=False)
            lst.owner = request.user
            lst.save()
            form.save_m2m()
            lst.contributors.add(request.user)
            return redirect('index')
    return render(request, 'lists/create_list.html', {'form': form})


@login_required
def list_dash(request, listid):
    lst = get_object_or_404(List, pk=listid)

    if request.method == 'POST':
        add_row_form = MediaListRowForm(request.POST)
        if add_row_form.is_valid():
            row = add_row_form.save(commit=False)
            row.appears_in = lst
            row.added_by = request.user
            row.save()
            return redirect('list_dash', listid=listid)
    else:
        add_row_form = MediaListRowForm()

    rows = lst.serialize_rows()
    ctx = {
        'list_name': lst.name,
        'is_owner': request.user == lst.owner,
        'is_contributor': lst.contributors.contains(request.user),
        'view_columns': rows[0].keys() if rows else None,
        'rows': rows,
        'add_row_form': add_row_form,
    }

    return render(request, 'lists/dashboard.html', ctx)


@login_required
@require_POST
def delete_row(request, listid, rowid):
    lst = get_object_or_404(List, pk=listid)
    is_owner = lst.owner == request.user
    row = get_object_or_404(MediaListRow, pk=rowid, appears_in=lst)

    if not (is_owner or row.added_by == request.user):
        return HttpResponseForbidden('not permitted to delete this row')

    row.delete()
    lst.date_updated = timezone.now()
    lst.save(update_fields=['date_updated'])

    return JsonResponse({'status': 'ok'})
