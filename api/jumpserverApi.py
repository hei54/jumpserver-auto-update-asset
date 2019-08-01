#!/usr/bin/python
import yaml
import requests,json
from pprint import pprint
import sys

class jumpserver:
	def __init__(self,ak,sk,url):
		get_token_url = url+'/api/users/v1/auth/' 
		query_args = {
			"username": ak,
			"password": sk
				}
		response = requests.post(get_token_url, data=query_args)
		token =  json.loads(response.text)['token']
		header_info = { "Authorization": 'Bearer ' + token }
		self.url = url
		self.header_info = header_info


	def get_user_info(self):
		url = self.url
		url = url+'/api/users/v1/users/'
		header_info = self.header_info
		response = requests.get(url, headers=header_info)	
		print(json.loads(response.text))
	

	def get_nodes(self):
		url = self.url
		url = url+'/api/assets/v1/nodes/children/'
		header_info = self.header_info
		response = requests.get(url,headers=header_info)
		datas = (json.loads(response.text))
		if len(datas) != 0:
			info = {}
			for data in datas:
				a = {}
				node_name = data['value']
				node_asset_num = data['assets_amount']
				node_id = data['id']
				a['node_asset_num'] = node_asset_num
				a['node_id'] = node_id
				info[node_name] = a	
			return info
		else:
			return {}

	def create_node(self,node):
		url = self.url
		url = url+'/api/assets/v1/nodes/'
		header_info = self.header_info
		data = {'value':node}
		response = requests.post(url,headers=header_info,data=data)
		data = (json.loads(response.text))
		return data
	
	def get_child_node(self,node_id):
		url = self.url
		url = url+'/api/assets/v1/nodes/'+node_id+'/children/'
		header_info = self.header_info
		response = requests.get(url,headers=header_info)

		datas = (json.loads(response.text))
		info = {}
		if len(datas)!=0:
			for data in datas:
				a = {}
				node_name = data['value']
				node_asset_num = data['assets_amount']
				node_id = data['id']
				a['node_asset_num'] = node_asset_num
				a['node_id'] = node_id
				info[node_name] = a	
			return info
		else:
			return {}
	
	def get_child_node_id(self,update_node_name,child_node_name):
		nodes_info = self.get_nodes()
		node_id = nodes_info[update_node_name]['node_id']
		
		child_nodes_info = self.get_child_node(node_id)
		return child_nodes_info[child_node_name]['node_id']
	
			
		
			

	def create_child_node(self,node,node_id):
		url = self.url
		url = url+'/api/assets/v1/nodes/'+node_id+'/children/'
		header_info = self.header_info
		data = {'value':node}
		response = requests.post(url,headers=header_info,data=data)
		data = (json.loads(response.text))
		return data


	def get_gateway_id(self,gateway):
		url = self.url
		url = url+'/api/assets/v1/gateway/'
		header_info = self.header_info
		response = requests.get(url,headers=header_info)
		datas = (json.loads(response.text))
		for data in datas:
			if gateway == data['name']:
				return data['domain']

	def get_adminUser_id(self,adminUser):
		
		url = self.url
		url = url+'/api/assets/v1/admin-user/'
		header_info = self.header_info
		response = requests.get(url,headers=header_info)
		datas = (json.loads(response.text))
		for data in datas:
			if adminUser == data['name']:
				return data['id']

	def add_asset(self,**kwargs):
		url = self.url
		header_info = self.header_info
		url = url+ '/api/assets/v1/assets/'
		#inner_ip = kwargs['ip']
		#hostname = kwargs['hostname']
		#public_ip = kwargs['public_ip']
		add_asset_group = kwargs['assets']
		admin_user = self.get_adminUser_id(kwargs['admin_user'])
		if admin_user is None:
			print ('还未创建管理员%s'%admin_user)
			sys.exit()
		update_node_name = kwargs['update_node_name']
		update_child_node_name = kwargs['update_child_node_name']
		node_id = self.get_child_node_id(update_node_name,update_child_node_name)
		gateway = kwargs['gateway']
		if gateway is not None:
			gateway_id = self.get_gateway_id(gateway)
			if gateway_id is  None:
				print ('还未创建网域%s'%gateway)
				sys.exit()
			for key,value in add_asset_group.items():
				innerip = value['innerip']
				pubip = value['pubip']
				info = {'ip':innerip,'hostname':key,'public_ip':pubip,'domain':gateway_id,'admin_user':admin_user,'nodes':node_id,'is_active': 'true'}
				response = requests.post(url,headers=header_info,data=info)
		else:
			for key,value in add_asset_group.items():
				innerip = value['innerip']
				pubip = value['pubip']
				info = {'ip':innerip,'hostname':key,'public_ip':pubip,'admin_user':admin_user,'nodes':node_id,'is_active': 'true'}
				response = requests.post(url,headers=header_info,data=info)

	def get_node_all_assets(self,updateRegion,child_node_names):
		true =1
		false = 0
		null = 2
		url1 = self.url
		node_assets = {}
		nodes_info = self.get_nodes()
		for child_node_name  in child_node_names:
			child_node_id = self.get_child_node_id(updateRegion,child_node_name)	
			url = url1+'/api/assets/v1/nodes/'+child_node_id+'/assets/'
			header_info = self.header_info
			
			response = requests.get(url,headers=header_info)
			datas = eval(response.text)
			for data in datas:
				asset_id = data['id']
				asset_name = data['hostname']
				node_assets[asset_name] = asset_id
		return node_assets

	def delete_node_asset(self,asset_id):
		url = self.url
		header_info = self.header_info
		url = url +'/api/assets/v1/assets/'+asset_id+'/'
		response = requests.delete(url,headers=header_info)
