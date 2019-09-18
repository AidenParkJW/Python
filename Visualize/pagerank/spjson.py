import sqlite3

conn = sqlite3.connect("spider.sqlite")
csr = conn.cursor()

print("Creating JSON output on spider.js...")
howmany = int(input("How many nodes? "))

csr.execute('''
    SELECT  COUNT(from_id)  AS inbound
    ,       old_rank
    ,       new_rank
    ,       id
    ,       url
    FROM Pages
    JOIN Links ON Links.to_id = Pages.id
    WHERE html IS NOT NULL
    AND error IS NULL
    GROUP BY id
    ORDER BY id, inbound
''')

fh = open("spider.js", "w")
nodes = list()
maxrank = None
minrank = None
for row in csr :
    nodes.append(row)
    rank = row[2]
    if maxrank is None or maxrank < rank :
        maxrank = rank

    if minrank is None or minrank > rank :
        minrank = rank

    if len(nodes) > howmany :
        break;

if maxrank == minrank or maxrank is None or minrank is None :
    print("Error - please run sprank.py to compute page rank")
    quit()

map = dict()
ranks = dict()
_nodes = list()
_links = list()

fh.write('spiderJson = {"nodes":[\n')
for row in nodes :
    # print row
    rank = row[2]
    rank = 19 * ((rank - minrank) / (maxrank - minrank))
    _nodes.appen("{'weight':'%s', 'rank':'%d', 'id':'%s', 'url':'%s'}" % (_row[0], rank, row[3], row[4]))
    map[row[3]] = count
    ranks[row[3]] = rank
    count += 1

fh.write(",\n".join(_nodes))
fn.write("],\n")

csr.execute("SELECT DISTINCT from_id, to_id FROM Links")
fh.write('"links":[\n')

for row in csr :
    # print rows
    if row[0] not in map or row[1] not in map :
        continue

    rank = ranks[row[0]]
    srank = 19 * ((rank - minrank) / maxrank - minrank)
    _links.append("{'source':'%s', 'target':'%s', 'value':3}" % (map[row[0]], map[row[1]]))

fh.write(",\n".join(_links))
fh.write("]};")
fh.close()

csr.close()
conn.close()

print("Open force.html in a browser to view the visualization")
