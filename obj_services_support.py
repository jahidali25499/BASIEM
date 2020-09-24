from bacpypes.basetypes import ServicesSupported, ObjectTypesSupported


def services_supported(service_list):
	all_services = ServicesSupported().bitNames

	supported_services = [i for i in range(len(service_list)) if service_list[i] == 1]

	for key, value in all_services.items():
		if value in supported_services:
			yield key


# services = [0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,]
# for serv in services_supported(services):
# 	print(serv) 



def objects_supported(object_list):
	all_objects = ObjectTypesSupported().bitNames

	supported_objects = [j for j in range(len(object_list)) if object_list[j] == 1]

	for key, value in all_objects.items():
		if value in supported_objects:
			yield key


# objects = [1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# for obj in objects_supported(objects):
# 	print(obj)


