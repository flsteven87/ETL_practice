import logging
import pandas as pd
from datetime import datetime
from src.supermarket.database.models import Branch, ProductLine, Product, Sale
from src.supermarket.database.database_manager import DatabaseManager

# 設定基本的 logging 配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class SuperMarketETL:
    def __init__(self, csv_path):
        logging.info(f"開始初始化 ETL 處理，CSV 路徑: {csv_path}")
        try:
            self.df = pd.read_csv(
                csv_path,
                low_memory=False,
                dtype = {
                    'Invoice ID': str, 
                    'Branch': str, 
                    'City': str, 
                    'Product line': str, 
                    'Unit price': float, 
                    'Quantity': int, 
                    'Tax 5%': float, 
                    'Total': float, 
                    'Time': str, 
                    'Payment': str, 
                    'cogs': float, 
                    'gross income': float,
                    'Rating': float
                }
            )
            logging.info(f"成功載入 CSV 檔案，共 {len(self.df)} 筆資料")
            
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.pre_process_csv()
            self.db_manager = DatabaseManager()
            self.db_manager.reset_database()
            
        except Exception as e:
            logging.error(f"初始化失敗: {str(e)}")
            raise

    def pre_process_csv(self):
        logging.info("開始前處理 CSV 資料")
        try:
            # 移除不需要的欄位
            self.df.drop('gross margin percentage', axis=1, inplace=True)
            
            # 轉換時間格式
            def convert_time_str(time_str):
                try:
                    return datetime.strptime(time_str, '%H:%M').time()
                except ValueError:
                    logging.warning(f"時間格式轉換失敗: {time_str}")
                    return None
            
            self.df['Time'] = self.df['Time'].apply(convert_time_str)
            logging.info("CSV 資料前處理完成")
            
        except Exception as e:
            logging.error(f"前處理失敗: {str(e)}")
            raise

    def transform_data(self):
        logging.info("開始轉換資料")
        with self.db_manager.get_db_session() as session:
            try:
                # 第一階段：先創建和提交主表數據
                branches = {}
                product_lines = {}
                products = {}
                
                # 先處理 Branch 和 ProductLine
                for _, row in self.df.iterrows():
                    # Branch
                    if row['Branch'] not in branches:
                        branch = Branch(
                            branch_code=row['Branch'],
                            city=row['City']
                        )
                        session.add(branch)
                        branches[row['Branch']] = branch

                    # ProductLine
                    if row['Product line'] not in product_lines:
                        product_line = ProductLine(
                            name=row['Product line']
                        )
                        session.add(product_line)
                        product_lines[row['Product line']] = product_line
                
                # 提交以獲取 ID
                session.flush()  # 使用 flush 而不是 commit，保持在同一個事務中

                # 第二階段：處理 Product
                for _, row in self.df.iterrows():
                    product_key = f"{row['Product line']}_{row['Unit price']}"
                    if product_key not in products:
                        product = Product(
                            unit_price=row['Unit price'],
                            product_line_id=product_lines[row['Product line']].id
                        )
                        session.add(product)
                        products[product_key] = product
                
                session.flush()

                # 第三階段：處理 Sales
                sales = []
                for _, row in self.df.iterrows():
                    product_key = f"{row['Product line']}_{row['Unit price']}"
                    sale = Sale(
                        invoice_id=row['Invoice ID'],
                        branch_id=branches[row['Branch']].id,
                        product_id=products[product_key].id,
                        quantity=row['Quantity'],
                        tax=row['Tax 5%'],
                        total=row['Total'],
                        date=row['Date'],
                        time=row['Time'],  # 現在這裡的 Time 已經是 time 物件了
                        payment_method=row['Payment'],
                        cogs=row['cogs'],
                        gross_income=row['gross income'],
                        rating=row['Rating']
                    )
                    sales.append(sale)

                # 批量插入 sales 數據
                session.bulk_save_objects(sales)
                # commit 會在 context manager 結束時自動執行

            except Exception as e:
                logging.error(f"轉換資料失敗: {str(e)}")
                raise

    def process(self):
        self.transform_data()

def main():
    supermarket_etl = SuperMarketETL("./data/raw/supermarket_sales.csv")
    supermarket_etl.process()

if __name__ == "__main__":
    main()