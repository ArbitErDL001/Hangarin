from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Priority, Task, SubTask, Note
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#class HomePageView(ListView):
 #  model = Task
#   context_object_name = 'home'
#   template_name = "home.html"

class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'home'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Totals across your domain models
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()
        context['total_tasks'] = Task.objects.count()
        context['total_subtasks'] = SubTask.objects.count()
        context['total_notes'] = Note.objects.count()

        # Provide counts under names expected by the template
        context['categories_count'] = context['total_categories']
        context['priorities_count'] = context['total_priorities']
        context['tasks_count'] = context['total_tasks']
        context['subtasks_count'] = context['total_subtasks']
        context['notes_count'] = context['total_notes']

        # Year-to-date counts for models with created_at
        today = timezone.now().date()
        year = today.year
        context['tasks_created_this_year'] = Task.objects.filter(created_at__year=year).count()
        context['subtasks_created_this_year'] = SubTask.objects.filter(created_at__year=year).count()
        context['notes_created_this_year'] = Note.objects.filter(created_at__year=year).count()

        return context


# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'hangarin/category_list.html'
    ordering = ['name']
    paginate_by = 5

    def get_ordering(self):
        allowed = ['name']
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'hangarin/category_form.html'
    success_url = reverse_lazy('category-list')
    paginate_by = 5


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'hangarin/category_form.html'
    success_url = reverse_lazy('category-list')
    paginate_by = 5


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'hangarin/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
    paginate_by = 5


# Priority Views
class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'hangarin/priority_list.html'
    ordering = ['name']
    paginate_by = 5

    def get_ordering(self):
        allowed = ['name']
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    fields = ['name']
    template_name = 'hangarin/priority_form.html'
    success_url = reverse_lazy('priority-list')
    paginate_by = 5


class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'hangarin/priority_form.html'
    success_url = reverse_lazy('priority-list')
    paginate_by = 5


class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'hangarin/priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')
    paginate_by = 5


# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'hangarin/task_list.html'
    ordering = ['category__name', 'priority__name', 'title']
    paginate_by = 5

    def get_ordering(self):
        allowed = [
            'title',
            'status',
            'deadline',
            'priority__name',
            'category__name',
            'created_at',
            '-created_at',
        ]
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'category__name'

    def get_queryset(self):
        qs = super().get_queryset().select_related('priority', 'category')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(status__icontains=q)
                | Q(priority__name__icontains=q)
                | Q(category__name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'deadline', 'priority', 'category']
    template_name = 'hangarin/task_form.html'
    success_url = reverse_lazy('task-list')
    paginate_by = 5


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'deadline', 'priority', 'category']
    template_name = 'hangarin/task_form.html'
    success_url = reverse_lazy('task-list')
    paginate_by = 5


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'hangarin/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
    paginate_by = 5


# SubTask Views
class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'hangarin/subtask_list.html'
    ordering = ['-created_at']
    paginate_by = 5

    def get_ordering(self):
        allowed = [
            'task__title',
            'title',
            'status',
            'created_at',
            '-created_at',
        ]
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return '-created_at'

    def get_queryset(self):
        qs = super().get_queryset().select_related('task')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(status__icontains=q) | Q(task__title__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'hangarin/subtask_form.html'
    success_url = reverse_lazy('subtask-list')
    paginate_by = 5


class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'hangarin/subtask_form.html'
    success_url = reverse_lazy('subtask-list')
    paginate_by = 5


class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'hangarin/subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')
    paginate_by = 5


# Note Views
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'hangarin/note_list.html'
    ordering = ['-created_at']
    paginate_by = 5

    def get_ordering(self):
        allowed = [
            'task__title',
            'content',
            'created_at',
            '-created_at',
        ]
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return '-created_at'

    def get_queryset(self):
        qs = super().get_queryset().select_related('task')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(content__icontains=q) | Q(task__title__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        # Use effective ordering so dropdown selection reflects current state
        context['sort_by'] = self.get_ordering()
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'hangarin/note_form.html'
    success_url = reverse_lazy('note-list')
    paginate_by = 5

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'hangarin/note_form.html'
    success_url = reverse_lazy('note-list')
    paginate_by = 5

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'hangarin/note_confirm_delete.html'
    success_url = reverse_lazy('note-list')
    paginate_by = 5
