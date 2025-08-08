import json
from jinja2 import Environment, FileSystemLoader
import datetime
import shutil
import os

class HTMLUpdater:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.data = self.load_data()
        
    def load_data(self):
        """تحميل البيانات من ملف JSON"""
        try:
            with open('data/daily_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Data file not found. Using default data.")
            return self.get_default_data()
    
    def get_default_data(self):
        """بيانات افتراضية في حالة عدم وجود البيانات"""
        return {
            'dubai_market': {
                'index': 6133.13,
                'change': '+0.37%',
                'volume': '254,636,802',
                'value': '745,710,563.77'
            },
            'abu_dhabi_market': {
                'fadgi': 10317.01,
                'fadgi_change': '-0.121%',
                'fadx15': 10814.71,
                'fadx15_change': '-0.021%'
            },
            'stocks': {
                'DEWA': {'price': 2.73, 'change': '+0.36%'},
                'SALIK': {'price': 6.54, 'change': '+0.90%'},
                'TALABAT': {'price': 1.27, 'change': '+0.78%'},
                'NMDC': {'price': 2.560, 'change': '-0.775%'}
            },
            'last_updated': datetime.datetime.now().isoformat()
        }
    
    def update_index_page(self):
        """تحديث الصفحة الرئيسية"""
        template = self.env.get_template('index.html')
        
        # إعداد البيانات للقالب
        template_data = {
            'dubai_market': self.data['dubai_market'],
            'abu_dhabi_market': self.data['abu_dhabi_market'],
            'stocks': self.data['stocks'],
            'last_updated': self.data['last_updated'],
            'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # توليد HTML
        html_content = template.render(**template_data)
        
        # حفظ الصفحة
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Index page updated successfully")
    
    def update_detail_pages(self):
        """تحديث صفحات التفاصيل"""
        stocks = ['dewa', 'salik', 'talabat', 'nmdc_energy']
        
        for stock in stocks:
            template_name = f'{stock}_details.html'
            template = self.env.get_template(template_name)
            
            # إعداد البيانات الخاصة بالسهم
            stock_data = self.get_stock_details(stock)
            
            # توليد HTML
            html_content = template.render(**stock_data)
            
            # حفظ الصفحة
            output_file = f'{stock}_details.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"{stock} details page updated successfully")
    
    def get_stock_details(self, stock_name):
        """الحصول على تفاصيل السهم"""
        stock_map = {
            'dewa': 'DEWA',
            'salik': 'SALIK',
            'talabat': 'TALABAT',
            'nmdc_energy': 'NMDC'
        }
        
        stock_symbol = stock_map[stock_name]
        stock_info = self.data['stocks'][stock_symbol]
        
        # بيانات إضافية لكل سهم
        stock_details = {
            'dewa': {
                'name': 'هيئة كهرباء ومياه دبي',
                'market_cap': '~50B',
                'pe_ratio': '12-14',
                'dividend_yield': '4-5%',
                'recommendation': 'شراء/احتفاظ',
                'prediction': '+5-8%',
                'revenue_sources': [
                    {'name': 'الكهرباء', 'percentage': 60, 'color': 'rgba(255, 99, 132, 0.8)'},
                    {'name': 'المياه', 'percentage': 30, 'color': 'rgba(54, 162, 235, 0.8)'},
                    {'name': 'خدمات أخرى', 'percentage': 10, 'color': 'rgba(255, 205, 86, 0.8)'}
                ]
            },
            'salik': {
                'name': 'شركة سالك',
                'market_cap': '~25B',
                'pe_ratio': '15-17',
                'dividend_yield': '3-4%',
                'recommendation': 'شراء/احتفاظ',
                'prediction': '+3-6%',
                'revenue_sources': [
                    {'name': 'رسوم المرور', 'percentage': 85, 'color': 'rgba(40, 167, 69, 0.8)'},
                    {'name': 'خدمات إدارة المرور', 'percentage': 15, 'color': 'rgba(32, 201, 151, 0.8)'}
                ]
            },
            'talabat': {
                'name': 'طلبات هولدينغ',
                'market_cap': '~15B',
                'pe_ratio': '25-30',
                'dividend_yield': '1-2%',
                'recommendation': 'شراء',
                'prediction': '+8-12%',
                'revenue_sources': [
                    {'name': 'توصيل الطعام', 'percentage': 60, 'color': 'rgba(255, 193, 7, 0.8)'},
                    {'name': 'البقالة الإلكترونية', 'percentage': 25, 'color': 'rgba(253, 126, 20, 0.8)'},
                    {'name': 'الإعلانات والخدمات', 'percentage': 15, 'color': 'rgba(255, 152, 0, 0.8)'}
                ]
            },
            'nmdc_energy': {
                'name': 'NMDC Energy',
                'market_cap': '~20B',
                'pe_ratio': '10-12',
                'dividend_yield': '5-6%',
                'recommendation': 'احتفاظ',
                'prediction': '+2-5%',
                'revenue_sources': [
                    {'name': 'مشاريع الطاقة', 'percentage': 50, 'color': 'rgba(220, 53, 69, 0.8)'},
                    {'name': 'البناء البحري', 'percentage': 30, 'color': 'rgba(232, 62, 140, 0.8)'},
                    {'name': 'الصيانة والخدمات', 'percentage': 20, 'color': 'rgba(255, 99, 132, 0.8)'}
                ]
            }
        }
        
        details = stock_details[stock_name]
        details.update({
            'price': stock_info['price'],
            'change': stock_info['change'],
            'last_updated': self.data['last_updated'],
            'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dubai_market': self.data['dubai_market'],
            'abu_dhabi_market': self.data['abu_dhabi_market']
        })
        
        return details
    
    def update_all_pages(self):
        """تحديث جميع الصفحات"""
        print("Starting HTML update process...")
        self.update_index_page()
        self.update_detail_pages()
        print("All pages updated successfully")
        
        # نسخ الملفات الثابتة
        self.copy_static_files()
    
    def copy_static_files(self):
        """نسخ الملفات الثابتة"""
        static_dirs = ['css', 'js', 'images']
        for dir_name in static_dirs:
            src_dir = f'static/{dir_name}'
            if os.path.exists(src_dir):
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                for file in os.listdir(src_dir):
                    src_file = os.path.join(src_dir, file)
                    dst_file = os.path.join(dir_name, file)
                    shutil.copy2(src_file, dst_file)

if __name__ == "__main__":
    updater = HTMLUpdater()
    updater.update_all_pages()
