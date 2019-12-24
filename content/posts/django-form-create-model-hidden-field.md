---
title: "Django下通过form创建model对象如何隐藏不必要的field"
date: 2015-10-25T10:00:00+0800
categories: ["Tech"]
tags: ["python", "django"]
slug: "django-form-create-model-hidden-field"
keywords:
  - python
  - django
  - web开发
description: "由一个一对多关系由form创建model对象想到的。 提供了2种方法。"
---

# 简述
例如Model A和Model S是一对多的关系，即A是one， S是many, 使用`ForeignKey`来定义

```python
class A(models.Model):
  name = models.CharFields(max_length=64)

class S(models.Model):
  name = models.CharFields(max_length=64)
  a = models.ForeignKey(A)
```


在某个页面创建S的时候，需要指定是哪个A。 如果为A和S注册了admin，那么在admin-site里创建S的时候，会看到需要选择哪个A的实例，它会把所有的A的记录都列出来

但这个是针对admin的，不是针对业务的，如果一个用户想为他名下的某个A资源建立一个S的资源，那么把所有A的记录都列出来是不合适的，也不安全；实际上例如`POST /A/1/S/create`这样的url已经含了A的主键，在创建S的时候只需要为a field赋值即可，而且是自动的，不需要用户选择。

# 策略
就是在创建S的时候，不能把a的field暴露出来，并且根据url里的A的主键，将a赋值为A.objects.get(pk=1)即可。

## 方法1
直接使用`CreateView`，model为S，form暴露的fields需要包括`a`，在获取form初始值时，将`a`赋值。form在render的时候，需要隐藏`a field`，需要自定义各form的field，不能使用form.as_p()等。

``` python
class SCreateView(CreateView):
    model = S
    fields = {'name','a'}
    success_url = 'myurl'
    template_name = 's_add.html'

    def get(self, request, *args, **kwargs):
        # 这里根据url参数获取A的对象
        self.a_object = A.objects.get(pk=kwargs['a_id'])

    def get_initial(self):
        # 这里这样默认的form里a field就有值了。
        return {'a':self.a_object.pk}
```


## 方法2
使用`SignalObjectMixin`和`FormView`的组合，`SignalObjectMixin`是为了获取`A`的对象，FormView用于处理form的get和post。特别是post，我们的Form不需要有`a field`，在form_valid()里，通过`form.save(commit=False)`来创建一个S对象，但是该对象还没有持久化，然后为该对象的`a field`赋值为self.object.pk(通过SignalObjectMixin)即可，然后调用s.save()即可。

``` python
class SForm(form.ModelForm):
    class Meta:
        model = S
        fields = {'name'}

class SCreateView(SingleObjectMixin, FormView):
    model = A
    form_class = SForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SCreateView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SCreateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # commit为False，创建一个未持久化对象
        s = form.save(commit=False)
        # 为s的隐藏field赋值
        s.a = self.object
        # 持久化
        s.save()
        # 后续处理
        return super.form_valid(self, form)
```

## 方法3
继承`CreateView`,重写`form_valid()`。

``` python
from django.views.generic.edit import CreateView
from myapp.models import Author

class SCreate(CreateView):
    model = S
    fields = ['name']

    def form_valid(self, form):
        # a_object可以从其他地方获取,例如url等获取a的对象，关键是form.instance，因为这个form是ModelForm，为该instance的成员赋值，然后通过super()方法去save即可。
        form.instance.a = self.a_object
        return super(SCreate, self).form_valid(form)
```
