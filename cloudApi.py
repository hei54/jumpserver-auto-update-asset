from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from openstack import connection
from kscore.session import get_session
class ali:
        def __init__(self,ak,sk,zome,project_id):
                self.zome = zome
                self.ak =  ak
                self.sk = sk
                client =AcsClient(ak,sk,zome)
                self.client =client
                response = self.get_ecs_info(1)
                all_vm_num_info = self.get_ecs_info(1)
                vm_num = all_vm_num_info['TotalCount']
                check_pages = vm_num%100
                if check_pages == 0:
                        pages = vm_num/100
                else:
                        pages = int(vm_num/100) +1
                vms = {}
                self.zome = zome
                self.ak =  ak
                self.sk = sk
                client =AcsClient(ak,sk,zome)
                self.client =client
                response = self.get_ecs_info(1)
                all_vm_num_info = self.get_ecs_info(1)
                vm_num = all_vm_num_info['TotalCount']
                check_pages = vm_num%100
                if check_pages == 0:
                        pages = vm_num/100
                else:
                        pages = int(vm_num/100) +1
                vms = {}
                for i in range(1,int(pages+1)):
                        response = self.get_ecs_info(i)
                        instances_info  = response['Instances']['Instance']
                        outerip = ''
                        count = 0
                        vm_a = []
                        vm_b = []
                        for a in instances_info:
                                if a['Status'] == 'Running':
                                        networktype = a['InstanceNetworkType']
                                        if networktype == 'vpc':
                                                vm = self.get_vpc_network_info(a)
                                                vm_a.append(vm)
                                                for b in vm:
                                                        vms[b] = vm[b]
                                        else:
                                                vm = self.get_classical_network_info(a)
                                                vm_b.append(vm)
                                                for b in vm:
                                                        if b in vms:
                                                            print (b)
                                                        vms[b] = vm[b]
                self.vms = vms

        def get_ecs_info(self,page):
		## not use definetion
                true = 1
                false =0
		

                client = self.client
                zome = self.zome
                request = CommonRequest()
                request.set_accept_format('json')
                request.set_domain('ecs.aliyuncs.com')
                request.set_method('POST')
                request.set_version('2014-05-26')
                request.set_action_name('DescribeInstances')
                request.add_query_param('RegionId',zome )
                request.add_query_param('PageNumber', page)
                request.add_query_param('PageSize', '100')
                response = client.do_action_with_exception(request)
                return eval(response)

        def get_classical_network_info(self,info):
                instanceinfo = {}
                instancename = info['InstanceName']
                instanceinfo[instancename] = {}

                try:
                        pubip =  info['PublicIpAddress']['IpAddress'][0]
                except:
                        pubip = ''

                instanceinfo[instancename]['pubip'] = pubip
                innerip = info['InnerIpAddress']['IpAddress'][0]
                instanceinfo[instancename]['innerip'] = innerip
                return instanceinfo

        def get_vpc_network_info(self,info):
                instanceinfo = {}
                instancename = info['InstanceName']
                instanceinfo[instancename] = {}
                try:
                        pubip =  info['PublicIpAddress']['IpAddress'][0]
                except:
                        pubip = ''
                instanceinfo[instancename]['pubip'] = pubip
                innerip = info['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
                instanceinfo[instancename]['innerip'] = innerip
                return instanceinfo

        def get_region_servers(self):
                vms = self.vms
                return vms


class hw:

	def __init__(self,ak,sk,zome_id,project_id):
                self.ak = ak
                self.sk = sk
                self.zome_id = zome_id
                conn = connection.Connection(ak=ak,sk=sk,user_domain_id='a3f800a816b54a88803d513005cc21b2',project_id=project_id,region=zome_id,domain='myhuaweicloud.com')
                self.conn = conn

                servers = conn.compute.servers(limit=1000)
                vms={}
                for server in servers:
                        for key,value in server.addresses.items():
                                        if len(value) > 1:
                                                pubip = str(value[1]['addr'])
                                                innerip = str(value[0]['addr'])
                                                instancename = str(server.name)
                                                vm_info = {}
                                                vm_info['pubip'] = pubip
                                                vm_info['innerip'] = innerip
                                                vms[instancename] = vm_info

                                        else:
                                                innerip = str(value[0]['addr'])
                                                instancename = str(server.name)
                                                vm_info = {}
                                                vm_info['pubip'] = ''
                                                vm_info['innerip'] = innerip
                                                vms[instancename] = vm_info

                self.vms =vms
	def get_region_servers(self):
		vms = self.vms
		return vms
class ks:
	def __init__(self,ak,sk,zome_id,project_id):
                self.ak = ak
                self.sk = sk
                self.zome_id = zome_id
                session  = get_session()
                self.session = session
                kecclient = session.create_client("kec",ks_access_key_id=ak,ks_secret_access_key=sk,region_name=zome_id)
                eipclient = session.create_client('eip',ks_access_key_id=ak,ks_secret_access_key=sk,region_name=zome_id)
                alleips=eipclient.describe_addresses(MaxResults=1000)
                response = kecclient.describe_instances()
                InstanceCount = response['InstanceCount']
                vms = {}
                if InstanceCount < 1000:
                        response = kecclient.describe_instances(MaxResults=1000)
                        for instance in response['InstancesSet']:
                                networkinterfaceid = instance['NetworkInterfaceSet'][0]['NetworkInterfaceId']
                                instancename = instance['InstanceName']
                                innerip = instance['PrivateIpAddress']
                                vm_info = {}
                                vm_info['innerip'] = innerip
                                vm_info['pubip'] = ''
                                vms[instancename] = vm_info
                else:
                        request_times = int(InstanceCount/1000)+1
                        marker = 0
                        for a in range(0,request_times):
                                marker +=1000
                                if (a+1) == request_times:
                                        response = kecclient.describe_instances(MaxResults=1000)
                                else:
                                        response = kecclient.describe_instances(MaxResults=1000,Marker=marker)
                                for instance in response['InstancesSet']:
                                        instancename = instance['InstanceName']
                                        innerip = instance['PrivateIpAddress']
                                        vm_info = {}
                                        vm_info['innerip'] = innerip
                                        vm_info['pubip'] = ''
                                        vms[instancename] = vm_info
                #alleips = alleips['AddressesSet']
                #for vm in vms:
                #        for networkinterfaceid,instancename in vm.items():
                #                for eipinfo  in alleips:
                #                        if 'NetworkInterfaceId' in eipinfo:
                #                                if networkinterfaceid == eipinfo['NetworkInterfaceId']:
                #                                        instancename_outerip[networkinterfaceid] = eipinfo['PublicIp']
                #                                        networkinterfaceid_allocationid[networkinterfaceid] = eipinfo['AllocationId']
                self.vms = vms

	def get_region_servers(self):
		vms = self.vms
		return vms
