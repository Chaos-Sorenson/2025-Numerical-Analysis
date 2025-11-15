MAXLEN = int(1024)

def normalize(x: str) -> tuple[bool, list[int]]:
    is_neg: bool = 0

    if x[0] == '-':
        is_neg = 1
        x = x[1:]
    
    n = x.find('.')
    
    if n == -1:
        n = len(x)

    x1 = x[:n]
    x2 = x[n+1:]

    return is_neg, (MAXLEN // 2 - len(x2)) * [0] + [int(d) for d in reversed(x1 + x2)] + (MAXLEN // 2 - len(x1)) * [0]


def sci_normalize(x: str) -> tuple[bool, list[int]]:
    n = x.find('e')

    if n == -1:
        return normalize(x)

    is_neg, num_list = normalize(x[:n])

    p = int(0)

    for d in x[n+2 if x[n+1] == '-' else n+1:]:
        p = p * 10 + int(d)

    if x[n+1] == '-':
        num_list = num_list + p * [0]
        num_list = num_list[-MAXLEN:]
    else:
        num_list = p * [0] + num_list
        num_list = num_list[:MAXLEN]

    return is_neg, num_list


def simple_plus(x: list[int], y: list[int]) -> list[int]:
    res: list[int] = []
    g: int = 0

    for i in range(MAXLEN):
        s = x[i] + y[i] + g
        g = s // 10
        res.append(s % 10)

    return res


def is_leq(x: list[int], y: list[int]) -> bool:
    for i in reversed(range(MAXLEN)):
        if x[i] < y[i]:
            return 1
        if x[i] > y[i]:
            return 0

    return 1


def simple_minus(x: list[int], y: list[int]) -> list[int]:
    res: list[int] = []
    g: int = 0

    for i in range(MAXLEN):
        s = x[i] - y[i] + g
        g = 0
        if s < 0:
            s += 10
            g = -1
        res.append(s)

    return res


def abs_minus(x: tuple[bool, list[int]], y: tuple[bool, list[int]]) -> list[int]:
    if x[0] == y[0]:
        if is_leq(x[1], y[1]):
            return simple_minus(y[1], x[1])
        else:
            return simple_minus(x[1], y[1])

    return simple_plus(x[1], y[1])


def get_len(x: str) -> int:
    res = int(0)
    start = int(0)
    for c in x:
        if c in ['-', '.']:
            continue
        if c == 'e':
            break
        if start == 0:
            if c == '0':
                continue
            start = 1
        res = res + 1
    return res


def get_significant_figure(ref: str, est: str) -> int:
    norm_ref = sci_normalize(ref)
    norm_est = sci_normalize(est)
    err = abs_minus(norm_ref, norm_est)

    res = int(0)

    for m in reversed(range(MAXLEN)):
        if norm_est[1][m] != 0:
            res = m
            break
    
    for n in reversed(range(MAXLEN)):
        if err[n] != 0:
            res = res - n
            break

    if err[n] > 5:
        res = res - 1
    elif err[n] == 5:
        for i in reversed(range(n)):
            if err[i] != 0:
                res = res - 1
                break

    high = min(get_len(ref), get_len(est))
    low = int(0)
    return max(min(res, high), low)


def main():
    # 有效数字位数不能大于 ref 和 est 的数位个数
    assert get_significant_figure("3.14", "3.1401") == 3
    assert get_significant_figure("3.1400", "3.14") == 3

    # 测试样例
    assert get_significant_figure("-3.1415926", "-3.1415") == 4
    assert get_significant_figure("2.2530", "2.3000") == 2

    # 支持 1.5e-3、-0.0314e2 等科学计数法形式的输入
    assert get_significant_figure("0.0015926", "1.5e-3") == 1
    assert get_significant_figure("-314.15926e-2", "-0.031415e2") == 4

    assert get_significant_figure("-0.01", "-0.01") == 1

    print("Pass")


if __name__ == "__main__":
    main()