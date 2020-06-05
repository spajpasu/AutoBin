import osmium
from LatLong import LatLong
import GeneralOperations as GO
import re
import InputData

class ForestDataHandler(osmium.SimpleHandler):  # here we use concept of handlers for data processing
    wayhandler = open(InputData.wayDATA, 'w+')
    forestHandler = open(InputData.forestinWAYS, 'w+')
    relationHandler = open(InputData.relationForest, 'w+')
    nodeHandler = open(InputData.nodeDATA, 'w+')
    requiredTags = GO.open_file(InputData.requiredTags)
    requiredTagArray = GO.create_tagValKey(requiredTags)
    closedWayHandler = open(InputData.closedWAYS, 'w+')


    def __init__(self):
        super(ForestDataHandler, self).__init__()

    def node(self, n):
        self.nodeHandler.write(str(n.id) + ':' + str([n.location.lat, n.location.lon]) + '\n')

    def way(self, w):
        self.wayhandler.write(str(w.id) + '-' + str(w.nodes) + '\n')
        if w.is_closed():
            for i in self.requiredTagArray:
                if w.tags.get(i[0]) == i[1]:
                    self.closedWayHandler.write(str(w.id) + '-' + str(w.nodes) + '\n')
                    break

        if w.tags.get("landuse") == 'forest':
            if w.is_closed():
                self.forestHandler.write(str(w.id) + '-' + str(w.nodes) + '\n')
            else:
                print("forest with id: {0} is not closed.".format(w.id))


    def relation(self, r):
        if r.tags.get("landuse") == 'forest':
            relation_data = r.members
            self.relationHandler.write(str(r.id) + '-' )
            for i in relation_data:
                i = str(i)
                self.relationHandler.write(str(re.search('w(.*)@', i).group(1)) + ':' + str(re.search('@(.*)', i).group(1)) + ',')
            self.relationHandler.write('\n')