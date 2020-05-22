from importlib import reload
import osmium
import LatLong
import re
import InputData

reload(LatLong)


class ForestDataHandler(osmium.SimpleHandler):  # here we use concept of handlers for data processing
    f = open(InputData.wayDATA, 'w+')

    def __init__(self):
        super(ForestDataHandler, self).__init__()

    # def node(self, n, build):
    def node(self, n):
        LatLong.LatLong().get_nodeID_loc(n.id, n.location)

    def way(self, w):
        self.f.write(str(w.id) + '-' + str(w.nodes) + '\n')
        if w.tags.get("landuse") == 'forest':
            if w.is_closed():
                LatLong.LatLong().get_wayID_nodeRef(int(w.id), w.nodes)
                # print(w.nodes)
            else:
                print("forest with id: {0} is not closed.".format(w.id))

    def relation(self, r):
        if r.tags.get("landuse") == 'forest':
            members = {}
            relation_data = r.members
            print(relation_data)
            for i in relation_data:
                i = str(i)
                key = re.search('w(.*)@', i).group(1)
                value = re.search('@(.*)', i).group(1)
                members[key] = value
            # print(members)
            LatLong.LatLong().read_latlon_ways(int(r.id), members)
            # pass
    # def area(self, a):
    #     if a.tags.get("landuse") == 'forest':
    #         print(a.from_way())
