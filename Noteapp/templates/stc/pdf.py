# def export_pdf(req):
# 	response=HttpResponse(content_type='text/pdf')
# 	response['Content-Disposition']='attachement;filename=Expenses'+str(datetime.datetime.now())+'.pdf'
# 	response['Content-Transfer-Encoding']='binary'
# 	html_string=render_to_string('expenses/pdf-output.html',{'expenses':[],'total':0})
# 	html=HTML(string=html_string)
# 	result=html.write_pdf()
# 	with tempfile.NamedTemporaryFile(delete=True) as output:
# 		output.write(result)
# 		output.flush()
# 		output=open(output.name,'rb')
# 		response.write[output.read()]
# 	return response