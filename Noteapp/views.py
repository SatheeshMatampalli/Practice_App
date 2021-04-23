from django.shortcuts import render,redirect
from Noteapp.forms import UsForm,ComplaintForm,ImForm,UtupForm,HallForm,ChpwdForm,BookForm
from django.core.mail import send_mail
from NoteSharing import settings
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from Noteapp.models import ImProfile,Bookreq,Halldistrict,Hallname,Halldetails
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

@login_required
def bookcheck(request):
	if request.method=="POST":
		p=BookForm(request.POST)
		if p.is_valid():
			d=p.save(commit=False)
			d.uploadby=request.user.email
			d.up_id=request.user.id
			# print(d.uploadby,d.uploaddate,d.upload_type.url)
			d.save()
		return redirect('/')
	p=BookForm()
	return render(request,'stc/bookcheck.html',{'p':p})

@login_required
def viewnt(req):
	accept=Bookreq.objects.filter(is_status=1).count()
	accept1=Bookreq.objects.filter(is_status=1)
	pending=Bookreq.objects.filter(is_status=0).count()
	pending1=Bookreq.objects.filter(is_status=0)
	allnotes=Bookreq.objects.all().count()
	allnotes1=Bookreq.objects.all()
	acc=Bookreq.objects.filter(is_status=2).count()
	acc1=Bookreq.objects.filter(is_status=2)
	return render(req,'stc/adminpage.html',{'acc':acc,'acc1':acc1,'accept1':accept1,'accept':accept,'pending':pending,'pending1':pending1,'allnotes':allnotes,'allnotes1':allnotes1})



def notipending(req):
	pending2=Bookreq.objects.filter(is_status=0)
	return render(req,'stc/noti_pendingdata.html',{'pending2':pending2})


@login_required
def myreq(req):
	notes=Bookreq.objects.filter(up_id=req.user)
	return render(req,'stc/myreq.html',{'data':notes})

def acceptadmin(req,id):
	ac=Bookreq.objects.get(id=id)
	ac.is_status='1'
	ac.save()
	return redirect('/viewn')

def rejectadmin(req,id):
	rc=Bookreq.objects.get(id=id)
	rc.is_status='2'
	rc.save()
	return redirect('/viewn')

def datadelete(req,id):
	obj=Bookreq.objects.get(id=id)
	obj.delete()
	return redirect('/myreq')


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
	d = Bookreq.objects.filter(is_status=0).count()
	return render(request,'stc/dashboard.html',{'d':d})

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
def reghalls(req):
	if req.method=="POST":
		u=HallForm(req.POST,req.FILES)
		if u.is_valid():
			u.save()
			return redirect('/')
	t=HallForm()
	return render(req,'stc/halls.html',{'t':t})


@login_required
def cgf(request):
	if request.method=="POST":
		c=ChpwdForm(user=request.user,data=request.POST)
		if c.is_valid():
			c.save()
			return redirect('/lg')

	c=ChpwdForm(user=request)
	return render(request,'stc/changepassword.html',{'t':c})


def load_courses(req):
	programming_id=req.GET.get('programming')
	print(programming_id)
	courses=Hallname.objects.filter(programming_id=programming_id).order_by('name')
	print(courses)
	return render(req,'stc/dropd.html',{'courses':courses})



def hallsview(req):
	if req.method=="POST":
		ml=req.POST['programming']
		mlm=req.POST['courses']
		print(ml,mlm)
		d=Halldetails.objects.filter(hallid=mlm)
		return render(req,'stc/hallsinfo.html',{'d':d})

	data=Halldistrict.objects.all()
	return render(req,'stc/hallbook.html',{'data':data})

