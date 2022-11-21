from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

#     pk_c96957675c4848fe8f7bdc10fbebae38

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        proxies = {"https": "http://no.client-swg.oneadr.net:8080"}
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_c96957675c4848fe8f7bdc10fbebae38".format(ticker), proxies=proxies)
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {"api":api})


    else:
        return render(request, 'home.html', {"ticker":"enter a ticker symbol above..."})

    
    #return render(request, 'home.html', {"api":api})

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json
    proxies = {"https": "http://no.client-swg.oneadr.net:8080"}

    if request.method == 'POST':
        form= StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect('add_stock')
        
    else: 
        ticker = Stock.objects.all()
        output=[]
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_c96957675c4848fe8f7bdc10fbebae38".format(str(ticker_item)), proxies=proxies)
            
            try:
                api = json.loads(api_request.content)
                output.append(api)
                
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})


#Defining deleting items. urls and add_stock.html
def delete(request, stock_id):
    item = Stock.objects.get(pk = stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted!"))
    return redirect(delete_stock)
    

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})