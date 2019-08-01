#!/usr/bin/python
#coding;utf8
import yaml
import requests,json
from api.jumpserverApi import jumpserver
from api.cloudApi import ali,hw,ks
import sys
from api.general import sort
import threading	
import time

def update(config,updateRegion):
	##get update region
	#updateRegion = sys.argv[1]

	##get jumpserver info	
	ak = config['jumpserver']['ak']
	sk = config['jumpserver']['sk']
	url = config['jumpserver']['url']
	js = jumpserver(ak,sk,url)

	node_info = js.get_nodes()
	##create node if node not exits
	if updateRegion not in node_info:
		js.create_node(updateRegion)
		node_info = js.get_nodes()
	##create childNode if childNode not exist
	node_id	= node_info[updateRegion]['node_id']



	
	node_num = node_info[updateRegion]['node_asset_num']
	child_node_info = js.get_child_node(node_id)
	
	##get cloud info
	for cloud in config['regionInfo'][updateRegion]:
		ak = config['regionInfo'][updateRegion][cloud]['ak']
		sk = config['regionInfo'][updateRegion][cloud]['sk']
		region_id = config['regionInfo'][updateRegion][cloud]['region_id']
		admin_user = config['regionInfo'][updateRegion][cloud]['admin_user']
		gateway = config['regionInfo'][updateRegion][cloud]['gateway']
		project_id = config['regionInfo'][updateRegion][cloud]['project_id']
		cloud_eval = eval(cloud)
		cloud_intf = cloud_eval(ak,sk,region_id,project_id)
		
		servers = cloud_intf.get_region_servers()

		##check if exist chidNode
		asset_child_nodes = config['regionInfo'][updateRegion][cloud]['assetGroup']
		asset_child_nodes['default'] = ''
		
		##check if exits childNode	
		servers_info = {}
		for asset_child_node in asset_child_nodes:
			if asset_child_node not in child_node_info:
				js.create_child_node(asset_child_node,node_id)
			servers_info[asset_child_node] = {}
		##
		child_node_names = []
		for child_node in config['regionInfo'][updateRegion][cloud]['assetGroup']:
			child_node_names.append(child_node)
		assets = (js.get_node_all_assets(updateRegion,child_node_names))
		

		##
		add_target = {}

		##delete asset
		for key,value in assets.items():
			if key not in servers:	
				print ('%s delete %s'%(cloud,key))
				js.delete_node_asset(value)
		
		##add asset
		for key,value in servers.items():
			if key not in assets:
				print ('%s add %s'%(cloud,key))
				add_target[key] = value
		

		servers_sort = sort(asset_child_nodes,add_target,servers_info)

		for key,value in servers_sort.items():
			if value != {}:
				js.add_asset(admin_user=admin_user,update_node_name=updateRegion,update_child_node_name=key,gateway=gateway,assets=value)

if __name__ == "__main__":
	f =open('config.yml')
	config = yaml.load(f)
	while True:
		for updateRegion in config['regionInfo']:
			t = threading.Thread(target=update,args=(config,updateRegion,))
			t.start()
		time.sleep(config["update_time"])
