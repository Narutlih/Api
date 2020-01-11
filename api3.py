import vk
import requests
import networkx as nx
import time
import collections

session = vk.Session(access_token='15af6ef954e21628d770b5e1177046ffb1a2b6514a875f6c212f14227b8fb9eb7f5024e9f25a435f71d3d')
vk_api = vk.API(session)

def get_friends_ids(user_id):
    return vk_api.friends.get(user_id=user_id,v='5.52')

def get_friends_friends(user_ids):
    API = "https://api.vk.com/method"
    ACCESS_TOKEN = "15af6ef954e21628d770b5e1177046ffb1a2b6514a875f6c212f14227b8fb9eb7f5024e9f25a435f71d3d"
    V = 5.52
    uid = int(user_ids[1])
    print(type(uid))
    response = requests.post(url=f"{API}/execute",
                             data={
                                 "code": "var members=[];"
                                         "members.push(API.friends.get({uid}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[2]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[3]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[4]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[5]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[6]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[7]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[8]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[9]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[10]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[11]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[12]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[13]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[14]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[15]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[16]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[17]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[18]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[19]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[20]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[21]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[22]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[23]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[24]\"}));"
                                         # "members.push(API.friends.get({\"user_id\": \"user_ids[25]\"}));"
                                         "return members;",
                                 "access_token": ACCESS_TOKEN,
                                 "v": V,
                             }).json()
    return response

# def trottling_request():
#     deq.appendleft(time.time())
#     if len(deq) == 4:
#         time.sleep(max(2 + deq[3] - deq[0], 0))

graph = {}
deq = collections.deque(maxlen=4)
friend_ids = get_friends_ids(137118302)['items']
g = nx.Graph(directed=False)
count=1
array = {}
counter = 1
for friend_id in friend_ids:
    # trottling_request()
    # print('Processing id: ', friend_id)
    if count<26:
        array[count]=friend_id
        count = count + 1
        continue
    result = get_friends_friends(array)
    for i in result['response']:
        graph[array[counter]] = i['items']
        counter = counter + 1
    count = 1
    counter = 1

for i in graph:
    g.add_node(i)
    for j in graph[i]:
        if i != j and i in friend_ids and j in friend_ids:
            g.add_edge(i, j)

nx.write_graphml(g, 'graph.graphml')

f = open("out_new.txt","w")
f.write( str(graph) )
f.close()