import sqlite3

# conn = sqlite3.connect("spider.sqlite")
# csr = conn.cursor()
#
# csr.execute('''
#     SELECT  COUNT(from_id) AS inbound
#     ,       old_rank
#     ,       new_rank
#     ,       id
#     ,       url
#     FROM Pages
#     JOIN Links  ON  Links.to_id = Pages.id
#     WHERE html is NOT NULL
#     GROUP BY id
#     ORDER BY inboud DESC
# ''')
#
# count = 0
# for row in csr :
#     if count < 50 :
#         print(row)
#
#     count += 1
#
# print(count, "rows.")
#
# csr.close()
# conn.close()


with sqlite3.connect("spider.sqlite") as conn :
    csr = conn.cursor()

    csr.execute('''
        SELECT  COUNT(from_id) AS inbound
        ,       old_rank
        ,       new_rank
        ,       id
        ,       url
        FROM Pages
        JOIN Links  ON  Links.to_id = Pages.id
        WHERE html IS NOT NULL
        GROUP BY id
        ORDER BY inboud DESC
    ''')

    count = 0
    for row in csr :
        if count < 50 :
            print(row)

        count += 1

    print(count, "rows.")
