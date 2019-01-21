from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def check_topic_owner(topic_owner, request_user):
	'''
	19-3 重构 ： 在views.py中， 我们在两个地方核实主题关联到的用户为当前登录的用户。 请将执行这种检查的代码放在一个名为check_topic_owner() 的函数中，
并在恰当的地方调用这个函数。
	'''
	if topic_owner != request_user:
		raise Http404

# Create your views here.
def index(request):
	return render(request, 'learning_logs/index.html')


def topics(request):
	#下面的if-else语句为让未登录的用户也可以看到所有公开的主题
	if request.user.is_authenticated:
		topics = Topic.objects.filter(Q(owner=request.user)|Q(public = True)).order_by('date_added') 
	else:
		topics = Topic.objects.filter(public = True).order_by('date_added') 
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required		
def topic(request, topic_id):
	topic = get_object_or_404(Topic, id=topic_id)
	"""显示单个主题及其所有的条目"""
	#topic = Topic.objects.get(id=topic_id)
	topic_owner = topic.owner
	#request_user = request.user
	check_topic_owner(topic.owner,request.user)
	
	'''
	if topic.owner != request.user:
		raise Http404
	'''
		
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required	
def new_topic(request):
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			#new_topic.publc = False               #####
		#	new_topic.public = request.POST.get('public')   ####
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
			
	context = {'form':form}
	return render(request,'learning_logs/new_topic.html',context)

@login_required		
def new_entry(request, topic_id):
	#topic = Topic.objects.get(id=topic_id)
	topic = get_object_or_404(Topic, id=topic_id)
	check_topic_owner(topic.owner,request.user)
	
	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
			
	context = {'topic':topic, 'form':form}
	return render(request,'learning_logs/new_entry.html',context)
'''
def edit_entry(request, entry_id):
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	
	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
			
	context = {'topic':topic, 'form':form}
	return render(request,'learning_logs/edit_entry.html',context)
'''
@login_required	
def edit_entry(request, entry_id):

#	entry = Entry.objects.get(id=entry_id)
	entry = get_object_or_404(Entry, id=entry_id)
	topic = entry.topic
	
	check_topic_owner(topic.owner,request.user)
	'''
	if topic.owner != request.user:
		raise Http404
	'''
	if request.method != 'POST':
	# 初次请求， 使用当前条目填充表单
		form = EntryForm(instance=entry)
	else:
	# POST提交的数据， 对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)
