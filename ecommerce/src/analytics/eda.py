import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 改用其中一個可用的 seaborn 風格
plt.style.use('seaborn-v0_8')  # 或是使用 'seaborn-darkgrid'
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class EcommerceAnalyzer:
    def __init__(self, db_path='ecommerce.db'):
        self.conn = sqlite3.connect(db_path)
        
    def load_data(self):
        # 載入主要分析所需的資料
        self.orders_df = pd.read_sql("""
            SELECT o.*, c.customer_since
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
        """, self.conn)
        
        self.order_items_df = pd.read_sql("""
            SELECT oi.*, p.sku, c.name as category_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
        """, self.conn)
        
    def analyze_sales_trends(self):
        # 將 created_at 轉換為日期格式
        self.orders_df['created_at'] = pd.to_datetime(self.orders_df['created_at'])
        
        # 按日期統計銷售額
        daily_sales = self.orders_df.groupby('created_at')['grand_total'].sum().reset_index()
        
        plt.figure(figsize=(15, 6))
        plt.plot(daily_sales['created_at'], daily_sales['grand_total'])
        plt.title('每日銷售額趨勢')
        plt.xlabel('日期')
        plt.ylabel('銷售額')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('./data/processed/image/daily_sales_trend.png')
        plt.close()
        
    def analyze_category_distribution(self):
        # 分析類別分布
        category_sales = self.order_items_df.groupby('category_name').agg({
            'qty_ordered': 'sum',
            'price': lambda x: (x * self.order_items_df.loc[x.index, 'qty_ordered']).sum()
        }).reset_index()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=category_sales.sort_values('price', ascending=False),
                   x='category_name', y='price')
        plt.title('各類別銷售總額')
        plt.xlabel('類別')
        plt.ylabel('銷售額')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('./data/processed/image/category_sales.png')
        plt.close()
        
    def analyze_payment_methods(self):
        # 分析支付方式
        payment_stats = self.orders_df['payment_method'].value_counts()
        
        plt.figure(figsize=(10, 6))
        payment_stats.plot(kind='pie', autopct='%1.1f%%')
        plt.title('支付方式分布')
        plt.axis('equal')
        plt.savefig('./data/processed/image/payment_methods.png')
        plt.close()
        
    def generate_summary_stats(self):
        # 產生摘要統計
        summary = {
            '訂單總數': f"{len(self.orders_df):,}",
            '總銷售額': f"${self.orders_df['grand_total'].sum():,.2f}",
            '平均訂單金額': f"${self.orders_df['grand_total'].mean():,.2f}",
            '不同商品類別數': f"{self.order_items_df['category_name'].nunique():,}",
            '不同顧客數': f"{self.orders_df['customer_id'].nunique():,}"
        }
        return pd.Series(summary)
    
    def analyze_order_status(self):
        # 分析訂單狀態分布
        status_stats = self.orders_df['status'].value_counts()
        
        plt.figure(figsize=(10, 6))
        status_stats.plot(kind='bar')
        plt.title('訂單狀態分布')
        plt.xlabel('狀態')
        plt.ylabel('訂單數量')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('./data/processed/image/order_status.png')
        plt.close()
        
        # 計算訂單完成率
        completion_rate = (status_stats['complete'] / len(self.orders_df)) * 100
        return f"訂單完成率: {completion_rate:.2f}%"

    def analyze_hourly_patterns(self):
        # 提取小時資訊
        self.orders_df['hour'] = pd.to_datetime(self.orders_df['created_at']).dt.hour
        
        # 分析每小時訂單量
        hourly_orders = self.orders_df.groupby('hour').size()
        
        plt.figure(figsize=(12, 6))
        hourly_orders.plot(kind='line', marker='o')
        plt.title('每小時訂單量分布')
        plt.xlabel('小時')
        plt.ylabel('訂單數量')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('./data/processed/image/hourly_orders.png')
        plt.close()

    def analyze_price_distribution(self):
        # 建立價格區間
        self.order_items_df['price_range'] = pd.cut(
            self.order_items_df['price'],
            bins=[0, 500, 1000, 5000, 10000, float('inf')],
            labels=['0-500', '501-1000', '1001-5000', '5001-10000', '10000+']
        )
        
        # 分析價格區間分布
        price_dist = self.order_items_df['price_range'].value_counts().sort_index()
        
        plt.figure(figsize=(10, 6))
        price_dist.plot(kind='bar')
        plt.title('商品價格區間分布')
        plt.xlabel('價格區間')
        plt.ylabel('商品數量')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('./data/processed/image/price_distribution.png')
        plt.close()

    def analyze_category_correlations(self):
        # 建立購物籃分析矩陣
        order_categories = self.order_items_df.groupby(['order_id', 'category_name']).size().unstack(fill_value=0)
        
        # 計算類別間的相關性
        category_corr = order_categories.corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(category_corr, annot=True, cmap='coolwarm', center=0)
        plt.title('類別關聯性熱力圖')
        plt.tight_layout()
        plt.savefig('./data/processed/image/category_correlations.png')
        plt.close()

    def analyze_customer_behavior(self):
        # 計算每個客戶的統計數據
        customer_stats = self.orders_df.groupby('customer_id').agg({
            'order_id': 'count',
            'grand_total': ['sum', 'mean'],
            'created_at': lambda x: (x.max() - x.min()).days
        }).reset_index()
        
        customer_stats.columns = ['customer_id', 'order_count', 'total_spent', 'avg_order_value', 'days_active']
        
        # 計算客戶存活期間的平均消費頻率
        customer_stats['purchase_frequency'] = customer_stats['order_count'] / customer_stats['days_active'].clip(lower=1)
        
        # 繪製消費頻率分布圖
        plt.figure(figsize=(10, 6))
        sns.histplot(data=customer_stats, x='purchase_frequency', bins=50)
        plt.title('客戶購買頻率分布')
        plt.xlabel('每日平均購買頻率')
        plt.ylabel('客戶數量')
        plt.tight_layout()
        plt.savefig('./data/processed/image/customer_purchase_frequency.png')
        plt.close()

def main():
    analyzer = EcommerceAnalyzer()
    analyzer.load_data()
    
    # 執行各項分析
    analyzer.analyze_sales_trends()
    analyzer.analyze_category_distribution()
    analyzer.analyze_payment_methods()
    analyzer.analyze_order_status()
    analyzer.analyze_hourly_patterns()
    analyzer.analyze_price_distribution()
    analyzer.analyze_category_correlations()
    analyzer.analyze_customer_behavior()
    
    # 印出摘要統計
    print("\n=== 電商平台分析摘要 ===")
    print(analyzer.generate_summary_stats())

if __name__ == "__main__":
    main()
