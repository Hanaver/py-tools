import pandas as pd
import re


# 读取 B 表
df_a = pd.read_excel('./sources/aaa.xlsx', header=0)

# 读取 A 表
df_b = pd.read_excel('./quotation.xlsx', header=0)

def extract_and_trim(text):
    result = re.findall(r'\((.*?)\)', text)
    return result[0].strip()

df_a['MatchValue'] = df_a['收货地址'].apply(extract_and_trim)

# 检查是否每个a列都有匹配的值，如果没有，默认为空字符串
df_a['MatchValue'] = df_a['MatchValue'].fillna('').apply(lambda x: x if x else '')

def fuzzy_match(row_a):
    # 在 B 表中模糊匹配 'c' 和 'd' 列
    match = df_b[(df_b['渠道类型'].str.contains(row_a['渠道'], case=False)) & (df_b['收货仓'].str.contains(row_a['MatchValue'],case=False))]
    
    # 如果有匹配结果，获取第一个匹配行的 'e' 列的值
    if not match.empty:
        e_value = match.iloc[0][get_field(row_a['总重量'])]
        return e_value
    else:
        return None
    
def get_field(all_w):
    print(all_w)
    field = '21kg+'
    if(all_w >= 50 and all_w < 100):
        field = '50kg+'
    if(all_w >= 100):
        field = '100kg+'
    return field


df_a['匹配单价'] = df_a.apply(fuzzy_match, axis=1)

def fuzzy_match_avg_price(row_a):
    return row_a['匹配单价'] * row_a['总重量'] / row_a['总数量']

df_a['商品平均单价'] = df_a.apply(fuzzy_match_avg_price, axis=1)

df_a.to_excel('result.xlsx', index=False)