class Person:
    #creation of the person, who will be staffed on a project. 
    def __init__(self):
        self.timeStaffed=0
        self.projectsStaffed=0
        self.weeklyProjectsStaffed ={}
        self.weeksOnProject=[]
        self.weeksSinceLastStaffing=0
        self.yearlyTime = {}
        
    def staffed(self, timeAllotted, projectLength, projectCount):
        ##staffs the person on a project, with a time allotted and a project length 
        self.timeStaffed += timeAllotted
        self.projectsStaffed += 1
        self.weeksOnProject.append([projectLength, projectCount, self.projectsStaffed, timeAllotted])
        self.weeksSinceLastStaffing=0

    def timeSinceLastStaffing(self):
        #increases the weeksSinceLastStaffing by 1
        self.weeksSinceLastStaffing +=1

    def downTime(self, timeReturned, weeksOffProject, projectNumber):
        #Showcases the downtime a person may have after a project is finished.         
        self.weeksOnProject.remove([weeksOffProject, weeksOffProject, projectNumber, timeReturned])
        self.timeStaffed -= timeReturned
        self.projectsStaffed -=1

    def updateTime(self):
        #goes through and updates the project count for each project.
        for project in self.weeksOnProject:
            project[1]+=1
    
    def checkProjects(self):
        #Goes through and looks at each projects, calling downtime for the ones that will be staffed off. 
        for project in self.weeksOnProject:
            if project[0]==project[1]:
                self.downTime(project[3], project[0], project[2])
            
    
    def calculateAPL(self):
        #Calculates the average project length for the person
        weeks =0
        for project in self.weeksOnProject:
            weeks += project[0]
        if self.projectsStaffed == 0:
            return 0
        else:
            return int(weeks/self.projectsStaffed)

    def trackTime(self, week):
        #tracks the time on a week to week basis for the person
        self.yearlyTime[week] = self.timeStaffed
        self.weeklyProjectsStaffed[week]= self.projectsStaffed

    def adjustTime(self):
        #adjusts the trime so that way we better reflect the fact that a person cannot go over 40 hours per week. 
        removeItem = self.weeksOnProject[-1]
        self.weeksOnProject.remove([removeItem[0], removeItem[1], removeItem[2], removeItem[3]])
        timeRemoval = removeItem[3]
        self.timeStaffed -= timeRemoval
        self.projectsStaffed -=1