from django.urls import path
from Noteapp import views
from django.contrib.auth import views as ad

urlpatterns = [
	path('',views.home,name="hm"),
	path('pro/',views.profile,name="profile"),
	path('show/',views.show,name="show"),
	path('excsv/',views.export_csv,name="export-csv"),
	# path('expdf/',views.export_pdf,name="export-pdf"),
	path('abt/',views.about,name="ab"),
	path('cnt/',views.contact,name="cn"),
	path('lg/',ad.LoginView.as_view(template_name='stc/login.html'),name="log"),
	path('rg/',views.regi,name="rge"),
	path('ds/',views.dashboard,name="dsh"),
	path('lgo/',ad.LogoutView.as_view(template_name='stc/logout.html'),name="logo"),
    path('comp/',views.complaint,name="cp"),
    path('updf/',views.updpf,name="upf"),
    path('ch/',views.cgf,name="cg"),
    path('createPdf/',views.pdf_report,name='createpdf'),
    path('rst/',ad.PasswordResetView.as_view(template_name="stc/resetpassword.html"),name="rt"),
    path('rst_done/',ad.PasswordResetDoneView.as_view(template_name="stc/resetpassworddone.html"),name="password_reset_done"),
    path('rst_cf/<uidb64>/<token>/',ad.PasswordResetConfirmView.as_view(template_name="stc/reset_password_confirm.html"),name="password_reset_confirm"),
    path('rst_cmplt/',ad.PasswordResetCompleteView.as_view(template_name="stc/reset_password_complete.html"),name="password_reset_complete"),
    ]