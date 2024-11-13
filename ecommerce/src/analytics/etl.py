import pandas as pd
from src.database.models import Customer, Category, Product, Order, OrderItem
from src.database.database_manager import DatabaseManager

class ETLProcessor:
    def __init__(self, csv_path):
        self.df = pd.read_csv(
            csv_path,
            low_memory=False,
            dtype={
                'Customer ID': str,
                'Customer Since': str,
                'created_at': str,
                'sku': str,
                'increment_id': str,
                'status': str,
                'payment_method': str,
                'sales_commission_code': str,
                'BI Status': str
            }
        )
        self.df.drop(['Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25'], axis=1, inplace=True)
        self.df.dropna(how='all',inplace=True)
        self.db_manager = DatabaseManager()
        
    def transform_data(self):
        
        records = []
        customers = {}
        categories = {}
        products = {}
        
        for _, row in self.df.iterrows():
            try:
                # 處理 Customer
                customer_id = row['Customer ID']
                if customer_id not in customers:
                    customer = Customer(
                        customer_id=customer_id,
                        customer_since=str(row['Customer Since'])
                    )
                    customers[customer_id] = customer
                    records.append(customer)
                
                # 處理 Category
                category_name = str(row['category_name_1'])
                if category_name not in categories:
                    category = Category(name=category_name)
                    categories[category_name] = category
                    records.append(category)
                
                # 處理 Product
                sku = str(row['sku'])
                if sku not in products:
                    try:
                        price = float(row['price'])
                    except (ValueError, TypeError):
                        price = 0.0
                        
                    product = Product(
                        sku=sku,
                        price=price,
                        category=categories[category_name]
                    )
                    products[sku] = product
                    records.append(product)
                
                # 處理 Order
                order = Order(
                    increment_id=str(row['increment_id']),
                    customer=customers[customer_id],
                    status=str(row['status']),
                    created_at=str(row['created_at']),
                    payment_method=str(row['payment_method']),
                    grand_total=float(row['grand_total']),
                    discount_amount=float(row['discount_amount'] or 0),
                    sales_commission_code=str(row['sales_commission_code']),
                    bi_status=str(row['BI Status'])
                )
                records.append(order)
                
                # 處理 OrderItem
                try:
                    qty_ordered = int(row['qty_ordered'])
                    item_price = float(row['price'])
                except (ValueError, TypeError):
                    qty_ordered = 1
                    item_price = 0.0
                    
                order_item = OrderItem(
                    order=order,
                    product=products[sku],
                    qty_ordered=qty_ordered,
                    price=item_price
                )
                records.append(order_item)
                
            except Exception as e:
                print(f"錯誤發生在處理第 {_} 行時: {str(e)}")
                continue
        
        return records

    
    def process(self):
        records = self.transform_data()
        self.db_manager.add_records(records)

def main():
    etl = ETLProcessor("./data/raw/Pakistan Largest Ecommerce Dataset.csv")
    etl.process()

if __name__ == "__main__":
    main()