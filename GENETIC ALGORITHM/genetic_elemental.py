
from typing import List
from random import choices, randint, randrange, random, sample
from get_database import Teachers_name,Teachers_majors,Class_name,Classes
import matplotlib.pyplot as plt
import pandas as pd
class ClassInfo:
    def __init__(self, name: str, periods: int):
        self.name = name
        self.periods = periods

class Thing:
    def __init__(self, subject_name: str, classes: List[ClassInfo], teacher_name: str, teacher_majors: List[str], class_name: str, value: int, weight: int):
        self.subject_name = subject_name
        self.classes = classes
        self.teacher_name = teacher_name
        self.teacher_majors = teacher_majors
        self.class_name = class_name
        self.value = value
        self.weight = weight

def create_things(teachers_name: List[str], teachers_majors: List[List[str]], class_name: List[str], classes: List[List[str]]) -> List[Thing]:
    subjects = []
    subject_details = {}  # Sử dụng dictionary để lưu trữ chi tiết của mỗi môn học

    # Gán mỗi môn học cho giáo viên tương ứng và lớp học (nếu có)
    for teacher_index, teacher_majors in enumerate(teachers_majors):
        teacher_name = teachers_name[teacher_index]
        for subject in teacher_majors:
            if subject not in subject_details:
                subject_details[subject] = {
                    'teacher_name': teacher_name,
                    'class_name': 'none',
                    'class_subjects': [],
                    'teacher_majors': teacher_majors
                }
            # Kiểm tra xem môn học này có thuộc về lớp học nào không
            for class_index, class_subjects in enumerate(classes):
                if subject in class_subjects:
                    subject_details[subject]['class_name'] = class_name[class_index]
                    subject_details[subject]['class_subjects'] = class_subjects
                    break

    # Tạo danh sách các đối tượng Thing từ dictionary
    for subject, details in subject_details.items():
        subjects.append(Thing(subject, details['class_subjects'], details['teacher_name'], details['teacher_majors'], details['class_name'], value=1, weight=1))
    return subjects

# # Gọi hàm create_things với dữ liệu từ database
all_subjects = create_things(Teachers_name, Teachers_majors, Class_name, Classes)
# for subject in all_subjects:
#     print(f"Subject: {subject.subject_name}, Taught by: {subject.teacher_name}, In class: {subject.class_name}")
# print(f"Total unique subjects: {len(all_subjects)}")


def check_duplicate_subjects(shuffled_subjects):
    # Sử dụng một từ điển để lưu trữ thông tin của mỗi môn học
    subject_info = {}
    # Khởi tạo danh sách để lưu trữ các môn học bị trùng lặp
    duplicate_subjects = []
    # Duyệt qua từng môn học
    for subject in shuffled_subjects:
        # Tạo một khóa duy nhất bằng cách kết hợp tên môn học, tên giáo viên, và tên lớp học
        key = (subject.subject_name)
        # Kiểm tra xem khóa đã tồn tại trong từ điển chưa
        if key in subject_info:
            # Nếu đã tồn tại, thêm môn học vào danh sách các môn học bị trùng lặp
            duplicate_subjects.append(subject)
        else:
            # Nếu chưa tồn tại, thêm khóa vào từ điển
            subject_info[key] = True
    # Kiểm tra xem có môn học nào bị trùng lặp không
    if duplicate_subjects:
        print("Found duplicate subjects:")
        for subject in duplicate_subjects:
            print("Subject Name:", subject.subject_name)
            print("Teacher Name:", subject.teacher_name)
            print("Class Name:", subject.class_name)
            print("---------------------------")
    else:
        print("NOT FOUND ANY DUPLICATED SUBJECTS.")
        

def get_subjects_in_class(class_name: str, subjects: List[Thing]) -> List[Thing]:
    # Khởi tạo danh sách rỗng để lưu trữ các môn học trong lớp
    subjects_in_class = []
    # Duyệt qua từng môn học trong danh sách all_subjects
    for subject in subjects:
        # Kiểm tra xem môn học đó có thuộc lớp cần tìm hay không
        if subject.class_name == class_name:
            # Nếu có, thêm môn học vào danh sách
            subjects_in_class.append(subject)
    return subjects_in_class

# TẠO HÀM XÁO TRỘN DANH SÁCH 30 MÔN HỌC
def shuffle_subjects(all_subjects: List[Thing]) -> List[Thing]:
    return sample(all_subjects, len(all_subjects))

def generate_class_time(genome, shuffled_subjects):
    class_time_info = []
    # Duyệt qua từng môn học trong shuffled_subjects
    for i, subject_info in enumerate(shuffled_subjects):
        # Kiểm tra bit tương ứng trong genome
        bit = genome[i]
        # Nếu bit bằng 1, thêm thông tin tiết học vào class_time_info
        if bit == 1:
            # Gán tên lớp mặc định cho các môn học có class_name là None
            class_name = subject_info.class_name if subject_info.class_name else "None"
            class_time_info.append([subject_info.subject_name, subject_info.teacher_name, class_name])
        else:
            # Nếu bit bằng 0, ghi chú là "|"
            class_time_info.append(["|","|","|"])
    return class_time_info

def create_timetable(class_time_info):
    # Danh sách các ngày trong tuần, bao gồm cả Chủ Nhật
    days_of_week = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy']
    # Tính toán số lượng hàng cần tạo dựa trên số lượng môn học và số nguyên bội của 7 (số ngày trong tuần)
    num_rows = (len(class_time_info) + len(days_of_week) - 1) // len(days_of_week)
    # Tạo DataFrame rỗng với các cột là các ngày trong tuần và số hàng được tính toán trước
    timetable_df = pd.DataFrame(index=range(num_rows), columns=days_of_week)
    # Bắt đầu từ thứ hai (cột thứ nhất) để điền giá trị từ class_time_info vào bảng
    for i, info in enumerate(class_time_info):
        row_index = i // len(days_of_week)  # Xác định chỉ số hàng dựa trên số lượng ngày trong tuần
        col_index = i % len(days_of_week)   # Xác định chỉ số cột dựa trên số lượng ngày trong tuần
        subject_name, class_name, teacher_name = info      
        # Điền thông tin vào ô tương ứng
        timetable_df.iat[row_index, col_index] = f"{subject_name}\n{class_name}\n{teacher_name}"
    return timetable_df

def plot_timetable(timetable_df):
    # Tạo một subplot với kích thước 10x8
    fig, ax = plt.subplots(figsize=(10, 8))
    # Vẽ bảng thời khóa biểu
    ax.axis('tight')
    ax.axis('off')
    timetable_table = ax.table(cellText=timetable_df.values, colLabels=timetable_df.columns, loc='center', cellLoc='center')
    # Tùy chỉnh định dạng và cỡ chữ
    timetable_table.auto_set_font_size(False)
    timetable_table.set_fontsize(10)
    # Loại bỏ các đường kẻ và mở rộng ô
    for key, cell in timetable_table.get_celld().items():
        cell.set_height(0.15)    # Mở rộng chiều cao của ô
        cell.set_width(0.15)     # Mở rộng chiều rộng của ô
        # Thêm đường kẻ vào các ô
        cell.set_edgecolor('black') 
    # Hiển thị biểu đồ
    plt.show()
# TIM MON
# for subject in all_subjects:
#     print(subject.subject_name)
shuffled_subjects = shuffle_subjects(all_subjects)
# for subject in shuffled_subjects:
#     if subject.teacher_name == "Toan":
#         print(f"Subject:", {subject.subject_name})
# a = get_subjects_in_class("ktpm0121",all_subjects)
# for subject in a:
#     print(f"Subject:", {subject.subject_name})
# for subject in shuffled_subjects:
#     print(f"subject: {subject.subject_name},{subject.teacher_name}, {subject.class_name},{subject.value},{subject.weight}")
# print("tong so mon hoc",len(shuffled_subjects))

# a = get_subjects_in_class("none",shuffled_subjects)
# for subject in a:
#     print(f"Subject:", {subject.subject_name})

# # print(len(shuffled_subjects))

# for subject in shuffled_subjects:
#     print(subject.subject_name)
# check_duplicate_subjects(shuffled_subjects)
# print(len(shuffled_subjects))