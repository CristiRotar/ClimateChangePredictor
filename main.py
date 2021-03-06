import csv
import os
import matplotlib.pyplot as plt

import numpy as np

from LinearRegressor import LinearRegressor
from SGDRegressor import SGDRegressor
from Scaler import normalisation
from sklearn.model_selection import train_test_split


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
                    if data[line_count - 1][valueIndex] == '':
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
            mean = (float(data[list[0] - 1][valueIndex]) + float(data[list[1] + 1][valueIndex])) / 2
            for i in range(list[0], list[1] + 1):
                data[i][valueIndex] = mean
        selectedVariable1 = dataNames.index(inputVariabName1)
        selectedVariable2 = dataNames.index(inputVariabName2)
        selectedVariable3 = dataNames.index(inputVariabName3)
        inputs = [[data[i][selectedVariable1], data[i][selectedVariable2], data[i][selectedVariable3]] for i in
                  range(len(data))]
        selectedOutput = dataNames.index(outputVariabName)
        outputs = [round(float(data[i][selectedOutput]), 4) for i in range(len(data))]
        return inputs, outputs


def splitData(inputs, outputs):
    np.random.seed(5)
    indexes = [i for i in range(len(inputs))]
    trainSample = np.random.choice(indexes, int(0.8 * len(inputs)), replace=False)
    validationSample = [i for i in indexes if not i in trainSample]

    trainInputs = [inputs[i] for i in trainSample]
    trainOutputs = [outputs[i] for i in trainSample]

    validationInputs = [inputs[i] for i in validationSample]
    validationOutputs = [outputs[i] for i in validationSample]

    return trainInputs, trainOutputs, validationInputs, validationOutputs

if __name__ == '__main__':
    crtDir = os.getcwd()
    filePath = os.path.join(crtDir, 'data', 'FAOSTAT_data_1-10-2022.csv')
    inputs, outputs = loadData(filePath, 'Area', 'Months', 'Year', 'Value')

    areaClassification = {}
    monthClassification = {}
    areaIndex = 0
    monthIndex = 0

    for input in inputs:
        if input[0] in areaClassification.keys():
            input[0] = areaClassification[input[0]]
        else:
            areaClassification[input[0]] = areaIndex
            input[0] = areaIndex
            areaIndex += 1
        if input[1] in monthClassification.keys():
            input[1] = monthClassification[input[1]]
        else:
            monthClassification[input[1]] = monthIndex
            input[1] = monthIndex
            monthIndex += 1
        input[2] = int(input[2])

    x1 = [inputs[i][0] for i in range(len(inputs))]
    x2 = [inputs[i][1] for i in range(len(inputs))]
    x3 = [inputs[i][2] for i in range(len(inputs))]

    # trainInputs, trainOutputs, validationInputs, validationOutputs = splitData(inputs, outputs)
    trainInputs, validationInputs, trainOutputs, validationOutputs = train_test_split(inputs, outputs, train_size=0.8, random_state=42)

    linearRegressor = LinearRegressor(trainInputs, trainOutputs, validationInputs, validationOutputs)
    w0, w1, w2, w3 = linearRegressor.fit()
    computedValidationOutputs = linearRegressor.predict()
    err = linearRegressor.error()

    inp = [input[2] for input in validationInputs if input[0] == 0]
    out = [validationOutputs[i] for i in range(len(inp))]
    outc = [computedValidationOutputs[i] for i in range(len(inp))]
    plt.scatter(inp, out, color='r')
    plt.plot(inp, outc, color='b')
    plt.xlabel('Year')
    plt.ylabel('Prediction')
    plt.show()

    print()
    validationInputsNenormalized = validationInputs
    trainInputs, validationInputs = normalisation(trainInputs, validationInputs)

    sgdRegressor = SGDRegressor(trainInputs, trainOutputs, validationInputs, validationOutputs)
    w0_, w1_, w2_, w3_ = sgdRegressor.fit()
    computedValidationOutputs_ = sgdRegressor.validate()
    err_ = sgdRegressor.error()

    inp = [input[2] for input in validationInputsNenormalized if input[0] == 0]
    out = [validationOutputs[i] for i in range(len(inp))]
    outc = [computedValidationOutputs_[i] for i in range(len(inp))]
    # print(outc)
    plt.scatter(inp, out, color='r')
    plt.scatter(inp, outc, color='b')
    plt.xlabel('Year')
    plt.ylabel('Prediction')
    plt.show()

