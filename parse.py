'''
Created on 02-May-2020

@author: mmahapat
'''
import regex


def parse(test_list):
    """

    :type test_list: list of byte arrays
    """
    res = []
    opt = 1
    print(test_list.pop(0))
    for i in test_list:
        # print(i)
        pattern = regex.compile(
            r'(?:\d+:)+\d+|\d{10}\s|\d{9}\s{2}|(?:(?:\w+[.& ,/()-]?[.&,/)(-]?\s{0,1})+[*]{0,1}:)|(?:(?:\w+[.& ,/()-]?[.&,/)(-]?\s{0,1})+\s+[*]{0,1}:)|(?:(?:\w+[.& ,/()-]?[.&,/)(-]?\s{0,1})+\s*[*]{0,1})|(?:(?:\w+[.& ,/()-]?[.&,/()-]?\s{0,1})+\s+)|(?:\w+[.& ,/()-]{0,2})+|(?:\d+\.)+\d+|(?:\b\d+\s?)|[=-]+')
        # temp = i.split(":")
        temp = pattern.findall(i)
        if len(temp) > 1 and opt == 1:
            for aTemp in temp:
                if aTemp.strip().isnumeric():
                    # print("yes numeric")
                    # print(int(aTemp.strip()))
                    temp[temp.index(aTemp)] = int(aTemp.strip())
        # print(temp)
        # res.append(temp)

        if len(temp) > 1 and opt == 0:
            j = 0
            while j < len(temp):
                # print("in while")
                if j > 0:
                    # print("in if 1")
                    # print(j)
                    # print(temp[j])
                    # print(temp[j].strip().split(" ", 2))
                    if temp[j].strip().split(" ", 2)[0].isnumeric():
                        # print("in if 2")
                        # print(temp[j].split(" ", 2)[1])
                        jSpilt = temp[j].strip().split(" ", 1)
                        # temp.insert(j, jSpilt[1])
                        # temp.insert(j, next(jSpilt))
                        # print(temp)
                        # print(j)
                        # temp[j + 1] = temp[j + 1].split(" ", 2)[2]
                        # temp[j + 1] = next(filter("", temp[j].split(" ")))
                        if len(jSpilt) > 1:
                            temp.insert(j, jSpilt[0])
                            temp[j + 1] = jSpilt[1]
                        else:
                            temp[j] = jSpilt[0]
                        j += 1
                    else:
                        temp[j] = temp[j] + ":"
                        j += 1
                        # print("hit break")
                        # break
                else:
                    temp[j] = temp[j] + ":"
                    j += 1
        # print(temp)
        res.append(temp)
        # print res
    return res