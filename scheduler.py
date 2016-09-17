import sys
# from pprint import pprint
import Queue
# x= sys.stdin.readline()
# y = sys.stdin.readline()
# sys.stdout.write(x+"\n"+y)
# print(type(sys.stdin)) #<type 'file'>
jobs = []
workers = []
temparray = jobs
job_len = 0
for i,line in enumerate(sys.stdin):
	line = line.strip()
	lineArray = line.split(' ')
	if len(lineArray)  == 6:
		for idx in range(2,6):
			# print(type(lineArray[idx]) )
			lineArray[idx] = int(lineArray[idx])
			# print(type(lineArray[idx]) )
		jobs.append(lineArray); 

		# print("Job: "+jobs[i][1])
	else:
		workers.append(lineArray);
		# print("Worker: "+workers[i-len(jobs)][1])
	# sys.stdout.write(str(i)+' '+line)
jobs = sorted(jobs, key=lambda x: x[5], reverse=True)
jobs = sorted(jobs, key=lambda x: x[4], reverse=False)
# started jobs should have higher priority, say +1 or double

# print("Jobs: ")
# pprint(jobs)
# print("Workers: ")
# pprint(workers)

jobs_new = [[False,False,job[2],[],job[-1]] for job in jobs]#  
# ("job_1":[isStarted? ,isFinished?,number_of_unrun_tasks, array_running_tasks_left_hour, temp_priority])
# pprint(jobs_new)

start_T = jobs[0][4]
t = start_T
nextJobIdx = 0
num_workers = len(workers)
schedule_log = []
idleWorkers = Queue.Queue()
workerLastJob = []# record which job was the worker last working on 
for workerIdx in range(len(workers)):
	idleWorkers.put(workerIdx)
	workerLastJob.append(-1)
isAllFinished = False
try:
	while not isAllFinished:
		# pprint(jobs_new)
		# assign new job if needed
		#
		lastQueueSize = idleWorkers.qsize()
		QueueSize = idleWorkers.qsize() -1
		while (not idleWorkers.empty() )and (not (lastQueueSize == QueueSize)):
			
			lastQueueSize = idleWorkers.qsize()
			# print("QueueSize"+str(idleWorkers.qsize()))
			candidateJobs = []
			# find candidate, can be
			# if have unrunned job and it can be start, then it is one possibility
			# if have unfinished job, its number of unrun tasks is larger than the number of its currently running tasks
			if nextJobIdx<len(jobs) and jobs[nextJobIdx][-2] >= t:
				# add job into the idle workers
				prty = jobs[nextJobIdx][-1]
				candidateJobs.append([nextJobIdx,prty]) # jobid and priority
			for i,job in enumerate(jobs_new):
				if job[0] and not job[1] and job[2]>0:#already started, not finished and have not started task
					prty = job[-1]
					candidateJobs.append([i,prty])
			if len(candidateJobs) > 0:
				# compare priority
				mx_prty = 0
				winnerJobIdx = -1
				# if len(candidateJobs) == 1:
				# 	# 
				# 	mx_prty = candidateJobs[0][1]
				# 	winnerJobIdx = -1
				# else:
				# print("Length candidateJobs"+str(len(candidateJobs)))
				# pprint(candidateJobs)
				for candidate in candidateJobs:
					if candidate[1]>mx_prty:
						mx_prty = candidate[1]
						winnerJobIdx = candidate[0]

				if jobs_new[winnerJobIdx][0]: #Already started
					# 1. find a worker
					workerIdx = idleWorkers.get()# string
					# 2. write log
					if not workerLastJob[workerIdx] == winnerJobIdx:
						schedule_log.append(str(t)+" "+workers[workerIdx][1]+" "+jobs[winnerJobIdx][1])
						workerLastJob[workerIdx] = winnerJobIdx
					jobs_new[winnerJobIdx][2] -= 1
					jobs_new[winnerJobIdx][3].append([workerIdx, jobs[winnerJobIdx][3]])
				else:
					if not winnerJobIdx == nextJobIdx:
						# print("winner: "+str(winnerJobIdx)+", next job: "+str(nextJobIdx))
						raise ValueError("Logic Wrong: winner is not next job")

					# 1. find a worker
					workerIdx = idleWorkers.get()# string
					# 2. write log
					schedule_log.append(str(t)+" "+workers[workerIdx][1]+" "+jobs[winnerJobIdx][1])
					# 3. change the jobs_new
					j = jobs_new[nextJobIdx]
					j[0] = True #Started
					j[2] -= 1 # task number -1
					j[3].append([workerIdx, jobs[winnerJobIdx][3]])
					# increase its priority
					j[-1] *= 2 
					# anything else?
					nextJobIdx += 1
			QueueSize = idleWorkers.qsize()
			# print(QueueSize)


		# print("finish the time")			
		# finish this time slot
		# 1. decrease time note only those with non 0 task list are working
		# 	remove task if finished
		# 2. put worker in queue
		for job in jobs_new:
			if job[0] and len(job[-2])>0:
				for ii,task in enumerate(job[-2]):
					task[1] -= 1
					if task[1] == 0:
						# release worker
						idleWorkers.put(task[0])
						# remove this task 
						del job[-2][ii]
		t += 1
		isAllFinished = True
		for job in jobs_new:
			if not job[1]:
				isAllFinished = False
		if idleWorkers.qsize() == len(workers):
			break
except Exception, e:
	raise e
finally:
	# pprint(jobs)
	# pprint(jobs_new)
	# pprint(workers)
	# print(len(schedule_log))
	for message in schedule_log:
		sys.stdout.write(message+"\n")
#Experiment
# x = "job job_1 88 17 12 6\n"
# y = x.strip()
# pprint(x)
# y = x.split(' ')
# print len(x),len(y),type(y)
# for word in y:
# 	print(word)
# 	pprint(word)

# sys.exit(0)