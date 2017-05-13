from __future__ import division
import warnings

def distance_euclidean(instance1, instance2):
	def detect_value_type(attribute):
		from numbers import Number
		attribute_type = None
		if isinstance(attribute, Number):
			attribute_type = float
			attribute = float(attribute)
		else:
			attribute_type = str
			attribute = str(attribute)
		return attribute_type, attribute
	if len(instance1) != len(instance2):
		raise AttributeError("Instances have different number of arguments.")
	# init differences vector
	differences = [0] * len(instance1)
	# compute difference for attributes
	for i, (attr1, attr2) in enumerate(zip(instance1, instance2)):
		type1, attr1 = detect_value_type(attr1)
		type2, attr2 = detect_value_type(attr2)
		if type1 != type2:
			raise AttributeError("Instances have different data types.")
		if type1 is float:
			differences[i] = attr1 - attr2
		else:
			if attr1 == attr2:
				differences[i] = 0
			else:
				differences[i] = 1
	rmse = (sum(map(lambda x: x**2, differences)) / len(differences))**0.5
	return rmse
	
class LOF:
	def __init__(self, instances, normalize=True, distance_function=distance_euclidean):
		self.instances = instances
		self.normalize = normalize
		self.distance_function = distance_function
		if normalize:
			self.normalize_instances()
			
	def compute_instance_attribute_bounds(self):
		min_values = [float("inf")] * len(self.instances[0]) 
		max_values = [float("-inf")] * len(self.instances[0])
		for instance in self.instances:
			min_values = tuple(map(lambda x,y: min(x,y), min_values,instance)) 
			max_values = tuple(map(lambda x,y: max(x,y), max_values,instance))
			
		diff = [dim_max - dim_min for dim_max, dim_min in zip(max_values, min_values)]
		if not all(diff):
			problematic_dimensions = ", ".join(str(i+1) for i, v in enumerate(diff) if v == 0)
			warnings.warn("No data variation in dimensions: %s. You should check your data or disable normalization." % problematic_dimensions)

		self.max_attribute_values = max_values
		self.min_attribute_values = min_values
		
	def normalize_instances(self):
		if not hasattr(self, "max_attribute_values"):
			self.compute_instance_attribute_bounds()
		new_instances = []
		# (instance - min_values) / (max_values - min_values)
		for instance in self.instances:
			new_instances.append(self.normalize_instance(instance)) 
		self.instances = new_instances
		
	def normalize_instance(self, instance):
		return tuple(map(lambda value,max,min: (value-min)/(max-min) if max-min > 0 else 0, instance, self.max_attribute_values, self.min_attribute_values))
		
	def local_outlier_factor(self, min_pts, instance):
		if self.normalize:
			instance = self.normalize_instance(instance)
		return local_outlier_factor(min_pts, instance, self.instances, distance_function=self.distance_function)
		
def k_distance(k, instance, instances, distance_function=distance_euclidean):
	distances = {}
	for instance2 in instances:
		distance_value = distance_function(instance, instance2)
		if distance_value in distances:
			distances[distance_value].append(instance2)
		else:
			distances[distance_value] = [instance2]
	distances = sorted(distances.items())
	neighbours = []
	[neighbours.extend(n[1]) for n in distances[:k]]
	k_distance_value = distances[k - 1][0] if len(distances) >= k else distances[-1][0]
	return k_distance_value, neighbours
	
def reachability_distance(k, instance1, instance2, instances, distance_function=distance_euclidean):
	(k_distance_value, neighbours) = k_distance(k, instance2, instances, distance_function=distance_function)
	return max([k_distance_value, distance_function(instance1, instance2)])

def local_reachability_density(min_pts, instance, instances, **kwargs):
	(k_distance_value, neighbours) = k_distance(min_pts, instance, instances, **kwargs)
	# init reach_distances
	reachability_distances_array = [0]*len(neighbours) 
	for i, neighbour in enumerate(neighbours):
		reachability_distances_array[i] = reachability_distance(min_pts, instance, neighbour, instances, **kwargs)
	if not any(reachability_distances_array):
		warnings.warn("Instance %s (could be normalized) is identical to all the neighbors. Setting local reachability density to inf." % repr(instance))
		return float("inf")
	else:
		return len(neighbours) / sum(reachability_distances_array)
		
def local_outlier_factor(min_pts, instance, instances, **kwargs):
	# min_pts is a parameter for specifying a minimum number of instances to comput LOF value
	(k_distance_value, neighbours) = k_distance(min_pts, instance, instances, **kwargs)
	instance_lrd = local_reachability_density(min_pts, instance, instances, **kwargs)
	lrd_ratios_array = [0]* len(neighbours)
	for i, neighbour in enumerate(neighbours):
		instances_without_instance = set(instances)
		instances_without_instance.discard(neighbour)
		neighbour_lrd = local_reachability_density(min_pts, neighbour, instances_without_instance, **kwargs)
		lrd_ratios_array[i] = neighbour_lrd / instance_lrd
	return sum(lrd_ratios_array) / len(neighbours)
	
def outliers(k, instances, **kwargs):
	instances_value_backup = instances
	outliers = []
	for i, instance in enumerate(instances_value_backup):
		instances = list(instances_value_backup)
		instances.remove(instance)
		l = LOF(instances, **kwargs)
		value = l.local_outlier_factor(k, instance)
		if value > 1.01:
			outliers.append({"lof": value, "instance": instance, "index": i})
	outliers.sort(key=lambda o: o["lof"], reverse=True)
	return outliers
	
	