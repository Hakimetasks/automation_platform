import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from .models import User, ReferenceCheck

@csrf_exempt
def request_login(request):
    """1.2.2 & 4.1.1: Phone-number-only authentication - Step 1"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()
        
        if not phone_number:
            return JsonResponse({'error': 'Phone number is required'}, status=400)
        
        # 2.1.1: Generate a unique Reference Number
        reference_number = f"REF-{random.randint(100000, 999999)}"
        
        # Get or create user
        user, created = User.objects.get_or_create(phone_number=phone_number)
        
        if user.is_frozen:
            return JsonResponse({'error': 'Account is frozen'}, status=403)
            
        # Create Reference Check entry for verification
        ReferenceCheck.objects.create(user=user, reference_number=reference_number)
        
        return JsonResponse({
            'message': 'Reference number generated successfully',
            'reference_number': reference_number,
            'is_new_user': created
        })
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def verify_login(request):
    """2.1.2 & 4.1.1: Verify reference and authenticate user with Anti-Brute Force"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()
        reference_number = data.get('reference_number', '').strip()
        
        if not phone_number or not reference_number:
            return JsonResponse({'error': 'Phone number and reference number are required'}, status=400)
            
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
            
        if user.is_frozen:
            return JsonResponse({'error': 'Account is frozen'}, status=403)
            
        # የቅርብ ጊዜውን ያልተረጋገጠ የሪፈረንስ ሙከራ ፈልግ
        ref_check = ReferenceCheck.objects.filter(user=user, is_verified=False).last()
        
        if not ref_check:
            return JsonResponse({'error': 'No active login request found'}, status=400)
            
        # 2.1.2: Anti-Brute Force (ከ 3 ሙከራ በላይ ከሆነ አካውንቱን እገድበዋለን)
        if ref_check.attempts >= 3:
            user.is_frozen = True
            user.save()
            return JsonResponse({'error': 'Too many failed attempts. Account has been frozen.'}, status=403)
            
        if ref_check.reference_number == reference_number:
            ref_check.is_verified = True
            ref_check.save()
            
            # የተሳካ መግቢያ
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'phone_number': user.phone_number,
                'balance': str(user.balance)
            })
        else:
            ref_check.attempts += 1
            ref_check.save()
            remaining = 3 - ref_check.attempts
            return JsonResponse({
                'error': 'Invalid reference number',
                'attempts_remaining': remaining
            }, status=401)
            
    return JsonResponse({'error': 'Invalid method'}, status=405)

from django.shortcuts import render

def login_page(request):
    """Render the login frontend page"""
    return render(request, 'core/login.html')
