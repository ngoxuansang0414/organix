from django.shortcuts import render
from vi_address.models import Ward, District, City
from django.http import JsonResponse

def select_city(request):
    cities_val = list(City.objects.values())
    return JsonResponse({'data': cities_val})

def select_district(request, *args, **kwargs):
    selected_city = kwargs.get('city')
    districts = list(District.objects.filter(parent_code_id = selected_city).values())
    return JsonResponse({'data': districts})

def select_ward(request, *args, **kwargs):
    selected_district = kwargs.get('district')
    wards = list(Ward.objects.filter(parent_code_id = selected_district).values())
    return JsonResponse({'data': wards})