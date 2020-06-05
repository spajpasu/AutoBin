import LatLong
import os



a = LatLong.LatLong()

for wayID, forestRef in enumerate(a.forest_way):
    a.get_wayID_nodeRef(a.wayIDS[wayID], forestRef)

for refID, forestRelation in enumerate(a.forest_relation):
    a.read_latlon_ways(a.forest_relation_ids[refID], forestRelation)
