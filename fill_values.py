#!/usr/bin/env python
# coding: utf-8

# In[1]:

from operator import index
import math   

def fill_missing():
    #data    
    with open("./testData.txt", 'r') as dataIn:
        data=dataIn.readlines()
    dataIn.close()

    #dataLabel
    with open("./testLabel.txt", 'r') as dataIn:
        dataLabel=dataIn.readlines()
    dataIn.close()

    #number of rows
    print("Rows Data {}".format(len(data)))
    print("Rows Label {}".format(len(dataLabel)))
    cleanData_json={}
    amountOfFeatures=0
    highest=1.00000000000000e+99

    for i in range(0, len(data)):
        temp_data=data[i].split("\t")
        amountOfFeatures=len(temp_data)
        #hold indexes of empty values
        highest=1.00000000000000e+99
        count=0
        #find column that the empty value is in
        index_of_empty=[]
        index_with_values=[]
        for j in range(0, len(temp_data)):
            if float(temp_data[j]) == float(highest):
                index_of_empty.append(j)
                count+=1
            else:
                index_with_values.append(j)
        
        cleanData_json.update({i:[temp_data, count, index_of_empty, index_with_values]})

    print("Amount of features {}".format(amountOfFeatures))

   #[ key for row in data : [original data , amount of empty data,[indexes of all empty values], [index with values]]  ]
    #now I have the 'clean' data but still with empty values...supposed to be set to the 1E9th
     
    
    def eucDist(primaryRow, index_withValues, iterationRow, index_NoValues):
        def dist(a,b):
            temp=float(a-b)
            return temp*temp

        sumDist =0
        columnsUsed =[]
        if len(cleanData_json[primaryRow][0])!= len(cleanData_json[iterationRow][0]):
            return False
        else:
            #for each column that has values in rowA
            for index in index_withValues:
                
                #if the current column is NOT null in the rowB
                #that means this column for Row A is not null AND the this colmn is not null for Row B
                #get euc dist
                if index not in index_NoValues:
                    columnsUsed.append(index)
                    value_fromRowA=cleanData_json[primaryRow][0][index]
                    value_fromRowB=cleanData_json[iterationRow][0][index]
                    distance=dist(float(value_fromRowA),float(value_fromRowB) )
                    sumDist+=distance
            EucDist=math.sqrt(sumDist)
            return [EucDist, columnsUsed]
                    

    rows=list(cleanData_json.keys())
    Knn_NullValue_columns_json={}

    for cur_data_row in rows:
        #list of columns with values
        values=cleanData_json[cur_data_row][3]
        data_perRow={}
        #need to find euclidean distance from cur_data_row to every other row
        
        for knn_row in rows:
            if knn_row != cur_data_row:
                temp_indices_of_nullData=cleanData_json[knn_row][2]
                
                
                #returns [sumDist, columnsUsed]
                response=eucDist(cur_data_row, values, knn_row, temp_indices_of_nullData)
                #update the relatinship between current row and row we are comparing it to
                data_perRow.update({knn_row: response})
        #update the data per row from every other row    
        Knn_NullValue_columns_json.update({cur_data_row: data_perRow})
        if int(cur_data_row) % 10 ==0:
            temp=list(data_perRow.keys())[0]
            # print("Row {} and info from {} row".format(str(cur_data_row), str(temp)))
            temp=list(data_perRow.keys())[0]
            # print(data_perRow[temp])
            # print("")

    #i have all knn values of each row with what columns the value for derived each row
    # Knn_NullValue_columns_json

    #current cleandatajson====
    #[ key for row in data : [original data , amount of empty data,[indexes of all empty values], [index with values]]  ]
    #now I have the 'clean' data but still with empty values...supposed to be set to the 1E9th

    s=list(Knn_NullValue_columns_json.keys())
    ValuesKnned=0
    for x in range (0, len(s)):
        data_for_currentRow=Knn_NullValue_columns_json[s[x]]
        indexofNullValues=cleanData_json[s[x]][2]
            
        #rows that contributed
        row_Contribution=[]
    #     print(indexofNullValues)
        
        for emptyValuekey in indexofNullValues:
            newValue=float(0)
            KNNdata_for_currentRow=Knn_NullValue_columns_json[s[x]]
    #knn dict holds k:(k-1)
    #so keys should not be hhave k 0:123  , 1:023 , 2:013
    #         print("type of empty Value {}".format(str(type(emptyValuekey))))
            for keys in KNNdata_for_currentRow:
                if emptyValuekey in cleanData_json[keys][3]:
                    valueFromOriginal=cleanData_json[keys][0][emptyValuekey]
                    
                    temp=row_Contribution
                    row_Contribution.append(float(valueFromOriginal))
                
                    
            row_Contribution.sort()
    #         print(row_Contribution)
            knn=math.sqrt(len(row_Contribution))
            temp=float(0)
            if knn !=0:
                ValuesKnned+=1
                for y in range(0, int(knn)):
                    temp+=row_Contribution[y]

                newValue=temp/int(knn)
                cleanData_json[s[x]][0][emptyValuekey] =newValue   
    #             #at this stage I have the rows that can contribute to the empty value
            else:
                print("a value was not found")
        if x%15==0:
            print("Done with row {}".format(str(x)))
    # for eachRow in cleanData_json:
    #     emptyVal=0
    #     highest=1.00000000000000e+99
    #     for numbers in cleanData_json[eachRow][0]:
    #         if float(numbers)==float(highest):
    #             emptyVal+=1
    #     print("Row {}: old amount of empty Vals {} , new amount of empty vals {}".format(str(eachRow),str(cleanData_json[eachRow][1]), str(emptyVal)))
    #     print("Value changed = {}".format(str(ValuesKnned)))
    with open("./NewNonEmptyValues.txt", 'w') as o:
        for everything in cleanData_json:
            o.write(str(cleanData_json[everything][0]))
    o.close()
            
fill_missing()




