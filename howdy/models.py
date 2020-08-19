from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save
from django.utils import timezone

from django.db.models.signals import post_save
from notifications.signals import notify
from django.db.models import Q
# Create your models here.



manger_choices = (
    ('coating', 'coating'),
    ('cutting', 'cutting'),
    ('looms', 'looms'),
    ('extruder', 'extruder'),
    ('sales', 'sales'),
    ('quality', 'quality'),
    ('printing', 'printing'),
    ('Production_manager', 'Production_manager'),
    ('follower', 'follower'),
    ('packing', 'packing'),
    ('normal', 'normal'),

)


from .usermanger import UserManager
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
########################################################################
class User(AbstractBaseUser, PermissionsMixin):

    full_name 		= models.CharField(max_length=255, blank=True, null=True)
    username 		= models.CharField(max_length=255, unique=True, verbose_name='username')
    email 			= models.EmailField(max_length=255, unique=True)
    date_joined 	= models.DateTimeField(_('date_joined'), default=timezone.now)
    is_active 		= models.BooleanField(default=True)
    is_staff 		= models.BooleanField(default=False)
    is_admin		= models.BooleanField(default=False)
    is_manger		= models.BooleanField(default=False)
    position 		= models.CharField(max_length=18, choices=manger_choices)
    timestamp		= models.DateTimeField(auto_now_add=True)

    groups 			= models.ForeignKey(
									Group,
									verbose_name=_('groups'),
									null=True,
                                   blank=True,
									on_delete=models.CASCADE,
									help_text=_(
										'The groups this user belongs to. A user will get all permissions '
										'granted to each of their groups.'
									),
									related_name="user_set",
									related_query_name="user",
									)

    objects = UserManager()
    # username_field shouldn't be added to the required_fields cause it's already required
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True




class Manger(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=18, choices=manger_choices)

    def __str__(self):
        return self.user_id.username
from django.urls import reverse




########################################################################







class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=100)
    email = models.EmailField()
    phones = models.CharField(max_length=1000)
    priority = models.CharField(max_length=20)

    def __str__(self):
        return self.customer_name


########################################################################################3test 3 for production manager
class Productio_order_test2(models.Model):
    CURRENCY=(('SP','SP'),('$','$'),('E','E'),)
    AGREEMENT=(('نعم','نعم'),('لا','لا'),)
    order_id = models.IntegerField(primary_key=True)
    customer_name=models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date=models.DateField()
    start_time=models.DateField()
    delivery_time=models.DateField()
    delivery_way=models.CharField(max_length=1000)
    order_status=models.CharField(max_length=1000)
    notes = models.CharField(max_length=1000)
    production_manager_agreement=models.CharField(max_length=10,choices=AGREEMENT,default='لا')

    def __str__(self):
        return str(self.order_id)+ " "+self.customer_name.customer_name

    def getItems(self):
       return Order_item.objects.filter(order_id=self.order_id)
""""
def my_handler2(sender, instance, created, **kwargs):
    if not created:
        user = User.objects.get(position="sales")
        notificate.objects.create(
            title='تم تعديل الطلبية من قبل مدير الانتاج',
            message='new product was added new product was added new product was added new product was added',
            url='{}'.format(reverse('update_F_M_BY_sales_one')),
            recipient=user
        )
    else:
        pass
    #   url='{}'.format(reverse('production_m_order_update_page', kwargs={'pk': instance.id})),
post_save.connect(my_handler2, sender=Productio_order_test2)

"""







#########################################33








class Productio_order(models.Model):
    CURRENCY=(('SP','SP'),('$','$'),('E','E'),)
    AGREEMENT=(('نعم','نعم'),('لا','لا'),)
    id = models.IntegerField(primary_key=True)
    customer_name=models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date=models.DateField()
    start_time=models.DateField()
    delivery_time=models.DateField()
    total_price=models.FloatField()
    payment_currency=models.CharField(max_length=10,choices=CURRENCY)
    payment_way=models.CharField(max_length=1000)
    delivery_way=models.CharField(max_length=1000)
    order_status=models.CharField(max_length=1000)
    notes = models.CharField(max_length=1000)
    isAdstar=models.CharField(max_length=10,choices=AGREEMENT,default="لا")
    payment_time_tolerance=models.CharField(max_length=1000,default="لا يوجد")
    production_manager_agreement=models.CharField(max_length=10,choices=AGREEMENT,default='لا')
    sales_manager_agreement=models.CharField(max_length=10,choices=AGREEMENT,default='لا')
    def __str__(self):
        return str(self.id)+ " "+self.customer_name.customer_name

    def getItems(self):
       return Order_item.objects.filter(order_id=self)


    def getTestOrder2(self):
        return Productio_order_test2.objects.get(order_id=self.id)

    def get_intenal_order_for_loom(self):
        return loom_internal_order.objects.filter(order_id=self)
""""
def my_handler(sender, instance, created, **kwargs):
    user = User.objects.get(position="Production_manager")
    if created:
        notificate.objects.create(
            title='تم اضافة طلبية جديدة',
            message='new product was added new product was added new product was added new product was added',
            url='{}'.format(reverse('production_m_order_update_page')),
            recipient=user
        )
    else:
        notificate.objects.create(
            title='تم تثبيت الطلبية من قبل المبيعات',
            message='new product was added new product was added new product was added new product was added',
            url='{}'.format(reverse('orders_in_p_manager_page')),
            recipient=user
        )
    #   url='{}'.format(reverse('production_m_order_update_page', kwargs={'pk': instance.id})),
post_save.connect(my_handler, sender=Productio_order)

"""

from django.db.models.signals import post_save
from notifications.signals import notify





class order_sch(models.Model):
    STATES=(('متوقف','متوقف'),('جاري التصنيع','جاري التصنيع'),('انتهى','انتهى'))
    FINISH=(('نعم','نعم'),('لا','لا'))
    sch_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    start_loom_date=models.DateField()
    end_loom_date = models.DateField()
    loom_fixed=models.CharField(max_length=10,choices=FINISH,default='لا')
    start_coating_date = models.DateField(default='2000-11-11')
    end_coating_date = models.DateField(default='2000-11-11')
    star_printing_date = models.DateField(default='2000-11-11')
    end_printing_date = models.DateField(default='2000-11-11')
    start_cutting_date = models.DateField(default='2000-11-11')
    end_cutting_date = models.DateField(default='2000-11-11')
    order_start_date= models.DateField(default='2000-11-11')
    order_end_date = models.DateField(default='2000-11-11')
    fixedd=models.CharField(max_length=10,choices=FINISH,default='لا')
    state=models.CharField(max_length=100,choices=STATES)
    notes=models.CharField(max_length=1000,default='no')

    def __str__(self):
        return str(self.sch_id)
    def getOrder(self):
        return Productio_order.objects.get(id=self.order_id.id)
    def getAgrees(self):
        return agreements_for_order_sch.objects.get(order_sch_id=self)
    def getCuttingInternalOrders(self):
            sum=0
            n= cutting_internal_order.objects.filter(sch_id=self)
            for i in n:
                sum+=i.getRollsForThisInternalOrder()
            return sum

    def getCoatingInternalOrders(self):
            sum=0
            n= coating_internal_order.objects.filter(sch_id=self)
            for i in n:
                s,w=i.getRollsForThisInternalOrder()
                sum+=s
            return sum

    def getPrintingInternalOrders(self):
            sum=0
            n= printing_internal_order.objects.filter(sch_id=self)
            for i in n:
                sum+=i.getRollsForThisInternalOrder()
            return sum

    def getAllprintingInternalOrderForPMANAGER(self):
        return printing_internal_order.objects.filter(sch_id=self)


    def getAllcuttingInternalOrderForPMANAGER(self):
        return cutting_internal_order.objects.filter(sch_id=self)


    def getAllcoatingInternalOrderForPMANAGER(self):
        return coating_internal_order.objects.filter(sch_id=self)
""""
def my_handler3(sender, instance, created, **kwargs):
    sch=order_sch.objects.get(sch_id=instance.sch_id)
    print(1)
    if sch.start_cutting_date!="2000-11-11":
        print(2)
        users = User.objects.filter(position="cutting")
        if created:
            for user in users:
                notificate.objects.create(
                    title='خطة عمل جديدة',
                    message='تم اضافة خطة عمل لطلبية جديدة الرجاء وضع التعديلات المناسبة',
                    url='{}'.format(reverse('update_order_sch_cutting_view')),
                    recipient=user
                )
    if sch.start_coating_date!="2000-11-11":
        print(3)
        users = User.objects.filter(position="coating")
        if created:
            for user in users:
                notificate.objects.create(
                    title='خطة عمل جديدة',
                    message='تم اضافة خطة عمل لطلبية جديدة الرجاء وضع التعديلات المناسبة',
                    url='{}'.format(reverse('update_order_sch_coating_view')),
                    recipient=user
                )
    if sch.star_printing_date!="2000-11-11":
        users = User.objects.filter(position="printing")
        if created:
            for user in users:
                notificate.objects.create(
                    title='خطة عمل جديدة',
                    message='تم اضافة خطة عمل لطلبية جديدة الرجاء وضع التعديلات المناسبة',
                    url='{}'.format(reverse('update_order_sch_printing_view')),
                    recipient=user
                )

    users = User.objects.filter(position="looms")
    if created:
        for user in users:
            notificate.objects.create(
                title='خطة عمل جديدة',
                message='تم اضافة خطة عمل لطلبية جديدة الرجاء وضع التعديلات المناسبة',
                url='{}'.format(reverse('update_order_sch_view')),
                recipient=user
            )
    #   url='{}'.format(reverse('production_m_order_update_page', kwargs={'pk': instance.id})),
post_save.connect(my_handler3, sender=order_sch)


"""


class Order_item(models.Model):
    CHOICE=(('نعم','نعم'),('لا','لا'))
    CHOICEe = ((0, 0),(1, 1), (2, 2),)
    item_id=models.IntegerField()
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    makok = models.CharField(max_length=10)
    knar = models.CharField(max_length=10)
    coating_or_not = models.CharField(max_length=10,choices=CHOICE)
    cutting = models.CharField(max_length=100,choices=CHOICE)
    cutting_kind=models.CharField(max_length=100,null=True)
    mobatn = models.CharField(max_length=10,choices=CHOICE)
    mobatn_width=models.FloatField(default=0)
    mobatn_height = models.FloatField(default=0)
    mobatn_weight = models.FloatField(default=0)
    modmag =models.CharField(max_length=10,choices=CHOICE)
    item_printing_name = models.CharField(max_length=100)
    first_face_colors=models.CharField(max_length=100,null=True)
    second_face_colors=models.CharField(max_length=100,null=True)
    print_one_face_or_two = models.IntegerField(choices=CHOICEe)
    sewing_item=models.CharField(max_length=100 ,default='لا')
    item_width=models.FloatField(10)
    tolerance_width=models.FloatField(default=0)
    item_height=models.FloatField(10)
    tolerance_height=models.FloatField(default=0)
    item_weight=models.FloatField(10)
    tolerance_weight=models.FloatField(default=0)
    quantity=models.IntegerField(100)
    peice_price=models.FloatField(default=0.0)
    batch_depth=models.FloatField(default=0.0)
    batch_height=models.FloatField(default=0.0)
    notes=models.CharField(max_length=1000)

    class Meta:
        unique_together = (("item_id", "order_id"),)

    def getCoatingInternalOrder(self):
        n=coating_internal_order.objects.get(order_id=self.order_id,item_id=self.item_id)
        if n:
            sum,w=n.getRollsForThisInternalOrder()
            return sum
        else:
            return "غير مطلي"

    def getPrintingInternalOrder(self):
        n = printing_internal_order.objects.get(order_id=self.order_id, item_id=self.item_id)
        if n:
           return n.getRollsForThisInternalOrder()
        else:
            return "غير مطبوع"

    def getCuttingInternalOrder(self):
        n = cutting_internal_order.objects.get(order_id=self.order_id, item_id=self.item_id)
        if n:
            return n.getRollsForThisInternalOrder()
        else:
            return "لا يحتاج قص"

class agreements_for_order_sch(models.Model):
    order_sch_id=models.ForeignKey(order_sch,on_delete=models.CASCADE)
    ls=models.DateField(default='2000-11-11')
    le = models.DateField(default='2000-11-11')
    l_reason=models.CharField(max_length=1000,default='لا')
    cots = models.DateField(null=True)
    cote = models.DateField(null=True)
    cot_reason=models.CharField(max_length=1000,default='لا')
    cuts = models.DateField(null=True)
    cute = models.DateField(null=True)
    cut_reason=models.CharField(max_length=1000,default='لا')
    prs = models.DateField(null=True)
    pre = models.DateField(null=True)
    pr_reason=models.CharField(max_length=1000,default='لا')

    def __str__(self):
        return str(self.order_sch_id)




#_____________________________________________________________________________________________
class Fiber_Code(models.Model):

    fiber_id=models.AutoField(primary_key=True)
    denier=models.IntegerField()
    fiber_width=models.FloatField()
    fiber_color=models.CharField(max_length=10)
    pp_percent=models.FloatField()
    ca_percent=models.FloatField()
    stain_percent=models.FloatField()
    def __str__(self):
        return str(self.fiber_id)

class extruder_shift(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id = models.AutoField(primary_key=True)
    shift = models.CharField(max_length=10, choices=SHIFTS)
    shift_supervisor_id = models.CharField(max_length=100)
    shift_date = models.DateField()

    def __str__(self):
        return str(self.shift_id)

    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date = timezone.localdate()
        return super(extruder_shift, self).save(*args, **kwargs)


from datetime import datetime
#######################################################################################################looms


class shift_identifier(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id=models.AutoField(primary_key=True)
    shift=models.CharField(max_length=10,choices=SHIFTS)
    shift_supervisor_id=models.CharField(max_length=100)
    shift_date=models.DateField()

    def __str__(self):
        return str(self.shift_id)
    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date=timezone.localdate()
        return super(shift_identifier, self).save(*args, **kwargs)




class Daily_Fiber_Order_From_Looms(models.Model):
    extroders = (('1400', '1400'), ('1500/1', '1500/1'), ('1500/2', '1500/2'),('لا','لا'),)
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    daily_order_id=models.AutoField(primary_key=True)
    expected_extruder=models.CharField(max_length=10,choices=extroders)
    makok_fiber_code=models.IntegerField(default=0)
    num_makok_lots=models.IntegerField()
    sdh_fiber_code=models.IntegerField()
    num_sdh_lots = models.IntegerField()
    kanar_fiber_code=models.IntegerField()
    num_kanar_lots=models.IntegerField()
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    order_date=models.DateField(auto_now_add=False, blank=True, null=True)
    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.daily_order_id)

    def get_names(self):
       names= loomers_related_daily_order_of_looms_to_extruder.objects.filter(order_id=self)
       return names

    def save(self, *args, **kwargs):
        if self.order_date == None:
            self.order_date = str(timezone.localdate())
        if self.num_kanar_lots== None :
            self.num_kanar_lots=0
        if self.num_makok_lots == None :
            self.num_makok_lots=0
        if self.num_sdh_lots== None:
            self.num_sdh_lots=0
        if self.shift_id==None:
            self.shift_id=shift_identifier.objects.all().last()
        return super(Daily_Fiber_Order_From_Looms, self).save(*args, **kwargs)

    def get_relted_report(self):
        report=Daily_Report_for_each_internal_Order.objects.get(daily_order_id=self)
        if report == None :
            report=Daily_Report_for_each_internal_Order(makok_production_amount=0,sebah_production_amount=0,
                                                        kanar_production_amount=0,total_production_amount=0,
                                                       shift= extruder_shift.objects.last(),report_date=timezone.localdate(),daily_order_id=self).save()
            return report
        else:
            return report



########################################################################extruder
class Lot_Identifiers(models.Model):
    TYPES=(('سيبة','سيبة'),('مكوك','مكوك'),('كنار','كنار'))
    SHIFTS=(('صباحية','صباحية'),('مسائية','مسائية'))
    extroders = (('1400', '1400'), ('1500/1', '1500/1'), ('1500/2', '1500/2'),)
    lot_id=models.AutoField(primary_key=True)
    extruder_id=models.CharField(max_length=10,choices=extroders)
    fiber_id=models.IntegerField()

    fiber_type=models.CharField(max_length=10,choices=TYPES)
    delievry_id=models.CharField(max_length=100,null=True)
    lot_date=models.DateTimeField()
    daily_order_id=models.ForeignKey(Daily_Fiber_Order_From_Looms,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.lot_id)



######################################################################workers name for daily order from looms to extruder
class loomers_related_daily_order_of_looms_to_extruder(models.Model):
    loomer_name=models.CharField(max_length=100)
    order_id=models.ForeignKey(Daily_Fiber_Order_From_Looms,on_delete=models.CASCADE)
    mkok_lots_num=models.IntegerField()
    sebh_lots_num = models.IntegerField()
    kanar_lots_num = models.IntegerField()
    def __str__(self):
        return loomers_related_daily_order_of_looms_to_extruder
    def save(self, *args, **kwargs):
        if self.sebh_lots_num == None:
            self.sebh_lots_num =0
        if self.mkok_lots_num == None:
            self.mkok_lots_num = 0
        if self.kanar_lots_num == None:
            self.kanar_lots_num = 0

        return super(loomers_related_daily_order_of_looms_to_extruder, self).save(*args, **kwargs)

##################################################################daily extroder report









class Daily_Extroder_Report_For_Each_Extruder(models.Model):
    extroders = (('1400', '1400'), ('1500/1', '1500/1'), ('1500/2', '1500/2'),)
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    report_id=models.AutoField(primary_key=True)
    extroder_id=models.CharField(max_length=10,choices=extroders)
    worker_id=models.CharField(max_length=100)
    pp_consumed=models.FloatField()
    ca_consumed=models.FloatField()
    stain_consumed=models.FloatField()
    total_production_amount=models.FloatField()
    report_date=models.DateField()
    shift_id=models.ForeignKey(extruder_shift,on_delete=models.CASCADE)


    def __str__(self):
        return str(self.report_id)

    def save(self, *args, **kwargs):
        self.report_date=timezone.localdate()

        return super(Daily_Extroder_Report_For_Each_Extruder, self).save(*args, **kwargs)



######################################################################################extruder
class Daily_Report_for_each_internal_Order(models.Model):
    extroders = (('1400', '1400'), ('1500/1', '1500/1'), ('1500/2', '1500/2'),)
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    report_id=models.AutoField(primary_key=True)
    makok_production_amount=models.FloatField()#number of produced lots
    sebah_production_amount=models.FloatField()
    kanar_production_amount=models.FloatField()
    total_production_amount=models.FloatField()
    shift_id=models.ForeignKey(extruder_shift,on_delete=models.CASCADE)
    report_date=models.DateTimeField()
    daily_order_id=models.ForeignKey(Daily_Fiber_Order_From_Looms,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.report_id)

    def get_makok_prooduction_amount(self):
        amount = Lot_Identifiers.objects.filter(daily_order_id=self.daily_order_id, fiber_type="مكوك").count()
        self.makok_production_amount = amount
        self.save()
        if amount == None:
            return 0
        else:
            return amount


    def get_sebah_prooduction_amount(self):
        amount=Lot_Identifiers.objects.filter(daily_order_id=self.daily_order_id,fiber_type="سيبة").count()
        self.sebah_production_amount=amount
        self.save()
        if amount == None:
            return 0
        else:
            return amount
    def get_kanar_prooduction_amount(self):
        amount=Lot_Identifiers.objects.filter(daily_order_id=self.daily_order_id,fiber_type="كنار").count()
        self.kanar_production_amount=amount
        self.save()
        if amount == None:
            return 0
        else:
            return amount
    def get_total_production_amount(self):
        amount=self.makok_production_amount+self.sebah_production_amount+self.kanar_production_amount

        self.total_production_amount=amount
        self.save()
        if amount == None:
            return 0
        else:
            return amount

    def save(self, *args, **kwargs):
        if self.makok_production_amount == None:
            self.makok_production_amount =0
        if self.sebah_production_amount == None:
            self.sebah_production_amount = 0
        if self.kanar_production_amount == None:
            self.kanar_production_amount = 0
        if self.total_production_amount == None:
            self.total_production_amount = 0
        if self.report_date == None:
            self.report_date=timezone.localdate()

        return super(Daily_Report_for_each_internal_Order, self).save(*args, **kwargs)

class Daily_extruder_waste(models.Model):
    extroders = (('1400', '1400'), ('1500/1', '1500/1'), ('1500/2', '1500/2'),)
    report_id=models.AutoField(primary_key=True)
    individual_waste=models.FloatField(default=0)
    stop_waste = models.FloatField(default=0)
    container_waste = models.FloatField(default=0)
    pull_waste = models.FloatField(default=0)
    change_waste = models.FloatField(default=0)
    electic_broken_waste= models.FloatField(default=0)
    electic_broken_waste_reson=models.CharField(max_length=1000,null=True)
    ele_repair_order_id=models.IntegerField(null=True)
    mecha_broken_waste = models.FloatField(default=0)
    mechabroken_waste_reson = models.CharField(max_length=1000,null=True)
    mecha_repair_order_id = models.IntegerField(null=True)
    total_waste=models.FloatField(default=0)
    extruder_id=models.CharField(max_length=10,choices=extroders,default="1400")
    extruder_shift_id=models.IntegerField(null=True)
    report_date=models.DateField(default=timezone.localdate())
    def __str__(self):
        return str(self.report_id)





"""    def get_makok_prooduction_amount(self):
        amount=Lot_Identifiers.objects.filter(daily_order_id=self.daily_order_id,fiber_type="مكوك").aggregate(Sum('lot_weight'))
        self.makok_production_amount=amount['lot_weight__sum']
        self.save()
        if amount==  None:
            return 0
        else:
            return amount['lot_weight__sum']

"""

######################################################################################production manager





class loom_internal_order(models.Model):
    STATES = (('متوقف', 'متوقف'), ('جاري التصنيع', 'جاري التصنيع'), ('انتهى', 'انتهى'), ('لم يبدأ', 'لم يبدأ'))
    WEIGHT=(('خفيف','خفيف'),('ثقيل','ثقيل'))
    inte_id=models.AutoField(primary_key=True)
    sch_id=models.ForeignKey(order_sch,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.CharField(max_length=100)
    sebh_fiber_id=models.IntegerField()
    makok_fiber_id=models.IntegerField()
    kanar_fiber_id=models.IntegerField()
    amount=models.FloatField()
    thickness=models.FloatField()
    fiber_weight_Kind = models.CharField(max_length=10, choices=WEIGHT)
    notes=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.inte_id)

    def getItemOrder(self):
        item=Order_item.objects.get(order_id=self.order_id,item_id=self.item_id)
        return item
    def getstartenddate(self):
        sch=order_sch.objects.get(sch_id=self.sch_id.sch_id)
        return sch
counter=0
def post_pre_save_reciver(sender, instance, *args, **kwargs):
    print('hello')
pre_save.connect(post_pre_save_reciver, sender=loom_internal_order)

class coating_internal_order(models.Model):
    STATES = (('متوقف', 'متوقف'), ('جاري التصنيع', 'جاري التصنيع'), ('انتهى', 'انتهى'), ('لم يبدأ', 'لم يبدأ'))
    inte_id=models.AutoField(primary_key=True)
    sch_id=models.ForeignKey(order_sch,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    weight_before=models.FloatField(null=True)
    weight_after=models.FloatField(null=True)
    thickness=models.FloatField()
    amount=models.FloatField()
    notes=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.inte_id)

    def getSchId(self):
        return order_sch.objects.get(sch_id=self.sch_id.sch_id)

    def getRollsForThisInternalOrder(self):
        n= Roll_Identifier.objects.filter(order_id=self.order_id,item_id=self.item_id,need_coating='نعم')
        sum=0
        coating_waste=0
        for i in n:
            temp=Roll_Coating.objects.get(roll_id=i)
            if temp:
                sum+=Roll_weaving.objects.get(roll_id=i).roll_long
                coating_waste+=temp.waste_long
        return sum,coating_waste


class printing_internal_order(models.Model):
    STATES = (('متوقف', 'متوقف'), ('جاري التصنيع', 'جاري التصنيع'), ('انتهى', 'انتهى'), ('لم يبدأ', 'لم يبدأ'))
    inte_id=models.AutoField(primary_key=True)
    sch_id=models.ForeignKey(order_sch,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    amount=models.CharField(max_length=100)

    notes=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.inte_id)

    def getItemOrder(self):
        item = Order_item.objects.get(order_id=self.order_id, item_id=self.item_id)
        return item


    def getSchId(self):
        return order_sch.objects.get(sch_id=self.sch_id.sch_id)


    def getRollsForThisInternalOrder(self):
        n= Roll_Identifier.objects.filter(order_id=self.order_id,item_id=self.item_id,need_printing='نعم')
        sum=0
        for i in n:
            temp=Roll_printing.objects.get(roll_id=i)
            if temp:
                sum+=Roll_weaving.objects.get(roll_id=i).roll_long
        return sum

class cutting_internal_order(models.Model):
    STATES = (('متوقف', 'متوقف'), ('جاري التصنيع', 'جاري التصنيع'), ('انتهى', 'انتهى'), ('لم يبدأ', 'لم يبدأ'))
    inte_id=models.AutoField(primary_key=True)
    sch_id=models.ForeignKey(order_sch,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    amount=models.FloatField()
    notes=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.inte_id)

    def getItemOrder(self):
        item = Order_item.objects.get(order_id=self.order_id, item_id=self.item_id)
        return item

    def getSchId(self):
        return order_sch.objects.get(sch_id=self.sch_id.sch_id)

    def getRollsForThisInternalOrder(self):
        n= Roll_Identifier.objects.filter(order_id=self.order_id,item_id=self.item_id,need_cutting='نعم')
        sum=0
        for i in n:
            sum+=  Roll_cutting.objects.get(roll_id=i).produced_packages
        return sum



###########################################################################looooooooooooooms






class coating_shift(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id=models.AutoField(primary_key=True)
    shift=models.CharField(max_length=10,choices=SHIFTS)
    shift_supervisor_id=models.CharField(max_length=100)
    shift_date=models.DateField()

    def __str__(self):
        return str(self.shift_id)

    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date=timezone.localdate()
        return super(coating_shift, self).save(*args, **kwargs)


class printing_shift(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id = models.AutoField(primary_key=True)
    shift = models.CharField(max_length=10, choices=SHIFTS)
    shift_supervisor_id = models.CharField(max_length=100)
    shift_date = models.DateField()

    def __str__(self):
        return str(self.shift_id)

    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date = timezone.localdate()
        return super(printing_shift, self).save(*args, **kwargs)



class cutting_shift(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id = models.AutoField(primary_key=True)
    shift = models.CharField(max_length=10, choices=SHIFTS)
    shift_supervisor_id = models.CharField(max_length=100)
    shift_date = models.DateField()

    def __str__(self):
        return str(self.shift_id)

    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date = timezone.localdate()
        return super(cutting_shift, self).save(*args, **kwargs)



class sewing_shift(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id = models.AutoField(primary_key=True)
    shift = models.CharField(max_length=10, choices=SHIFTS)
    shift_supervisor_id = models.CharField(max_length=100)
    shift_date = models.DateField()

    def __str__(self):
        return str(self.shift_id)

    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date = timezone.localdate()
        return super(sewing_shift, self).save(*args, **kwargs)




class Roll_Identifier(models.Model):
    roll_id=models.CharField(max_length=100,primary_key=True)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField(null=True)
    need_coating=models.CharField(max_length=10,default='نعم')
    need_printing=models.CharField(max_length=10,default='نعم')
    need_cutting=models.CharField(max_length=10,default='نعم')
    need_sewing = models.CharField(max_length=10, default='نعم')


    def __str__(self):
        return str(self.roll_id)

    def getWeavingInfo(self):
        return Roll_weaving.objects.get(roll_id=self.roll_id)

    def getCoatInfo(self):
        return Roll_Coating.objects.get(roll_id=self.roll_id)

    def getPrintInfo(self):
        return Roll_printing.objects.get(roll_id=self.roll_id)

    def setPropereties(self):
        item = Order_item.objects.get(order_id=self.order_id, item_id=self.item_id)
        if item.coating_or_not!= "نعم" :
            self.need_coating = "لا"


        if item.print_one_face_or_two==0:
            self.need_printing= "لا"
        else :
            self.need_printing = "نعم"
        if item.cutting!="نعم":
            self.need_cutting = "لا"


        print(self.need_coating)
        print(self.need_printing)
        print(self.need_cutting)
        self.save()
        return



class Roll_weaving(models.Model):
    AGREEMENT = (('yes', 'yes'), ('no', 'no'),)
    GROUPS=(('أولى','أولى'),('ثانية','ثانية'),('ثالثة','ثالثة'))
    roll_id=models.ForeignKey(Roll_Identifier,on_delete=models.CASCADE,primary_key=True)
    weaving_date=models.DateField()
    group_id=models.CharField(max_length=10,choices=GROUPS,default='أولى')
    roll_long=models.FloatField()
    loom_id=models.IntegerField()
    current_shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE)
    lommers_id=models.CharField(max_length=100)
    quality_agreement=models.CharField(max_length=10,choices=AGREEMENT,null=True)
    quality_notes=models.CharField(max_length=1000,null=True)

    def save(self, *args, **kwargs):
        if self.weaving_date == None:
            self.weaving_date = timezone.localdate()
        return super(Roll_weaving, self).save(*args, **kwargs)

    def getRollInfo(self):
        return  Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)

    def getItemInfo(self):
        roll=Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)
        item = Order_item.objects.get(order_id=roll.order_id, item_id=roll.item_id)
        return item

    def getFiberInfo(self):
        roll=Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)
        fibers_in_internal_order_to_extruder=Daily_Fiber_Order_From_Looms.objects.get(order_id=roll.order_id, item_id=roll.item_id)
        print(fibers_in_internal_order_to_extruder)
        return fibers_in_internal_order_to_extruder



class Roll_Coating(models.Model):
    AGREEMENT = (('yes', 'yes'), ('no', 'no'),)
    MACHINES = (('1', '1'), ('2', '2'))
    roll_id=models.ForeignKey(Roll_Identifier,on_delete=models.CASCADE,primary_key=True)
    waste_long=models.FloatField()
    coating_date=models.DateField()
    worker_id=models.CharField(max_length=100)
    machine_id=models.IntegerField(default=1,choices=MACHINES)
    thikness=models.FloatField()
    quality_agreement=models.CharField(max_length=10,choices=AGREEMENT,null=True)
    shift_id=models.ForeignKey(coating_shift,on_delete=models.CASCADE)
    quality_notes=models.CharField(max_length=1000,null=True)

    def save(self, *args, **kwargs):
        if self.coating_date == None:
            self.coating_date = timezone.localdate()
        return super(Roll_Coating, self).save(*args, **kwargs)

    def getRollInfo(self):
        return  Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)

class Roll_printing(models.Model):
    MACHINES=(('1','1'),('2','2'),('3','3'),('4','4'))
    AGREEMENT = (('yes', 'yes'), ('no', 'no'),)
    STAINS=(('عادي','عادي'),('حراري','حراري'))
    roll_id=models.ForeignKey(Roll_Identifier,on_delete=models.CASCADE,primary_key=True)
    printing_date=models.DateField()
    machine_id=models.IntegerField(default=1,choices=MACHINES)
    stain_type=models.CharField(max_length=10)
    stain_info=models.CharField(max_length=100)
    worker_id=models.CharField(max_length=100)
    shift_id=models.ForeignKey(printing_shift,on_delete=models.CASCADE)
    quality_agreement=models.CharField(max_length=10,choices=AGREEMENT,null=True)
    quality_notes=models.CharField(max_length=1000,null=True)

    def save(self, *args, **kwargs):
        if self.printing_date == None:
            self.printing_date = timezone.localdate()
        if self.shift_id== None:
            self.shift_id=printing_shift.objects.all().last()
        return super(Roll_printing, self).save(*args, **kwargs)

    def getRollInfo(self):
        return  Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)

    def getItemInfo(self):
        roll=Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)
        item = Order_item.objects.get(order_id=roll.order_id, item_id=roll.item_id)
        return item

class Roll_cutting(models.Model):
    AGREEMENT = (('yes', 'yes'), ('no', 'no'),)
    roll_id=models.ForeignKey(Roll_Identifier,on_delete=models.CASCADE,primary_key=True)
    cutting_date=models.DateField()
    produced_packages=models.IntegerField(default=0)
    machine_id=models.IntegerField(default=0)
    worker_id=models.CharField(max_length=100)
    shift_id=models.ForeignKey(cutting_shift,on_delete=models.CASCADE)
    quality_agreement=models.CharField(max_length=10,choices=AGREEMENT,null=True)
    quality_notes=models.CharField(max_length=1000,null=True)

    def save(self, *args, **kwargs):
        if self.cutting_date == None:
            self.cutting_date = timezone.localdate()
        if self.shift_id== None:
            self.shift_id=cutting_shift.objects.all().last()
        return super(Roll_cutting, self).save(*args, **kwargs)

    def getRollInfo(self):
        return  Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)

    def getItemInfo(self):
        roll=self.getRollInfo()
        item = Order_item.objects.get(order_id=roll.order_id, item_id=roll.item_id)
        return item





class Roll_sewing(models.Model):
    roll_id = models.ForeignKey(Roll_Identifier, on_delete=models.CASCADE, primary_key=True)
    sewing_date = models.DateField()
    shift_id = models.ForeignKey(sewing_shift, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.sewing_date == None:
            self.sewing_date = timezone.localdate()
        if self.shift_id == None:
            self.shift_id = sewing_shift.objects.all().last()
        return super(Roll_sewing, self).save(*args, **kwargs)

    def getRollInfo(self):
        return Roll_Identifier.objects.get(roll_id=self.roll_id.roll_id)

    def getItemInfo(self):
        roll = self.getRollInfo()
        item = Order_item.objects.get(order_id=roll.order_id, item_id=roll.item_id)
        return item

    def getSewingWorker(self):
        return Roll_sewing_two.objects.filter(roll_id=self.roll_id)



class Roll_sewing_two(models.Model):
    roll_id = models.ForeignKey(Roll_Identifier, on_delete=models.CASCADE)
    machine_id=models.IntegerField(default=0)
    job_kind=models.CharField(max_length=100)
    worker_id=models.CharField(max_length=100)




class roll_final_waste(models.Model):
    roll_id=models.ForeignKey(Roll_Identifier,on_delete=models.CASCADE,primary_key=True)
    cutting_waste=models.IntegerField()
    printing_waste=models.IntegerField()
    coating_waste=models.IntegerField()
    weaving_waste=models.IntegerField()
    shift_id=models.ForeignKey(cutting_shift,on_delete=models.CASCADE,null=True)





##samar
class loom_daily_production_report(models.Model):
    report_id=models.AutoField(primary_key=True)
    loom_id=models.IntegerField()
    loomer_id=models.CharField(max_length=100)
    production=models.FloatField()
    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE)
    notes=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.report_id)



class part_internal_order_between_loomers(models.Model):
    GROUPS=(('أولى','أولى'),('ثانية','ثانية'),('ثالثة','ثالثة'))
    parting_id=models.AutoField(primary_key=True)
    inte_id=models.ForeignKey(loom_internal_order,on_delete=models.CASCADE)
    group_id=models.CharField(max_length=10,choices=GROUPS,default='أولى')
    loom_id=models.IntegerField()
    amount=models.IntegerField()
    start_time=models.DateField()
    end_time=models.DateField()
    notes=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.parting_id)

class loom_daily_order_production_report(models.Model):
    report_id=models.AutoField(primary_key=True)
    loom_id=models.IntegerField()
    loomer_id=models.CharField(max_length=100)
    parting_id=models.ForeignKey(part_internal_order_between_loomers,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    production=models.FloatField()
    rest_of_production=models.FloatField()
    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE)
    notes=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.report_id)
    def save(self, *args, **kwargs):
        if self.rest_of_production == None:
            pa=part_internal_order_between_loomers.objects.get(parting_id=self.parting_id.parting_id)
            self.rest_of_production=pa.amount-self.production
        return super(loom_daily_order_production_report, self).save(*args, **kwargs)

class First_Group(models.Model):
    STATES=(('متوقف','متوقف'),('يعمل','يعمل'))
    loom_id=models.IntegerField()
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField(default=0)
    current_produced_amount=models.FloatField(null=True)
    reast_amount=models.FloatField(null=True)
    thickness = models.FloatField(null=True)
    worker_id=models.CharField(max_length=100,null=True)
    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE,null=True)
    state=models.CharField(max_length=10,choices=STATES,default='يعمل')

    def get_internal_order(self):
        return loom_internal_order.objects.get(order_id=self.order_id,item_id=self.item_id)

    def get_item(self):
        return Order_item.objects.get(order_id=self.order_id,item_id=self.item_id)



class Second_Group(models.Model):
    STATES=(('متوقف','متوقف'),('يعمل','يعمل'))
    loom_id=models.IntegerField()
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField(default=0)
    current_produced_amount=models.FloatField(null=True)
    reast_amount=models.FloatField(null=True)
    thickness = models.FloatField(null=True)
    worker_id=models.CharField(max_length=100,null=True)

    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE,null=True)
    state=models.CharField(max_length=10,choices=STATES,default='يعمل')

    def get_internal_order(self):
        return loom_internal_order.objects.get(order_id=self.order_id,item_id=self.item_id)

    def get_item(self):
        return Order_item.objects.get(order_id=self.order_id,item_id=self.item_id)

class Third_Group(models.Model):
    STATES=(('متوقف','متوقف'),('يعمل','يعمل'))
    loom_id=models.IntegerField()
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField(default=0)
    current_produced_amount=models.FloatField(null=True)
    reast_amount=models.FloatField(null=True)
    thickness = models.FloatField(null=True)
    worker_id=models.CharField(max_length=100,null=True)
    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE,null=True)
    state=models.CharField(max_length=10,choices=STATES,default='يعمل')

    def get_internal_order(self):
        return loom_internal_order.objects.get(order_id=self.order_id,item_id=self.item_id)

    def get_item(self):
        return Order_item.objects.get(order_id=self.order_id,item_id=self.item_id)



class printing_daily_report(models.Model):
    MACHINES=(('1','1'),('2','2'),('3','3'),('4','4'))
    report_id=models.AutoField(primary_key=True)
    machine_id=models.IntegerField(choices=MACHINES)
    worker_id=models.CharField(max_length=100)
    shift_id=models.ForeignKey(printing_shift,on_delete=models.CASCADE,null=True)
    total_production=models.FloatField(null=True)

    def __str__(self):
        return str(self.report_id)

    def getOrdersDetails(self):
        return printing_daily_report_two.objects.filter(report_id=self)



class printing_daily_report_two(models.Model):
    report_id_two=models.AutoField(primary_key=True)
    report_id=models.ForeignKey(printing_daily_report,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    meters=models.FloatField()
    consumed_stain=models.FloatField()
    consumed_solvent=models.FloatField()

class coating_daily_report(models.Model):
    report_id=models.AutoField(primary_key=True)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    shift_id=models.ForeignKey(coating_shift,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return str(self.report_id)

    def getOrdersDetails(self):
        return coating_daily_report_two.objects.filter(report_id=self)


class coating_daily_report_two(models.Model):
    report_id_two=models.AutoField(primary_key=True)
    report_id=models.ForeignKey(coating_daily_report,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    meters=models.IntegerField()
    consumed_pp=models.FloatField()
    waste=models.FloatField()

    def getCoatingInfo(self):
        return coating_internal_order.objects.get(order_id=self.order_id,item_id=self.item_id)


class cutting_daily_report(models.Model):
    report_id=models.AutoField(primary_key=True)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    shift_id=models.ForeignKey(cutting_shift,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.report_id)

class cutting_daily_report_two(models.Model):
    report_id_two=models.AutoField(primary_key=True)
    report_id=models.ForeignKey(cutting_daily_report,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    prodused_pockets=models.IntegerField()
    printing_waste=models.FloatField()
    cutting_waste=models.FloatField()
    coating_waste=models.FloatField()
    weaving_waste=models.FloatField()

class looms_update(models.Model):
    GROUPS=(('أولى','أولى'),('ثانية','ثانية'),('ثالثة','ثالثة'))
    update_id=models.AutoField(primary_key=True)
    update_time=models.TimeField()
    group_id=models.CharField(max_length=10,choices=GROUPS)
    looms_id=models.IntegerField()
    update_state=models.CharField(max_length=10000)

class order_follow_up(models.Model):
    STATES=(('متوقف','متوقف'),('جاري التصنيع','جاري التصنيع'),('انتهى','انتهى'))
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    produced_amount=models.FloatField()
    state=models.CharField(max_length=15,choices=STATES,default='جاري التصنيع')

    def getItem(self):
        return Order_item.objects.get(order_id=self.order_id,item_id=self.item_id)


#######################quality

class waste_breach_cutting(models.Model):
    WASTE=(('طباعة','طباعة'),('انوال','انوال'),('قص','قص'))
    report_id=models.AutoField(primary_key=True)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField()
    assicent_id=models.CharField(max_length=100,null=True)
    pockets_num=models.IntegerField()
    waste_reason=models.CharField(max_length=1000)
    department_reason=models.CharField(max_length=15,choices=WASTE)
    roll_id=models.IntegerField()
    sending_time=models.TimeField()
    recived_time=models.TimeField(null=True)
    cutting_shift=models.ForeignKey(cutting_shift,on_delete=models.CASCADE)
    quality_monitor=models.CharField(max_length=100)
    notes=models.CharField(max_length=1000)


class waste_breach_printing(models.Model):
    AGREEMENT = (('yes', 'yes'), ('no', 'no'),)
    report_id=models.AutoField(primary_key=True)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField()
    problem=models.CharField(max_length=1000)
    reason=models.CharField(max_length=1000)
    counter_point=models.FloatField()
    is_updated=models.CharField(max_length=10,choices=AGREEMENT)
    printing_shift=models.ForeignKey(printing_shift,on_delete=models.CASCADE)
    sending_time=models.TimeField()
    recived_time=models.TimeField(null=True)
    roll_id=models.IntegerField()
    notes = models.CharField(max_length=1000)
    quality_monitor=models.CharField(max_length=100)

class waste_breach_looms(models.Model):
    AGREEMENT = (('yes', 'yes'), ('no', 'no'),)
    GROUPS=(('أولى','أولى'),('ثانية','ثانية'),('ثالثة','ثالثة'))
    report_id=models.AutoField(primary_key=True)
    group_id=models.CharField(max_length=15,choices=GROUPS)
    loom_id=models.IntegerField()
    loomer_id=models.CharField(max_length=100)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE,null=True)
    item_id=models.IntegerField(null=True)
    problem=models.CharField(max_length=1000)
    reason=models.CharField(max_length=1000)
    sending_time=models.TimeField()
    recived_time=models.TimeField(null=True)
    roll_id=models.IntegerField()
    counter_point=models.FloatField(null=True)
    loom_shift=models.ForeignKey(shift_identifier,on_delete=models.CASCADE)
    is_updated=models.CharField(max_length=10,choices=AGREEMENT)
    notes = models.CharField(max_length=1000)
    quality_monitor=models.CharField(max_length=100)

class printing_dep(models.Model):
    shift_id=models.ForeignKey(printing_shift,on_delete=models.CASCADE,primary_key=True)
    sum_meters=models.FloatField()
    sum_stain=models.FloatField()
    sum_solvent=models.FloatField()
    breach=models.IntegerField(null=True)
    breach1=models.IntegerField(null=True)
    breach2=models.IntegerField(null=True)
    breach3=models.IntegerField(null=True)
    breach4=models.IntegerField(null=True)
    print_waste_from_cutting=models.FloatField()


class cutting_dep(models.Model):
    shift_id=models.ForeignKey(cutting_shift,on_delete=models.CASCADE,primary_key=True)
    sum_pockets=models.FloatField()
    breach=models.IntegerField(null=True)
    breach1=models.IntegerField(null=True)
    breach2=models.IntegerField(null=True)
    breach3=models.IntegerField(null=True)
    breach4=models.IntegerField(null=True)
    breach5=models.IntegerField(null=True)
    breach6=models.IntegerField(null=True)
    breach7=models.IntegerField(null=True)
    breach8=models.IntegerField(null=True)
    cutting_waste=models.FloatField()


class extruder_dep(models.Model):
    shift_id=models.ForeignKey(extruder_shift,on_delete=models.CASCADE,primary_key=True)
    sum_lots=models.FloatField()
    sum_pp = models.FloatField()
    sum_ca = models.FloatField(default=0)
    sum_stain = models.FloatField(default=0)
    sum_waste=models.FloatField()

###################################################################################3 follow up
class printing_prodution_follow_up_one(models.Model):
    report_id=models.AutoField(primary_key=True)
    shift_id=models.ForeignKey(printing_shift,on_delete=models.CASCADE)

class printing_prodution_follow_up_two(models.Model):
    CHOICES=(('يعمل','يعمل'),('متوقف','متوقف'))
    report_id=models.ForeignKey(printing_prodution_follow_up_one,on_delete=models.CASCADE)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    meters=models.IntegerField()
    machine_state=models.CharField(max_length=10,choices=CHOICES)


class cutting_prodution_follow_up_one(models.Model):
    report_id=models.AutoField(primary_key=True)
    shift_id=models.ForeignKey(cutting_shift,on_delete=models.CASCADE)

class cutting_production_follow_up_two(models.Model):
    CHOICES=(('يعمل','يعمل'),('متوقف','متوقف'))
    report_id=models.ForeignKey(printing_prodution_follow_up_one,on_delete=models.CASCADE)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    assicent_id=models.CharField(max_length=100)
    pockets=models.IntegerField()
    machine_state=models.CharField(max_length=10,choices=CHOICES)

class coating_prodution_follow_up_one(models.Model):
    report_id=models.AutoField(primary_key=True)
    shift_id=models.ForeignKey(coating_shift,on_delete=models.CASCADE)

class coating_production_follow_up_two(models.Model):
    CHOICES=(('يعمل','يعمل'),('متوقف','متوقف'))
    report_id=models.ForeignKey(coating_prodution_follow_up_one,on_delete=models.CASCADE)
    machine_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    pockets=models.IntegerField()
    machine_state=models.CharField(max_length=10,choices=CHOICES)

class weaving_prodution_follow_up(models.Model):
    report_id=models.AutoField(primary_key=True)
    shift_id=models.ForeignKey(shift_identifier,on_delete=models.CASCADE)


class weaving_prodution_follow_up_one(models.Model):
    GROUPS=(('أولى','أولى'),('ثانية','ثانية'),('ثالثة','ثالثة'))
    report_idd=models.ForeignKey(weaving_prodution_follow_up,on_delete=models.CASCADE)
    group_id=models.CharField(max_length=15,choices=GROUPS)

class weaving_production_follow_up_two(models.Model):
    CHOICES=(('يعمل','يعمل'),('متوقف','متوقف'))
    r_id=models.AutoField(primary_key=True)
    report_id=models.ForeignKey(weaving_prodution_follow_up_one,on_delete=models.CASCADE)
    loom_id=models.IntegerField()
    worker_id=models.CharField(max_length=100)
    current_produced_amount=models.IntegerField()
    tate=models.CharField(max_length=10,choices=CHOICES)




###############################################################################################################33packing


class packing_rolls(models.Model):
    PACKERS=(('أول','أول'),('ثاني','ثاني'),('ثالث','ثالث'))
    roll_id=models.CharField(max_length=100,primary_key=True)
    packer_id=models.CharField(max_length=10,choices=PACKERS)
    worker_id=models.CharField(max_length=100)
    recorder_id=models.CharField(max_length=100)
    packing_date=models.DateField(auto_now_add=True,null=True)

    def getRollInfo(self):
        return Roll_Identifier.objects.get(roll_id=self.roll_id)



class packs_barcode(models.Model):
    roll_id=models.ForeignKey(packing_rolls,on_delete=models.CASCADE)
    pac_id=models.CharField(max_length=100)
    pockets_num=models.IntegerField()

######################################################################################AD STAR




class adstar_shift(models.Model):
    SHIFTS = (('صباحية', 'صباحية'), ('مسائية', 'مسائية'))
    shift_id=models.AutoField(primary_key=True)
    shift=models.CharField(max_length=10,choices=SHIFTS)
    shift_supervisor_id=models.CharField(max_length=100)
    shift_date=models.DateField()

    def __str__(self):
        return str(self.shift_id)
    def save(self, *args, **kwargs):
        if self.shift_date == None:
            self.shift_date=timezone.localdate()
        return super(adstar_shift, self).save(*args, **kwargs)


class AD_daily_report_one(models.Model):
    MACHINES=(('أولى','أولى'),('ثانية','ثانية'),('ثالثة','ثالثة'))
    report_id=models.AutoField(primary_key=True)
    machine_id=models.CharField(max_length=10,choices=MACHINES)
    worker_id=models.CharField(max_length=100)
    shift_id=models.ForeignKey(adstar_shift,on_delete=models.CASCADE)
    production_amount = models.FloatField(default=0)


class AD_daily_report_two(models.Model):
    report_id_two = models.AutoField(primary_key=True)
    report_id=models.ForeignKey(AD_daily_report_one,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Productio_order,on_delete=models.CASCADE)
    item_id=models.IntegerField()
    packages=models.IntegerField(default=0)
    printing_waste=models.FloatField(default=None)
    cutting_waste=models.FloatField(default=None)
    coating_waste=models.FloatField(default=None)
    weaving_waste=models.FloatField(default=None)


######################################################################################3

class Raw_Material_Order_one(models.Model):
    agreement = (('لا', 'لا'), ('نعم', 'نعم'))
    DERPARTMENT = (('الخيوط', 'الخيوط'), ('الطلي', 'الطلي'))
    report_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100, choices=DERPARTMENT)
    warehouse_worker = models.CharField(max_length=100, default="لم يحدد")
    handed = models.CharField(max_length=100, default="لم يحدد")
    supervisor_id = models.CharField(max_length=100)
    order_date = models.DateField(null=True)

    def __str__(self):
        return str(self.report_id)


class Raw_Material_Order_two(models.Model):
    UNITS = (('طن', 'طن'), ('كغ', 'كغ'))
    MATERIAL = (('بولي بروبيلين', 'بولي بروبيلين'), ('كربونات', 'كربونات'), ('أصبغة', 'أصبغة'))
    idd = models.AutoField(primary_key=True)
    report_id = models.ForeignKey(Raw_Material_Order_one, on_delete=models.CASCADE)
    material_id = models.CharField(max_length=15, choices=MATERIAL, default="بولي بروبيلين")
    unit = models.CharField(max_length=10, choices=UNITS)
    material_describtion = models.CharField(max_length=100, default="لا يوجد")
    amount = models.FloatField()
    recived_amount = models.FloatField(default=0)
    send_amount = models.FloatField(default=0)
    machine_id = models.CharField(max_length=10)

############3
class Central_Warehouse_Order_one(models.Model):
    agreement = (('لا', 'لا'), ('نعم', 'نعم'))
    DERPARTMENT = (('الخيوط', 'الخيوط'), ('الطلي', 'الطلي'))
    report_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100, choices=DERPARTMENT)
    warehouse_worker = models.CharField(max_length=100, default="لم يحدد")
    handed = models.CharField(max_length=100, default="لم يحدد")
    supervisor_id = models.CharField(max_length=100)
    order_date = models.DateField(null=True)

    def __str__(self):
        return str(self.report_id)


class Central_Warehouse_Order_two(models.Model):
    UNITS = (('طن', 'طن'), ('كغ', 'كغ'))
    MATERIAL = (('بولي بروبيلين', 'بولي بروبيلين'), ('كربونات', 'كربونات'), ('أصبغة', 'أصبغة'))
    idd = models.AutoField(primary_key=True)
    report_id = models.ForeignKey(Raw_Material_Order_one, on_delete=models.CASCADE)
    material_id = models.CharField(max_length=15, choices=MATERIAL, default="بولي بروبيلين")
    unit = models.CharField(max_length=10, choices=UNITS)
    material_describtion = models.CharField(max_length=100, default="لا يوجد")
    amount = models.FloatField()
    recived_amount = models.FloatField(default=0)
    send_amount = models.FloatField(default=0)
    machine_id = models.CharField(max_length=10)

###############################################################################################################attendence
class Worker_Identifier(models.Model):
    worker_id=models.AutoField(primary_key=True)
    worker_name=models.CharField(max_length=100)
    worker_dep=models.CharField(max_length=15)
    worker_position=models.CharField(max_length=100)

    def __str__(self):
        return self.worker_name

class attendence_report(models.Model):
    report_id=models.AutoField(primary_key=True)
    department=models.CharField(max_length=15)
    shift_id=models.IntegerField()

class supervisor_attendence(models.Model):
    report_id=models.ForeignKey(attendence_report,on_delete=models.CASCADE)
    machine_id=models.CharField(max_length=15)
    worker_id=models.ForeignKey(Worker_Identifier,on_delete=models.CASCADE)
    assicent_id=models.CharField(max_length=100,null=True)


class Other_Worker_attendence(models.Model):
    report_id=models.ForeignKey(attendence_report,on_delete=models.CASCADE)
    worker_id=models.ForeignKey(Worker_Identifier,on_delete=models.CASCADE)

class Other_worker_absence(models.Model):
    report_id=models.ForeignKey(attendence_report,on_delete=models.CASCADE)
    worker_id=models.ForeignKey(Worker_Identifier,on_delete=models.CASCADE)
    reason=models.CharField(max_length=100)




