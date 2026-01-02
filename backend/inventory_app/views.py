"""
Django REST API views
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone as tz
from datetime import date, timedelta, datetime
import json
from .models import Product, DailyCount, Image
from .serializers import (
    ProductSerializer, DailyCountSerializer, ImageSerializer,
    ImageUploadResponseSerializer, WeeklyAnalyticsResponseSerializer,
    RecommendationsResponseSerializer
)
from .services import AnalyticsService, RecommendationService
from .inference_service import InferenceService, StorageService
import os
import tempfile
import time


# Initialize services
inference_service = InferenceService()
storage_service = StorageService()
analytics_service = AnalyticsService()
recommendation_service = RecommendationService()


@csrf_exempt
@api_view(['POST'])
def upload_image(request):
    """Upload a shelf image, run YOLO inference, and store results"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        uploaded_file = request.FILES['file']
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        try:
            # Run inference
            start_time = time.time()
            detections = inference_service.run_inference(tmp_path)
            processing_time = time.time() - start_time
            
            # Upload to storage
            storage_path = storage_service.upload_file(tmp_path, uploaded_file.name)
            
            # Save image metadata
            confidence_summary = str({d["product_name"]: d["confidence"] for d in detections}) if detections else ""
            db_image = Image.objects.create(
                date=timezone.now(),
                path=storage_path,
                confidence_summary=confidence_summary
            )
            
            # Update daily counts
            today = date.today()
            detection_results = []
            total_products = 0
            
            for detection in detections:
                product_name = detection["product_name"]
                count = detection["count"]
                confidence = detection["confidence"]
                
                # Get or create product
                product, _ = Product.objects.get_or_create(
                    name=product_name,
                    defaults={'category': None}
                )
                
                # Update or create daily count
                daily_count, _ = DailyCount.objects.update_or_create(
                    product=product,
                    date=today,
                    defaults={'count': count}
                )
                
                detection_results.append({
                    'product_name': product_name,
                    'count': count,
                    'confidence': confidence
                })
                total_products += count
            
            return Response({
                'image_id': db_image.id,
                'detections': detection_results,
                'total_products': total_products,
                'processing_time': processing_time
            }, status=status.HTTP_200_OK)
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_images(request):
    """Get recent images"""
    try:
        limit = int(request.GET.get('limit', 10))
        if limit < 1 or limit > 100:
            limit = 10
    except (ValueError, TypeError):
        limit = 10
    
    images = Image.objects.all().order_by('-date')[:limit]
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET', 'POST'])
def products(request):
    """Get all products or create a new product"""
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            # DRF automatically parses JSON into request.data
            # Handle both QueryDict and regular dict
            if hasattr(request.data, 'get'):
                name = request.data.get('name', '').strip()
                category = request.data.get('category', '').strip() or None
            else:
                # Fallback: try to parse from body
                try:
                    body_data = json.loads(request.body.decode('utf-8'))
                    name = body_data.get('name', '').strip()
                    category = body_data.get('category', '').strip() or None
                except:
                    # Last resort: form data
                    name = request.POST.get('name', '').strip()
                    category = request.POST.get('category', '').strip() or None
            
            # Debug logging
            print(f"=== PRODUCT CREATE DEBUG ===")
            print(f"Request method: {request.method}")
            print(f"Content-Type: {request.content_type}")
            print(f"Request.data type: {type(request.data)}")
            print(f"Request.data: {request.data}")
            print(f"Name: {name}")
            print(f"Category: {category}")
            
            # Validate name
            if not name:
                print("ERROR: Name is empty")
                return Response({
                    'error': 'نام محصول الزامی است',
                    'message': 'نام محصول الزامی است'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create product
            try:
                product = Product.objects.create(
                    name=name,
                    category=category
                )
                print(f"SUCCESS: Product created with ID {product.id}")
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as db_error:
                print(f"DB ERROR: {str(db_error)}")
                import traceback
                print(traceback.format_exc())
                return Response({
                    'error': f'خطا در ذخیره در دیتابیس',
                    'message': str(db_error)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"=== GENERAL ERROR ===")
            print(f"Error: {str(e)}")
            print(f"Traceback: {error_trace}")
            return Response({
                'error': f'خطا در ذخیره محصول',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_product(request, product_id):
    """Delete a product"""
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def product_counts(request, product_id):
    """Get daily counts for a specific product"""
    try:
        days = int(request.GET.get('days', 7))
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    start_date = date.today() - timedelta(days=days)
    
    counts = DailyCount.objects.filter(
        product_id=product_id,
        date__gte=start_date
    ).order_by('date')
    
    if not counts.exists():
        return Response({'error': 'Product not found or no counts available'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    serializer = DailyCountSerializer(counts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def weekly_analytics(request):
    """Get weekly analytics for all products"""
    try:
        days = int(request.GET.get('days', 7))
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    
    products = Product.objects.all()
    summaries = []
    
    for product in products:
        counts = DailyCount.objects.filter(
            product=product,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')
        
        if counts.count() >= 2:
            count_values = [c.count for c in counts]
            dates_list = [c.date for c in counts]
            
            summary = analytics_service.calculate_product_analytics(
                product_id=product.id,
                product_name=product.name,
                counts=count_values,
                dates=dates_list
            )
            summaries.append(summary)
    
    return Response({
        'start_date': start_date,
        'end_date': end_date,
        'products': summaries
    })


@api_view(['GET'])
def daily_summary(request):
    """Get daily summary for a specific date"""
    target_date_str = request.GET.get('target_date')
    if target_date_str:
        try:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        target_date = date.today()
    
    counts = DailyCount.objects.filter(date=target_date)
    
    return Response({
        'date': target_date,
        'total_products': counts.count(),
        'total_items': sum(c.count for c in counts),
        'products': [
            {
                'product_id': c.product_id,
                'product_name': c.product.name,
                'count': c.count
            }
            for c in counts
        ]
    })


@api_view(['GET'])
def weekly_recommendations(request):
    """Get weekly investment and restocking recommendations"""
    try:
        days = int(request.GET.get('days', 7))
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    
    products = Product.objects.all()
    product_data = []
    
    for product in products:
        counts = DailyCount.objects.filter(
            product=product,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')
        
        if counts.count() >= 3:
            count_values = [c.count for c in counts]
            dates_list = [c.date for c in counts]
            
            product_data.append({
                'product': product,
                'counts': count_values,
                'dates': dates_list
            })
    
    recommendations = recommendation_service.generate_recommendations(
        product_data=product_data,
        start_date=start_date,
        end_date=end_date
    )
    
    return Response({
        'week_start': start_date,
        'week_end': end_date,
        'recommendations': recommendations,
        'generated_at': timezone.now()
    })


def home(request):
    """Home page view"""
    return render(request, 'home.html')


@login_required(login_url='/login/')
def dashboard(request):
    """Dashboard view"""
    return render(request, 'dashboard.html')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید')
            return render(request, 'auth/register.html')
        
        if password != password2:
            messages.error(request, 'رمزهای عبور مطابقت ندارند')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً استفاده شده است')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل قبلاً استفاده شده است')
            return render(request, 'auth/register.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفاً وارد شوید')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'خطا در ثبت نام: {str(e)}')
            return render(request, 'auth/register.html')
    
    return render(request, 'auth/register.html')


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'لطفاً نام کاربری و رمز عبور را وارد کنید')
            return render(request, 'auth/login.html')
        
        # Try to authenticate with username or email
        user = None
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
            return render(request, 'auth/login.html')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('login')


def password_reset_view(request):
    """Password reset request view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'لطفاً ایمیل خود را وارد کنید')
            return render(request, 'auth/password_reset.html')
        
        try:
            user = User.objects.get(email=email)
            # Generate reset token
            reset_token = get_random_string(length=32)
            # In production, save this token to database with expiration
            
            # Send email (configure email settings in settings.py)
            reset_url = f"{request.scheme}://{request.get_host()}/password-reset-confirm/?token={reset_token}&email={email}"
            
            try:
                send_mail(
                    subject='بازیابی رمز عبور - Inventory Management',
                    message=f'برای بازیابی رمز عبور خود روی لینک زیر کلیک کنید:\n{reset_url}',
                    from_email='noreply@inventory.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'لینک بازیابی رمز عبور به ایمیل شما ارسال شد')
            except Exception as e:
                # In development, show the link
                messages.info(request, f'در حالت توسعه، لینک بازیابی: {reset_url}')
        except User.DoesNotExist:
            messages.error(request, 'کاربری با این ایمیل یافت نشد')
        except Exception as e:
            messages.error(request, f'خطا در ارسال ایمیل: {str(e)}')
    
    return render(request, 'auth/password_reset.html')



