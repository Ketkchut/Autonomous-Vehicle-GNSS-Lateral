import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

class main(object):
    
    def __init__(self):
        
        self.value_min = 20
        self.value_max = 150
        self.value_step = 2
        
        self.number = 0
        self.window_size = 20                                        
        self.speed_buff = []                                         
        self.sum_speed = 0.0                                
        self.filter_speed = []
        
        self.raw_buffer = []
        self.filter_buffer = []
        self.mean_raw = []
        self.mean_filter = []
        
        self.DigitalPoten = list(range(self.value_min, self.value_max+1, self.value_step))
        
        self.readcsv()
        self.plot()

    def readcsv(self):
        
        for i in range(self.value_max +1): 
            
            self.number = i
            
            if (i >= self.value_min)&(i % 2 == 0):
                
                name = "backward_240465/value_b_%d.csv" %i
                self.df = pd.read_csv(name)
                self.time = self.df.time_operate
                self.raw_speed = self.df.raw_speed
                
                self.MovingAverage()
                
    def MovingAverage(self):
        
        for x in range(len(self.raw_speed)):                        
    
            self.speed_buff.append(self.raw_speed[x])          
            
            self.sum_speed = self.sum_speed + self.raw_speed[x]        
            
            if len(self.speed_buff) > self.window_size:                
                
                self.sum_speed = self.sum_speed - self.speed_buff.pop(0) 
                
                self.speed_ms = float(self.sum_speed)/len(self.speed_buff) 
                
                self.filter_speed.append(self.speed_ms) 
                     

        if len(self.filter_speed) < len(self.time):
            
            for j in range(self.window_size):
                
                self.filter_speed.append(self.filter_speed[-1])
            
        self.mean()   

    def mean(self):
        
        if len(self.filter_speed) != len(self.time):
            print(self.number)
               
        if len(self.filter_speed) == len(self.time):
    
            for i in range(len(self.filter_speed)):
                
                if self.time[i] > 15:
                    self.filter_buffer.append(self.filter_speed[i])
                    self.raw_buffer.append(self.raw_speed[i])
                    
            self.mean_filter.append(mean(self.filter_buffer))   
            self.mean_raw.append(mean(self.raw_buffer))
            
        self.filter_buffer = []   
        self.raw_buffer = []
        self.filter_speed = []
                 
    def plot(self):
        
        print(self.mean_filter)
        print(len(self.mean_filter))
        print(len(self.mean_raw))
        print(len(self.DigitalPoten)) 
                
        plt.plot(self.DigitalPoten ,self.mean_raw ,color='red',label='Raw')
        plt.plot(self.DigitalPoten ,self.mean_filter ,color='blue',label='filter')
        
        plt.xlim([10 , 160])
        plt.ylim([0, 6])
        plt.xlabel("DigitalPoten Value")
        plt.ylabel("Velocity (Km/hr)")
        plt.title("Backard Speed Control By Digital Poten")
        plt.legend()
        plt.show() 

if __name__ == "__main__":
    try:
        cls = main()
    except KeyboardInterrupt:
        print("End Program..")    
