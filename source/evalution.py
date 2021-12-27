## Olgun's Code
def calculate_precision_and_recall(y_true,y_pred):
    
    precisions = []
    recalls = []

    for true,pred in zip(y_true,y_pred):
        try:
            max_precision = 0
            max_recall = 0

            x = true
            y = pred

            if len(x) > 0 and len(y) > 0:
                shared_items = dict()
                for k in x:
                    if (k in y) and (x.index(k) == y.index(k)):
                        shared_items[k] = x.index(k)

                recall = len(shared_items)/len(x)
                precision = len(shared_items)/len(y)

                if precision > max_precision:
                    max_precision = precision

                if recall > max_recall:
                    max_recall = recall

            precisions.append(max_precision)
            recalls.append(max_recall)

        except KeyError:
            precisions.append(0)
            recalls.append(0)


    sum = 0
    for item in precisions:
        sum += item
    print('average_precision =', sum/len(precisions)) 
    average_precision = sum/len(precisions)

    sum = 0

    for item in recalls:
        sum += item

    print('average_recall =', sum/len(recalls))
    average_recall = sum/len(precisions)

    
    return average_precision, average_recall