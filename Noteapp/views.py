from django.shortcuts import render,redirect
from Noteapp.forms import UsForm,ComplaintForm,ImForm,UtupForm,ChpwdForm
from django.core.mail import send_mail
from NoteSharing import settings
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from Noteapp.models import ImProfile
from django.contrib.auth.decorators import login_required
import datetime
import csv
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

def pdf_report(req):
	data1=User.objects.all()
	d={}
	for i in data1:
		data=ImProfile.objects.get(uid_id=i.id)
		d[i.id]=data.age,i.username
	dd=d.values()
	template_path='stc/pdfreport.html'
	context={'dd':dd}
	response=HttpResponse(content_type='application/pdf')
	response['Content-Disposition']='attachement;filename="data_report.pdf'
	template=get_template(template_path)
	html=template.render(context)
	pisa_status=pisa.CreatePDF(html,dest=response)
	if pisa_status.err:
		return HttpResponse("wrong")
	return response


def home(request):
	return render(request,'stc/home.html')

def export_csv(req):
	response=HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachement;filename=Expenses'+str(datetime.datetime.now())+'.csv'
	writer=csv.writer(response)
	writer.writerow(['username','age'])
	data1=User.objects.all()
	d={}
	for i in data1:
		data=ImProfile.objects.get(uid_id=i.id)
		writer.writerow([i.username,data.age])
	return response


def show(request):
	
	data1=User.objects.all()
	d={}
	for i in data1:
		data=ImProfile.objects.get(uid_id=i.id)
		d[i.id]=data.age,i.username
	dd=d.values()
	print(dd)
	paginator=Paginator(data1,3)
	page=request.GET.get('page')
	try:
		data1=paginator.page(page)
	except PageNotAnInteger:
		data1=paginator.page(1)
	except EmptyPage:
		data1=paginator.page(paginator.num_pages)

	return render(request,'stc/show.html',{'dd':dd,'page':page,'data1':data1})

def about(request):
	return render(request,'stc/about.html')

def contact(request):
	return render(request,'stc/contact.html')

def regi(request):
	if request.method=="POST":
		p=UsForm(request.POST)
		if p.is_valid():
			p.save()
			return redirect('/lg')
	p=UsForm()
	return render(request,'stc/register.html',{'u':p})

@login_required
def dashboard(request):
	return render(request,'stc/dashboard.html')

@login_required	
def profile(req):
	d=ImForm()
	return render(req,'stc/profile.html',{'d':d})

def complaint(req):
	if req.method=="POST":
		data=ComplaintForm(req.POST)
		if data.is_valid():
			subject='Confirmation_complaint'
			body="thank you for complaint"+req.POST['p_name']
			receiver=req.POST['p_email']
			sender=settings.EMAIL_HOST_USER
			send_mail(subject,body,sender,[receiver])
			data.save()
			messages.success(req,"Successfully sent to your mail "+receiver)
			return redirect('/')
	form=ComplaintForm()
	return render(req,'stc/complaint.html',{'c':form})

@login_required
def updpf(request):
	if request.method == "POST":
		u=UtupForm(request.POST,instance=request.user)
		i=ImForm(request.POST,request.FILES,instance=request.user.improfile)
		if u.is_valid() and i.is_valid():
			u.save()
			i.save()
			return redirect('/pro')
	u=UtupForm(instance=request.user)
	i=ImForm(instance=request.user.improfile)
	return render(request,'stc/updateprofile.html',{'us':u,"imp":i})

@login_required
def cgf(request):
	if request.method=="POST":
		c=ChpwdForm(user=request.user,data=request.POST)
		if c.is_valid():
			c.save()
			return redirect('/lg')

	c=ChpwdForm(user=request)
	return render(request,'stc/changepassword.html',{'t':c})