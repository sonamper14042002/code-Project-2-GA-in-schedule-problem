from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Chọn cơ sở dữ liệu
db = client['ctuet_database']

Toan_majors = ["AI", "NNLT2", "HQTCSDL", "NMCNPM", "KTLP"]
Phu_majors = ["NPL", "HCI", "NNLT1", "CTDL", "LTW"]
Quynh_majors = ["TXLDL", "ML", "KTMT", "CSDL", "OOP"]
Kiet_majors = ["DHMT", "TGMT", "NNLT4", "LTDD", "LTWEB"]
An_majors = ["PMMNM", "MMT", "PPNC", "KHMT", "NNLT3"]
Uyen_majors = ["CTDLVGT", "KHMT1", "PTDL", "LTUD", "TKDH"]

khmt0121_class = ["AI", "NPL", "TXLDL", "DHMT", "PMMNM", "CTDLVGT"]
# ktpm0121_class = ["AI", "NPL", "HCI", "TGMT", "MMT", "KHMT1"]
ktpm0121_class = ["NNLT2", "ML", "HCI", "TGMT", "MMT", "KHMT1"]
cntt0121_class = ["HQTCSDL", "NNLT1", "KTMT", "NNLT4", "PPNC", "PTDL"]
httt0121_class = ["NMCNPM", "CTDL", "CSDL", "LTDD", "KHMT", "LTUD"]

def insert_data(majors, collection_name):
    # Chọn collection tương ứng
    collection = db[collection_name]
    # Chèn dữ liệu và theo dõi thành công
    successful_inserts = []
    for major in majors:
        result = collection.insert_one({"name": major})
        if result.acknowledged:
            successful_inserts.append(major)
    # Thông báo khi chèn dữ liệu thành công
    print("Dữ liệu các môn sau đã được chèn vào collection", collection_name, "thành công:", successful_inserts)

insert_data(Toan_majors,"Toan_major")
insert_data(Phu_majors,"Phu_major")
insert_data(An_majors,"An_major")
insert_data(Quynh_majors,"Quynh_major")
insert_data(Kiet_majors,"Kiet_major")
insert_data(Uyen_majors,"Uyen_major")
insert_data(khmt0121_class,"khmt0121_class")
insert_data(ktpm0121_class,"ktpm0121_class")
insert_data(cntt0121_class,"cntt0121_class")
insert_data(httt0121_class,"httt0121_class")
