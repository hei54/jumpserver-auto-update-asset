#coding:utf8
##sort assets into assetGroup
##根据config.yaml将servers完成分组返回
##每个分组都有一个默认的default组
def sort(assetGroups,servers,info):
	for server,server_info in servers.items():
		for assetGroup in assetGroups:
			score = 0
			tags = assetGroup.split('-')
			for tag in tags:
				if tag in server:
					score +=1
			if score == len(tags) and assetGroup != 'default':
				info[assetGroup][server] = servers[server]
				break
			elif assetGroup == 'default':
				info[assetGroup][server]  = servers[server]
	return info
