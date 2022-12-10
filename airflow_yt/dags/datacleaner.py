def data_cleaner():

    import pandas as pd
    import re
    #đọc file
    df = pd.read_csv("~/op_files/raw_store_transactions.csv")
    #xoá tất cả kí hiệu đặc biệt ở cột store location
    def clean_store_location(st_loc):
        return re.sub(r'[^\w\s]', '', st_loc).strip()
    # clean cột id, loại bỏ tất cả các kí hiệu ngoài số nguyên và return chỉ số nguyên
    def clean_product_id(pd_id):
        matches = re.findall(r'\d+', pd_id)
        if matches:
            return matches[0]
        return pd_id
    # xoá kí hiệu $ từ tất cả các cột giá để cho phép cộng trừ nhân chia
    def remove_dollar(amount):
        return float(amount.replace('$', ''))
    # thực hiện 2 func 1 và 2
    df['STORE_LOCATION'] = df['STORE_LOCATION'].map(lambda x: clean_store_location(x))
    df['PRODUCT_ID'] = df['PRODUCT_ID'].map(lambda x: clean_product_id(x))
    # gọi hàm for vì đến 4 column cần xoá kí hiệu $
    for to_clean in ['MRP', 'CP', 'DISCOUNT', 'SP']:
        df[to_clean] = df[to_clean].map(lambda x: remove_dollar(x))
    #cuối cùng lưu tập mới lại đè lên tập cũ
    df.to_csv('~/op_files/clean_store_transactions.csv', index=False)
