from src.view.main_window import MainWindow

class AppController:
    def __init__(self):
        # Khởi tạo cửa sổ chính
        self.main_window = MainWindow()
        
        # Sau này, nếu cần kết nối Model chung cho toàn app, bạn sẽ viết ở đây
        # self.setup_connections()
        
    def run(self):
        # Hiển thị cửa sổ
        self.main_window.show()