import pymongo

# https://www.w3schools.com/python/python_mongodb_getstarted.asp

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# select db (if not exists this creates a db)
db = myclient['testdb']

# drop and create collection
for col in db.list_collection_names():
    db[col].drop()

db.create_collection("node_persons")
# db.create_collection("node_programming_languages")
# db.create_collection("node_epics")
db.create_collection("node_meetings")

persons = [
    {'id': 'huizinga, paul'},
    {'id': 'algra, pieter'},
    {'id': 'hol, robert'},
    {'id': 'harker, steve'},
    {'id': 'olmstead, carrie'},
    {'id': 'hastie, derrick'},
    {'id': 'peeters, wouter'},
    {'id': 'maatman, sander'},
    {'id': 'nieuwe weme, bas'},
    {'id': 'hopper, graham'},
    {'id': 'schurgers, monique'},
    {'id': 'fettkecher, lorri'},
    {'id': 'righolt, andre'},
    {'id': 'chin, joan'},
    {'id': 'freeke, paul'},
    {'id': 'basstein, christan'}
     ]
db["node_persons"].insert_many(persons)

meetings = [
    {'id': 'python working group'},
    {'id': 'data governance'},
    {'id': 'raft steerco'},
    {'id': 'technical design authority'},
    {'id': 'blackrock friday call'},
    {'id': 'subs and reds'}
]
db["node_meetings"].insert_many(meetings)

db.create_collection("edge_reports_to")
reports_to = [
    {'source': 'huizinga, paul', 'target': 'harker, steve'},
    {'source': 'harker, steve', 'target': 'hastie, derrick'},
    {'source': 'hastie, derrick', 'target': 'maatman, sander'},
    {'source': 'maatman, sander', 'target': 'nieuwe weme, bas'},
    {'source': 'hol, robert', 'target': 'olmstead, carrie'},
    {'source': 'olmstead, carrie', 'target': 'peeters, wouter'},
    {'source': 'peeters, wouter', 'target': 'maatman, sander'},
    {'source': 'schurgers, monique', 'target': 'harker, steve'},
    {'source': 'hopper, graham', 'target': 'harker, steve'},
    {'source': 'fettkecher, lorri', 'target': 'harker, steve'}
]
for row in reports_to:
    db.edge_reports_to.insert_one(row)

db.create_collection("edge_is_member_of")
memberships = [
    {'source': 'huizinga, paul', 'target': 'python working group'},
    {'source': 'huizinga, paul', 'target': 'blackrock friday call'},
    {'source': 'huizinga, paul', 'target': 'data governance'},
    {'source': 'hol, robert', 'target': 'data governance'},
    {'source': 'olmstead, carrie', 'target': 'data governance'},
    {'source': 'algra, pieter', 'target': 'python working group'},
    {'source': 'harker, steve', 'target': 'blackrock friday call'},
    {'source': 'harker, steve', 'target': 'raft steerco'},
    {'source': 'peeters, wouter', 'target': 'raft steerco'},
    {'source': 'harker, steve', 'target': 'technical design authority'},
    {'source': 'hopper, graham', 'target': 'technical design authority'},
    {'source': 'schurgers, monique', 'target': 'technical design authority'},
    {'source': 'hopper, graham', 'target': 'blackrock friday call'},
    {'source': 'fettkecher, lorri', 'target': 'blackrock friday call'},
    {'source': 'righolt, andre', 'target': 'subs and reds'},
    {'source': 'chin, joan', 'target': 'subs and reds'},
    {'source': 'chin, joan', 'target': 'data governance'},
    {'source': 'freeke, paul', 'target': 'subs and reds'},
    {'source': 'basstein, christan', 'target': 'subs and reds'},
    {'source': 'huizinga, paul', 'target': 'subs and reds'}
]
for row in memberships:
    db.edge_is_member_of.insert_one(row)


# programming_languages = [
#     {'id': 'python'},
#     {'id': 'html'},
#     {'id': 'css'},
#     {'id': 'vba'},
#     {'id': 'c#'},
#      ]
# db["node_programming_languages"].insert_many(programming_languages)

# db.create_collection("edge_knows")
# knows = [
#     {'source': 'huizinga, paul', 'target': 'python'},
#     {'source': 'huizinga, paul', 'target': 'html'},
#     {'source': 'huizinga, paul', 'target': 'css'},
#     {'source': 'huizinga, paul', 'target': 'vba'},
#     {'source': 'algra, pieter', 'target': 'python'},
#     {'source': 'algra, pieter', 'target': 'c#'}
# ]
# for row in knows:
#     db.edge_knows.insert_one(row)