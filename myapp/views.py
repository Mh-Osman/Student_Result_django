from django.shortcuts import render
from django.http import HttpResponse
from .models import Institution
from .models import student,result
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.


def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'institution_form':
            name = request.POST.get('name')
            email = request.POST.get('email')
            uid = request.POST.get('uid')

            # Check if UID exists
            if Institution.objects.filter(uid=uid).exists():
                institution = Institution.objects.get(uid=uid)

                # If name and email also match, allow access
                if institution.name == name and institution.email == email:
                    messages.success(request, 'Access granted.')
                    return redirect('institution', name=name, uid=uid)
                else:
                    messages.error(request, 'UID already exists, but Name or Email does not match.')
                    return render(request, 'index.html', {'name': name, 'email': email, 'uid': uid})

            # If UID does not exist, create a new institution
            Institution.objects.create(name=name, email=email, uid=uid)
            messages.success(request, 'Institution created successfully.')
            return redirect('institution', name=name, uid=uid)

        elif form_type == 'student_form':
            uid = request.POST.get('uid')
            roll = request.POST.get('roll')
            # You can add more logic here if needed
            messages.success(request, f"Student UID submitted: {uid}, Roll Number: {roll}")
            return redirect('students', roll=roll)

    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')


def institution(request, name, uid):
    if request.method == 'POST':
        result_entries = []
        for key in request.POST:
            if key.startswith('subject_'):
                index = key.split('_')[1]
                subject = request.POST.get(f'subject_{index}')
                mid = request.POST.get(f'mid_{index}')
                final = request.POST.get(f'final_{index}')
                student_id = request.POST.get(f'sid_{index}')
                student_roll = request.POST.get(f'roll_{index}')
                full_mark = request.POST.get(f'full_mark_{index}', 100)  # Default to 100 if not provided


                try:
                    mid = int(mid)
                    final = int(final)
                    student_obj = student.objects.get(roll=student_roll)
                    total = mid + final
                except (ValueError, student.DoesNotExist):
                    continue

                result_entries.append(result(
                    student=student_obj,
                    subject=subject,
                    mid=mid,
                    final=final,
                    total=total,

                ))

        result.objects.bulk_create(result_entries)
        return redirect('institution', name=name, uid=uid)

    all_students = student.objects.filter(uid=uid)
    try:
        institution = Institution.objects.get(name=name)
    except Institution.DoesNotExist:
        return HttpResponse("Institution not found", status=404)

    return render(request, 'institution.html', {'institution': institution, 'students': all_students})

def add_student(request, name , uid):
    
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_email = request.POST.get('student_email')
        roll = request.POST.get('roll')

        institution = Institution.objects.get(name=name)
        student.objects.create(name=student_name, email=student_email, uid=uid, roll=roll, institution=institution)
        return redirect('institution', name=name, uid=uid)

    return render(request, 'add_student.html', {'institution_name': name})


def students(request, roll):
    try:
        student_instance = student.objects.get(roll=roll)
        results = result.objects.filter(student=student_instance)
    except student.DoesNotExist:
         return render(request, 'student_not_found.html', status=404)

    return render(request, 'student.html', {'student': student_instance, 'results': results})





