from django.http import Http404
from django.shortcuts import get_object_or_404, redirect


class SuperUserAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")


class FieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
		'teacher', 'students', 'category', 'title', 'slug', 'description', 'image', 'is_active', 'price', 'time', 'status', 'tag', 'likes', 'comments', 'tag',
		]
		return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
	def form_valid(self, form):
		if self.request.user.is_superuser:
			form.save()
		else:
			self.obj = form.save()
		return super().form_valid(form)
