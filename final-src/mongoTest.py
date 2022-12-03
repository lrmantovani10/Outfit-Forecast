import backend_functions as back
import requests
from urllib.parse import unquote
from urllib.parse import quote_plus

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
db = client["User"]
userCollection = db["Test"]

import api
debugUser = api.createPerson('forunittests2')

debugUser.dailyRecommender([20, 30, 25, "nothing"], "new")

# output = [
# "hoodie",
# "shirt",
# "pants",
# "shoes",
# ]
# output2 = [
# "sweater",
# None,
# None,
# "vans"]
#
# def genKey(output):
#     str = ""
#     for item in output:
#         str += item
#     return str
#
# outfitQueue = []
#
# dupMap = {}
# outfitQueue.append(output)
# dupMap[genKey(output)] = True
#
#
# for i in range(4):
#     if output2[i] != None:
#         fit = output[:i] + [output2[i]] + output[i+1:]
#         try:
#             temp = dupMap[genKey(fit)]
#         except:
#             outfitQueue.append(fit)
#             dupMap[genKey(fit)] = True
#
# for i in range(4):
#     if output2[i] != None:
#         for j in range(i+1,4):
#             if output2[j] != None:
#                 newOutput = output
#                 newOutput[i] = output2[i]
#                 newOutput[j] = output2[j]
#                 try:
#                     temp = dupMap[genKey(newOutput)]
#                 except:
#                     outfitQueue.append(newOutput)
#                     dupMap[genKey(newOutput)] = True
#
#
#
# for i in range(4):
#     if output2[i] != None:
#         for j in range(i + 1, 4):
#             if output2[j] != None:
#                 for k in range(j + 1, 4):
#                     if output2[k] != None:
#                         newOutput = output
#                         newOutput[i] = output2[i]
#                         newOutput[j] = output2[j]
#                         newOutput[k] = output2[k]
#                         try:
#                             temp = dupMap[genKey(newOutput)]
#                         except:
#                             outfitQueue.append(newOutput)
#                             dupMap[genKey(newOutput)] = True
#
# allowedNones = []
# for idx, piece in enumerate(output):
#     if piece == None:
#         allowedNones.append(idx)
#
# allowed = True
# if output2 != [None, None, None, None]:
#     for idx, piece in enumerate(output2):
#         if piece == None:
#             if idx not in allowedNones:
#                 allowed = False
#     if allowed:
#         try:
#             temp = dupMap[genKey(output2)]
#         except:
#             outfitQueue.append(output2)
#             dupMap[genKey(output2)] = True
#
#
# # don't suggest yesterday's exact chosen outfit, but move it to back of recommended
# if len(self.getClothingHistory()) > 0 and output2 != [None, None, None, None]:
#     yesterdaysIDs = list(map(lambda x: getID(x), self.getClothingHistory()[-1]))
#     #print(yesterdaysIDs)
#     if len(outfitQueue) != 1:
#         for y in range(len(outfitQueue)):
#             todaysIDs = list(map(lambda x: getID(x), outfitQueue[y]))
#             #print(todaysIDs)
#             if yesterdaysIDs == todaysIDs:
#                 dup = outfitQueue[y]
#                 outfitQueue.append(dup)
#                 outfitQueue.pop(y) # remove original duplicate, put it last
#                 break

