import json
  
# Opening JSON file
f = open('train_spider.json')
  
data = json.load(f)

def num_tables_one(sql_canonical):
    return len(sql_canonical['from']['table_units']) == 1

def num_select_one(sql_canonical):
    return len(sql_canonical["select"][1]) == 1 

def distinct_select(sql_canonical):
    return sql_canonical["select"][0]

def group_by(sql_canonical):
    return sql_canonical["groupBy"]

def order_by(sql_canonical):
    return sql_canonical["orderBy"]

def having(sql_canonical):
    return sql_canonical["having"]

def limit(sql_canonical):
    return sql_canonical["limit"]

def intersect(sql_canonical):
    return sql_canonical["intersect"]

def union(sql_canonical):
    return sql_canonical["union"]

def except_sql(sql_canonical):
    return sql_canonical["except"]

print(type(data))
print(len(data))

count_wiki_type = 0
count_all_mult_sel = 0
count_wiki_irr_sel = 0
count_mult_sel_and_easy = 0
count_total = 0

result = []
for elem in data:
    temp = elem['sql']

    if num_tables_one(temp) and num_select_one(temp) and not distinct_select(temp) and not group_by(temp) and not order_by(temp) \
        and not having(temp) and not limit(temp) and not intersect(temp) and not union(temp) and not except_sql(temp):
        count_wiki_type += 1

    if num_tables_one(temp) and not num_select_one(temp) and not distinct_select(temp) and not group_by(temp) and not order_by(temp) \
        and not having(temp) and not limit(temp) and not intersect(temp) and not union(temp) and not except_sql(temp):
        count_mult_sel_and_easy += 1
    if num_select_one(temp):
        count_all_mult_sel += 1
    
    if num_tables_one(temp) and not distinct_select(temp) and not group_by(temp) and not order_by(temp) \
        and not having(temp) and not limit(temp) and not intersect(temp) and not union(temp) and not except_sql(temp):
        result.append(elem)
        count_wiki_irr_sel += 1 

    count_total += 1


final = json.dumps(result, indent=2)
file = open("output.json", 'w')
file.writelines(final)
print("WIKI type: ", count_wiki_type)
print("Mult select type ", count_mult_sel_and_easy)
print("All mult select: ", count_all_mult_sel)
print("Irrespective of mult sel: ", count_wiki_irr_sel)
print("Total", count_total)

