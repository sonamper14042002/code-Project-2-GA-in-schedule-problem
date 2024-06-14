from pymongo import MongoClient
# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Chọn cơ sở dữ liệu
db = client['ctuet_database']  
# Cơ sở dữ liệu

def get_major_names(collection_name):
    collection = db[collection_name]
    major_names = []
    documents = collection.find({}, {"_id": 0, "name": 1})
    for document in documents:
        major_names.append(document['name'])
    # print(f"DEBUG: {collection_name} - {major_names}")  # Thêm để gỡ lỗi
    return major_names


# Sử dụng hàm để lấy danh sách tên môn học từ collection 'Toan_major'
Toan_majors = get_major_names('Toan_major')
Phu_majors = get_major_names('Phu_major')
Quynh_majors = get_major_names('Quynh_major')
Kiet_majors = get_major_names('Kiet_major')
An_majors = get_major_names('An_major')
Uyen_majors = get_major_names('Uyen_major')

# # In ra danh sách tên môn học
khmt0121_class = get_major_names('khmt0121_class')
ktpm0121_class = get_major_names('ktpm0121_class')
cntt0121_class = get_major_names('cntt0121_class')
httt0121_class = get_major_names('httt0121_class')
# các biến kết quả cuối
Teachers_name = ["Toan", "Phu", "Quynh", "Kiet", "An", "Uyen"]
Teachers_majors = [Toan_majors, Phu_majors, Quynh_majors, Kiet_majors, An_majors, Uyen_majors]
Class_name = ["khmt0121", "ktpm0121", "cntt0121", "httt0121"]
Classes = [khmt0121_class, ktpm0121_class, cntt0121_class, httt0121_class]
# print("Checking for duplicates in major lists:")
# for lst in [Toan_majors, Phu_majors, Quynh_majors, Kiet_majors, An_majors, Uyen_majors, khmt0121_class, ktpm0121_class, cntt0121_class, httt0121_class]:
#     if len(lst) != len(set(lst)):
#         print("Duplicate found in list:", lst)
# def check_documents_count():
#     collections = ["Toan_major", "Phu_major", "An_major", "Quynh_major", "Kiet_major", "Uyen_major", "khmt0121_class", "ktpm0121_class", "cntt0121_class", "httt0121_class"]
#     for col in collections:
#         count = db[col].count_documents({})
#         print(f"{col} has {count} documents")
# check_documents_count()

# def check_collection_data(collection_name):
#     documents = db[collection_name].find()
#     for doc in documents:
#         print(doc)
# check_collection_data("Toan_major")  # Thay đổi tên collection để kiểm tra các collection khác

# Hàm để in danh sách các môn học của từng giáo viên
# def print_teacher_majors(teachers_names, teachers_majors):
#     for name, majors in zip(teachers_names, teachers_majors):
#         print(f"Môn học của giáo viên {name}:")
#         for major in majors:
#             print(major)
#         print()  # Thêm dòng trống để tách biệt giữa các giáo viên
# print_teacher_majors(Teachers_name, Teachers_majors)
# # Hàm để in danh sách các môn học của từng lớp học
# def print_class_majors(class_names, classes):
#     for name, majors in zip(class_names, classes):
#         print(f"Môn học trong lớp {name}:")
#         for major in majors:
#             print(major)
#         print() 
# print_class_majors(Class_name, Classes)