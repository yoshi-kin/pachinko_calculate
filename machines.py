#仮面ライダー轟音天井期待値
def kamen(current_count, count_per_250):
    #スペック詳細
    low = 319.9
    high = 74.7
    limit_count = 950
    limit_count -= current_count
    round_bonus = 140

    #大当たり確率を求める関数
    def hit(denominator, count):
        not_hit = ((denominator - 1) / denominator) ** count
        hit = (1 - not_hit)
        return hit 

    #通常950回転までに当たる確率
    normal_hit_rate = hit(low, limit_count)
    #遊タイム1200回転で当たる確率
    yutime_hit_rate = (1 - normal_hit_rate) * hit(low, 1200)
    #st120回転中に当たる確率
    st_hit_rate = hit(high, 120)
    #時短120回転中に当たる確率
    jitan_hit_rate = hit(low, 120)
    #st120+時短120回転中に当たる確率
    st_jitan_hit_rate = hit(high, 120) + (1 - hit(high, 120)) * hit(low, 120)

    #電サポ大当たり時の平均獲得ラウンド数
    sup_hit_get_round = (10 * 0.8) + (2 * 0.2)
    #st継続率
    st_keep_rate = (st_jitan_hit_rate * 0.4) + (st_hit_rate * 0.6)
    #電サポstの継続回数
    st_keep_count = st_keep_rate / (1 - st_keep_rate)
    #遊タイムで初当たりを引いた場合の平均獲得ラウンド数
    yutime_hit_get_round = sup_hit_get_round + sup_hit_get_round * st_keep_count

    #通常で初当たりを引いた場合の平均獲得ラウンド数
    def normal_hit_get_round():
        init_get_round = 10 * 0.01 + 3 * 0.99
        init_hit_rate = st_jitan_hit_rate * 0.11 + st_hit_rate * 0.39 +      jitan_hit_rate * 0.5

        init_get_ave_round = init_get_round + ((1 + st_keep_count) * sup_hit_get_round) * init_hit_rate

        return init_get_ave_round

    #遊タイムを含む回転数以内に当たった場合の平均獲得ラウンド数
    limit_get_ave_round = normal_hit_get_round() * normal_hit_rate + yutime_hit_get_round * yutime_hit_rate

    limit_get_ave_bonus = limit_get_ave_round * round_bonus

    #limit_count内で当たる場合のみの平均試行回数
    t = (1 - (limit_count + 1) * (1 - 1/low)**limit_count + limit_count * (1 - 1/low)**(limit_count + 1)) / (1/low * normal_hit_rate)

    #残りlimit_count回転の場合に必要な平均試行回数
    ave_count = normal_hit_rate * t + yutime_hit_rate * limit_count

    #残りlimit_count回転の場合に必要な平均投資玉数
    ave_invest = ave_count / count_per_250 * 250

    #残りlimit_count回転時に打った場合の期待値
    expected_value = (limit_get_ave_bonus - ave_invest) * 4

    return expected_value

    # print('平均獲得玉数:' + str(round(limit_get_ave_bonus)) + '個')
    # print('平均投資玉数:' + str(round(ave_invest)) + '個')
    # print('期待値:' + str(round(expected_value)) + '円')

#真・牙狼
def singaro(count, rate):
    low = 319.68
    high = 73.63
    to_yutime = 900
    to_yutime -= count
    round_bonus = 140

    def hit(denominator, count):
        not_hit = ((denominator - 1) / denominator) ** count
        hit = (1 - not_hit)
        return hit 
    
    normal_hit_rate = hit(low, to_yutime)
    yutime_hit_rate = (1 - normal_hit_rate) * hit(low, 1200)
    st_hit_rate = hit(high, 130)
    jitan_hit_rate = hit(low, 50)
    
    sup_hit_get_round = (10 * 0.7) + (2 * 0.3)
    st_keep_rate = st_hit_rate
    st_keep_count = st_keep_rate / (1 - st_keep_rate)

    yutime_hit_get_round = (1 + st_keep_count) * sup_hit_get_round
    def normal_hit_get_round():
        init_get_round = 3
        init_hit_rate = jitan_hit_rate * 0.5 + st_hit_rate * 0.5

        normal_hit_get_round = init_get_round + ((1 + st_keep_count) * sup_hit_get_round) * init_hit_rate + ((1 + st_keep_count) * sup_hit_get_round) * hit(89.04, 4) * hit(low, 2100)

        return normal_hit_get_round

    normal_yutime_get_round = normal_hit_get_round() * normal_hit_rate + yutime_hit_get_round * yutime_hit_rate

    normal_yutime_get_bonus = normal_yutime_get_round * round_bonus

    t = (1 - (to_yutime + 1) * (1 - 1/low)**to_yutime + to_yutime * (1 - 1/low)**(to_yutime + 1)) / (1/low * normal_hit_rate)

    ave_count = normal_hit_rate * t + yutime_hit_rate * to_yutime

    ave_invest = ave_count / rate * 250

    expected_value = (normal_yutime_get_bonus - ave_invest) * 4

    return expected_value


print(singaro(600, 15))
print(kamen(600, 15))