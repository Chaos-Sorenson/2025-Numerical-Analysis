def resample(series, tgt_length):
    """对 series 输入序列进行重采样，使得重采样后的长度等于 tgt_length
        注：请使用分段线性插值方法，假设 x0, x1, ... 依次是 0, 1, ...
        Args:
            series (List[float]): 对应函数值 y0, y1, ... 的一维实数序列（长度大于 0）
            tgt_length (int): 期望输出的序列长度（一定大于 0）
        Returns:
            ret (List[float]): 重采样后的一维序列
    """

    assert isinstance(series, list) and len(series) > 0
    assert all(isinstance(y, (int, float)) for y in series)
    assert isinstance(tgt_length, int) and tgt_length > 0

    tot_length = len(series)

    if tot_length == 1:
        return series * tgt_length

    resampled_series = [series[0]]

    if tgt_length == 1:
        return resampled_series

    step = 1
    while step < tgt_length - 1:
        x = step * (tot_length - 1) / (tgt_length - 1)
        l = int(x)
        r = l + 1
        y = (r - x) * series[l] + (x - l) * series[r]
        resampled_series.append(y)
        step = step + 1
    
    resampled_series.append(series[-1])
    return resampled_series


def test():
    assert resample([1.0], 8000) == [1.0] * 8000
    assert resample([1.0, 3.0, 4.0], 2) == [1.0, 4.0]
    assert resample([0.0, 2.0, 3.0, 1.0], 5) == [0.0, 1.5, 2.5, 2.5, 1.0]
    print("Pass")


if __name__ == "__main__":
    import json
    series = json.loads(input())
    tgt_length = int(input())
    resampled_series = resample(series, tgt_length)
    print(json.dumps(resampled_series))

    # test()