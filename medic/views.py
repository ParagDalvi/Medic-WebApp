from django.shortcuts import render
import pyrebase

config = {
    'apiKey': "AIzaSyBymW3eeqoT4cIFlVB1sm58g8DTfsQdy3o",
    'authDomain': "medic-mini-pro.firebaseapp.com",
    'databaseURL': "https://medic-mini-pro.firebaseio.com",
    'projectId': "medic-mini-pro",
    'storageBucket': "medic-mini-pro.appspot.com",
    'messagingSenderId': "369829213491",
    'appId': "1:369829213491:web:70037dc22d44bebf"
}

firebase = pyrebase.initialize_app(config)
authFirebase = firebase.auth()
db = firebase.database()


def home(request):
    completeData = db.child('Products').get()
    withoutCrazyId = []
    for i in completeData.each():
        withoutCrazyId.append(i.val())

    name = []
    quantity = []
    cost = []
    category = []
    for i in withoutCrazyId:
        name.append(i.get('name'))
        quantity.append(i.get('quantity'))
        cost.append(i.get('cost'))
        category.append(i.get('category'))

    wholePackage = zip(name, quantity, cost, category)
    return render(request, 'home.html', {'wholePackage':wholePackage, 'category':category})


def signIn(request):
    return render(request, 'signIn.html')


def storeAdmin(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authFirebase.sign_in_with_email_and_password(email, passw)
    except:
        messagePopUp = 'Invalid Credentials'
        return render(request, 'signIn.html', {'messagePopUp':messagePopUp})

    sessionId = user['idToken']
    request.session = str(sessionId)

    completeData = db.child('Products')
    IDs = []
    withoutCrazyId = []
    for i in completeData.get().each():
        withoutCrazyId.append(i.val())
        IDs.append(i.key())

    name = []
    quantity = []
    cost = []
    category = []
    for i in withoutCrazyId:
        name.append(i.get('name'))
        quantity.append(i.get('quantity'))
        cost.append(i.get('cost'))
        category.append(i.get('category'))

    wholePackage = zip(name, quantity, cost, category)


    return render(request, 'storeAdmin.html', {'wholePackage':wholePackage})


def adminUpload(request):
    name = request.POST.get('productName')
    quantity = request.POST.get('productQuantity')
    cost = request.POST.get('productCost')
    category = request.POST.get("category")
    data = {'name': name, 'quantity':quantity, 'cost':cost, 'category':category}
    db.child('Products').push(data)
    return render(request, 'addNew.html')


def addNew(request):
    return render(request, 'addNew.html')

def updateProduct(request):
    n = request.GET.get('n')
    n = n.split('/')
    name = n[0]
    quant = n[1]
    cost = n[2]
    cat = n[3]
    return render(request, 'updateProduct.html', {'name':name, 'quant':quant, 'cost':cost, 'cat':cat})


def adminUpdate(request):
    oldName = request.GET.get('n')
    updateName = request.POST.get('productName')
    updateQuant = request.POST.get('productQuantity')
    updateCost = request.POST.get('productCost')
    updateCat = request.POST.get("category")

    name = []
    quantity = []
    cost = []
    category = []
    withoutCrazyId = []
    completeData = db.child('Products')
    for i in completeData.get().each():
        withoutCrazyId.append(i.val())
        if db.child('Products').child(i.key()).child('name').get().val() == oldName:
            db.child('Products').child(i.key()).update({'name':updateName, 'quantity':updateQuant, 'cost': updateCost, 'category':updateCat})

    for i in withoutCrazyId:
            name.append(i.get('name'))
            quantity.append(i.get('quantity'))
            cost.append(i.get('cost'))
            category.append(i.get('category'))

    wholePackage = zip(name, quantity, cost, category)

    return render(request, 'storeAdmin.html', {'wholePackage':wholePackage, 'category':category})

