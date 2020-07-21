from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from . import util
from django.http import HttpResponse, HttpResponseRedirect
import re

markdowner = Markdown()
all_entries = util.list_entries()
print(all_entries)

def index(request):
    context = {
        "entries": util.list_entries(),
    }
    return render(request, "encyclopedia/index.html", context)

def single_page(request, slug):
    contents = markdowner.convert(util.get_entry(slug))
    context = {
        "entry": contents,
        "title": slug,
    }
    return render(request, "encyclopedia/single_page.html", context)

def search_results(request, methods=['GET', 'POST']):
    if request.method == 'POST':
        query = request.POST.get('q')
        #print(query)
        if query is "":
            return HttpResponseRedirect(reverse('index'))
        else:    
            if query in all_entries:
                #prints(query)
                return single_page(request, query) 
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
    context = {
        
    }
    return render(request, "encyclopedia/create.html", context)


