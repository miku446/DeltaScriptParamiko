# if __name__ == '__main__':
#    pass


def delta(res_1=[['Non-Ip PDN sessions        ', '0'],
                 ['Bearers                    ', '32024', '     Default Bearers', '32024'],
                 ['Issues on DNS res Emer APN ', '0', '0']], res_2=[['Non-Ip PDN sessions        ', '10'],
                                                                    ['Bearers                    ', '32624',
                                                                     '     Default Bearers', '32324'],
                                                                    ['Issues on DNS res Emer APN ', '0', '5']]
          , interval=1):
    delta_res = []
    fullStr = ""
    #print(res_1)
    #print(res_2)
    for (i, j) in zip(res_1, res_2):
        temp_res = []
        ele = 1
        for (m, n) in zip(i, j):
            # print ("n = "+n)
            if str(m).isdigit() and str(n).isdigit():
            #if m.isdigit() and n.isdigit():
                #temp_res.append('\t{0}\t\t '.format(str(n)))
                #temp_res.append(str(int(n) - int(m)) + "\t")
                #temp_res.append("(" + str(float(int(n) - int(m)) / interval) + ")" + "\t")
                temp_res.append('{0: <16}'.format(" "+str(n)))
                temp_res.append('{0: <12}'.format(str(int(n) - int(m))))
                temp_res.append('{0: <12}'.format("(" + str(float(int(n) - int(m)) / interval) + ")"))
            else:
                if ele == 1:
                    temp_res.append("\n" + n)
                    # temp_res.append(n)
                    ele += 1
                else:
                    temp_res.append('\t\t\t' + n)
        delta_res.append(temp_res)
    for aList in delta_res:
        for aStr in aList:
            fullStr += aStr
    print(fullStr)
