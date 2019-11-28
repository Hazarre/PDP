import pickle
import time
import csv
class Supply:
    def __init__ (self,number,start,end,stime, etime, path, capacity, assignments):
        self.n = number # an integer
        self.s = start #  a vertex
        self.e = end # a vertex
        self.st = stime # a tuple of two integers
        self.et = etime
        self.p = path
        self.c = capacity # the available capacity
        self.a = assignments
class Request:
    def __init__ (self,number,start,end,stime, etime, volume , matchlist):
        self.n = number # an integer
        self.s = start #  a vertex
        self.e = end # a vertex
        self.st = stime # a tuple of two integers
        self.et = etime
        self.v = volume
        self.ml = matchlist
def AnalyzeOverAll():
    f = pickle.load(open("ChicagoCommunityAreas_path_dis_database.picke",'rb'))
    dis = f["dis_database"]
    open("ChicagoCommunityAreas_path_dis_database.picke",'rb').close()
    missing = []
    csv_out = open('OverallResult.csv',"wb")
    out_rows = csv.writer(csv_out)
    out_rows.writerow(["day","reqWaitTime",'reqDis',"CarWaitTime",'carDis',"Rides","NumCar","NumReq","C:R ratio", "carFlex","ReqFlex", "NumFeasible", "totalCPUtime", "tranferTimes"])

    for i in range(1,22):
        for x in range(1,6):
            S_flex = 1+x/10.0
            for y in range(1,21):
                R_flex = 1+y/10.0
                tag = "_"+str(S_flex)+"_"+str(R_flex)
                file_name = "ChicagoTaxi2014\Finished_day%d"%i + tag + '.picke'
                try:
                    result = pickle.load(open(file_name,'r'))
                    open(file_name,'r').close()
                    reqWaitTime, reqDis, carDis = 0,0,0
                    carWaitTime = 0
                    assignedcars = set()
                    for r in result['Requests']:
                        if len(r.ml)>0:
                            arrival = r.ml[-1][2]
                            eat = (r.st + dis[r.s][r.e])
                            if arrival > r.et:
                                print i,x,y,"not verified"
                            reqWaitTime += arrival - eat
                            reqDis += dis[r.s][r.e]
                        for ass in r.ml:
                            assignedcars.add(ass[1])
                    for c in result["Supplies"]:
                        arrival = c.a[c.e][0]
                        eat = (c.st + dis[c.s][c.e])
                        if c.n in assignedcars:
                            carWaitTime +=  arrival- eat
                            carDis += dis[c.s][c.e]
                    NumCar = len(result['Supplies'])
                    NumReq = len(result['Requests'])
                    print "day",i
                    out_rows.writerow([i, reqWaitTime, reqDis, carWaitTime, carDis, NumCar+NumReq,NumCar,NumReq,2,result['S_flex'], result['R_flex'],result["n_feasible"], result["total_time"], result["total_transfer"]])
                    print S_flex,R_flex,"General result updated in csv"
                except IOError:
                    print file_name, "not find"
                    missing.append(file_name)
                #save to csv
    csv_out.close()
    print missing
def AnalyzeCarDensity():
    csv_out = open('carDensityday3.csv',"wb")
    out_rows = csv.writer(csv_out)
    out_rows.writerow(["Hour","Num Car/s"])
    for i in range(3,4):
        out_rows.writerow(["day%d"%i])
        for x in range(2,3):
            S_flex = 1+x/10.0
            for y in range(5,6):
                R_flex = 1+y/10.0
                tag = "_"+str(S_flex)+"_"+str(R_flex)
                file_name = "ChicagoTaxi2014\Finished_day%d"%i + tag + '.picke'
                result = pickle.load(open(file_name,'rb'))
                open(file_name,'rb').close()
                #save to csv
                carDensity = result["carDensity"]
                out_CarDensity = []
                for m in range(24*4):
                    NumCar=0
                    for s in range(60*15):
                        NumCar += carDensity[m*s+s]
                    out_rows.writerow([m, NumCar/900])
                print S_flex,R_flex,"carDensity result updated in csv"
                print
    csv_out.close()
def AnalyzeFeasibilityTransferByTime():
    for i in range(3,4):
        csv_out = open('Feasibility&Transfer.csv',"wb")
        out_rows = csv.writer(csv_out)
        out_rows.writerow(["day%d"%i])
        out_rows.writerow(["feasible_stime","tranfertime"])
        for x in range(2,3):
            S_flex = 1+x/10.0
            for y in range(5,6):
                R_flex = 1+y/10.0
                tag = "_"+str(S_flex)+"_"+str(R_flex)
                file_name = "ChicagoTaxi2014\Finished_day%d"%i + tag + '.picke'
                result = pickle.load(open(file_name,'rb'))
                open(file_name,'rb').close()
                #save to csv
                R = result['Requests']
                feasible_stime = []
                feasible_etime = []
                tranfer_time = []
                for r in R:
                    if len(r.ml) > 0:
                        feasible_stime.append(r.st)
                        feasible_etime.append(r.et)
                        if r.ml[-1][-1] >0:
                            for index in range(len(r.ml)-1):
                                if r.ml[index][-1] != r.ml[index+1][-1]:
                                    tranfer_time.append((r.ml[index][-3]+r.ml[index+1][-3])/2)
                timeslices = []
                for z in range(4*24):
                    timeslices.append([0,0])
                for z in feasible_stime:
                    if z/(60*15) > 4*24-1:
                        timeslices[-1][0] += 1
                    else:
                        timeslices[z/900][0] += 1
                for z in tranfer_time:
                    if z/(60*15) > 4*24-1:
                        timeslices[-1][1] += 1
                    else:
                        timeslices[z/900][1] += 1
                for z in timeslices:
                    out_rows.writerow(z)
                print S_flex,R_flex,"Feasibility&Transfer result updated in csv"
                print
    csv_out.close()
def AnalyzeFlexibility():
    csv_in = open("OverallResults.csv","rb")
    in_rows = csv.reader(csv_in, delimiter=',')
    F=[]
    T=[]
    for x in range(5):
        F.append([0]*20)
        T.append([0]*20)
    for i in in_rows:
        if i[0] != "day":
            carFlex = float(i[5])
            reqFlex = float(i[6])
            feasibility = float(i[7])*100/float(i[3])/21.0
            tranferPercentage = float(i[9])*100/float(i[3])/21.0
            x = int((carFlex*10-10))-1
            y = int((reqFlex*10-10))-1
            F[x][y] += feasibility
            T[x][y] += tranferPercentage
            print feasibility, tranferPercentage
            print float(i[7])*100, float(i[3])
            print float(i[9])*100
            print
    csv_out = open('FLexibility.csv',"wb")
    out_rows = csv.writer(csv_out)
    for x in F:
        out_rows.writerow(x)
    csv_out.close()
def AnalyzeCPUtime():
        csv_out = open('CPUtimeAnalysis.csv',"wb")
        out_rows = csv.writer(csv_out)
        out_rows.writerow(["day","carFlex","ReqFlex","averageCPU","worstCaseCPU","MaxNumCar/s","averageNumCar/s"])
        for i in range(1,32):
            for x in range(1,6):
                S_flex = 1+x/10.0
                for y in range(1,21):
                    R_flex = 1+y/10.0
                    tag = "_"+str(S_flex)+"_"+str(R_flex)
                    file_name = "ChicagoTaxi2014\Finished_day%d"%i + tag + '.picke'
                    try:
                        result = pickle.load(open(file_name,'r'))
                        open(file_name,'r').close()
                        averageCPU = float(result["total_time"])/len(result['Requests'])
                        worstCaseCPU = -1
                        for ct in result['cpu_t']:
                            worstCaseCPU = max(ct, worstCaseCPU)
                        max_cd = -1
                        count_cd = 0
                        carDensity  = result["carDensity"]
                        for cd in carDensity:
                            count_cd += cd
                            max_cd = max(max_cd,cd)
                        averageNumCar =  float(count_cd)/len(carDensity)
                        print "day",i
                        out_rows.writerow([i,S_flex, R_flex,averageCPU, worstCaseCPU, max_cd,averageNumCar])
                        print S_flex,R_flex,"General result updated in csv"
                    except IOError:
                        print file_name, "not find"
                        missing.append(file_name)
                    #save to csv
        csv_out.close()
def CPUtime3D():
    csv_in = open("OverallResult.csv","rb")
    in_rows = csv.reader(csv_in, delimiter=',')
    CPUtime = []
    NumReq = []
    for x in range(5):
        CPUtime.append([0]*20)
        NumReq.append([0]*20)
    for i in in_rows:
        if i[0] != "day":
            carFlex = float(i[1])
            reqFlex = float(i[2])
            x = int((carFlex*10-10))-1
            y = int((reqFlex*10-10))-1
            CPUtime[x][y] += i[5]
            NumReq[x][y] += i[10]
    csv_out = open('AvgCPUtime3D.csv',"wb")
    out_rows = csv.writer(csv_out)
    for x in range(5):
        out_rows.writerow(float(CPUtime[x])/NumReq)
    csv_out.close()
def AnalyzeTransferLocation():
    tranferTimes = [0]*78
    for i in range(1,32):
        for x in range(2,3):
            S_flex = 1+x/10.0
            for y in range(5,6):
                R_flex = 1+y/10.0
                tag = "_"+str(S_flex)+"_"+str(R_flex)
                file_name = "ChicagoTaxi2014\Finished_day%d"%i + tag + '.picke'
                try:
                    result = pickle.load(open(file_name,'r'))
                    open(file_name,'r').close()
                    for r in result['Requests']:
                        if len(r.ml)>0:
                            for ass in range(len(r.ml)-2):
                                if r.ml[ass][-1] != r.ml[1+ass][-1]:
                                    node = r.ml[ass][0]
                                    tranferTimes[node] += 1
                    print "day",i
                    print S_flex,R_flex,"General result updated in csv"
                except IOError:
                    print file_name, "not find"
                    missing.append(file_name)
    csv_out = open('TransferLocation.csv',"wb")
    out_rows = csv.writer(csv_out)
    out_rows.writerow(["tranferTimes"])
    print tranferTimes
    for t in tranferTimes:
        out_rows.writerow([t])
    csv_out.close()



#CPUtime3D()
#AnalyzeCPUtime()
#AnalyzeFlexibility()
#AnalyzeCarDensity()
#AnalyzeOverAll()
#AnalyzeFeasibilityTransferByTime()
AnalyzeTransferLocation()
