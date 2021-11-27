from django.shortcuts import render
from .models import foodMenu, barMenu, foodOrder, barOrder
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
import decimal


# Create your views here.

@login_required(login_url = '/login')
def homePage(request):

    all_cuisine = (
        ("1", "Soup"),
        ("2", "Salad"),
        ("3", "Appetizers"),
        ("4", "Italian Mainfare"),
        ("5", "Mexican Mainfare"),
        ("6", "Pastas"),
        ("7", "Pizzas"),
        ("8", "Rice"),
        ("9", "Fondue"),
        ("10", "Desserts"),
    )
    all_drinktype = (
        ("1", "Beer"),
        ("2", "Cocktail"),
        ("3", "Gin"),
        ("4", "Red Wine"),
        ("5", "Sparkling Wine"),
        ("6", "Vodka"),
        ("7", "Whiskey"),
        ("8", "White Wine"),
    )

    #Newest Tab
    newest = foodMenu.objects.all().filter(newest=True)
    for i in newest:
        number = int(i.cuisine) - 1
        i.cuisine = all_cuisine[number][1]

    #recommended tab
    recommended = foodMenu.objects.all().filter(recommended=True)
    for i in recommended:
        number = int(i.cuisine)-1
        i.cuisine = all_cuisine[number][1]
    
    #recommended_Drink  
    recommended_drink = barMenu.objects.all().filter(recommended_drink=True)
    for i in recommended_drink:
        number = int(i.drinktype) - 1
        i.drinktype = all_drinktype[number][1]

    return render(request, "main/home.html", {"newest": newest, "recommended": recommended, "recommended_drink": recommended_drink})


@login_required(login_url = '/login')
def explorePage(request):

    all_cuisine = (
        ("1", "Soup"),
        ("2", "Salad"),
        ("3", "Appetizers"),
        ("4", "Italian Mainfare"),
        ("5", "Mexican Mainfare"),
        ("6", "Pastas"),
        ("7", "Pizzas"),
        ("8", "Rice"),
        ("9", "Fondue"),
        ("10", "Desserts"),
    )

    all_drinktype = (
        ("1", "Beer"),
        ("2", "Cocktail"),
        ("3", "Gin"),
        ("4", "Red Wine"),
        ("5", "Sparkling Wine"),
        ("6", "Vodka"),
        ("7", "Whiskey"),
        ("8", "White Wine"),
    )

    #For diplaying different cuisines in explore page
    allcuisine = foodMenu.objects.order_by('cuisine').values('cuisine').distinct()
    for i in allcuisine:
        number = int(i['cuisine']) - 1
        i['cuisine'] = all_cuisine[number][1]


    #for displaying Drinktypes in Explore Page
    alldrinks = barMenu.objects.order_by('drinktype').values('drinktype').distinct()
    for i in alldrinks:
        number = int(i['drinktype']) - 1
        i['drinktype'] = all_drinktype[number][1]

    return render(request, "main/explore.html", {'allcuisine': allcuisine, 'alldrinks': alldrinks})


@login_required(login_url = '/login')
@csrf_protect
@csrf_exempt
def showMenu(request, cuisine):
    all_cuisine = (
        ("1", "Soup"),
        ("2", "Salad"),
        ("3", "Appetizers"),
        ("4", "Italian Mainfare"),
        ("5", "Mexican Mainfare"),
        ("6", "Pastas"),
        ("7", "Pizzas"),
        ("8", "Rice"),
        ("9", "Fondue"),
        ("10", "Desserts"),
    )

    for c in all_cuisine:
        if c[1] == cuisine:
            cuisinename = cuisine
            cuisine = c[0]
            break

    #For Sending Order
    if request.method == 'POST':
        
        dname = request.POST.get('dname', False)
        dqty = request.POST.get('dqty', False)
        dprice = request.POST.get('dprice', False)
        totamt = int(dprice) * int(dqty)

        if dname != False:
            order = foodOrder.objects.create(
                user = request.user,
                dishName = dname,
                price = totamt,
                quantity = dqty,
                cooked = False
            )

    all_dish = foodMenu.objects.all().filter(cuisine__icontains = cuisine)

    return render(request, "main/menu.html", {'all_dish': all_dish, 'cuisine': cuisinename})


@login_required(login_url = '/login')
@csrf_protect
@csrf_exempt
def showBarMenu(request, drinktype):

    all_drinktype = (
        ("1", "Beer"),
        ("2", "Cocktail"),
        ("3", "Gin"),
        ("4", "Red Wine"),
        ("5", "Sparkling Wine"),
        ("6", "Vodka"),
        ("7", "Whiskey"),
        ("8", "White Wine"),
    )

    for drink in all_drinktype:
        if drink[1] == drinktype:
            drinkTypeName = drinktype
            drinkType = drink[0]
            break

    # For Sending Order Items
    if request.method == 'POST':
        
        dname = request.POST.get('dname', False)
        dtype = request.POST.get('dtype', False)
        dqty = request.POST.get('dqty', False)
        dprice = request.POST.get('dprice', False)
        totamt = int(dprice) * int(dqty)

        if dname != False:
            order = barOrder.objects.create(
                user = request.user,
                drinkName = dname,
                drinkType = dtype,
                price = totamt,
                quantity = dqty
            )
            print("Dyanmic")
            x = dynamicPricing(dname, dtype, dqty)
            print(x)

    all_drinks = barMenu.objects.all().filter(drinktype__icontains = drinkType)

    return render(request, "main/barmenu.html",{'all_drinks': all_drinks, 'drinkTypeName': drinkTypeName})


@login_required(login_url = '/login')
def orderPage(request):
    ordered = foodOrder.objects.all().filter(user = request.user)
    bar = barOrder.objects.all().filter(user = request.user)
    return render(request, "main/order.html", {"ordered" : ordered, 'bar' : bar})


def dynamicPricing(dname, dtype, quantity):
    print("start")
    ordered = barMenu.objects.all().filter(name = dname)

    ordered[0].current_price = ordered[0].current_price + (ordered[0].actual_price * decimal.Decimal(int(quantity)/100))
        
    if ordered[0].high < ordered[0].current_price:
        ordered[0].high = ordered[0].current_price
        ordered[0].save()

    all_drinks = barMenu.objects.all().filter(drinktype = dtype).exclude(name = dname)
    for drink in all_drinks:
        drink.current_price = drink.current_price - decimal.Decimal((ordered[0].actual_price * decimal.Decimal(quantity/100)/2))

        if drink.low > drink.current_price:
            drink.low = drink.current_price
        print("Drink Price Updated")
        drink.save()
        
    return 1
