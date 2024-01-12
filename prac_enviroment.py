from typing import List

class Environment:
    env:List
    def __init__(self):
        self.env=[{}]

    def enter_scope(self):
        self.env.append({})

    def exit_scope(self):
        assert self.env
        self.env.pop()

    def add(self,name,value):
        print("add_env ",name,value)
        if name not in self.env[-1]:
            print("add_env ",name,value)
            self.env[-1][name]=value
        # else:
        #     print(" ")
        #     print("786")
        #     self.update(name,value)
    
    def get(self,value):
        for dict in reversed(self.env):
            print("self.env1 ",dict)
            if value in dict:
                print("self.env2 ",value," ",dict[value])
                return dict[value]
        raise KeyError()

    def check(self,name):
        for dict in reversed(self.env):
            if name in dict:
                return True
            else:
                return False
            
    def update(self,name,value):
        for dict in reversed(self.env):
            if name in dict:
                dict[name]=value
                return
        raise KeyError()
    

class TypeError(Exception):
    pass



                
