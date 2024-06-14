from typing import List
from random import choices
from genetic_elemental import shuffled_subjects,Thing

Genome = List[int]
Population = List[Genome]

length = len(shuffled_subjects)
class Subject:
    def __init__(self, subject_name, classes):
        self.subject_name = subject_name
        self.classes = classes
        
def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)
def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def has_schedule_conflict(genome: List[int], shuffled_subjects: List[Thing]) -> bool:
    # Tạo một bảng lịch trống để theo dõi các thời điểm học
    schedule_table = {}
    for i, gene in enumerate(genome):
        # Nếu gene được chọn (1), kiểm tra xem genome này đã được sử dụng chưa
        if gene == 1:
            # lấy thông tin tên môn học tại vị trí đó
            subject = shuffled_subjects[i]
            # Kiểm tra xem môn học có `class_name` khác None không
            if subject.class_name != "none":
                for sj_name in subject.teacher_majors:
                    # Kiểm tra xem thời điểm này đã được sử dụng chưa
                    if sj_name in schedule_table:
                        if subject.subject_name in schedule_table[sj_name]:
                            # Nếu môn học i đã được sử dụng cho môn khác, xung đột lịch dạy xảy ra
                            # print(f"Conflict detected for subject {subject.subject_name} in class {subject.class_name}")
                            return True
                        else:
                            schedule_table[sj_name].append(subject.subject_name)
                    else:
                        schedule_table[sj_name] = [subject.subject_name]

    # Nếu không có xung đột lịch dạy
    return False

def has_same_day_lectures(genome: List[int], shuffled_subjects: List[Thing]) -> bool:
    # Tạo một bảng lịch trống để theo dõi các ngày dạy của giáo viên
    teacher_schedule = {}
    for i, gene in enumerate(genome):
        # Nếu gene được chọn (1), kiểm tra xem ngày dạy của giáo viên đã được sử dụng chưa
        if gene == 1:
            subject = shuffled_subjects[i]
            teacher_name = subject.teacher_name
            # lấy thông tin môn học tại vị trí i 
            # Kiểm tra xem môn học có class_name không phải None hay không
            if subject.class_name != "none":
                # Kiểm tra xem ngày dạy của giáo viên đã được sử dụng chưa
                if teacher_name in teacher_schedule:
                    if subject.class_name in teacher_schedule[teacher_name]:
                        # Nếu ngày dạy của giáo viên đã được sử dụng cho môn khác, trùng ngày dạy xảy ra
                        return True
                    else:
                        teacher_schedule[teacher_name].append(subject.class_name)
                else:
                    teacher_schedule[teacher_name] = [subject.class_name]
    # Nếu không có trùng ngày dạy
    return False


def calculate_total_value(genome: List[int], shuffled_subjects: List[Thing]) -> int:
    total_value = 0
    # Duyệt qua từng môn học được chọn trong genome
    for index, is_chosen in enumerate(genome):
        if is_chosen == 1:
            # Lấy thông tin về môn học từ danh sách all_subjects
            subject = shuffled_subjects[index]
            # Kiểm tra nếu class_name không phải None
            if subject.class_name != "none":
                # Tăng giá trị tổng cộng dựa trên một số thuộc tính của môn học
                total_value += subject.value
    return total_value

def calculate_balance_penalty(genome: List[int], shuffled_subjects: List[Thing]) -> int:
    # Tạo một từ điển để theo dõi số lượng môn học của mỗi giáo viên
    teacher_workload = {}
    # Duyệt qua từng môn học được chọn trong genome
    for index, is_chosen in enumerate(genome):
        if is_chosen == 1 :
            # Lấy thông tin về môn học từ danh sách shuffled_subjects
            subject = shuffled_subjects[index]
            # Kiểm tra xem môn học có class_name không phải None hay không
            if subject.class_name != "none":
                # Tăng số lượng môn học của giáo viên trong từ điển
                teacher_workload[subject.teacher_name] = teacher_workload.get(subject.teacher_name, 0) + 1
    # Tính toán chênh lệch giữa số lượng môn học của các giáo viên
    max_workload = max(teacher_workload.values())
    min_workload = min(teacher_workload.values())
    balance_penalty = max_workload - min_workload
    # trả về giá trị balance penalty 
    return balance_penalty

def has_sufficient_subjects_per_class(genome: List[int], shuffled_subjects: List[Thing]) -> bool:
    class_subject_count = {}
    # Duyệt qua genome để xác định những môn học nào được chọn
    for i, gene in enumerate(genome):
        if gene == 1:  # Môn học được chọn
            subject = shuffled_subjects[i]
            class_name = subject.class_name
            # Bỏ qua những môn học không có tên lớp hợp lệ
            if class_name != "none":
                if class_name not in class_subject_count:
                    class_subject_count[class_name] = set()
                class_subject_count[class_name].add(subject.subject_name)
    
    # Kiểm tra xem mỗi lớp có đủ 4 môn học khác nhau không
    for subjects in class_subject_count.values():
        if len(subjects) < 4:
            return True  # Có ít nhất một lớp không đủ 4 môn học
    
    return False  # Tất cả các lớp đều đáp ứng yêu cầu

def fitness(genome: List[int], shuffled_subjects: List[Thing], weight_limit: int) -> int:
    # Thiết lập các tham số cho việc đánh giá
    schedule_conflict_penalty = -100
    same_day_penalty = -50
    balance_workload_penalty = -30
    insufficient_subjects_penalty = -200  # Giảm điểm nếu một lớp không có đủ 4 môn học

    total_penalty = 0
    total_value = 0
    # Kiểm tra xung đột lịch dạy và trùng ngày dạy
    if has_schedule_conflict(genome, shuffled_subjects):
        total_penalty += schedule_conflict_penalty
    if has_same_day_lectures(genome, shuffled_subjects):
        total_penalty += same_day_penalty

    # Kiểm tra xem các lớp có đủ 4 môn học không
    if has_sufficient_subjects_per_class(genome, shuffled_subjects):
        total_penalty += insufficient_subjects_penalty
    
    # Kiểm tra cân bằng công việc của giáo viên
    balance_penalty = calculate_balance_penalty(genome, shuffled_subjects)
    if balance_penalty != 0:
        total_penalty += balance_penalty * balance_workload_penalty

    # Tính toán giá trị tổng cộng của lịch học
    for index, is_chosen in enumerate(genome):
        if is_chosen == 1:
            subject = shuffled_subjects[index]
            if subject.class_name != "none":
                total_value += subject.value
    # Trả về tổng giá trị nếu không có vi phạm tất cả các yêu cầu
    return total_value + total_penalty

# for i in range(len(shuffled_subjects)):
#     print("heare",shuffled_subjects[i].subject_name,shuffled_subjects[i].class_name,shuffled_subjects[i].teacher_majors)
# genomet=[0]*30
# # value = has_schedule_conflict(genomet,shuffled_subjects)
# value2 = has_sufficient_subjects_per_class(genomet,shuffled_subjects)
# value3 = fitness(genomet,shuffled_subjects,1)
# print(value3)
# print(genomet,value2)





