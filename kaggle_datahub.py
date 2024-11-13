import kagglehub
import os
import shutil

class DataDownloader:
    def __init__(self, target_path="./data/"):
        self.target_path = os.path.abspath(target_path)
        
    def download_dataset(self, dataset_name):
        """
        下載指定的 Kaggle 資料集並移動到目標路徑
        
        Args:
            dataset_name (str): Kaggle 資料集名稱，格式為 "username/dataset-name"
        """
        try:
            # 確保目標目錄存在
            os.makedirs(self.target_path, exist_ok=True)
            
            # 使用官方建議的下載方式
            path = kagglehub.dataset_download(dataset_name)
            print(f"檔案已下載至暫存位置: {path}")
            
            # 移動檔案到目標位置
            self._move_files(path)
            print(f"檔案已移動至目標位置: {self.target_path}")
            print(f"目標資料夾內容: {os.listdir(self.target_path)}")
            
        except Exception as e:
            raise Exception(f"處理資料集時發生錯誤: {str(e)}")
            
    def _move_files(self, source_path):
        """
        將下載的檔案移動到目標路徑
        
        Args:
            source_path (str): 下載檔案的暫存路徑
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"找不到來源路徑: {source_path}")
        
        def move_recursive(src_path):
            # 遞迴處理所有子目錄和檔案
            for item in os.listdir(src_path):
                src_item = os.path.join(src_path, item)
                dst_item = os.path.join(self.target_path, item)
                
                if os.path.isdir(src_item):
                    # 如果是目錄，遞迴處理
                    os.makedirs(dst_item, exist_ok=True)
                    move_recursive(src_item)
                    try:
                        os.rmdir(src_item)  # 嘗試刪除空目錄
                    except OSError:
                        pass  # 如果目錄不為空則忽略
                else:
                    # 如果是檔案，直接移動
                    shutil.move(src_item, dst_item)
                    print(f"已移動檔案: {item}")
        
        try:
            move_recursive(source_path)
        except Exception as e:
            raise Exception(f"移動檔案時發生錯誤: {str(e)}")

# 使用範例
if __name__ == "__main__":
    downloader = DataDownloader()
    # downloader.download_dataset("sazidthe1/data-science-salaries")
    # downloader.download_dataset("zusmani/pakistans-largest-ecommerce-dataset")
    # downloader.download_dataset("valakhorasani/mobile-device-usage-and-user-behavior-dataset")
    # downloader.download_dataset("akashbommidi/super-market-sales")
    # downloader.download_dataset("olistbr/brazilian-ecommerce")
    # downloader.download_dataset("octopusteam/full-netflix-dataset")
    downloader.download_dataset("ironwolf437/laptop-price-dataset")
