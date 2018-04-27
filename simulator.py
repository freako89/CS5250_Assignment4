'''
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.last_process_time = arrive_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        current_time = max(current_time, process.arrive_time)
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    _process_list = copy.deepcopy(process_list)
    schedule = []
    queue = []
    time = 0
    waiting_time = 0
    ap = 0
    rp = 0
    done = 0
    q = time_quantum
    start = 0
    
    last_id = -1
    
    n = len(process_list)
    _process_list = copy.deepcopy(process_list)
    while (done < n):
        for i in range(ap,n):
            if time >= _process_list[i].arrive_time:
                queue.append(_process_list[i])
                ap+=1
                rp+=1
        if rp<1:
            time+=1
            continue
        if start:
            queue = queue[1:]+[queue[0]]
        if queue[0].burst_time>0:
            waiting_time += (time - queue[0].last_process_time)
            if queue[0].burst_time > q:
                if queue[0].id != last_id:
                    schedule.append((time,queue[0].id))
                    last_id = queue[0].id
                time += q
                queue[0].burst_time -=q
                queue[0].last_process_time = time
            else:
                if queue[0].id != last_id:
                    schedule.append((time,queue[0].id))
                    last_id = queue[0].id 
                time += queue[0].burst_time
                queue[0].burst_time = 0
                queue[0].last_process_time = time
                done += 1
                rp -= 1
            start = 1   
        
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule,average_waiting_time

def SRTF_scheduling(process_list):
    schedule = []
    queue = []
    time = 0
    waiting_time = 0
    done = 0
    
    prev_a = -1
    a = 0

    n = len(process_list)
    rp = 0
    idx = 0
    arrive_time_array = [process_list[i].arrive_time for i in range(0,len(process_list))]
    id_array = [process_list[i].id for i in range(0,len(process_list))]
    burst_time_array = [process_list[i].burst_time for i in range(0,len(process_list))]
    last_process_time_array = [process_list[i].last_process_time for i in range(0,len(process_list))]
    while (done < n):
        if idx < len(process_list):
            if time >= process_list[idx].arrive_time:
                idx+=1
                rp+=1
        if rp<1:
            time+=1
            continue
        a = burst_time_array[0:idx].index(min([e for e in burst_time_array[0:idx] if e > 0]))
        waiting_time += (time - last_process_time_array[a])
        if prev_a!=a:
            schedule.append((time,id_array[a]))
        prev_a = a
        time += 1
        burst_time_array[a] -=1
        last_process_time_array[a] = time
        if burst_time_array[a]==0:
            done += 1
            rp -= 1   
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule,average_waiting_time

def SJF_scheduling(process_list, alpha):
    schedule = []
    current_time = 0
    waiting_time = 0
    undone = [1] * len(process_list)

    #Initial predicted burst time = 5
    pred = dict((pid, 5.0) for pid in list(set(proc.id for proc in process_list)))
    for cnt in range(len(process_list)):
        candidate_list_idx = [i for i in range(len(process_list)) if undone[i] and process_list[i].arrive_time <= current_time]
        if len(candidate_list_idx) == 0:
            current_time = process_list[cnt].arrive_time
            candidate_list_idx = [i for i in range(len(process_list)) if
                                 undone[i] and process_list[i].arrive_time <= current_time]

        idx = candidate_list_idx[[pred[process_list[e].id] for e in candidate_list_idx].index(min([pred[process_list[e].id] for e in candidate_list_idx]))] 
        proc = process_list[idx]
        current_time = max(current_time, proc.arrive_time)
        schedule.append((current_time, proc.id))
        waiting_time = waiting_time + (current_time - proc.arrive_time)
        current_time = current_time + proc.burst_time

        #Formula for exponential averaging in lecture notes
        pred[proc.id] = alpha * proc.burst_time + (1 - alpha) * pred[proc.id]
        undone[idx] = 0

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

    #Finding optimal values of Q and alpha for RR and SJF respectively
    RR_timings = [RR_scheduling(process_list,time_quantum = tq)[1] for tq in [x * 0.1 for x in range(1, 101)]]
    print ('\nOptimal value of Q for RR is '+str([x * 0.1 for x in range(1, 101)][RR_timings.index(min(RR_timings))]))
    print ('with an average waiting time of '+str(min(RR_timings)))
    SJF_timings = [SJF_scheduling(process_list, alpha = al)[1] for al in [x * 0.001 for x in range(0, 101)]]
    print ('\nOptimal value of alpha for SJF is '+str([x * 0.1 for x in range(0, 101)][SJF_timings.index(min(SJF_timings))]))
    print ('with an average waiting time of '+str(min(SJF_timings)))
    
if __name__ == '__main__':
    main(sys.argv[1:])
