import random
import matplotlib.pylab as plt
import numpy as np
import Person


class Staffing:
    #Creates a staffing simulation, which will run our experiment, and house the data used to visualize
    def __init__(self, annualPercent, employeeNumbers):
        self.Staff = []
        self.employeeCount = employeeNumbers
        for i in range(0,self.employeeCount): self.Staff.append(Person.Person())
        self.totalHoursPerWeek = (40*self.employeeCount)
        self.APLUTE = {}
        self.HPUTE = {}
        self.completedProjects={}
        self.manHours = (50*40*self.employeeCount)
        self.projectCounts = {}
        self.halfTimeProjects = {}
        self.halfTimePercentWeekly ={}
        self.halfTimeGoal = annualPercent
        self.annualUTE = 0.0

    def generateWeek(self, AWmean, AWsd, week):
        # Variables:
        #
        #   AWmean = Project Week Runtime, as a mean for a Gaussian distribution
        #   AWsd = Standard deviation of Project runtime in weeks for a Gaussian distribution
        halftimeCount=0
        projectCount =0
        if week==0:
            for person in self.Staff:
                firstStaff = random.randint(0,self.employeeCount)
                if firstStaff <= (self.employeeCount-(self.halfTimeGoal*self.employeeCount)):
                    halfChance = random.random()
                    weeks = int(np.random.normal(AWmean, AWsd))
                    if(halfChance <= self.halfTimeGoal/2):
                        person.staffed(20, weeks, int(weeks/2))
                        halftimeCount += 1
                    else:
                        person.staffed(40, weeks, int(weeks/2))
                        projectCount += 1
                else:
                    pass
        else:
            for person in self.Staff:
                person.updateTime()
                person.checkProjects()
                if(person.timeStaffed == 40):
                    pass
                else:
                    probability = self.staffProbability(person.weeksSinceLastStaffing)
                    staffChance = random.random()
                    if(probability>=staffChance):
                        timeChoice = random.choice([20,40])
                        if(timeChoice ==20):
                            halftimeCount +=1
                        person.staffed(timeChoice,int(np.random.normal(AWmean, AWsd)), 1)
                        projectCount += 1
                        if (person.timeStaffed > 40):
                            person.adjustTime()
                            projectCount-=1
                    else:
                        person.timeSinceLastStaffing()
        self.halfTimeProjects[week]=halftimeCount
        self.projectCounts[week]=projectCount
                
                                 
    def staffProbability(self, weeksSinceLastStaff):
        #generates the probability that a person will be staffed, based upon when they were last staffed.
        #Expected Value: Approximately 5
        #Variable:
        #
        # weeksSinceLastStaff: integer that represents how long it has been since person was last staffed.
        #
        prob= {
            0: 0.001,
            1: 0.05,
            2: 0.3,
            3: 0.45,
            4: 0.5,
            5: 0.6,
            6: 0.7,
            7: 0.8,
            8: 0.9,
            9: 1.0
        }
        return prob[weeksSinceLastStaff]  

    def analyzeWeek(self, week):
        #Analyzes the week, getting for us the UTE, the Average Project Length for that week, and the percentageofHalfStaffProjects after modification
        count = 0
        weeks = 0
        hours = 0
        projectCount = 0
        for person in self.Staff:
            if person.projectsStaffed >= 1: 
                projectCount += 1
                if person.projectsStaffed == 2:
                    count+=1
            weeks += person.calculateAPL()
            hours += person.timeStaffed
        if projectCount ==0:
            percentHalfStaffed = 0.0
        else:
            percentHalfStaffed = count/projectCount
        averageProjectLength = weeks/100
        ute = hours/self.totalHoursPerWeek
        self.APLUTE[averageProjectLength]= ute
        self.HPUTE[percentHalfStaffed] = ute
        self.halfTimePercentWeekly[percentHalfStaffed]= week

    def displayData(self, choices):
        #displays the data for our file, by first displaying our data as a Dataframe
        apList = self.APLUTE.items()
        apList = sorted(apList)
        aX, aY = zip(*apList)

        plt.plot(aX, aY)
        plt.xlabel('Average Project Length')
        plt.ylabel('UTE')
        plt.title("UTE on Average Project Length")
        plt.show()

        hpList = self.HPUTE.items()
        hpList = sorted(hpList)
        hx, hY = zip(*hpList)
        #multiply hY by gaussian normal between 0 and 1
        plt.scatter(hx, hY)
        plt.xlabel('Percent of Half Staffed')
        plt.ylabel('UTE')
        plt.title("UTE on Percent of Half Staffed")
        plt.show()

        for person in choices:
            employeeList =self.Staff[person].yearlyTime.items()
            employeeList = sorted(employeeList)
            employeeX, employeeY = zip(*employeeList)
            plt.yticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
            plt.plot(employeeX, employeeY)
            plt.savefig('plot'+str(person)+'.png')
        plt.title("Annual Employee Scheduling Sample")
        plt.legend(employeeX)
        plt.show()


    def employeeYear(self, choices, week):
        #Looks at the employee data for the year, and analyzes to showcase what it looks like from their view for a year. 
        #
        #Variables:
        #
        #  choice: an list of integers which are our employee selction for that year. 
        for person in choices:
            self.Staff[person].trackTime(week)

    def analyzeYear(self, UTECollection):
        #Analyzes the UTE values obtained over the year, and brings them together into a single value based upon the average of that year. 
        #
        # Variables:
        #
        # UTECollection: a dictionary containing the annual value of UTE, with the key being the percent half time of projects for that year. 
        for key in self.HPUTE.keys():
            self.annualUTE += self.HPUTE[key]
        self.annualUTE = self.annualUTE/50
        UTECollection[self.halfTimeGoal] = self.annualUTE

    def displayUTETotal(self, UTECollection, beginPoint, endPoint):
        #Displays the Annual UTE values, displaying them on a graph with the percentage of values we expected to see.
        # 
        # Variables:
        # 
        # UTECollection: a dictionary containing the annual value of UTE, with the key being the percent half time of projects for that year
        # beginPoint: the start of our x axis on our graph, given as the first value in our range. 
        # endPoint: the end of our y axis on our graph, gives as the last value in our range. 
        uteList = UTECollection.items()
        uteList = sorted(uteList)
        uteX, uteY = zip(*uteList)
        plt.plot(uteX, uteY)
        plt.yticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
        plt.xlabel('Percent of Half Staffed (per Year)')
        plt.xlim(beginPoint, endPoint)
        plt.ylabel('Average Utilization (per Year)')
        plt.title("UTE on Percent of Half Staffed")
        plt.show()

    def projectGoalAnalysis(self):
        #Looks at the number of projects staffed compared to the goal, 
        # if half staff is above that, 
        # then update the weeks that had low total project counts with 40 a week and recalculate annual UTE. 
        halfTimeProjectTotal = 0
        projectTotal =0
        employeeHours =0
        for i in range(0,50):
            halfTimeProjectTotal += self.halfTimeProjects[i]
            projectTotal += self.projectCounts[i]
        if(halfTimeProjectTotal/projectTotal) < self.halfTimeGoal:
            for key in self.HPUTE.keys():
                if key > self.halfTimeGoal:
                    for employee in self.Staff:
                        timeStaffed = employee.yearlyTime[self.halfTimePercentWeekly[key]]
                        if timeStaffed <= 40 and timeStaffed !=0:
                            if employee.weeklyProjectsStaffed[self.halfTimePercentWeekly[key]]==1:
                                employee.yearlyTime[self.halfTimePercentWeekly[key]] = 40
                            elif employee.weeklyProjectsStaffed[self.halfTimePercentWeekly[key]==2]:
                                employee.yearlyTime[self.halfTimePercentWeekly] = 40
                                employee.weeklyProjectsStaffed = 1
            self.HPUTE.clear()
            for i in range(0,50):
                for employee in self.Staff:
                    projectTotal += employee.weeklyProjectsStaffed[i]
                    if projectTotal == 2:
                        halfTimeProjectTotal += employee.weeklyProjectsStaffed[i]
                    elif projectTotal ==1:
                        if employee.yearlyTime[i] == 20:
                            halfTimeProjectTotal += employee.weeklyProjectsStaffed[i]
                    employeeHours += employee.yearlyTime[i]
                ute = employeeHours/self.totalHoursPerWeek
                projectsHalfPercent = halfTimeProjectTotal/projectTotal
                self.HPUTE[projectsHalfPercent] = ute
                    
            

if __name__ =="__main__":
    annualUTEAverage ={}
    employeeCount = 1000
    for j in np.arange(0.0,0.4,0.025):
        for k in range(0,5):
            staffing = Staffing(j, employeeCount)
            staffChoices = random.sample(range(0,employeeCount), 5)
            for i in range(0,50):
                staffing.generateWeek(12, 3, i)
                staffing.analyzeWeek(i)
                staffing.employeeYear(staffChoices, i)
            staffing.projectGoalAnalysis()
            staffing.analyzeYear(annualUTEAverage)
        #staffing.displayData(staffChoices)
    staffing.displayUTETotal(annualUTEAverage, 0.0, 0.4)   

    
