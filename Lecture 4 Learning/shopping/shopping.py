import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence=[]
    labels=[]
    with open(filename, mode='r') as file:
        csvdata = csv.reader(file)
        for line in csvdata:
            evidence.append(line[0:-1])
            labels.append(line[-1])
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for line in evidence:        
            for i in range(len(months)):
                if(line[10]==months[i]):
                    line[10] = i+1
        for line in evidence:
            if(line[15] == 'Returning_Visitor'):
                line[15] = 1
            else:
                line[15] = 0
        for line in evidence:
            if(line[16] == 'TRUE'):
                line[16] = 1
            elif(line[16] == 'FALSE'):
                line[16] = 0
        for i in range(len(labels)):
            if(labels[i] == 'TRUE'):
                labels[i] = 1
            if(labels[i] == 'FALSE'):
                labels[i] = 0
    evidence.pop(0)
    labels.pop(0)
    #Data Type Conversion As Specification ------------
    for i in range(len(evidence)):
        evidence[i][0] = int(evidence[i][0])
        evidence[i][1] = float(evidence[i][1])
        evidence[i][2] = int(evidence[i][2])
        evidence[i][3] = float(evidence[i][3])
        evidence[i][4] = int(evidence[i][4])
        for j in range(5,10):
            evidence[i][j] = float(evidence[i][j])
        for j in range(10,17):
            evidence[i][j] = int(evidence[i][j])
    #---------------------------------------------------
    # print(len(evidence))
    # print(evidence)
    # print(labels)
    return (evidence,labels)



    # with open(filename, 'r') as file:
    #     lines = list(csv.DictReader(file))
    #     for line in lines:

    #         # convert month to a number
    #         months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    #         for i in range(len(months)):
    #             if line['Month'] == months[i]:
    #                 line['Month'] = i
    #                 break

    #         # convert VisitorType to a number
    #         line['VisitorType'] = 1 if line['VisitorType'] == 'Returning_Visitor' else 0

    #         # convert Weekend to a number
    #         line['Weekend'] = 1 if line['Weekend'] == 'TRUE' else 0

    #         # convert fields to ints
    #         for field in ['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems', 'Browser', 'Region', 'TrafficType']:
    #             line[field] = int(line[field])

    #         # convert fields to floats
    #         for field in ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']:
    #             line[field] = float(line[field])

    #         evidence.append(list(line.values())[:-1])
    #         labels.append(1 if line['Revenue'] == 'TRUE' else 0)
    # # print(evidence)
    # print(labels)
    # return (evidence, labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # print(labels)
    pos = labels.count(1)
    neg = labels.count(0)
    sensitivity = 0
    specificity = 0
    # print(predictions)
    for i in range(len(predictions)):
        if labels[i] == 1 and predictions[i] == 1:
            sensitivity+=1
        if labels[i] == 0 and predictions[i] == 0:
            specificity+=1
    sensitivity = sensitivity/pos
    specificity = specificity/neg
    return (sensitivity,specificity)

if __name__ == "__main__":
    main()
