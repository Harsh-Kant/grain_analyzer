


def dnn_classification(ratio):
    ratio =round(ratio,1)
    toret=""
    if(ratio>=3 and ratio<3.5):
        toret="Slender"
    elif(ratio>=2.1 and ratio<3):
        toret="Medium"
    elif(ratio>=1.1 and ratio<2.1):
        toret="Bold"
    elif(ratio>0.9 and ratio<=1):
        toret="Round"
    else:
        toret="Dust"
    return toret
