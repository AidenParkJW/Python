import sqlite3

# conn = sqlite3.connect("spider.sqlite")
# csr = conn.cursor()
#
# csr.execute("UPDATE Pages SET new_rnak = 1.0, old_rank = 0.0")
# conn.commit()
#
# csr.close()
# conn.close()
#
# print("All pages set to a rank of 1.0")


with sqlite3.connect("spider.sqlite") as conn :
    csr = conn.cursor()

    csr.execute("UPDATE Pages SET new_rnak = 1.0, old_rank = 0.0")
    conn.commit()

print("All pages set to a rank of 1.0")
