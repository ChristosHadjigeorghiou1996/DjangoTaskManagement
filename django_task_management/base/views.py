from functools import wraps
from typing import Callable, Union
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404, JsonResponse
from django.db.models import Count, Q, Sum
# use flash messages for error
from django.contrib import messages
  
from datetime import date

from .models import Task, Label, Comment, User

from .helpers.CalendarHelper import CalendarHelper

# create custom decorator for views for authenticated or temporary users
def custom_login_required(view_func: Callable) -> Union[Callable, HttpResponseRedirect]:
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        # Check if the user is authenticated or a temporary user
        if request.user.is_authenticated or getattr(request.user, 'is_temporary', False):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page or any other page

    return _wrapped_view

@custom_login_required
def home(request: HttpRequest) -> HttpResponse:
    """
    Request to access home 
    :param request: http request
    :return render response
    """
    # get date and month for calendar
    current_date = date.today()
    # get month from url when you use back and next
    selected_month = request.GET.get('month')
    if selected_month:
        current_date = date.fromisoformat(selected_month)
    next_month = CalendarHelper.get_next_month(current_date)
    prev_month = CalendarHelper.get_previous_month(current_date)
    calendar_days = CalendarHelper.populate_calendar_days_for_month(current_date)

    tasks_by_user = Task.objects.filter(created_by=request.user).order_by("due_date")
    tasks_shared_with_user = Task.objects.filter(shared_with=request.user).order_by("due_date")
    tasks_including_user = tasks_by_user | tasks_shared_with_user

    labels_with_task_count = Label.objects.annotate(tasks_relating_to_user_count=Count('tasks', filter=Q(tasks__created_by=request.user) | Q(tasks__shared_with=request.user)))
    # Sum up total_task_count for all labels
    total_task_count_labels_relating_to_user = labels_with_task_count.aggregate(Sum('tasks_relating_to_user_count'))['tasks_relating_to_user_count__sum']
   
    # Create a list of dictionaries for each date and its tasks
    date_task_info = [{'date': day, 'tasks': [task.title for task in tasks_by_user if task.due_date == day]} for day in calendar_days]

    # Filter tasks for the current month
    current_month_tasks = Task.objects.filter(due_date__month=current_date.month)
    # comments by user
    user_comments_set = set(Comment.objects.filter(author=request.user))
    # comments by others on tasks of user
    user_task_ids = tasks_by_user.values_list('id', flat=True)
    other_user_comments_set = set(Comment.objects.filter(task__in=user_task_ids).exclude(author=request.user))
    # merge sets
    all_user_comments = user_comments_set | other_user_comments_set

    context = {
        "tasks_including_user":tasks_including_user,
        "current_month_tasks": current_month_tasks,
        "total_task_count_labels_relating_to_user": total_task_count_labels_relating_to_user,
        "labels_with_task_count": labels_with_task_count,
        'month_name': current_date.strftime("%B"),
        "date_task_info" : date_task_info,
        "next_month": next_month,
        "prev_month": prev_month,
        "all_user_comments": all_user_comments
    }
    return render(request, 'base/home.html', context)

def label(request: HttpRequest, id: str) -> HttpResponse:
    try:
        active_label = Label.objects.get(pk=id)
    except Label.DoesNotExist:
        raise Http404("Label does not exist")

    labels_with_task_count = Label.objects.annotate(tasks_relating_to_user_count=Count('tasks', filter=Q(tasks__created_by=request.user) | Q(tasks__shared_with=request.user)))
    total_task_count_labels_relating_to_user = labels_with_task_count.aggregate(Sum('tasks_relating_to_user_count'))['tasks_relating_to_user_count__sum']
    tasks_by_user_with_label = Task.objects.filter(created_by=request.user, labels=active_label).order_by("due_date")
    tasks_shared_by_others_with_label = Task.objects.filter(shared_with=request.user, labels=active_label).order_by("due_date")

    tasks_including_user = (tasks_by_user_with_label | tasks_shared_by_others_with_label)
    context = {
        'active_label': active_label,
        'total_task_count_labels_relating_to_user':total_task_count_labels_relating_to_user,
        "labels_with_task_count": labels_with_task_count,
        "tasks_including_user":tasks_including_user,
    }
    return render(request, 'base/label.html', context)

def profile(request: HttpRequest, id: str) -> HttpResponse:
    try:
        user_profile = User.objects.get(pk=id)
    except User.DoesNotExist:
        
        raise Http404(f"User with id {id} does not exist")

    labels_with_task_count = Label.objects.annotate(tasks_relating_to_user_count=Count('tasks', filter=Q(tasks__created_by=user_profile) | Q(tasks__shared_with=user_profile)))
    total_task_count_labels_relating_to_user = labels_with_task_count.aggregate(Sum('tasks_relating_to_user_count'))['tasks_relating_to_user_count__sum']
    tasks_by_user = Task.objects.filter(created_by=user_profile).order_by("due_date")
    tasks_shared_by_others_with = Task.objects.filter(shared_with=user_profile).order_by("due_date")
    tasks_including_user = (tasks_by_user | tasks_shared_by_others_with)
    context = {
        'user_profile': user_profile,
        'total_task_count_labels_relating_to_user':total_task_count_labels_relating_to_user,
        "labels_with_task_count": labels_with_task_count,
        "tasks_including_user":tasks_including_user,
    }
    return render(request, 'base/user-profile.html', context)

def update_task_status(request, task_id: str):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        task = get_object_or_404(Task, pk=task_id)
        previous_status = task.status
        task.status = new_status
        task.save()
        messages.success(request, 'Task status updated successfully.')
        response_data = {
            'status': 'success',
            'message': f"Task status changed from {previous_status} be {new_status}",
        }

    else:
        messages.error(request, 'Task status could not be changed.')
        response_data = {
            'status': 'error',
            'message': f"Task status could not be changed",
        }
    return JsonResponse(response_data)
