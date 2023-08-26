import pandas as pd

# Đọc dữ liệu từ file CSV
csv_file_path = 'origin_data.csv'
data = pd.read_csv(csv_file_path)

# Xác định đường dẫn và tên file Excel mới
excel_file_path = 'origindata2.xlsx'

# Chuyển dữ liệu vào file Excel
data.to_excel(excel_file_path, index=False)

print("Chuyển đổi thành công từ CSV sang Excel.")
