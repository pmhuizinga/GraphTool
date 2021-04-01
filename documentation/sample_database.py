import pymongo

# https://www.w3schools.com/python/python_mongodb_getstarted.asp

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# select db (if not exists this creates a db)
db = myclient['testdb']

# drop and create collection
for col in db.list_collection_names():
    db[col].drop()

db.create_collection("node_person")
# db.create_collection("node_programming_languages")
# db.create_collection("node_epics")
db.create_collection("node_meeting")

persons = [
    {'id': 'huizinga, paul'},
    {'id': 'algra, pieter'},
    {'id': 'hol, robert'},
    {'id': 'harker, steve'},
    {'id': 'olmstead, carrie'},
    # {'id': 'hastie, derrick'},
    {'id': 'peeters, wouter'},
    # {'id': 'maatman, sander'},
    # {'id': 'nieuwe weme, bas'},
    {'id': 'hopper, graham'},
    {'id': 'schurgers, monique'},
    {'id': 'fettkecher, lorri'},
    {'id': 'righolt, andre'},
    {'id': 'chin, joan'},
    {'id': 'freeke, paul'},
    {'id': 'wood, angela'},
    {'id': 'michelson, lisa'},
    {'id': 'marriot, michael'},
    {'id': 'payne, angel'},
    {'id': 'eisenhart, jennifer'},
    {'id': 'killin, karen'},
    {'id': 'pieters, ronald'},
    {'id': 'johnson-logan, jennifer'},
    {'id': 'tjaden, sarah'},
    {'id': 'jensen, scott'},
    {'id': 'keyser, nick de'},
    {'id': 'kargin, ayfer'},
    {'id': 'nims, pamela'},
    {'id': 'lawson, amy'},
    {'id': 'ramponi, stephanie'},
    {'id': 'sebers, ben'},
    {'id': 'mccreary, michael'},
    {'id': 'basstein, christan'}

     ]
db["node_person"].insert_many(persons)

meetings = [
    {'id': 'python working group'},
    {'id': 'data governance'},
    {'id': 'raft steerco'},
    {'id': 'technical design authority'},
    {'id': 'blackrock friday call'},
    {'id': 'subs and reds'},
    {'id': 'daily architecture huddle'},
    {'id': 'raft data mapping and reports'},
    {'id': 'raft data storage and data outputs'}
]
db["node_meeting"].insert_many(meetings)

# db.create_collection("edge_reports_to")
# reports_to = [
#     {'source': 'huizinga, paul', 'target': 'harker, steve'},
#     {'source': 'harker, steve', 'target': 'hastie, derrick'},
#     {'source': 'hastie, derrick', 'target': 'maatman, sander'},
#     {'source': 'maatman, sander', 'target': 'nieuwe weme, bas'},
#     {'source': 'hol, robert', 'target': 'olmstead, carrie'},
#     {'source': 'olmstead, carrie', 'target': 'peeters, wouter'},
#     {'source': 'peeters, wouter', 'target': 'maatman, sander'},
#     {'source': 'schurgers, monique', 'target': 'harker, steve'},
#     {'source': 'hopper, graham', 'target': 'harker, steve'},
#     {'source': 'fettkecher, lorri', 'target': 'harker, steve'}
# ]
# for row in reports_to:
#     db.edge_reports_to.insert_one(row)

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
    {'source': 'huizinga, paul', 'target': 'subs and reds'},
    {'source': 'huizinga, paul', 'target': 'daily architecture huddle'},
    {'source': 'harker, steve', 'target': 'daily architecture huddle'},
    {'source': 'hopper, graham', 'target': 'daily architecture huddle'},
    {'source': 'fettkecher, lorri', 'target': 'daily architecture huddle'},
    {'target': 'raft data storage and data outputs', 'source': 'wood, angela'},
    {'target': 'raft data storage and data outputs', 'source': 'michelson, lisa'},
    {'target': 'raft data storage and data outputs', 'source': 'marriot, michael'},
    {'target': 'raft data storage and data outputs', 'source': 'payne, angel'},
    {'target': 'raft data storage and data outputs', 'source': 'eisenhart, jennifer'},
    {'target': 'raft data storage and data outputs', 'source': 'killin, karen'},
    {'target': 'raft data storage and data outputs', 'source': 'pieters, ronald'},
    {'target': 'raft data storage and data outputs', 'source': 'johnson-logan, jennifer'},
    {'target': 'raft data storage and data outputs', 'source': 'tjaden, sarah'},
    {'target': 'raft data storage and data outputs', 'source': 'jensen, scott'},
    {'target': 'raft data storage and data outputs', 'source': 'hol, robert'},
    {'target': 'raft data storage and data outputs', 'source': 'fettkecher, lorri'},
    {'target': 'raft data storage and data outputs', 'source': 'huizinga, paul'},
    {'target': 'raft data mapping and reports', 'source': 'marriot, michael'},
    {'target': 'raft data mapping and reports', 'source': 'wood, angela'},
    {'target': 'raft data mapping and reports', 'source': 'michelson, lisa'},
    {'target': 'raft data mapping and reports', 'source': 'eisenhart, jennifer'},
    {'target': 'raft data mapping and reports', 'source': 'keyser, nick de'},
    {'target': 'raft data mapping and reports', 'source': 'kargin, ayfer'},
    {'target': 'raft data mapping and reports', 'source': 'lawson, amy'},
    {'target': 'raft data mapping and reports', 'source': 'fettkecher, lorri'},
    {'target': 'raft data mapping and reports', 'source': 'ramponi, stephanie'},
    {'target': 'raft data mapping and reports', 'source': 'payne, angel'},
    {'target': 'raft data mapping and reports', 'source': 'sebers, ben'},
    {'target': 'raft data mapping and reports', 'source': 'mccreary, michael'},
    {'target': 'raft data mapping and reports', 'source': 'nims, pamela'},
    {'target': 'raft data mapping and reports', 'source': 'huizinga, paul'},

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