from howdy.models import printing_shift,printing_daily_report_two,printing_daily_report,printing_internal_order,waste_breach_printing,\
    cutting_daily_report,cutting_daily_report_two,cutting_shift,printing_dep,waste_breach_cutting,cutting_dep,Daily_Extroder_Report_For_Each_Extruder,\
    Daily_Report_for_each_internal_Order,extruder_shift,Daily_extruder_waste,extruder_dep,order_sch
from django.shortcuts import render,redirect
#################charts
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


#______________________________________________________printing

def printing_department(request):
    count = printing_shift.objects.all().count()
    shift = printing_shift.objects.get(shift_id=count - 1)
    reports = printing_daily_report.objects.filter(shift_id=shift)
    sum_meters = 0
    sum_stain = 0
    sum_solvent = 0
    # num of production meters and consumed stain and solvent for last shift
    for report in reports:
        for i in printing_daily_report_two.objects.filter(report_id=report):
            sum_meters += i.meters
            sum_stain += i.consumed_stain
            sum_solvent += i.consumed_solvent
    # num of breach for ech machine
    breach = waste_breach_printing.objects.filter(printing_shift=shift).count()
    breach1 = waste_breach_printing.objects.filter(printing_shift=shift, machine_id=1).count()
    breach2 = waste_breach_printing.objects.filter(printing_shift=shift, machine_id=2).count()
    breach3 = waste_breach_printing.objects.filter(printing_shift=shift, machine_id=3).count()
    breach4 = waste_breach_printing.objects.filter(printing_shift=shift, machine_id=4).count()

    # printing waste form cutting daily report
    shift2 = cutting_shift.objects.get(shift_id=count - 1)
    waste = cutting_daily_report.objects.filter(shift_id=shift2)
    printing_was_from_cutting = 0
    for w in waste:
        for i in cutting_daily_report_two.objects.filter(report_id=w):
            printing_was_from_cutting += i.printing_waste


    print(shift)
    print(printing_dep.objects.all().last().shift_id)
    print(shift!=printing_dep.objects.all().last().shift_id)
    if shift!=printing_dep.objects.all().last().shift_id:
        printing_dep.objects.create(shift_id=shift, sum_meters=sum_meters, sum_stain=sum_stain,
                                    sum_solvent=sum_solvent,
                                    breach=breach, print_waste_from_cutting=printing_was_from_cutting)
    return render(request,'Owner/charts.html')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        labels_Meters=[x.shift_id for x in printing_shift.objects.all()]
        items_Meters=[x.sum_meters for x in printing_dep.objects.all()]
        items_stain=[x.sum_stain for x in printing_dep.objects.all()]
        items_solvent = [x.sum_solvent for x in printing_dep.objects.all()]
        items_breach=[x.breach for x in printing_dep.objects.all()]
        print(items_breach)
        items_print_waste= [x.print_waste_from_cutting for x in printing_dep.objects.all()]

        data = {
                "labels_Meters": labels_Meters,
                "items_Meters": items_Meters,
                "items_stain":items_stain,
                "items_solvent":items_solvent,
                "items_breach":items_breach,
                "items_print_waste":items_print_waste,

        }
        return Response(data)


#________________________________________________________________________________________cutting


def cutting_department(request):
    count = cutting_shift.objects.all().count()
    shift = cutting_shift.objects.get(shift_id=count - 1)
    reports = cutting_daily_report.objects.filter(shift_id=shift)
    # num of production meters and consumed stain and solvent for last shift
    sum_pockets=0
    cutting_waste=0
    for report in reports:
        for i in cutting_daily_report_two.objects.filter(report_id=report):
            sum_pockets+=i.prodused_pockets
            cutting_waste+=i.cutting_waste

    # num of breach for ech machine
    breach = waste_breach_cutting.objects.filter(printing_shift=shift).count()
    breach1 = waste_breach_cutting.objects.filter(printing_shift=shift, machine_id=1).count()
    breach2 = waste_breach_cutting.objects.filter(printing_shift=shift, machine_id=2).count()
    breach3 = waste_breach_cutting.objects.filter(printing_shift=shift, machine_id=3).count()
    breach4 = waste_breach_cutting.objects.filter(printing_shift=shift, machine_id=4).count()

    # printing waste form cutting daily report

    if shift!=cutting_dep.objects.all().last().shift_id:
        cutting_dep.objects.create(shift_id=shift, sum_pockets=sum_pockets,cutting_waste=cutting_waste,breach=breach)
    return render(request,'Owner/charts_cutting.html')




class ChartDataCutting(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        labels_shifts=[x.shift_id for x in cutting_shift.objects.all()]
        items_pockets=[x.sum_pockets for x in cutting_dep.objects.all()]
        cutting_waste=[x.cutting_waste for x in cutting_dep.objects.all()]
        items_breach=[x.breach for x in cutting_dep.objects.all()]

        data = {
                "labels_shifts": labels_shifts,
                "items_pockets": items_pockets,
                "cutting_waste":cutting_waste,
                "items_breach":items_breach,
         }
        return Response(data)

#_______________________________________________________________________________________extruder


def extruder_department(request):
    count = extruder_shift.objects.all().count()
    shift = extruder_shift.objects.get(shift_id=count - 1)
    reports = Daily_Extroder_Report_For_Each_Extruder.objects.filter(shift_id=shift)
    # amount of primary material consumed in this shift plus waste
    sum_pp=0
    sum_ca=0
    sum_stain=0
    sum_waste=0
    for report in reports:
        wr=Daily_extruder_waste.objects.get(main_report_id=report)
        sum_waste=sum_waste+wr.change_waste+wr.container_waste+wr.individual_waste+wr.electic_broken_waste+wr.mecha_broken_waste
        sum_pp+=report.pp_consumed
        sum_ca+=report.ca_consumed
        sum_stain+=report.stain_consumed

    # num of lots produced in this shift
    reps=Daily_Report_for_each_internal_Order.objects.filter(shift_id=shift)
    sum_lots=0
    for r in reps:
        sum_lots+=r.makok_production_amount+r.sebah_production_amount+r.kanar_production_amount

    if shift!=extruder_dep.objects.all().last().shift_id:
        extruder_dep.objects.create(shift_id=shift,sum_waste=sum_waste,sum_lots=sum_lots,sum_stain=sum_stain,
                                   sum_pp=sum_pp,sum_ca=sum_ca)
    return render(request,'Owner/charts_extruder.html')




class ChartDataExtruder(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        labels_shifts=[x.shift_id for x in extruder_shift.objects.all()]
        items_pp=[x.sum_pp for x in extruder_dep.objects.all()]
        items_ca=[x.sum_ca for x in extruder_dep.objects.all()]
        items_stain=[x.sum_stain for x in extruder_dep.objects.all()]
        items_lots=[x.sum_lots for x in extruder_dep.objects.all()]
        extruder_waste=[x.cutting_waste for x in cutting_dep.objects.all()]


        data = {
                "labels_shifts": labels_shifts,
                "items_pp": items_pp,
                "items_ca":items_ca,
                "items_lots":items_lots,
                "extruder_waste": extruder_waste,
                "items_stain": items_stain,
         }
        return Response(data)


def testt(request):
    return render(request, 'extruder/testHtml.html')



def order_plan_state_owner(request):
    plans=order_sch.objects.filter(state="جاري التصنيع")
    return render(request,'Owner/plaining_states.html',{'plans':plans})
