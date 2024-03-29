from django.shortcuts import render
from django.shortcuts import render_to_response
from sblog.models import Blog
from sblog.models import Author
from sblog.forms import BlogForm
from django.http import Http404


# Create your views here.

def blog_list(request):
	blogs = Blog.objects.all()
	return render_to_response("sblog/blog_list.html",{"blogs":blogs})

def blog_show(request, blog_id = ''):
	try:
		blog = Blog.objects.get(id = blog_id)
	except Blog.DoesNotExist:
		raise Http404
	return render_to_response("sblog/blog_show.html", {"blog": blog})

def blog_filter(request,id = ''):
	tags = Tag.objects.all()
	tag = Tag.objects.get(id = id)
	blogs = tag.blog_set.all()
	return render_to_response("blog_filter.html",
		{"blogs": blogs, "tag": tag, "tags": tags})

def blog_add(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		tag = TagForm(request.POST)
		if form.is_valid() and tag.is_valid():
			cd = form.cleaned_data
			cdtag = tag.cleaned_data
			tagname = cdtag['tag_name']
			for taglist in tagname.split():
				Tag.objects.get_or_create(tag_name = taglist.strip())
			title = cd['caption']
			author = Author.objects.get(id = 1)
			content = cd['content']
			blog = Blog(caption = title, author = author,content = content)
			blog.save()
			for taglist in tagname.split():
				blog.tags.add(Tag.objects.get(tag_name = taglist.strip()))
				blog.save()
			id = Blog.objects.order_by('-publish_time')[0].id
			return HttpResponseRedirect('/sblog/blog/%s' %id)
	else:
		form = BlogForm()
		tag = TagForm(initial = {'tag_name': 'notags'})
	return render_to_response('blog_add.html',
		{'form': form, 'tag': tag}, context_instance = RequestContext(request))

def blog_update(request, blog_id = ""):
	id = blog_id
	if request.method == 'POST':
		form = BlogForm(request.POST)
		tag = TagForm(request.POST)
		if form.is_valid() and tag.is_valid():
			cd = form.cleaned_data
			cdtag = tag.cleaned_data
			tagname = cdtag['tag_name']
			tagnamelist = tagname.split()
			for taglist in tagnamelist:
				Tag.objects.get_or_create(tag_name = taglist.strip())
			title = cd['caption']
			content = cd['content']
			blog = Blog.objects.get(id = id)
			if blog:
				blog.caption = title
				blog.content = content
				blog.save()
				for taglist in tagnamelist:
					blog.tags.add(Tag.objects.get(tag_name = taglist.strip()))
					blog.save()
				tags = blog.tags.all()
				for tagname in tags:
					tagname = unicode(str(tagname), "utf-8")
					if tagname not in tagnamelist:
						notag = blog.tags.get(tag_name = tagname)
						blog.tags.remove(notag)
			else:
				blog = Blog(caption = blog.caption, content = blog.content)
				blog.save()
			return HttpResponseRedirect('/sblog/blog/%s' %id)
	else:
		try:
			blog = Blog.objects.get(id = id)
		except Exception:
			raise Http404
		form = BlogForm(initial = {'caption': blog.caption, 'content': blog.content}, auto_id = False)
		tags = blog.tags.all()
		if tags:
			taginit = ''
			for x in tags:
				taginit += str(x) + ''
			tag = TagForm(initial = {'tag_name': taginit})
		else:
			tag = TagForm()
	return render_to_response('blog_add.html',
		{'blog': blog, 'form': form, 'id': id, 'tag': tag},
		context_instance = RequestContext(request))

def blog_del(request, blog_id = ""):
	try:
		blog = Blog.objects.get(id = blog_id)
	except Exception:
		raise Http404
	if blog:
		blog.delete()
		return HttpResponseRedirect("/sblog/bloglist/")
	blogs = Blog.objects.all()
	return render_to_response("blog_list.html", {"blogs": blogs})

