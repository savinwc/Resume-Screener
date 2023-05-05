from django.http import HttpResponse
from django.shortcuts import render
from .ai.resume_screener import job_result
import os
from wordcloud import WordCloud
import mysql.connector
from django.shortcuts import redirect
import base64

def index(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'aboutus.html')

def careeradvice(request):
    return render(request,'careeradvice.html')

def contact(request):
    return render(request,'contact.html')

def Employeesignup(request):
    return render(request,'Employeesignup.html')

def Employersignup(request):
    return render(request,'Employersignup.html')

def Login(request):
    return render(request,'loginpage.html')


def singlepost(request):
    return render(request,'singlepost.html')

def loginaction(request):
    if request.method == "POST":
        m = mysql.connector.connect(host="localhost", user="root", password="1234", database='project')
        cursor = m.cursor()
        d = request.POST
        EmployerEmailID = d['EmployerEmailID']
        AccountPassword = d['AccountPassword']

        c = "select * from users where EmployerEmailID='{}' and AccountPassword='{}'".format(EmployerEmailID, AccountPassword)
        cursor.execute(c)
        t = cursor.fetchone()
        if t:
            # Login successful, redirect to search page
            return redirect('search')
        else:
            # Login unsuccessful, display error message
            message = "User not found"
            return render(request, 'loginpage.html', {'message': message})

    # If request method is not POST, redirect to login page
    return redirect('Login')


def employeesignup(request):
    if request.method=='POST':
        EmployeeName = request.POST.get('EmployeeName')
        EmployeeEmailID = request.POST.get('EmployeeEmailID')
        EmployeePhoneNO = request.POST.get('EmployeePhoneNO')
        EmployeePosition = request.POST.get('EmployeePosition')
        EmployeeStartDate = request.POST.get('EmployeeStartDate')
        CurrentEmployeeStatus = request.POST.get('CurrentEmployeeStatus')
        Password = request.POST.get('Password')
        resume = request.FILES.get('resume').read() 
        
        mydb= mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="project"
        )

        mycursor = mydb.cursor()
        
        sql = "INSERT INTO employees (EmployeeName,EmployeeEmailID, EmployeePhoneNO,EmployeePosition,EmployeeStartDate,CurrentEmployeeStatus,Password,resume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (EmployeeName,EmployeeEmailID, EmployeePhoneNO,EmployeePosition,EmployeeStartDate,CurrentEmployeeStatus,Password,resume)
        mycursor.execute(sql, val)
        mydb.commit()

        # Close database connection
        mycursor.close()
        mydb.close()

        # Redirect to success page
        return redirect('Employeesignup')

    # If request method is not POST, display signup form
    return render(request, 'Employeesignup.html')
    

import mysql.connector

def employersignup(request):
    if request.method == 'POST':
        # Get form data
        CompanyName = request.POST['CompanyName']
        CompanyAddress = request.POST['CompanyAddress']
        PositionRequired = request.POST['PositionRequired']
        EmployerName = request.POST['EmployerName']
        EmployerDOB = request.POST['EmployerDOB']
        EmployerEmailID=request.POST['EmployerEmailID']
        EmployerPosition=request.POST['EmployerPosition']
        AccountPassword=request.POST['AccountPassword']

        try:
            # Connect to MySQL database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="project"
            )

            # Create cursor
            mycursor = mydb.cursor()

            # Insert data into database
            sql = "INSERT INTO users (CompanyName, CompanyAddress, PositionRequired, EmployerName, EmployerDOB, EmployerEmailID, EmployerPosition, AccountPassword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (CompanyName, CompanyAddress, PositionRequired, EmployerName, EmployerDOB, EmployerEmailID, EmployerPosition, AccountPassword)
            mycursor.execute(sql, val)
            mydb.commit()

            # Close database connection
            mycursor.close()
            mydb.close()

            # Redirect to success page
            return redirect('Employersignup')

        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table: {}".format(error))

    # If request method is not POST, display signup form
    return render(request, 'Employersignup.html')




def search(request):
    if request.method == 'POST':
        jd = request.POST.get('search-data', '')
        job_description, best_resume_path, best_similarity_score,ranked_resumes = job_result(jd)

        # Extract text from the best matching resume PDF
        print(best_similarity_score)

       

        # Return the search results
        return render(request, 'demo.html', {
            'job_description': job_description,
            'best_resume': best_resume_path,
            'best_similarity_score': best_similarity_score,
            'resume_url': best_resume_path,
            'ranked_resumes':ranked_resumes
        })

    return render(request, 'search.html')


    
def employeeloginpage(request):
    return render(request,'employeeloginpage.html')

def employeeloginaction(request):
    if request.method == "POST":
        m = mysql.connector.connect(host="localhost", user="root", password="1234", database='project')
        cursor = m.cursor()
        d = request.POST
        EmployeeEmailID = d['EmployeeEmailID']
        Password = d['Password']

        c = "select * from employees where EmployeeEmailID='{}' and Password='{}'".format(EmployeeEmailID, Password)
        cursor.execute(c)
        employee = cursor.fetchone()
        if employee:
            request.session['employee_name'] = employee[0]
            request.session['employee_email'] = employee[1]
            request.session['employee_phone'] = employee[2]
            request.session['employee_position'] = employee[3]
            request.session['employee_start_date'] = employee[4]
            request.session['current_employee_status'] = employee[5]
            request.session['resume'] = base64.b64encode(employee[7]).decode('utf-8')
           
            return redirect('employeepage')
        else:
            # Login unsuccessful, display error message
            message = "User not found"
            return render(request, 'employeeloginpage.html', {'message': message})

    # If request method is not POST, redirect to login page
    return redirect('Login')

def employeepage(request):
    resume_blob = request.session.get('resume')
    resume_bytes = resume_blob.encode('utf-8')
    employee_name = request.session.get('employee_name')
    employee_email = request.session.get('employee_email')
    employee_phone = request.session.get('employee_phone')
    employee_position = request.session.get('employee_position')
    employee_start_date = request.session.get('employee_start_date')
    current_employee_status = request.session.get('current_employee_status')
    resume_base64 =resume_bytes.decode('utf-8')
    
    if employee_name and employee_email and employee_phone and employee_position and employee_start_date and current_employee_status:
        context = {'EmployeeName': employee_name, 'EmployeeEmailID': employee_email, 'EmployeePhoneNO': employee_phone,
                   'EmployeePosition': employee_position, 'EmployeeStartDate': employee_start_date,
                   'CurrentEmployeeStatus': current_employee_status,'resume_base64': resume_base64}
        return render(request, 'world.html', context)
    else:
        return redirect('Login')
    
def pdf_view(request, file_path):
    with open(file_path, 'rb') as f:
        pdf_data = f.read()

    pdf_data_url = 'data:application/pdf;base64,' + base64.b64encode(pdf_data).decode('utf-8')

    return HttpResponse('<iframe src="%s" width="100%%" height="100%%"></iframe>' % pdf_data_url)


    
    

    
    




    

