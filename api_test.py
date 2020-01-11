import vk
import time
import collections
import xlsxwriter

session = vk.Session(
    access_token='a59e5aaa3a3775c46c9a7a522ec899a4c26dc533b97e507fd4fa194a3eea4aa7836c78fc11b429235c23d')
vk_api = vk.API(session)
deq = collections.deque(maxlen=4)


def pause_request():
    deq.appendleft(time.time())
    if len(deq) == 4:
        time.sleep(max(2 + deq[3] - deq[0], 0))

group = 2976989

count = vk_api.groups.getMembers(group_id=group, v='5.103')['count']
members = []

if count > 1000:
    for i in range(0, 1 + count // 1000):
        pause_request()
        members.extend(
            vk_api.groups.getMembers(group_id=group, offset=i * 1000, count=1000, fields=('sex', 'city', 'bdate'),
                                     lang=3,
                                     v='5.103')['items'])
else:
    members = vk_api.groups.getMembers(group_id=group, fields=('sex', 'city', 'bdate'), lang=3, v='5.103')['items']

users = []
for x in members:
    if 'deactivated' not in x:
        users.append(x)

workbook = xlsxwriter.Workbook('group_info.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

worksheet.write(row, col, 'Group')
worksheet.write(row, col + 1, 'id_person')
worksheet.write(row, col + 2, 'group_id')
worksheet.write(row, col + 3, 'group_name')

row += 1

count = 0

for x in range(6000,10000):
    if vk_api.users.get(user_id=users[x]['id'], fields='blacklisted', v='5.103')[0]['blacklisted'] == 0:
        if not users[x]['is_closed']:
            pause_request()
            print(users[x]['id'])
            groups = vk_api.groups.get(user_id=users[x]['id'], extended=1, fields='members_count', offset=0, v='5.103')['items']
            users[x]['groups'] = groups
            if 'groups' in users[x]:
                for y in users[x]['groups']:
                    if 'members_count' in y and y['members_count'] > 5000:
                        worksheet.write(row, col, 'Fantastica')
                        worksheet.write(row, col + 1, users[x]['id'])
                        worksheet.write(row, col + 2, y['id'])
                        worksheet.write(row, col + 3, y['name'])
                        row += 1
            count += 1
            print(count)

workbook.close()