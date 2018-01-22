from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, FormView, DeleteView

from .models import TimeLog
from .forms import TimeLogForm


class HomeView(LoginRequiredMixin,View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return render(request, "home.html", {})
		user = request.user
		if user.is_staff:
			return redirect('/admin/')
		qs = TimeLog.objects.filter(user=self.request.user).order_by("-updated")[:10]
		return render(request, "timelog/home-feed.html", {'object_list':qs})

class TimeLogListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)

class TimeLogDetailView(LoginRequiredMixin,DetailView):
	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)

class TimeLogFormView(LoginRequiredMixin,FormView):
	template_name = 'timelog/forms.html'
	form_class = TimeLogForm
	
	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)
	
	def get_form_kwargs(self):
		kwargs = super(TimeLogFormView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs
	
	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogFormView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Worktime'
		return context

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(TimeLogFormView,self).form_valid(form)


class TimeLogCreateView(LoginRequiredMixin,CreateView):
	template_name = 'timelog/forms.html'
	form_class = TimeLogForm

	
	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)
	
	def get_form_kwargs(self):
		kwargs = super(TimeLogCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs
	
	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogCreateView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Worktime'
		return context

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(TimeLogCreateView,self).form_valid(form)
		

class TimeLogUpdateView(LoginRequiredMixin,UpdateView):
	template_name = 'timelog/detail-update.html'
	form_class = TimeLogForm

	def get_object(self):
		pk = self.kwargs.get("pk")
		if pk is None:
			raise Http404
		return get_object_or_404(TimeLog, id__iexact=pk)

	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)
	
	def get_form_kwargs(self):
		kwargs = super(TimeLogUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogUpdateView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Worktime'
		return context


class TimeLogDeleteView(LoginRequiredMixin,DeleteView):
	model = TimeLog
	success_url = '/'
	template_name = 'timelog/delete_confirm.html'
