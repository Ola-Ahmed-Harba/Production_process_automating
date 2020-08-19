from django.contrib.auth.models import  User
from django import forms
from .models import agreements_for_order_sch,order_sch,Productio_order,Order_item,Customer,Productio_order_test2

from .models import  waste_breach_cutting,waste_breach_looms,waste_breach_printing,Roll_sewing,Roll_sewing_two,Roll_cutting,coating_daily_report,coating_daily_report_two,cutting_daily_report,cutting_daily_report_two,printing_daily_report,printing_daily_report_two,cutting_shift,extruder_shift,coating_internal_order,loom_internal_order,order_sch,Daily_extruder_waste,Daily_Extroder_Report_For_Each_Extruder,Productio_order, Order_item,Fiber_Code,Daily_Fiber_Order_From_Looms,\
    loomers_related_daily_order_of_looms_to_extruder,Daily_Extroder_Report_For_Each_Extruder,Lot_Identifiers,Daily_Report_for_each_internal_Order,printing_internal_order,cutting_internal_order,shift_identifier,\
loom_daily_production_report,loom_daily_order_production_report,part_internal_order_between_loomers,Roll_printing,\
    Roll_Coating,Roll_weaving,Roll_Identifier,printing_shift,coating_shift,adstar_shift,AD_daily_report_two,AD_daily_report_one


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)

#______________



class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'user_id', "placeholder": 'Username.'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password', "placeholder": 'Password.'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)



#_______________


class OrderForm(forms.ModelForm):
    class Meta:
        model = Productio_order
        fields = ('id','customer_name', 'start_time', 'delivery_time', 'total_price', 'payment_currency',
                  'payment_way', 'delivery_way','order_status','notes','payment_time_tolerance','isAdstar')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Order_item
        fields = ('item_id', 'makok', 'knar', 'coating_or_not', 'cutting','cutting_kind', 'mobatn', 'modmag', 'item_printing_name',
                  'first_face_colors','second_face_colors', 'print_one_face_or_two', 'item_width','sewing_item', 'item_height', 'item_weight','quantity',
                  'notes','mobatn_height','mobatn_weight','mobatn_width','tolerance_height','tolerance_weight','tolerance_width','peice_price',
                  'batch_depth','batch_height')


#for production manager
class OrderForm_test2(forms.ModelForm):
    class Meta:
        model = Productio_order_test2
        fields = ( 'start_time', 'delivery_time', 'delivery_way','production_manager_agreement')


class customerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('customer_name','email','phones','priority')

class order_sch_Form(forms.ModelForm):
    class Meta:
        model=order_sch
        fields=('order_id','start_loom_date','end_loom_date','loom_fixed','start_coating_date','end_coating_date'
                ,'star_printing_date','end_printing_date','start_cutting_date','end_cutting_date','order_start_date',
                'order_end_date','state','notes','fixedd')


class agreements_for_order_sch_form(forms.ModelForm):
    class Meta:
        model=agreements_for_order_sch
        fields=('ls','le','l_reason','cots','cote','cot_reason',
                'cuts','cute','cut_reason','prs','pre','pr_reason')


#_________________________________________________________________________________________________________________________________

class AddFiberForm(forms.ModelForm):
    class Meta:
        model= Fiber_Code
        fields= ('denier','fiber_width','fiber_color','pp_percent','ca_percent','stain_percent')

############################################for add new order from looms to extruders

class Daily_Fiber_Order_From_Looms_Form(forms.ModelForm):
    class Meta:
        model=Daily_Fiber_Order_From_Looms
        fields=('expected_extruder','makok_fiber_code','sdh_fiber_code','kanar_fiber_code','order_id','item_id')


class loomers_related_daily_order_of_looms_to_extruder_Form(forms.ModelForm):
    class Meta:
        model=loomers_related_daily_order_of_looms_to_extruder
        fields=('loomer_name','mkok_lots_num','sebh_lots_num','kanar_lots_num')

##########################################################extruder


###############################################################add lots form
class Lot_Identifier_Form(forms.ModelForm):
    class Meta:
        model=Lot_Identifiers
        fields=('extruder_id','fiber_id','fiber_type','delievry_id','daily_order_id')

class Daily_Report_For_Each_internal_Order_Form(forms.ModelForm):
    class Meta :
        model=Daily_Report_for_each_internal_Order
        fields=('shift_id','daily_order_id')


class Daily_Extroder_Report_For_Each_Extruder_Form(forms.ModelForm):
    class Meta :
        model=Daily_Extroder_Report_For_Each_Extruder
        fields=('extroder_id','worker_id','pp_consumed','ca_consumed','stain_consumed',)

"""
class  Daily_extruder_waste_Form(forms.ModelForm):
    class Meta:
        model=Daily_extruder_waste
        fields=('individual_waste','stop_waste','container_waste','pull_waste','change_waste','electic_broken_waste','electic_broken_waste_reson','ele_repair_order_id',
                'mecha_broken_waste','mechabroken_waste_reson','mecha_repair_order_id','extruder_shift_id')
"""

#############################################################################production manager

class loom_internal_order_Form(forms.ModelForm):
    class Meta:
        model=loom_internal_order
        fields=('sch_id','item_id','sebh_fiber_id','makok_fiber_id','kanar_fiber_id','amount','thickness',
                'fiber_weight_Kind','notes')

class  coating_internal_order_Form(forms.ModelForm):
    class Meta:
        model= coating_internal_order
        fields=('sch_id',)

class  printing_internal_order_Form(forms.ModelForm):
    class Meta:
        model= printing_internal_order
        fields=('sch_id',)


class cutting_internal_order_Form(forms.ModelForm):
    class Meta:
        model = cutting_internal_order
        fields = ('sch_id', )

#############################################################################loooooooooooms

class shift_identifier_Form(forms.ModelForm):
    class Meta:
        model = shift_identifier
        fields = ('shift', 'shift_supervisor_id')

class loom_daily_production_report_Form(forms.ModelForm):
    class Meta:
        model=loom_daily_production_report
        fields=('loom_id','loomer_id','production','shift_id','notes')


class loom_daily_order_production_report_Form(forms.ModelForm):
    class Meta:
        model = loom_daily_order_production_report
        fields = ('loom_id','loomer_id','parting_id','order_id','item_id','production','shift_id','notes')


class part_internal_order_between_loomers_Form(forms.ModelForm):
    class Meta:
        model = part_internal_order_between_loomers
        fields = ('inte_id' ,'group_id', 'loom_id','amount','start_time','end_time','notes')

class Roll_identifier_Form(forms.ModelForm):
    class Meta:
        model=Roll_Identifier
        fields=('order_id','item_id')


class Roll_weaving_Form(forms.ModelForm):
    class Meta:
        model=Roll_weaving
        fields=('roll_long','group_id','loom_id','lommers_id',)

class Roll_coating_Form(forms.ModelForm):
    class Meta:
        model=Roll_Coating
        fields=('roll_id','waste_long','worker_id','thikness')

class Roll_printing_Form(forms.ModelForm):
    class Meta:
        model=Roll_printing
        fields=('roll_id','stain_type','stain_info','worker_id',)

class shift_identifier_coating_Form(forms.ModelForm):
    class Meta:
        model = coating_shift
        fields = ('shift', 'shift_supervisor_id')

class shift_identifier_printing_Form(forms.ModelForm):
    class Meta:
        model = printing_shift
        fields = ('shift', 'shift_supervisor_id')

class shift_identifier_extruder_Form(forms.ModelForm):
    class Meta:
        model = extruder_shift
        fields = ('shift', 'shift_supervisor_id')

class shift_identifier_cutting_Form(forms.ModelForm):
    class Meta:
        model = cutting_shift
        fields = ('shift', 'shift_supervisor_id')

#printing
class printing_daily_report_Form(forms.ModelForm):
    class Meta:
        model=printing_daily_report
        fields=('worker_id',)

class printing_daily_report_two_Form(forms.ModelForm):
    class Meta:
        model=printing_daily_report_two
        fields=('order_id','item_id','meters','consumed_stain','consumed_solvent')

#cutting
class cutting_daily_report_Form(forms.ModelForm):
    class Meta:
        model=cutting_daily_report
        fields=('worker_id',)

class cutting_daily_report_two_Form(forms.ModelForm):
    class Meta:
        model=cutting_daily_report_two
        fields=('order_id','item_id','prodused_pockets','printing_waste','weaving_waste','coating_waste','cutting_waste')


#coating
class coating_daily_report_Form(forms.ModelForm):
    class Meta:
        model=coating_daily_report
        fields=('worker_id',)

class coating_daily_report_two_Form(forms.ModelForm):
    class Meta:
        model=coating_daily_report_two
        fields=('order_id','item_id','meters','consumed_pp','waste',)


class Roll_cutting_Form(forms.ModelForm):
    class Meta:
        model=Roll_cutting
        fields=('roll_id','machine_id','worker_id','produced_packages')


class waste_breach_cutting_Form(forms.ModelForm):
    class Meta:
        model=waste_breach_cutting
        fields=('machine_id','worker_id','assicent_id','order_id','item_id','pockets_num','waste_reason','department_reason',
                'roll_id','notes',)

class waste_breach_printing_Form(forms.ModelForm):
    class Meta:
        model=waste_breach_printing
        fields=('machine_id','worker_id','problem','order_id','item_id','reason','counter_point','is_updated',
                'roll_id','notes',)

class waste_breach_looms_Form(forms.ModelForm):
    class Meta:
        model=waste_breach_looms
        fields=('group_id','loom_id','problem','reason','counter_point','roll_id','is_updated',
                'notes',)


#######################################################################################################33   adstar

class adstar_shift_Form(forms.ModelForm):
    class Meta:
        model = adstar_shift
        fields = ('shift', 'shift_supervisor_id')

class adstar_daily_report_Form(forms.ModelForm):
    class Meta:
        model=AD_daily_report_one
        fields=('worker_id',)

class adstar_daily_report_two_Form(forms.ModelForm):
    class Meta:
        model=AD_daily_report_two
        fields=('order_id','item_id','packages','printing_waste','weaving_waste','coating_waste','cutting_waste')
