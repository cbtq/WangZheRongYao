in_list = [1, 1, 1, 1, 0, 0, 2, 0, 3, 5, 3]


def state0(input0):
    print("状态0")
    print("input0=" + str(input0))
    if input0 % 2 == 0:
        return state0
    else:
        return state1


def state1(input1):
    print("状态1")
    print("input1=" + str(input1))
    if input1 % 2 == 0:
        return state1
    else:
        return state0


if __name__ == '__main__':
    i = state0
    num = 1
    for t in in_list:
        print('--------\n循环轮次：' + str(num))
        i = i(t)
        num += 1
