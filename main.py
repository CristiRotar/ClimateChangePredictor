import csv
import os



def loadData(fileName, inputVariabName1, inputVariabName2, inputVariabName3, outputVariabName):
    data = []
    dataNames = []
    indexesWithNULLValue = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        startIndex = -1
        endIndex = -1
        for row in csv_reader:
            if line_count == 0:
                dataNames = row
                monthIndex = row.index(inputVariabName2)
                valueIndex = row.index(outputVariabName)
                line_count += 1
            else:
                if row[monthIndex] != 'Meteorological year' and '?' not in row[monthIndex]:
                    data.append(row)
                    if data[line_count-1][valueIndex] == '':
                        if startIndex == -1:
                            startIndex = line_count - 1
                        else:
                            endIndex = line_count - 1
                    else:
                        if startIndex != -1:
                            if endIndex == -1:
                                indexesWithNULLValue.append([startIndex, startIndex])
                            else:
                                indexesWithNULLValue.append([startIndex, endIndex])
                            startIndex = -1
                            endIndex = -1
                    line_count += 1
        for list in indexesWithNULLValue:
            mean = (float(data[list[0]-1][valueIndex]) + float(data[list[1]+1][valueIndex])) / 2
            for i in range(list[0], list[1]+1):
                data[i][valueIndex] = mean
        selectedVariable1 = dataNames.index(inputVariabName1)
        selectedVariable2 = dataNames.index(inputVariabName2)
        selectedVariable3 = dataNames.index(inputVariabName3)
        inputs = [[data[i][selectedVariable1], data[i][selectedVariable2], data[i][selectedVariable3]] for i in range(len(data))]
        selectedOutput = dataNames.index(outputVariabName)
        outputs = [round(float(data[i][selectedOutput]), 4) for i in range(len(data))]
        return inputs, outputs


if __name__ == '__main__':
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data', 'FAOSTAT_data_1-10-2022.csv')
    inputs, outputs = loadData(filePath, 'Area', 'Months', 'Year', 'Value')

