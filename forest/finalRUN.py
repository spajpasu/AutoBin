import LatLong
import InputData
import GeneralOperations as GO



a = LatLong.LatLong()

a.building_creator()

Uncomment below 4 lines this to write trees  to database

for wayID, forestRef in enumerate(a.forest_way):
    a.get_wayID_nodeRef(a.wayIDS[wayID], forestRef)

for refID, forestRelation in enumerate(a.forest_relation):
    a.read_latlon_ways(a.forest_relation_ids[refID], forestRelation)


# All file removing operations shifted to CanalTreeRunner.py