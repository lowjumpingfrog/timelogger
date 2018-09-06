from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, FormView, DeleteView
from .models import TimeLog
from .forms import TimeLogForm, TimeLogReportForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime as dt
from django.db.models import Sum, F, ExpressionWrapper, fields, Value
from django.db.models.functions import Concat

class HomeView(LoginRequiredMixin,View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return render(request, "home.html", {})
		user = request.user
		if user.is_staff:
			return redirect('/admin/')
		qs = TimeLog.objects.filter(user=self.request.user).order_by("-updated")[:10]

		return render(request, "timelog/home-feed.html", {'object_list':qs})

class ReportView(LoginRequiredMixin, ListView):
	#request.META['QUERY_STRING']
	def get(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			return render(request, "home.html", {})

		pay_summary = TimeLog.objects.filter(timestamp__range=[dt.datetime.strptime(kwargs['report_start'],'%Y-%m-%d'),dt.datetime.strptime(kwargs['report_end'],'%Y-%m-%d')])\
									.order_by('user__last_name')\
									.filter(reconciled=False)\
									.filter(pay__gt=0)\
									.values('user__username')\
									.annotate(pay=Sum('pay')).annotate(fullname=Concat('user__last_name', Value(', '), 'user__first_name'))
		detail_pay = TimeLog.objects.filter(timestamp__range=[dt.datetime.strptime(kwargs['report_start'],'%Y-%m-%d'),
							dt.datetime.strptime(kwargs['report_end'],'%Y-%m-%d')]).order_by('user__last_name').filter(reconciled=False).filter(pay__gt=0)

		duration = ExpressionWrapper((F('work_end_time')-F('work_start_time')), output_field=fields.DurationField())
		other_summary = TimeLog.objects.filter(timestamp__range=[dt.datetime.strptime(kwargs['report_start'],'%Y-%m-%d'),dt.datetime.strptime(kwargs['report_end'],'%Y-%m-%d')])\
									.order_by('user__last_name')\
									.filter(reconciled=False)\
									.filter(reason__billable=False)\
									.values('user__username','reason__reason')\
									.annotate(time=Sum(duration)).annotate(fullname=Concat('user__last_name', Value(', '), 'user__first_name'))

		other = TimeLog.objects.filter(timestamp__range=[dt.datetime.strptime(kwargs['report_start'],'%Y-%m-%d'),
							dt.datetime.strptime(kwargs['report_end'],'%Y-%m-%d')]).order_by('user__last_name').filter(reconciled=False).filter(reason__billable=False)

		return render(request,
			"timelog/report.html",
			{'pay_summary':pay_summary,
			'detail_pay':detail_pay,
			'other_summary':other_summary,
			'other':other,
			'start_date':kwargs['report_start'],
			'end_date':kwargs['report_end']})

class TimeLogListView(LoginRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return render(request, "home.html", {})
		user = request.user
		if user.is_staff:
			return redirect('/admin/')
		qs = TimeLog.objects.filter(user=self.request.user).order_by("-work_start_time")

		return render(request, "timelog/list.html", {'object_list':qs})

class TimeLogDetailView(LoginRequiredMixin,DetailView):
	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)

class TimeLogFormView(LoginRequiredMixin,FormView):

	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)

	def get_form_kwargs(self):
		kwargs = super(TimeLogFormView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogFormView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Worktime'
		context['instructions'] = 'Fill out form to record your work details'
		return context

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(TimeLogFormView,self).form_valid(form)


class TimeLogCreateView(LoginRequiredMixin,CreateView):
	template_name = 'timelog/forms.html'
	form_class = TimeLogForm
	success_url = '/'

	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)

	def get_form_kwargs(self):
		kwargs = super(TimeLogCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogCreateView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Worktime'
		context['instructions'] = 'Fill out form to record your work details'
		return context

	def form_valid(self,form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(TimeLogCreateView,self).form_valid(form)


class TimeLogUpdateView(LoginRequiredMixin,UpdateView):
	template_name = 'timelog/forms.html'
	form_class = TimeLogForm
	success_url = '/'

	def get_object(self):
		pk = self.kwargs.get("pk")
		if pk is None:
			raise Http404
		return get_object_or_404(TimeLog, id__iexact=pk)

	def get_queryset(self):
		return TimeLog.objects.filter(user=self.request.user)

	def get_form_kwargs(self):
		kwargs = super(TimeLogUpdateView, self).get_form_kwargs()
		kwargs['id'] = self.kwargs.get("pk")
		kwargs['user'] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogUpdateView,self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Worktime'
		context['instructions'] = 'Make adjustments as needed'
		return context


class TimeLogDeleteView(LoginRequiredMixin,DeleteView):
	model = TimeLog
	success_url = '/'
	template_name = 'timelog/delete_confirm.html'


class TimeLogReportView(LoginRequiredMixin,FormView):
	template_name = 'timelog/forms.html'
	form_class = TimeLogReportForm
	success_url = '/admin/timelog/timelog/'


	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			report_start = str(form.cleaned_data['report_start'])
			report_end = str(form.cleaned_data['report_end'])
			url = reverse('timelog:view', kwargs={ 'report_start': report_start, 'report_end': report_end})
			return HttpResponseRedirect(url)

		return render(request, self.template_name, {'form': form})


	def get_context_data(self, *args, **kwargs):
		context = super(TimeLogReportView,self).get_context_data(*args, **kwargs)
		context['title'] = 'TimeLog Report'
		context['instructions'] = 'Select start and end date for reporting period'
		return context

	def form_valid(self,form):
		instance = form.save(commit=False)
		return super(TimeLogFormView,self).form_valid(form)
