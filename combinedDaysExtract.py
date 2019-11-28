import pickle,csv
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
portions = [4000, 2000, 1000, 800,400,200,100, 80, 40 ,20, 10 , 8,4,3,2,1,]


csv_out = open('NumCarPerDay&Feasibility.csv',"wb")
out_rows = csv.writer(csv_out)
out_rows.writerow(["general information: reqFlex =1.5, carFlex=1.2, NumReq: NumCar =1:2, testcases collect from Jan3,10,17,24"])
out_rows.writerow(["Num Car/day", "feasible request(%)", "tranfered(%)"])
for p in portions:
    file_name = 'ChicagoTaxi2014/CombinedDaysFinished_'+str(p)+'.picke'
    result = pickle.load(open(file_name,'r'))
    open(file_name,'r').close()
    NumCar = len(result['Supplies'][::p])
    NumReq = len(result['Requests'][::p])
    t = result['total_transfer']
    f = result['n_feasible']
    tpercent = 0
    if f !=0:
        tpercent= float(t)*100/float(f)
    out_rows.writerow([NumCar,float(f)*100/NumReq, tpercent])
    print p, "complete"
csv_out.close()
