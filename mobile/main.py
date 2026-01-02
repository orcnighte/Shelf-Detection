"""
Kivy Mobile App for Inventory Management
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.logger import Logger
import requests
import json
from datetime import datetime, date
from plyer import camera
import os
from pathlib import Path

# API Configuration
API_BASE_URL = "http://192.168.1.100:8000"  # TODO: Change to your backend IP


class MainScreen(Screen):
    """Main screen with camera and daily counts"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='Inventory Manager', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)
        
        # Camera preview area
        self.camera_preview = Image(source='', size_hint_y=0.4)
        layout.add_widget(self.camera_preview)
        
        # Capture button
        capture_btn = Button(text='Capture Image', size_hint_y=None, height=50)
        capture_btn.bind(on_press=self.capture_image)
        layout.add_widget(capture_btn)
        
        # Daily counts
        self.counts_label = Label(
            text='Daily Counts:\n(No data yet)',
            text_size=(None, None),
            halign='left',
            valign='top',
            size_hint_y=0.3
        )
        scroll = ScrollView()
        scroll.add_widget(self.counts_label)
        layout.add_widget(scroll)
        
        # Navigation buttons
        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        analytics_btn = Button(text='Analytics')
        analytics_btn.bind(on_press=self.go_to_analytics)
        nav_layout.add_widget(analytics_btn)
        
        recommendations_btn = Button(text='Recommendations')
        recommendations_btn.bind(on_press=self.go_to_recommendations)
        nav_layout.add_widget(recommendations_btn)
        
        layout.add_widget(nav_layout)
        
        self.add_widget(layout)
        self.load_daily_counts()
    
    def capture_image(self, instance):
        """Capture image using camera"""
        try:
            # Request camera permission and capture
            camera.take_picture(
                filename=self.get_image_path(),
                on_complete=self.on_camera_complete
            )
        except Exception as e:
            Logger.error(f"Camera error: {e}")
            self.show_message("Camera error. Please check permissions.")
    
    def get_image_path(self):
        """Get path for saving image"""
        app_dir = App.get_running_app().user_data_dir
        os.makedirs(os.path.join(app_dir, 'images'), exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(app_dir, 'images', f'capture_{timestamp}.jpg')
    
    def on_camera_complete(self, filename):
        """Handle camera capture completion"""
        if filename and os.path.exists(filename):
            self.camera_preview.source = filename
            self.upload_image(filename)
        else:
            self.show_message("Failed to capture image")
    
    def upload_image(self, image_path):
        """Upload image to backend"""
        try:
            url = f"{API_BASE_URL}/api/v1/images/upload"
            with open(image_path, 'rb') as f:
                files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(url, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.show_message(f"Uploaded! {data.get('total_products', 0)} products detected")
                self.load_daily_counts()
            else:
                self.show_message(f"Upload failed: {response.status_code}")
        except Exception as e:
            Logger.error(f"Upload error: {e}")
            self.show_message(f"Upload error: {str(e)}")
    
    def load_daily_counts(self):
        """Load daily counts from API"""
        try:
            today = date.today().isoformat()
            url = f"{API_BASE_URL}/api/v1/analytics/daily?target_date={today}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                if products:
                    text = "Daily Counts:\n\n"
                    for p in products:
                        text += f"{p['product_name']}: {p['count']}\n"
                    self.counts_label.text = text
                else:
                    self.counts_label.text = "Daily Counts:\n(No data for today)"
            else:
                self.counts_label.text = "Daily Counts:\n(Failed to load)"
        except Exception as e:
            Logger.error(f"Load counts error: {e}")
            self.counts_label.text = "Daily Counts:\n(Connection error)"
    
    def go_to_analytics(self, instance):
        self.manager.current = 'analytics'
    
    def go_to_recommendations(self, instance):
        self.manager.current = 'recommendations'
    
    def show_message(self, message):
        """Show message to user"""
        Logger.info(f"Message: {message}")


class AnalyticsScreen(Screen):
    """Analytics screen with charts and data"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='Analytics', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)
        
        # Analytics content
        self.analytics_label = Label(
            text='Loading analytics...',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        scroll = ScrollView()
        scroll.add_widget(self.analytics_label)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(text='Back', size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        self.load_analytics()
    
    def load_analytics(self):
        """Load weekly analytics"""
        try:
            url = f"{API_BASE_URL}/api/v1/analytics/weekly?days=7"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                if products:
                    text = "Weekly Analytics:\n\n"
                    for p in products:
                        text += f"{p['product_name']}:\n"
                        text += f"  Avg Demand: {p['average_daily_demand']:.2f}\n"
                        text += f"  Growth Rate: {p['growth_rate']:.2f}%\n"
                        text += f"  Consistency: {p['demand_consistency']:.2f}%\n"
                        text += f"  Total: {p['total_count']}\n\n"
                    self.analytics_label.text = text
                else:
                    self.analytics_label.text = "No analytics data available"
            else:
                self.analytics_label.text = "Failed to load analytics"
        except Exception as e:
            Logger.error(f"Analytics error: {e}")
            self.analytics_label.text = f"Error: {str(e)}"
    
    def go_back(self, instance):
        self.manager.current = 'main'


class RecommendationsScreen(Screen):
    """Recommendations screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='Recommendations', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)
        
        # Recommendations content
        self.recommendations_label = Label(
            text='Loading recommendations...',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        scroll = ScrollView()
        scroll.add_widget(self.recommendations_label)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(text='Back', size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        self.load_recommendations()
    
    def load_recommendations(self):
        """Load weekly recommendations"""
        try:
            url = f"{API_BASE_URL}/api/v1/recommendations/weekly?days=7"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get('recommendations', [])
                if recommendations:
                    text = "Weekly Recommendations:\n\n"
                    for i, rec in enumerate(recommendations[:10], 1):  # Top 10
                        text += f"{i}. {rec['product_name']}\n"
                        text += f"   Score: {rec['score']:.2f}\n"
                        text += f"   {rec['explanation']}\n\n"
                    self.recommendations_label.text = text
                else:
                    self.recommendations_label.text = "No recommendations available"
            else:
                self.recommendations_label.text = "Failed to load recommendations"
        except Exception as e:
            Logger.error(f"Recommendations error: {e}")
            self.recommendations_label.text = f"Error: {str(e)}"
    
    def go_back(self, instance):
        self.manager.current = 'main'


class InventoryApp(App):
    """Main Kivy Application"""
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AnalyticsScreen(name='analytics'))
        sm.add_widget(RecommendationsScreen(name='recommendations'))
        return sm


if __name__ == '__main__':
    InventoryApp().run()



