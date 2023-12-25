from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code
from django.conf import settings
from decouple import config



def home(request):
	
	
	lang_list=['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'erlang', 'go', 'html', 'java', 'javascript', 'jsx', 'markup', 'markup-templating', 'matlab', 'perl', 'php', 'python', 'r', 'regex', 'ruby', 'rust', 'sql', 'swift', 'typescript', 'yaml']
	if request.method=="POST":
		code=request.POST['code']
		lang=request.POST['lang']

		#check to make sure they picked a lang

		if lang=='Select Programming Language':
			messages.success(request,"Hey! You forgot to pick a programming language")
			return render(request, 'home.html', {'lang_list':lang_list, 'code':code,'lang':lang})
		else:

			#OPEN AI key
			openai.api_key=config('OPENAI_API_KEY')
			
			#create OPEN AI instance
			openai.Model.list()
			#make an OPEN AI request

			try:
				response=openai.Completion.create(
					engine="gpt-3.5-turbo-instruct",
				    prompt=f'Respond only with code.{code}',
				    temperature=0,
				    max_tokens=1000,
				    top_p=1.0,
				    frequency_penalty=0.0,
				    presence_penalty=0.0
					)
				#parse the response
				response=(response["choices"][0]["text"].strip())
				#save to database
				record=Code(question=code,code_answer=response,language=lang,user=request.user)
				record.save()
				return render(request, 'home.html', {'lang_list':lang_list,"response":response,'lang':lang})
			except Exception as e:
				return render(request, 'home.html', {'lang_list':lang_list,"code":e,'lang':lang})
	return render(request, 'home.html', {'lang_list':lang_list})



def suggest(request):
	
	
	lang_list=['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'erlang', 'go', 'html', 'java', 'javascript', 'jsx', 'markup', 'markup-templating', 'matlab', 'perl', 'php', 'python', 'r', 'regex', 'ruby', 'rust', 'sql', 'swift', 'typescript', 'yaml']
	if request.method=="POST":
		code=request.POST['code']
		lang=request.POST['lang']

		#check to make sure they picked a lang

		if lang=='Select Programming Language':
			messages.success(request,"Hey! You forgot to pick a programming language")
			return render(request, 'suggest.html', {'lang_list':lang_list, 'code':code,'lang':lang})
		else:

			#OPEN AI key
			openai.api_key=config('OPENAI_API_KEY')
			
			#create OPEN AI instance
			openai.Model.list()
			#make an OPEN AI request

			try:
				response = openai.Completion.create(
				    engine="gpt-3.5-turbo-instruct",
				    prompt=f'Respond only with code.{code}',
				    temperature=0,
				    max_tokens=1000,
				    top_p=1.0,
				    frequency_penalty=0.0,
				    presence_penalty=0.0
				)
				#parse the response
				response=(response["choices"][0]["text"].strip())
				#save to database
				record=Code(question=code,code_answer=response,language=lang,user=request.user)
				record.save()
				return render(request, 'suggest.html', {'lang_list':lang_list,"response":response,'lang':lang})
			
			except Exception as e:
				return render(request, 'suggest.html', {'lang_list':lang_list,"code":e,'lang':lang})
	return render(request, 'suggest.html', {'lang_list':lang_list})


def login_user(request):
	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username, password=password)
		if user is not None:
			login(request,user)
			messages.success(request, "you have been logged in succesfully")
			return redirect('home')
		else:
			messages.success(request,"Error Logging in. Please try again")
			return redirect('home')
	else:
		return render(request,'home.html',{})


def logout_user(request):
	logout(request)
	messages.success(request,'you have been logged out')
	return redirect('home')


def register_user(request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data['username']
			password=form.cleaned_data['password1']
			user= authenticate(username=username,password=password)
			login(request,user)
			messages.success(request,'you have been registered')
	else:
		form=SignUpForm()
	return render(request,'register.html',{'form':form})


def past(request):
	if request.user.is_authenticated:
		code = Code.objects.filter(user_id=request.user.id)
		return render(request, 'past.html', {"code":code})	
	else:
		messages.success(request, "You Must Be Logged In To View This Page")
		return redirect('home')


def delete_past(request, Past_id):
	past = Code.objects.get(pk=Past_id)
	past.delete()
	messages.success(request, "Deleted Successfully...")
	return redirect('past')