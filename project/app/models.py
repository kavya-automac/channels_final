from django.dispatch import Signal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# inform = Signal(providing_args=['data'])

inform = Signal(['data'])


def notify_people(sender, **kwargs):
    print(kwargs.get('data'))
    print("all the things")


@receiver(inform)
def notify_admin(sender, **kwargs):
    print(kwargs.get('data'))
    print("this is admin")


inform.connect(notify_people)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField('address', max_length=1024, )

    def __str__(self):
        return self.user.username


# Create your models here.

class Department(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):  # to display the dept name in admin page
        return self.name


class Role(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, null=False)

    def __str__(self):  # to display the role name in admin page
        return self.name


class Employee(models.Model):
    objects = models.Manager()
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_date = models.DateField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.id = None

    def __str__(self):  # to display the  frstand lastnames and phnno. in admin page
        return "%s %s %s" % (self.first_name, self.last_name, self.phone)

    def get_absolute_url(self):
        return ('device_detail', (), {'pk': self.id})

    def notify(self):
        data = ('kavya', 'neha', 'a', 'b')
        inform.send(sender=self, data=data)


"""
@receiver(pre_save,sender=device_detail)
def pre_fun(sender,instance,**kwargs):
    print(sender.objects.all())

    #print(sender.objects.get(id=instance.id))
    print(instance)
    print(sender.objects.get(id=instance.id).device_units)
    print(instance.device_units)
    print(device_detail.objects.all())
    print(device_detail)
-------------------------------------------------
@receiver(pre_save,sender=device_detail)
def pre_fun(sender,instance,*args,**kwargs):
    print('args',args)
    print('kwargs',kwargs)


    print('instance',instance.device_name,instance.id)
    # trigger pre_save
    # dont do this -> instance.save()  # for this we get an error that recursion error ,maximum recursion depth exceeded while calling a python object
    # trigger post_save

    #print(device_detail.objects.filter(id=instance.id).values())




@receiver(post_save,sender=device_detail)
def post_fun(sender,instance,created,*args,**kwargs):
    #instance=instance.device_name
    if created:
        #device_detail.objects.create(device_name=instance)
        print(instance.device_name, 'added')
        # trigger pre_save
        instance.save()
        # trigger post_save

        #print(device_detail)

    else:
       print(instance.device_name,"just saved")

@receiver(pre_delete,sender=device_detail)
def pre_del_fun(sender,instance,*args,**kwargs):
    print(f"{instance.id} will be removed")

#pre_delete.connect(pre_del_fun,sender=device_detail)


@receiver(post_delete,sender=device_detail)
def post_del_fun(sender,instance,*args,**kwargs):
    print(f"{instance.id} has deleted")


#post_delete.connect(post_del_fun,sender=device_detail)
"""