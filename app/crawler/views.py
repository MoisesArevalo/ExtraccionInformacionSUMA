from django.shortcuts import render
from app.crawler.models import CrawlerWeb
from .models import Busqueda
# Create your views here.
diccionario = {'ml':'Mercado Libre', 'olx':'OLX', 'amz':'Amazon'}
def sitios(clave, busqueda, n_pag=1):
    crawler =  CrawlerWeb()
    crawler.newDriver()
    def olx():
        df = crawler.e_commerceOLX(key=busqueda , n_result=n_pag)
        df['pagina']=0
        print(df.shape)
        return df
    def mercadolibre():
        crawler.setUrl('https://listado.mercadolibre.com.ec/')
        crawler.setElement(by='as_word', findby=0)
        df = crawler.e_commerceML( keys=[busqueda] ,n_result=n_pag)
        df['pagina']=1
        print(df.shape)
        return df
    def amazon():
        crawler.setUrl('https://www.amazon.com/-/es/')
        crawler.setElement(by='field-keywords', findby=0)
        df = crawler.e_commerceAmz( keys=[busqueda], n_result=n_pag)
        df['pagina']=2
        print(df.shape)
        return df
    guia ={'ml':mercadolibre, 'olx':olx, 'amz':amazon}
    return guia[clave]()
def iniciar(request):
    crawler =  CrawlerWeb()
    if request.method == 'POST':
        paginas = request.POST.getlist('check')
        texto = request.POST.get('q')
        n_pag = int(request.POST.get('links'))
        if not paginas:
            paginas = ['ml','olx','amz']
        for elem in paginas:
            sitios(elem, texto, n_pag)
        sitio =', '.join([diccionario[e] for e in paginas])
        busqueda = Busqueda(texto=texto, n_paginas =n_pag, sitios =sitio)
        busqueda.save()
    return render(request, 'index.html')
def historial(request):
    historia = Busqueda.objects.all()
    contexto = {"elementos": historia}
    return render(request, 'historial.html', contexto)
