from django.shortcuts import render,redirect
# Create your views here.
from django.http import HttpResponse
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
from ecommapp.forms import EmpForm,ProductModelForm,UserForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import random
import razorpay
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home(request):
    #data=Product.objects.all() #select * from ecommapp_product;active and inactive
    #print(data)
    data=Product.objects.filter(status=1)#fetch only active products
    content={}
    content['products']=data
    return render(request,'index.html',content)

def delete(request,rid):
    print("Id to be deleted:",rid)
    return HttpResponse("Id to be deleted:"+rid)

def edit(request,rid):
    print("Id to be edited is:",rid)
    return HttpResponse("Id to be edited:"+rid)

def addition(request,x,y):
     z=int(x)+int(y)
     print("Addition is:",z)
     return HttpResponse("Addition is:"+str(z))
'''
def user_register(request):

    return render(request,'register.html')

'''


def product_list(request):
    context={}
    context['name']="iphone"
    context['x']=1000
    context['y']=200
    context['data']=[10,20,30,40,50]
    #context['plist']=['Iphone','samsung','Nokia','vivo','abc']
    context['plist']=[
        {'name':'Samsung','pimage':'image of samsung','price':30000,'desc':'Product description'},
        {'name':'iphone','pimage':'image of iphone','price':85000,'desc':'Product description'},
        {'name':'Vivo','pimage':'image of vivo','price':35000,'desc':'Product description'},


    ]
    return render(request,'productlist.html',context)


def reuse(request):

    return render(request,'base.html')

#sorting start
def sort(request,sv):
    if sv=='0':
        param='price'  
    else:
        param='-price'  
    data=Product.objects.order_by(param).filter(status=1)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def catfilter(request,catv):
    q1=Q(cat=catv)
    q2=Q(status=1)
    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def pricefilter(request,pv):
    q1=Q(status=1)
    if pv=='0':
        q2=Q(price__lt=5000)
    else:
        q2=Q(price__gte=5000)
    
    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def pricerange(request):

    low=request.GET['min']
    high=request.GET['max']
    #print(low)
    #print(high)
    #select * from ecommapp_product where price>=low and price<=high and status=1;
    q1=Q(status=1)
    q2=Q(price__gte=low)
    q3=Q(price__lte=high)
    data=Product.objects.filter(q1 & q2 & q3)
    content={}
    content['products']=data
    return render(request,'index.html',content)

def product_details(request,pid):
    #print("Id of the Product:",pid)
    data=Product.objects.filter(id=pid)
    content={}
    content['products']=data
    return render(request,'product_details.html',content)

def addproduct(request):
    #print("Method is:",request.method)
    if request.method=="POST":
        #print("Insert record into database")
        #fetch data fron request POST 
        n=request.POST['pname']
        c=request.POST['pcat']
        amt=request.POST['pprice']
        s=request.POST['status']
        #print(n)
        #print(cat)
        #print(amt)
        #print(s)
        p=Product.objects.create(name=n,cat=c,price=amt,status=s)
        #print(p)
        p.save()
        return redirect('/addproduct')

    else:
        #print("In else part")
        p=Product.objects.all()
        content={}
        content['products']=p
        return render(request,'addproduct.html',content)
    

def delproduct(request,rid):
    #print("ID to be deleted:",rid)
    #fetch record to be deleted
    p=Product.objects.filter(id=rid)
    p.delete()
    return redirect('/addproduct')

def editproduct(request,rid):

    if request.method=="POST":
        upname=request.POST['pname']
        ucat=request.POST['pcat']
        uprice=request.POST['pprice']
        ustatus=request.POST['status']

        #print(upname)
        #print(ucat)
        #print(uprice)
        #print(ustatus)
        p=Product.objects.filter(id=rid)
        p.update(name=upname,cat=ucat,price=uprice,status=ustatus)
        return redirect('/addproduct')

    else:
        p=Product.objects.filter(id=rid)
        content={}
        content['products']=p
        return render(request,'editproduct.html',content)

def djangoform(request):
    if request.method=="POST":
        ename=request.POST['name']
        dept=request.POST['dept']
        email=request.POST['email']
        sal=request.POST['salary']
        print("Employee Name:",ename)
        print("Department:",dept)
        print("Email:",email)
        print("Salary:",sal)
    else:
        eobj=EmpForm()
        #print(eobj)
        content={}
        content['form']=eobj
        return render(request,'djangoform.html',content)

def modelform(request):
    if request.method=="POST":
        pass
    else:
        pobj=ProductModelForm()
        #print(pobj)
        content={}
        content['mform']=pobj
        return render(request,'modelform.html',content)

def user_register(request):
    content={}
    regobj=UserForm()
    content['userform']=regobj
    if request.method=="POST":
       regobj=UserForm(request.POST)
       #print(regobj)
       #print(regobj.is_valid())
       if regobj.is_valid():
           regobj.save()
           content['success']="User Created Successfully"
           return render(request,'user_register.html',content)
    else:
        #regobj=UserCreationForm()
        #print(regobj)
        #print(regobj)
        return render(request,'user_register.html',content)

def user_login(request):
    if request.method=="POST":
        dataobj=AuthenticationForm(request=request,data=request.POST)
        #print(dataobj)
        if dataobj.is_valid():
            uname=dataobj.cleaned_data['username']
            upass=dataobj.cleaned_data['password']
            #print("Username:",uname)
            #print("Password:",upass)
            u=authenticate(username=uname,password=upass)
            #print(u)
            if u:
                print("In login function if block")
                login(request,u)
                return redirect('/')
    else:
        obj=AuthenticationForm()
        content={}
        content['loginform']=obj 
        return render(request,'user_login.html',content)
    
def setsession(request):

    request.session['name']='Itvedant'
    return render(request,'setsession.html')

def getsession(request):

    content={}
    content['data']=request.session['name']
    return render(request,'getsession.html',content)

def addtocart(request,pid):#5

    if request.user.is_authenticated:
        userid=request.user.id #5
        #check whether user already added product in the cart 
        q1=Q(pid=pid)
        q2=Q(uid=userid)
        c=Cart.objects.filter(q1 & q2)#0 0r 1 or more than 1 => to check whether product already added in cart
        p=Product.objects.filter(id=pid)
        content={}
        content['products']=p
        if c:
            content['msg']="Product Already Exists in the cart"
            return render(request,'product_details.html',content)
        else:
            #print("User ID:",uid)
            #print("Product Id:",pid)
            u=User.objects.filter(id=userid)
            #print(u[0])
            #print(p)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            content['success']="Product Added in cart"
            return render(request,'product_details.html',content)
        
    else:
        return redirect('/login')
    

def user_logout(request):

    logout(request)
    return redirect('/login')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    #print(c[0])
    #print(c[0].pid)
    #print(c[0].uid)
    #calculating total product price 
    sum=0
    for x in c:
        #print(type(x.qty))
        #print(type(x.pid.price))
        sum=sum+(x.qty*x.pid.price)
    print("Total Product Price:",sum)
    content={}
    content['products']=c
    content['nitems']=len(c)
    content['total']=sum
    #print(len(c))
    return render(request,'viewcart.html',content)


def changeqty(request,pid,f):
   content={}
   c=Cart.objects.filter(pid=pid)
   if f=='1':
       x=c[0].qty+1 #c.qty+=1
   else:
       x=c[0].qty-1

   if x>0:
      c.update(qty=x)
   
   
   return redirect('/viewcart')
   

def placeorder(request):
    
    oid=random.randrange(1000,9999)
    #print(oid)
    user_id=request.user.id #user_id=5
    c=Cart.objects.filter(uid=user_id)#uid=5
    #print(c)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()

    o=Order.objects.filter(uid=user_id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)

    content={}
    content['products']=o
    content['nitems']=len(o)
    content['total']=sum

    
    return render(request,'placeorder.html',content)


def makepayment(request):
    userid=request.user.id
    client = razorpay.Client(auth=("rzp_test_KLuc8q5Pngg5XZ", "ftAymVb196pQvWtafzWAM5GE"))
    o=Order.objects.filter(uid=userid)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    
    sum=sum*100  #conversion of Rs into Paise
    data = { "amount":sum, "currency": "INR", "receipt":str(o[0].id) }
    payment = client.order.create(data=data)
    print(payment)
    content={}
    content['payment']=payment
    
    return render(request,'pay.html',content)


def storedetails(request):
    pay_id=request.GET['pid']
    order_id=request.GET['oid']
    sign=request.GET['sign']
    userid=request.user.id 
    u=User.objects.filter(id=userid)
    #print(u[0])
    #print(u[0].email)
    #print(pay_id)
    #print(order_id)
    #print(sign)
    email=u[0].email
    msg="Order Placed Successfully. Details are Payment ID:"+pay_id+" and Order Id is:"+order_id
    send_mail(
    "Order Status-Ekart ",
    msg,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )

    return HttpResponse("Email Sent successfully")

