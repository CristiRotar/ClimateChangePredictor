import csv
import os


def loadData(fileName, inputVariabName1, inputVariabName2, inputVariabName3, outputVariabName):
    data = []
    dataNames = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dataNames = row
                monthIndex = row.index(inputVariabName2)
                valueIndex = row.index(outputVariabName)
            else:
                if row[monthIndex] != 'Meteorological year' and '?' not in row[monthIndex]:
                    data.append(row)
                    # if data[line_count][valueIndex] != '':
                    #     firstValidValue = data[line_count][valueIndex]
                    # else:

            line_count += 1

        selectedVariable1 = dataNames.index(inputVariabName1)
        selectedVariable2 = dataNames.index(inputVariabName2)
        selectedVariable3 = dataNames.index(inputVariabName3)
        inputs = [[data[i][selectedVariable1], data[i][selectedVariable2], data[i][selectedVariable3]] for i in range(len(data))]
        selectedOutput = dataNames.index(outputVariabName)
        outputs = [data[i][selectedOutput] for i in range(len(data))]
        return inputs, outputs





if __name__ == '__main__':
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data', 'FAOSTAT_data_1-10-2022.csv')
    inputs, outputs = loadData(filePath, 'Area', 'Months', 'Year', 'Value')
    print("hi")

