import random
from model import BuildingLoad, HourlyState, RandomEvent




class Testing:
    def __init__(self, control):

        self.control = control
        self.hours = 24
        self.building_count = 10

    def run(self):

        total_cost = 0.0

        for hour in range(self.hours):
            state = self.generate(hour)
            output = self.control.update(state)
            
            total_cost += 


        return total_cost

        #repeats 24 hours

       #7-10 buildings

        #generate the bullshit
        
        #run control

        #validate is it cooked
  
        #add cost
  
        #print random bullshit

     
     def generate(self, hour) -> HourlyState:

  

    
        