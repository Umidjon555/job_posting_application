from django.views import generic
from django.shortcuts import render
from .models import Careers, Tag, Category, Applicants
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.views.decorators import csrf


def Careers_list(request):
    cat_query = request.GET.get("c")

    query = request.GET.get("q")
    if query != None:
        object_list = Careers.objects.filter(Q(title__icontains=query) | Q(tags__name=query))
    else:
        if cat_query != None:
            object_list = Careers.objects.filter(Q(category__name=cat_query))
        else:
            object_list = Careers.objects.filter().order_by('-created_on')
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, 3) # 6 employees per page
    
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    tags = Tag.objects.all()

    cat = Category.objects.all().distinct()
    

    categories = {}
    for i in cat:
        categories[i] = Category.objects.filter(name=i).all()

    context = {
        'blogs': page_obj,
        "tags": tags,
        "categories": categories
        }
    print(context)
    return render(request, 'blog.html', context)



def blog_single(request, pk):
    blog = Careers.objects.filter(pk=pk).first()
    context ={
        'blog': blog,
         'msg': "",
         'show_msg': False
    }   
    if  request.method == 'POST':
            existing_emails = [x for x in Applicants.objects.values_list('email')]

            #          to_email = request.POST['email']
            #          ver_num = verification_code()
            #          subject = "Verification of Email Address - Intrepid IT Outsourcing"
            #          msg = f"""Dear valued customer,

            # We are writing to verify your email address on file with Intrepid IT Outsourcing. In order to ensure that we have your correct contact information and to provide you with the best possible service, we kindly ask that you verify your email address by entering the verification code below.

            # Verification Code: {ver_num}

            # Please note that this code will only be active for 1 hour. If you do not verify your email address within this time, we will have to assume that the email address is no longer valid and update our records accordingly.

            # If you have any questions or concerns, please do not hesitate to contact us.

            # Thank you for your cooperation and for choosing Intrepid IT Outsourcing as your IT solutions provider.

            # Best regards,
            # The Intrepid IT Outsourcing Team"""
        #  if sendmail(from_email, password, to_email, subject, msg):
    
            post_applicants = Applicants()
            print(existing_emails)
            print(request.POST['email'])

            email_list = Applicants.objects.filter().values_list('email', flat=True)
            if  request.POST['email'] not in email_list:
                if len(request.POST['full_name'])>3:
                     return render(request, 'messages.html', {'msg': "Sorry. Name is Too Short."})
                post_applicants.full_name = request.POST['full_name']
                
                post_applicants.email = request.POST['email']
                post_applicants.message = request.POST['message']
                post_applicants.resume = request.FILES["resume"]
                post_applicants.job_id = blog
                post_applicants.save()
           
                return render(request, 'messages.html', {'msg': "Tanks for the Application."})
            else:
                return render(request, 'messages.html', {'msg': "Sorry. this email is already registered for this job"})
    return render(request, 'blog-single.html', context)







def verify_email(request, pk):

    # context= {
    #             'is_mail_sent': False,
    #             'verification_num': 0,
    #             'err_msg': 'Invalid email'
    #         }
    
    #

    # EMAIL VERIFICATION

   

    if  request.method == 'POST':

         post_applicants = Applicants()
         post_applicants.full_name = request.POST['full_name']
         post_applicants.email = request.POST['email']
         post_applicants.message = request.POST['message']
         post_applicants.job_id = pk
         post_applicants.save()
    return render(request, 'blog-single.html', {'msg': 'saved'})
        
