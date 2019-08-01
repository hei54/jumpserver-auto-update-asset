# jumpserver-auto-update-asset
云环境下的开源堡垒机资产自动更新
当前仅支持阿里云、金山云、华为云

主要修改config.yaml文件，相关注释如下：

		jumpserver:
        		ak: xxxxxxxx ##堡垒机账号
        		sk: xxxxxxxxxx #堡垒机账号密码 
        		url: https://baidu.com ##域名或者堡垒机ip+port		
		update_time: 3600 ##更新频率(s)
		regionInfo:
			{{ asset-name }}: #分组的名字
                		{{ cloud_type }}: ##云厂商简称阿里云(ali)\华为云(hw)\金山云(js)
                        		ak: xxxxxxxxxxxxxxxxxxxxx ##云厂商提供的ak
                        		sk: xxxxxxxxxxxxxxxxxxxxxx ##云厂商提供的sk
                        		region_id: cn-hangzhou  ##云厂商提供的区域ID
                        		admin_user: hz-dvlvpc ##资产管理-系统用户对应的自定义账号
                        		gateway: hz-dvlvpc ##资产管理-网域列表对应的自定义网关名字,如果没有通过网关，则置空
                        		project_id: '' ##针对华为云的project_id
                        		assetGroup: ##资产分组，最少一组(分组名:资产名称包含的字段，通过切割“-”，判断资产是否存在该字段，如果均存在，则将该资产划入该组下)
                                		func-open: func-open
                                		dvl-open: dvl-open
                                		func-shop: func-shop
                                		dvl-shop: dvl-shop
                                		func: func
                                		dvl: dvl
                                		bigdata: bigdata

TODO
添加aws、azure、百度云
  
