from os import listdir, getcwd
from easygui import diropenbox, msgbox
from pandas import DataFrame, read_excel

class SumExcel(): 

    def __init__(self): 
        # setup

        # check if the folder to find all excel exist 
        self.folder_path = self._askFolder()
        # find excel names under this directory 
        allExcelNames = self._findExcel(self.folder_path)
        # get excel data
        tables_of_sums = self._splitTablesAndSum(allExcelNames)
        # save as csv
        self._toCSV(obj=tables_of_sums)
        pass

    def _askFolder(self) -> str: 
        Path = diropenbox()
        Path += "\\"
        return Path

    def _findExcel(self, folderPath: str) -> list[str]:
        '''
        store all excel filenames with ".xlsx" in a list
        ''' 
        excelNames = []
        for exceFile in listdir(folderPath): 
            if exceFile.endswith(".xlsx") and exceFile != "output.xlsx":  # just to ignore the output one
                excelNames.append(folderPath+exceFile)
        return excelNames

    def _splitTablesAndSum(self, listOfNames: list[str]) -> list[DataFrame]: 
        N = len(listOfNames)
        for i, excelName in enumerate(listOfNames): 
            if i == 0: 
                tables = []
                for j in range(6): 
                    df = read_excel(
                        excelName, 
                        sheet_name="Analysis", 
                        header=0,
                        usecols="A:L", 
                        index_col=0, 
                        nrows=8,
                        skiprows=j*10,  
                        engine="openpyxl")
                    tables.append(df)
            else: 
                for j in range(6): 
                    df = read_excel(
                        excelName, 
                        sheet_name="Analysis", 
                        header=0,
                        usecols="A:L", 
                        index_col=0, 
                        nrows=8,
                        skiprows=j*10,  
                        engine="openpyxl")
                    tables[j] += df
            print(f'{i+1}/{N} done', end="\r")
        return tables

    def _sumAndSave(self, listOfNames: list[str]) -> DataFrame:
        """
        this is an old method
        """
        output = DataFrame({})
        numberOfJobs = len(listOfNames)
        for job, name in enumerate(listOfNames):
            df = read_excel(self.folder_path+name, sheet_name="Analysis")  # transform to DataFrame
            if output.empty:
                output = df.copy()
                rowOfNan = [i for i, isSth in enumerate( output.any(axis=1) ) if isSth == False]  # find row_indices of Nan
                # so if row_indices+1, means the start(heading) of the next table
            else:
                for i, row_idx in enumerate(rowOfNan): 
                    if i == 0:  # first table is different
                        # the first table starts with 0 upto the first nan row_index [0:row_idx:, bla], and ignore the first column [bla, 1:] (as they are str)
                        output.iloc[0:row_idx, 1:] += df.iloc[0:row_idx, 1:]
                        last_row_idx = row_idx  # save the last row_index
                    elif i == len(rowOfNan)-1:  # last table is different too
                        # the last table starts with the last nan row_index and the rest [row_idx+2:, bla], and ignore the first column [bla, 1:] (as they are str)
                        output.iloc[row_idx+2, 1:] += df.iloc[row_idx+2, 1:]
                    else:
                        # the middle tables start with the last nan row_index+2 (itself and the next headings) upto the next nan row_index [last_row_idx+2:row_idx, bla], 
                        # and ignore the first column [bla, 1:] (as they are str)
                        output.iloc[last_row_idx+2:row_idx, 1:] += df.iloc[last_row_idx+2:row_idx, 1:]
                        last_row_idx = row_idx  # save the last row_index
            print(f'{job+1}/{numberOfJobs} done', end='\r')
        return output

    def _toExcel(self, df: DataFrame, fileName: str="output.xlsx"): 
        # TODO check name
        # create path
        path = self.folder_path + fileName
        # save
        df.to_excel(path, index=False)
        # masbox to inform where to find
        msgbox(f'find your output.xlsx in the directory, \n{path}\nyou better highlight and copy it and save it somewhere else.', title='Done', ok_button="Got it")
        pass

    def _toCSV(self, obj: list[DataFrame], intialName: str="output"): 
        for i, df in enumerate(obj): 
            df.to_csv(f'{intialName}{i+1}.csv')
        # masbox to inform where to find
        msgbox(f'find your csv files with name "{intialName}" in the directory, \n{getcwd()}\nyou better highlight and copy it and save it somewhere else.', title='Done', ok_button="Got it")
        
if __name__ == "__main__": 
    SumExcel()
