import logging
import pandas as pd
from datetime import datetime
from .models import User, Device, OS, UserBehavior
from .database_manager import DatabaseManager

logging.basicConfig(
    level=logging.INFO
)

class UserBehaviorETL:
    def __init__(self, csv_path):
        logging.info(f"開始 ETL，CSV 路徑: {csv_path}")
        try:
            self.df = pd.read_csv(
                csv_path,
                low_memory=False,
                dtype={
                    'User ID': int,
                    'Device Model': str,
                    'Operating System': str,
                    'App Usage Time (min/day)': float,
                    'Screen On Time (hours/day)': float,
                    'Battery Drain (mAh/day)': float,
                    'Number of Apps Installed': int,
                    'Data Usage (MB/day)': float,
                    'Age': int,
                    'Gender': str,
                    'User Behavior Class': int
                }
            )
            logging.info(f"已載入 {len(self.df)} 筆資料")
        except Exception as e:
            logging.error(f'CSV 載入失敗: {e}')

        self.db_manager = DatabaseManager()
        self.db_manager.initialize_database()
    
    def transform_data(self):
        logging.info('開始將 CSV 資料轉換到 SQLite...')
        with self.db_manager.get_db_session() as session:
            # 建立裝置和作業系統的對照表
            device_dict = {}
            os_dict = {}
            
            # 逐行處理資料
            for _, row in self.df.iterrows():
                # 處理裝置資訊
                device_model = row['Device Model']
                if device_model not in device_dict:
                    device = Device(device_model=device_model)
                    session.add(device)
                    session.flush()  # 取得 ID
                    device_dict[device_model] = device.device_id
                
                # 處理作業系統資訊
                os_name = row['Operating System']
                if os_name not in os_dict:
                    os = OS(operating_system=os_name)
                    session.add(os)
                    session.flush()  # 取得 ID
                    os_dict[os_name] = os.os_id
                
                # 建立使用者資料
                user = User(
                    user_id=row['User ID'],
                    age=row['Age'],
                    gender=row['Gender']
                )
                session.add(user)
                session.flush()
                
                # 建立使用者行為資料
                behavior = UserBehavior(
                    user_id=user.user_id,
                    device_id=device_dict[device_model],
                    os_id=os_dict[os_name],
                    app_usage_time=row['App Usage Time (min/day)'],
                    screen_on_time=row['Screen On Time (hours/day)'],
                    battery_drain=row['Battery Drain (mAh/day)'],
                    num_apps_installed=row['Number of Apps Installed'],
                    data_usage=row['Data Usage (MB/day)'],
                    behavior_class=row['User Behavior Class']
                )
                session.add(behavior)
                
            try:
                session.commit()
                logging.info('資料轉換完成')
            except Exception as e:
                session.rollback()
                logging.error(f'資料轉換失敗: {e}')
                raise

    def process(self):
        self.transform_data()

def main():
    etl = UserBehaviorETL("./data/user_behavior_dataset.csv")
    etl.process()

if __name__ == "__main__":
    main()   