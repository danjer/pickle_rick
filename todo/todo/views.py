from dataclasses import dataclass, field
from typing import Set
from django.shortcuts import render, redirect, reverse


@dataclass
class TodoList:
    name: str
    tasks: Set[str] = field(default_factory=set, init=False)

    @property
    def total_tasks(self):
        return len(self.tasks)

    def add_task(self, task: str):
        self.tasks.add(task)

    def delete_task(self, task: str):
        self.tasks = set([i for i in self.tasks if i != task])


# Constants
TODO_LIST = "todo_list"
TODO_LIST_VIEW = "detail_todo_view"


def list_todo_list(request):
    context = {TODO_LIST: request.session.get(TODO_LIST)}
    return render(request, 'index.html', context=context)


def create_todo_list(request):
    request.session[TODO_LIST] = TodoList(request.POST['name'])
    return redirect(reverse(TODO_LIST_VIEW))


def delete_todo_list(request):
    request.session[TODO_LIST] = None
    return redirect(reverse(TODO_LIST_VIEW))


def add_task(request):
    todo = request.session[TODO_LIST]
    todo.add_task(request.POST['task'])
    request.session[TODO_LIST] = todo
    return redirect(reverse(TODO_LIST_VIEW))


def delete_task(request):
    todo = request.session[TODO_LIST]
    todo.delete_task(request.POST['task'])
    request.session[TODO_LIST] = todo
    return redirect(reverse(TODO_LIST_VIEW))
