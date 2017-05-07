import json
import MySQLdb
import sys

from InsertTools import InsertHelper
import InsertTools


class App(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.tableName = "app"
        self.startedEvent = ["SparkListenerApplicationStart"]
        self.finishedEvent = ["SparkListenerApplicationEnd"]
        self.failedEvent = []
        self.tags = ["App ID", "App Name", "Timestamp", "User", "Timestamp"]
        self.cols = ["app_id", "app_name", "start_time", "user", "end_time"]
        self.params = dict.fromkeys(self.cols, None)
        self.uniqueTag = ["app_id"]
        self.uniqueTagValue = [None for i in range(len(self.uniqueTag))]
        self.typeTag = "Event"
        self.path={
            "app_id":{self.typeTag:["SparkListenerApplicationStart"],"path":[["App ID"]]},
            "app_name":{self.typeTag:["SparkListenerApplicationStart"],"path":[["App Name"]]},
            "start_time":{self.typeTag:["SparkListenerApplicationStart"],"path":[["Timestamp"]]},
            "user":{self.typeTag:["SparkListenerApplicationStart"],"path":[["User"]]},
            "end_time":{self.typeTag:["SparkListenerApplicationEnd"],"path":[["Timestamp"]]},
        }
        self.keysFilter=[]
    def isMatch(self, obj):
        return obj[self.typeTag] in self.finishedEvent

class Job(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.tableName = "job"
        self.startedEvent = ["SparkListenerJobStart"]
        self.finishedEvent = ["SparkListenerJobEnd"]
        self.failedEvent = []
        self.tags = ["Job ID", "Submission Time", "Completion Time","Job Result"]
        self.cols = ["job_id", "job_submit_time", "job_finish_time","job_result"]
        self.params = dict.fromkeys(self.cols, None)
        self.uniqueTag = ["job_id"]
        self.uniqueTagValue = [None for i in range(len(self.uniqueTag))]
        self.typeTag = "Event"
        self.path={
            "job_id":{self.typeTag:["SparkListenerJobStart","SparkListenerJobEnd"],"path":[["Job ID"],["Job ID"]]},
            "job_submit_time":{self.typeTag:["SparkListenerJobStart"],"path":[["Submission Time"]]},
            "job_finish_time":{self.typeTag:["SparkListenerJobEnd"],"path":[["Completion Time"]]},
            "job_result":{self.typeTag:["SparkListenerJobEnd"],"path":[["Job Result","Result"]]}
        }
        self.keysFilter=["app_id"]
    def isMatch(self, obj):
        if obj[self.typeTag] not in self.finishedEvent:
            return False
        for k in self.uniqueTag:
            if self.uniqueTagValue[self.uniqueTag.index(k)]!=self.find(obj,k):
                return False
        return True

class Stage(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.tableName = "stage"
        self.startedEvent = ["SparkListenerStageSubmitted"]
        self.finishedEvent = ["SparkListenerStageCompleted"]
        self.failedEvent = []
        self.tags = ["Stage ID","Stage Attempt ID", "Submission Time", "Completion Time","Stage Name"]
        self.cols = ["stage_id","attempt_id", "submission_time", "completion_time","stage_name"]
        self.params = dict.fromkeys(self.cols, None)
        self.uniqueTag = ["stage_id","attempt_id"]
        self.uniqueTagValue = [None for i in range(len(self.uniqueTag))]
        self.typeTag = "Event"
        self.path={
            "stage_id":{self.typeTag:["SparkListenerStageSubmitted","SparkListenerStageCompleted"],"path":[["Stage Info","Stage ID"],["Stage Info","Stage ID"]]},
            "attempt_id":{self.typeTag:["SparkListenerStageSubmitted","SparkListenerStageCompleted"],"path":[["Stage Info","Stage Attempt ID"],["Stage Info","Stage Attempt ID"]]},
            "submission_time":{self.typeTag:["SparkListenerStageCompleted"],"path":[["Stage Info","Submission Time"]]},
            "completion_time":{self.typeTag:["SparkListenerStageCompleted"],"path":[["Stage Info","Completion Time"]]},
            "stage_name":{self.typeTag:["SparkListenerStageSubmitted"],"path":[["Stage Info","Stage Name"]]}
        }
        self.keysFilter=["app_id","job_id"]

class Task(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.tableName = "task"
        self.startedEvent = ["SparkListenerTaskStart"]
        self.finishedEvent = ["SparkListenerTaskEnd"]
        self.failedEvent = []
        self.tags = ["Stage ID", "Stage Attempt ID", "Task ID","Index","Attempt","Launch Time","Executor ID","Host","Task Type","Finish Time","Reason","Locality","Speculative"]
        self.cols = ["stage_id", "attempt_id", "task_id","task_index","task_attempt","task_launchTime","executor_id","task_host","task_type","task_finishTime","task_status","locality","speculative"]
        self.params = dict.fromkeys(self.cols, None)
        self.uniqueTag = ["task_id","task_attempt","stage_id","attempt_id"]
        self.uniqueTagValue = [None for i in range(len(self.uniqueTag))]
        self.typeTag = "Event"
        self.path={
            "stage_id":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Stage ID"],["Stage ID"]]},
            "attempt_id":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Stage Attempt ID"],["Stage Attempt ID"]]},
            "task_id":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Task Info","Task ID"],["Task Info","Task ID"]]},
            "task_index":{self.typeTag:["SparkListenerTaskStart"],"path":[["Task Info","Index"]]},
            "task_attempt":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Task Info","Attempt"],["Task Info","Attempt"]]},
            "task_launchTime":{self.typeTag:["SparkListenerTaskStart"],"path":[["Task Info","Launch Time"]]},
            "executor_id":{self.typeTag:["SparkListenerTaskStart"],"path":[["Task Info","Executor ID"]]},
            "task_host":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Info","Host"]]},
            "task_type":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Type"]]},
            "task_finishTime":{self.typeTag:["SparkListenerTaskEnd","SparkListenerTaskEnd"],"path":[["Task Info","Finish Time"],["Task Info","Finish Time"]]},
            "task_status":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task End Reason","Reason"]]},
            "locality":{self.typeTag:["SparkListenerTaskStart"],"path":[["Task Info","Locality"]]},
            "speculative":{self.typeTag:["SparkListenerTaskStart"],"path":[["Task Info","Speculative"]]}
        }
        self.keysFilter=["app_id","job_id"]

class RDD(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.params = {}
        self.keysFilter=["app_id","job_id"]
    def rdd(self,obj):
        self.tableName="rdd"
        self.params["rdd_id"]=obj["RDD ID"]
        self.params["name"]=obj["Name"]
        scope=json.loads(obj["Scope"])
        self.params["scope_id"]=scope["id"]
        self.params["scope_name"]=scope["name"]
       # self.params["callsite"]=obj["Callsite"]
        self.params["parent_id"]=None
        self.params["storage_level_use_disk"]=obj["Storage Level"]["Use Disk"]
        self.params["storage_level_use_memory"]=obj["Storage Level"]["Use Memory"]
        self.params["storage_level_use_externalblockstore"]=obj["Storage Level"]["Use ExternalBlockStore"]
        self.params["storage_level_deserialized"]=obj["Storage Level"]["Deserialized"]
        self.params["storage_level_replication"]=obj["Storage Level"]["Replication"]
        self.params["number_of_partitions"]=obj["Number of Partitions"]
        self.params["number_of_cached_partitions"]=obj["Number of Cached Partitions"]
        self.params["memory_size"]=obj["Memory Size"]
        self.params["externalblockstore_size"]=obj["ExternalBlockStore Size"]
        self.params["disk_size"]=obj["Disk Size"]
        return self

class RDDs(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.tableName = "rdd"
        self.startedEvent = ["SparkListenerStageCompleted"]
        self.finishedEvent = ["SparkListenerStageCompleted"]
        self.failedEvent = []
        self.tags = []
        self.cols = []
        self.params = dict.fromkeys(self.cols, None)
        self.uniqueTag = ["rdd_id"]
        self.uniqueTagValue = [None for i in range(len(self.uniqueTag))]
        self.typeTag = "Event"
        self.path={
            "stage_id":{self.typeTag:["SparkListenerStageCompleted"],"path":[["Stage Info","Stage ID"]]},
            "attempt_id":{self.typeTag:["SparkListenerStageCompleted"],"path":[["Stage Info","Stage Attempt ID"]]},
            "rdds":{self.typeTag:["SparkListenerStageCompleted"],"path":[["Stage Info","RDD Info"]]}
        }
        self.keysFilter=["app_id","job_id"]
    def rdds(self,obj):
        self.params["stage_id"]=self.find(obj,"stage_id")
        self.params["attempt_id"]=self.find(obj,"attempt_id")
        rdds=self.find(obj,"rdds")
        res=[]
        for rdd in rdds:
            if len(rdd["Parent IDs"])==0:
                t=RDD().rdd(rdd)
                t.params["stage_id"]=self.params["stage_id"]
                t.params["attempt_id"]=self.params["attempt_id"]
                t.isCompleted=True
                t.isSucc=True
                res.append(t)
            else:
                for pid in rdd["Parent IDs"]:
                    t=RDD().rdd(rdd)
                    t.params["parent_id"]=pid
                    t.params["stage_id"]=self.params["stage_id"]
                    t.params["attempt_id"]=self.params["attempt_id"]
                    t.isCompleted=True
                    t.isSucc=True
                    res.append(t)
        self.isCompleted=True
        self.isSucc=True
        return res

class Metrics(InsertHelper):
    def __init__(self):
        InsertHelper.__init__(self)
        self.tableName = "task_metrics"
        self.startedEvent = ["SparkListenerTaskEnd"]
        self.finishedEvent = ["SparkListenerTaskEnd"]
        self.failedEvent = []
        self.tags = ["Stage ID", "Stage Attempt ID", "Task ID","Index","Attempt","Host Name","Executor Deserialize Time","Executor Run Time","Result Size","JVM GC Time","Result Serialization Time","Memory Bytes Spilled","Disk Bytes Spilled"]
        self.cols = ["stage_id", "attempt_id", "task_id","task_index","task_attempt","hostname","executor_deserialize_time","executor_run_time","result_size","jvm_gc_time","result_serialization_time","memory_bytes_spilled","disk_bytes_spilled"]
        self.params = dict.fromkeys(self.cols, None)
        self.uniqueTag = ["task_id","task_attempt","stage_id","attempt_id"]
        self.uniqueTagValue = [None for i in range(len(self.uniqueTag))]
        self.typeTag = "Event"
        self.path={
            "stage_id":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Stage ID"],["Stage ID"]]},
            "attempt_id":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Stage Attempt ID"],["Stage Attempt ID"]]},
            "task_id":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Task Info","Task ID"],["Task Info","Task ID"]]},
            "task_index":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Task Info","Index"],["Task Info","Index"]]},
            "task_attempt":{self.typeTag:["SparkListenerTaskStart","SparkListenerTaskEnd"],"path":[["Task Info","Attempt"],["Task Info","Attempt"]]},
            "hostname":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Host Name"]]},
            "executor_deserialize_time":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Executor Deserialize Time"]]},
            "executor_run_time":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Executor Run Time"]]},
            "result_size":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Result Size"]]},
            "jvm_gc_time":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","JVM GC Time"]]},
            "result_serialization_time":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Result Serialization Time"]]},
            "memory_bytes_spilled":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Memory Bytes Spilled"]]},
            "disk_bytes_spilled":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Disk Bytes Spilled"]]},

            # 20160520 update
            "shuffle_bytes_written":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Write Metrics","Shuffle Bytes Written"]]},
            "shuffle_write_time":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Write Metrics","Shuffle Write Time"]]},
            "shuffle_records_written":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Write Metrics","Shuffle Records Written"]]},

            "remote_blocks_fetched":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Read Metrics","Remote Blocks Fetched"]]},
            "local_blocks_fetched":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Read Metrics","Local Blocks Fetched"]]},
            "fetch_wait_time":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Read Metrics","Fetch Wait Time"]]},
            "remote_bytes_read":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Read Metrics","Remote Bytes Read"]]},
            "local_bytes_read":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Read Metrics","Local Bytes Read"]]},
            "total_records_read":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Shuffle Read Metrics","Total Records Read"]]},

            "data_read_method":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Input Metrics","Data Read Method"]]},
            "bytes_read":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Input Metrics","Bytes Read"]]},
            "records_read":{self.typeTag:["SparkListenerTaskEnd"],"path":[["Task Metrics","Input Metrics","Records Read"]]}
            # 20160520 update end
        }
        self.keysFilter=["app_id","job_id"]
    def fill(self,obj):
        if obj[self.typeTag] in self.finishedEvent and self.isCompleted==False:
            self.isCompleted=True
            for k in self.uniqueTag:
                try:
                    self.uniqueTagValue[self.uniqueTag.index(k)]=self.find(obj,k)
                    self.params[k]=self.find(obj,k)
                except:pass

            if obj["Task End Reason"]["Reason"]=="Success" and self.isMatch(obj):
                for k in self.path:
                    try:
                        self.params[k]=self.find(obj,k)
                    except:pass
        return self

if __name__ == '__main__':
    log = []
    for line in open(sys.argv[1], "r").readlines():
        obj = None
        try:
            obj = json.loads(line)
        except:
            continue
        for ele in log:
            ele.fill(obj)
        if "SparkListenerApplicationStart" == obj["Event"]:
            log.append(App().fill(obj))
            pass
        if "SparkListenerApplicationEnd" == obj["Event"]:
            pass
        if "SparkListenerJobStart" == obj["Event"]:
            log.append(Job().fill(obj))
            pass
        if "SparkListenerStageSubmitted" == obj["Event"]:
            log.append(Stage().fill(obj))
            pass
        if "SparkListenerStageCompleted" == obj["Event"]:
            t=RDDs().rdds(obj)
            for i in t:
                log.append(i)
            pass
        if "SparkListenerTaskStart" == obj["Event"]:
            log.append(Task().fill(obj))
            pass
        if "SparkListenerTaskEnd" == obj["Event"]:
            log.append(Metrics().fill(obj))
            pass
    for i in range(len(log)):
        for j in range(i+1,len(log)):
            log[j].canGetKeys(log[i])
    conn=InsertTools.getConnection()
    cur=conn.cursor()
    for ele in log:
        sql=ele.getInsertSql()
        try:
            cur.execute(sql)
        except:
            print "insert error!"
            print(sql)
    cur.close()
    conn.commit()
    conn.close()
