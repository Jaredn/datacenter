# datacenter app

the purpose of this app is to give the user a visual representation of a rack, and patch panel. Each Rack has two 
tables, Front and back. these are displayed on 1 page. each row = 1u. For each object in the rack rowspan = u
this will format the table nicely. clicking on an item will allow you to edit it.

## database

* metro
- label
* dc
- label
* rack
- label
* asset - something that is racked
- label
- rackunit
- unitsize
- front
- back
- type: 1 patch panel, 2 server, 3 network device
* port
- asset_id
- label
- front: boolean 
- z-side

### racks and stuff
problem:

every rack has a front and a back, how should this go into the database?

there should be 1 db call
```
rack.objects.get(id=1)
```
this should give me all the assets in the rack
the asset will tell me if it's in the front or the back
if front = true, render front
if back = true render back

the same applies to ports