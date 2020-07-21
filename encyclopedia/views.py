from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from . import util
from django.http import HttpResponse, HttpResponseRedirect
import re
import random as rndm

markdowner = Markdown()
all_entries = util.list_entries()
#print(all_entries)

def index(request):
    context = {
        "entries": util.list_entries(),
    }
    return render(request, "encyclopedia/index.html", context)

def single_page(request, slug):
    if slug not in all_entries:
        return HttpResponse("<h1>The requested page could not be found</h1>")
        #return render(request, 'encyclopedia/error.html', {"message": "The requested page could not be found"}) 
    try:
        contents = markdowner.convert(util.get_entry(slug))
        context = {
            "entry": contents,
            "title": slug,
        }
        return render(request, "encyclopedia/single_page.html", context)
    except:
        return HttpResponse("<h1>The requested page could not be found</h1>")
        #return render(request, 'encyclopedia/error.html', {"message": "The requested page could not be found"})

def search_results(request, methods=['GET', 'POST']):
    if request.method == 'POST':
        query = request.POST.get('q')
        #print(query)
        if query is "":
            return HttpResponseRedirect(reverse('index'))
        else:    
            if query in all_entries:
                #prints(query)
                return HttpResponseRedirect(reverse('single_page', args=[query])) 
            elif query not in all_entries:
                result = []
                
                for elem in all_entries:
                    if re.search(query.lower(), elem.lower()):
                        result.append(elem)
                
                context = {
                    "query": query,
                    "result": result,
                    "length": len(result),
                }
                    
                return render(request, "encyclopedia/list.html", context)
    else:
        return HttpResponseRedirect(reverse('index'))

def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('mdcontent')
        if title in all_entries:
            return HttpResponse("<h1>A page with this title already exists!</h1>")
            #return render(request, 'encyclopedia/create.html', {"message": "A page with this title already exists!"})
        if title is "":
            return HttpResponse("<h1>Please enter valid title!</h1>")
            #return render(request, 'encyclopedia/create.html', {"message": "Please enter valid title!"})
        if content is "":
            return HttpResponse("</h1>Please enter valid content in markdown format!</h1>")
            #return render(request, 'encyclopedia/create.html', {"message": "Please enter valid content in markdown format!"})
        
        util.save_entry(title, content)
        all_entries.append(title)
        #return HttpResponseRedirect(reverse('single_page', args=[title]))        
        return single_page(request, title)
    else:
        return render(request, "encyclopedia/create.html")

def edit_page(request, slug):
    contents = util.get_entry(slug)
    context = {
        "contents": contents,
        "title": slug,
    }
    #print(contents)
    return render(request, "encyclopedia/edit.html", context)

def update(request):
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_contents = request.POST.get('mdcontent')
        if new_title is "":
            return HttpResponse("<h1>Please enter valid title!</h1>")
            #return render(request, 'encyclopedia/create.html', {"message": "Please enter valid title!"})            
        if new_contents is "":
            return HttpRespconse("<h1>Please enter valid content in markdown format!</h1>")
            #return render(request, 'encyclopedia/create.html', {"message": "Please enter valid content in markdown format!"})
        util.save_entry(new_title, new_contents)
        #return single_page(request, new_title)
        return HttpResponseRedirect(reverse('single_page', args=[new_title]))   
        #return url_for('single_page', new_title)
    else:
        return HttpResponseRedirect(reverse('index'))

def random(request):
    random_title = rndm.choice(all_entries)
    return HttpResponseRedirect(reverse('single_page', args=[random_title]))


