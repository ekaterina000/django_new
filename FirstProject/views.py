import hashlib
from django.shortcuts import render, redirect
from FirstProject.models import Resident, Housing, Government, District, Citie
from FirstProject.forms import HousingForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def register_resident(request):
    if request.method == 'GET':
        form = residentForm()
        print("1111")
        return render(request, 'registerResident.html', {'form': form})
    else:
        print("2222")
        form = residentForm(request.POST)
        if form.is_valid():
            print("3333")
            Resident.objects.filter(id_user_id=request.user).update(first_name=form.cleaned_data['first_name'],
                                                                    last_name=form.cleaned_data['last_name'],
                                                                    district=form.cleaned_data['district'],
                                                                   )
            print("4444")
            return redirect('/info')
        else:
            print("asdfasdfasdf")

def show_info(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Government").exists():
            government = Government.objects.get(id_user_id=user.id)
            cities = list(Citie.objects.filter(government_id=government.id))
            return render(request, 'GovernmentView.html', {"cities": cities})
        else:
            resident = Resident.objects.get(id_user_id=user.id)
            housings = list(Housing.objects.filter(resident=resident.id))
            return render(request, 'residentInfo.html',
                          {"resident": resident,
                           "link_img": hashlib.md5(user.email.encode('utf-8')).hexdigest(),
                           "housings": housings
                           })
    else:
        return redirect("/")


def show_resident(request, name_city, id_district,  id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Government").exists():
        resident = Resident.objects.get(id_user_id=id_user)
        housings = list(Housing.objects.filter(resident=resident.id))
        return render(request, 'residentInfo.html',
                      {"resident": resident,
                       "link_img": hashlib.md5(User.objects.get(id=resident.id_user_id).email.encode('utf-8')).hexdigest(),
                       "housings": housings,
                       "name_city": name_city,
                       "id_district": id_district})
    else:
        return render(request, 'notAccess.html')


def show_residentFromGovernment(request, name_city, id_district,  id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Government").exists():
        resident = Resident.objects.get(id_user_id=id_user)
        housings = list(Housing.objects.filter(resident=resident.id))
        return render(request, 'GovernmentResidentInfo.html',
                      {"resident": resident,
                       "link_img": hashlib.md5(User.objects.get(id=resident.id_user_id).email.encode('utf-8')).hexdigest(),
                       "housings": housings,
                       "name_city": name_city,
                       "id_district": id_district})
    else:
        return render(request, 'notAccess.html')


def show_index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info")
        else:
            return render(request, 'index.html')
    else:
        print(request.body)
        if (request.POST.get("email") != None):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
                return redirect("/info")
            except Exception:
                print("Not correct email or pass")
                return redirect("")

        else:
            email = request.POST.get("create_email")
            username = request.POST.get("create_user_name")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return redirect("/info")


def create_housing(request, name_city, id_district, id_user):

    if request.method == "GET":
        housingForm = HousingForm()
        return render(request, "templateForm.html", {"form": housingForm})
    else:
        housingform = HousingForm(request.POST)
        if housingform.is_valid():

            obj = Housing.objects.create(
                resident_id=Resident.objects.get(id_user_id=id_user).id,
                area=housingform.cleaned_data['area'],
                address=housingform.cleaned_data['address'],
                cost=housingform.cleaned_data['cost'])

            return redirect(f"/governmentView/{name_city}/{id_district}/{id_user}")
        else:
            return redirect("/")


def delete_housing(request, name_city, id_district, id_user, area_housing):
    resident_id = Resident.objects.get(id_user_id=id_user).id
    housing = Housing.objects.filter(area=area_housing, resident_id=resident_id).first().delete()

    if User.objects.get(id=id_user).groups.filter(name="Government").exists():
        return redirect(f"/governmentView/{name_city}/{id_district}/{id_user}")
    return redirect(f"/governmentView/{name_city}/{id_district}/{id_user}")


def show_district_ofCity(request, name_city):
    city = Citie.objects.get(name_city=name_city)
    districts = city.districts.filter(citie=city.name_city)
    return render(request, 'GovernmentViewDistrict.html', {"districts": districts, "name_city": name_city})


def show_residentFromDistrict(request, id_district, name_city):
    residents = Resident.objects.filter(district=District.objects.get(id=id_district))
    residentsSumHousing = []
    for resident in residents:
        residentHousings = Housing.objects.filter(resident_id=resident.id)
        sumCosts = sum(map(lambda x: x.cost, residentHousings))
    residentsSumHousing.append(sumCosts)
    residents = zip(residents, residentsSumHousing)
    return render(request, 'GovernmentViewResidents.html', {"residents": residents,
                                                            "name_city": name_city,
                                                            "id_district": id_district})


def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def validate_email(request):
    email = request.GET.get('create_email', None)
    response = {
        'taken': User.objects.filter(email__exact=email).exists()
    }
    return JsonResponse(response)