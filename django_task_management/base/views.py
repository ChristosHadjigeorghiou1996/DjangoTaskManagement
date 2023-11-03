from functools import wraps
from typing import Callable, Union
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest 
from django.db.models import Count

from datetime import date

from .models import Task, Label, Comment

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
    labels_with_task_count = Label.objects.annotate(task_count=Count('tasks')).order_by('name')
    
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
        "tasks_by_user":tasks_by_user,
        "current_month_tasks": current_month_tasks,
        "labels_with_task_count": labels_with_task_count,
        'month_name': current_date.strftime("%B"),
        "date_task_info" : date_task_info,
        "next_month": next_month,
        "prev_month": prev_month,
        "all_user_comments": all_user_comments
    }
    return render(request, 'base/home.html', context)
