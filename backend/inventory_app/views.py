"""
Django REST API views
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Authentication removed - no login required
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
    try:
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response({
                'error': 'فایل ارسال نشده است',
                'message': 'لطفاً یک فایل تصویر انتخاب کنید'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        
        # Validate file type
        if not uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return Response({
                'error': 'فرمت فایل نامعتبر است',
                'message': 'لطفاً یک فایل تصویر (JPG, PNG, GIF) ارسال کنید'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save uploaded file temporarily
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name
            
            # Run inference (IF/ELSE for two image types)
            start_time = time.time()
            detections = inference_service.run_inference(tmp_path)
            processing_time = time.time() - start_time
            
            if not detections:
                return Response({
                    'error': 'هیچ محصولی شناسایی نشد',
                    'message': 'لطفاً یک تصویر معتبر از قفسه ارسال کنید'
                }, status=status.HTTP_400_BAD_REQUEST)
            
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
                'processing_time': round(processing_time, 2)
            }, status=status.HTTP_200_OK)
        
        finally:
            # Clean up temporary file
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"=== UPLOAD ERROR ===")
        print(f"Error: {str(e)}")
        print(f"Traceback: {error_trace}")
        return Response({
            'error': 'خطا در پردازش تصویر',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_images(request):
    """Get recent images"""
    try:
        limit = int(request.GET.get('limit', 10))
        if limit < 1 or limit > 100:
            limit = 10
    except (ValueError, TypeError):
        limit = 10
    
    try:
        images = Image.objects.all().order_by('-date')[:limit]
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    except Exception as e:
        import traceback
        print(f"=== GET IMAGES ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': 'خطا در دریافت تصاویر',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'POST'])
def products(request):
    """Get all products or create a new product"""
    if request.method == 'GET':
        try:
            products = Product.objects.all().order_by('-id')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'error': 'خطا در دریافت محصولات',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            # Parse request data
            name = None
            category = None
            
            # Try to get from request.data (DRF parsed)
            if hasattr(request, 'data') and request.data:
                if isinstance(request.data, dict):
                    name = request.data.get('name', '').strip()
                    category = request.data.get('category', '').strip() or None
                elif hasattr(request.data, 'get'):
                    name = request.data.get('name', '').strip()
                    category = request.data.get('category', '').strip() or None
            
            # Fallback: try to parse from body
            if not name:
                try:
                    if request.body:
                        body_data = json.loads(request.body.decode('utf-8'))
                        name = body_data.get('name', '').strip()
                        category = body_data.get('category', '').strip() or None
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass
            
            # Last resort: form data
            if not name:
                name = request.POST.get('name', '').strip()
                category = request.POST.get('category', '').strip() or None
            
            # Validate name
            if not name:
                return Response({
                    'error': 'نام محصول الزامی است',
                    'message': 'لطفاً نام محصول را وارد کنید'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if product already exists
            if Product.objects.filter(name=name).exists():
                return Response({
                    'error': 'این محصول قبلاً ثبت شده است',
                    'message': f'محصول "{name}" در سیستم موجود است'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create product
            product = Product.objects.create(
                name=name,
                category=category
            )
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"=== PRODUCT CREATE ERROR ===")
            print(f"Error: {str(e)}")
            print(f"Traceback: {error_trace}")
            return Response({
                'error': 'خطا در ذخیره محصول',
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
        import traceback
        print(f"=== DELETE PRODUCT ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': 'خطا در حذف محصول',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def product_counts(request, product_id):
    """Get daily counts for a specific product"""
    try:
        days = int(request.GET.get('days', 7))
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    try:
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
    except Exception as e:
        import traceback
        print(f"=== PRODUCT COUNTS ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': 'خطا در دریافت تعداد محصولات',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def weekly_analytics(request):
    """Get weekly analytics for all products"""
    try:
        days = int(request.GET.get('days', 7))
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    try:
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
    except Exception as e:
        import traceback
        print(f"=== WEEKLY ANALYTICS ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': 'خطا در دریافت تحلیل‌ها',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def daily_summary(request):
    """Get daily summary for a specific date"""
    try:
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
    except Exception as e:
        import traceback
        print(f"=== DAILY SUMMARY ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': 'خطا در دریافت خلاصه روزانه',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def weekly_recommendations(request):
    """Get weekly investment and restocking recommendations"""
    try:
        days = int(request.GET.get('days', 7))
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    try:
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
    except Exception as e:
        import traceback
        print(f"=== WEEKLY RECOMMENDATIONS ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': 'خطا در دریافت توصیه‌ها',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def home(request):
    """Home page view - redirect to dashboard"""
    return redirect('dashboard')


def dashboard(request):
    """Dashboard view - no authentication required"""
    try:
        return render(request, 'dashboard.html')
    except Exception as e:
        import traceback
        print(f"=== DASHBOARD ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        from django.http import HttpResponse
        return HttpResponse(f'خطا در بارگذاری داشبورد: {str(e)}', status=500)


# Authentication views removed - no login required



