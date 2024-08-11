import pandas as pd


class Context:
    def __init__(self, file_path:str=None, step_size:int=128):
        self.file_path = file_path
        self.step_size = step_size
        self.df = None


    def get_file_path(self):
        if self.file_path is None:
            raise ValueError('File path is not set.')
        return self.file_path
    
    def get_step_size(self):
        return self.step_size
    
    def set_file_path(self, file_path:str | None):
        if file_path is None:
            raise ValueError('File path cannot be None.')
        self.file_path = file_path

    def set_step_size(self, step_size:int):
        self.step_size = step_size

    def load_file(self):
        self.df = pd.read_csv(self.file_path)
        
    
    def load_file_with_file_path(self, file_path:str | None):
        if file_path is None:
            raise ValueError('File path cannot be None.')
        self.df = pd.read_csv(file_path)
        
    def get_dataframe(self):
        if self.df is None:
            raise ValueError('Dataframe is not loaded.')
        return self.df
    
    def get_unique_memory(self):
        if self.df is None:
            raise ValueError('Dataframe is not loaded.')
        return self.df['Memory'].unique()
    
    def get_unique_input(self):
        if self.df is None:
            raise ValueError('Dataframe is not loaded.')
        return self.df['Input'].unique()
    
    def get_execution_time(self, memory:int, input:int):
        if self.df is None:
            raise ValueError('Dataframe is not loaded.')
        return self.df[(self.df['Memory'] == memory) & (self.df['Input'] == input)]['Duration'].values[0]
    
    def get_dataframe_at_memory_input(self, memory:int, input:int):
        if self.df is None:
            raise ValueError('Dataframe is not loaded.')
        return self.df[(self.df['Memory'] == memory) & (self.df['Input'] == input)]