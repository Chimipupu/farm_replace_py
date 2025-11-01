# -----------------------------------------------------------------------------
# @file farm_replace.py
# @author Chimipupu (https://github.com/Chimipupu)
# @brief 「農家はReplace()されました」用のPython
# @version 0.1
# @date 2025-11-1
# @copyright Copyright (c) 2025 Chimipupu (https://github.com/Chimipupu)
# -----------------------------------------------------------------------------
# [定数]

# ifdefでコンパイルスイッチ
PROC_TYPE_PLANT             = 1 # 農作業アプリ実行 (1で有効)
PROC_TYPE_MAZE              = 0 # 迷路探索アプリ実行 (1で有効)

ENTITIES_LIST_IDX_GRASS     = 0
ENTITIES_LIST_IDX_BUSH      = 1
ENTITIES_LIST_IDX_TREE      = 2
ENTITIES_LIST_IDX_CARROT    = 3
ENTITIES_LIST_IDX_PUMPKIN   = 4
ENTITIES_LIST_IDX_SUNFLOWER = 5
ENTITIES_LIST_IDX_CACTUS    = 6

MAIN_DRONE                  = 0
SUB_DRONE                   = 1

# -----------------------------------------------------------------------------
# [グローバル変数]
# 農作物テーブル
g_entities_list = [
    Entities.Grass,     # 草
    Entities.Bush,      # 茂み
    Entities.Tree,      # 木
    Entities.Carrot,    # にんじん
    Entities.Pumpkin,   # かぼちゃ
    Entities.Sunflower, # ひまわり
    Entities.Cactus     # サボテン
]

# 方角テーブル(東西南北の順)
g_direction_tbl = [
    East,   # 東
    West,   # 西
    South,  # 南
    North,  # 北
]
# -----------------------------------------------------------------------------

# 水と肥料の散布関数
def farm_SpeedUp():
    if get_water() < 1:
        if num_items(Items.Water) > 0:
            use_item(Items.Water) # 水やり
    else :
        if num_items(Items.Fertilizer) > 0:
            use_item(Items.Fertilizer)  # 肥料

# サボテン用の並び替えアルゴリズム
def sort_algo():
    # サイズ取得ステップ(サイズ範囲:0~9)
    cactus_size       = measure()      # 中心のサボテンサイズ
    cactus_east_size  = measure(East)  # 東のサボテンサイズ
    cactus_west_size  = measure(West)  # 西のサボテンサイズ
    cactus_south_size = measure(South) # 南のサボテンサイズ
    cactus_north_size = measure(North) # 北のサボテンサイズ

    # 並び替えステップ
    # None を -1(最小) として比較（明示的な if/else で書く）
    if cactus_size == None:
        center = -1
    else:
        center = cactus_size

    if cactus_east_size == None:
        e_size = -1
    else:
        e_size = cactus_east_size

    if cactus_west_size == None:
        w_size = -1
    else:
        w_size = cactus_west_size

    if cactus_south_size == None:
        s_size = -1
    else:
        s_size = cactus_south_size

    if cactus_north_size == None:
        n_size = -1
    else:
        n_size = cactus_north_size

    neighbors = [
        (East,  e_size),
        (West,  w_size),
        (South, s_size),
        (North, n_size),
    ]

    # 中央を含めた最大値を見つける
    max_neighbor_dir = None
    max_size = center

    for dir_const, sz in neighbors:
        if sz > max_size:
            max_size = sz
            max_neighbor_dir = dir_const

    # 中央が最大なら何もしない。そうでなければ最大の方向とswapする
    if max_neighbor_dir != None:
        swap(max_neighbor_dir)


# 農作物作成ステートマシーン
def sm_plant_entities(arg_entities, i, j):
    if (arg_entities > ENTITIES_LIST_IDX_SUNFLOWER):
        return

    # サボテン
    if (arg_entities == ENTITIES_LIST_IDX_CACTUS):
        if can_harvest(): # 刈り取る
            sort_algo() # 並び替えアルゴリズム実施
            harvest()
        else: # 植え付け
            plant(g_entities_list[arg_entities])

    # にんじん or かぼちゃ
    if ((arg_entities == ENTITIES_LIST_IDX_CARROT) or (arg_entities == ENTITIES_LIST_IDX_PUMPKIN)):
        if get_ground_type() != Grounds.Soil:
            harvest()
            till()

        if can_harvest():
            harvest()

        plant(g_entities_list[arg_entities])
        farm_SpeedUp()

    # 茂み
    if (arg_entities == ENTITIES_LIST_IDX_BUSH):
        if can_harvest():
            harvest()
            plant(g_entities_list[arg_entities])

    # 木
    if (arg_entities == ENTITIES_LIST_IDX_TREE):
        if get_ground_type() == Grounds.Soil:
            harvest()
            till()

        if((i % 2 == 0) and (j % 2 == 0)) or ((i % 2 == 1) and (j % 2 == 1)) :
            if can_harvest():
                harvest()
                plant(g_entities_list[arg_entities])
        else:
            harvest() # 空き地の草刈り

    # ひまわり
    if (arg_entities == ENTITIES_LIST_IDX_SUNFLOWER):
        if get_ground_type() != Grounds.Soil:
            harvest()
            till()

        # ひまわりの最大の花びら(=15)のときに刈り取る
        petals_cnt = measure()
        if ((petals_cnt == None) or can_harvest()):
            harvest()
            plant(g_entities_list[arg_entities])
            farm_SpeedUp()

    # 草
    if (arg_entities == ENTITIES_LIST_IDX_GRASS):
        if can_harvest():
            harvest()

# 農作業（メインドローン）
def plant_main_proc():
    wortd_size = get_world_size() # 32x32面 = 1024面
    for i in range(wortd_size): # 横32面
        move(East) # 東に移動
        for j in range(wortd_size): # 縦32面
            # ひまわりのパワーバブで速度2倍速
            if(i < 2): # 農地の32x2はひまわり
                sm_plant_entities(ENTITIES_LIST_IDX_SUNFLOWER,0,0) # ひまわり
            else:
                sm_plant_entities(ENTITIES_LIST_IDX_GRASS,i,j)    # 草
                # sm_plant_entities(ENTITIES_LIST_IDX_TREE,i,j)    # 木
                # sm_plant_entities(ENTITIES_LIST_IDX_BUSH,0,0)    # 茂み
                # sm_plant_entities(ENTITIES_LIST_IDX_CARROT,0,0)  # にんじん
                # if num_items(Items.Fertilizer) > 0:
                #         use_item(Items.Weird_Substance)
                # sm_plant_entities(ENTITIES_LIST_IDX_PUMPKIN,0,0) # かぼちゃ
                sm_plant_entities(ENTITIES_LIST_IDX_CACTUS,0,0) # サボテン
            move(North) # 北に移動

# 農作業（サブドローン）
def plant_sub_proc():
    wortd_size = get_world_size() # 32x32面 = 1024面
    for i in range(wortd_size): # 横32面
        move(East) # 東に移動
        for j in range(wortd_size): # 縦32面
            if(i < 2): # ひまわり
                # ひまわりのパワーバブで速度2倍速
                sm_plant_entities(ENTITIES_LIST_IDX_SUNFLOWER,0,0) # ひまわり
            else:
                sm_plant_entities(ENTITIES_LIST_IDX_TREE,i,j)    # 木
                sm_plant_entities(ENTITIES_LIST_IDX_BUSH,0,0)    # 茂み
                sm_plant_entities(ENTITIES_LIST_IDX_CARROT,0,0)  # にんじん
                if num_items(Items.Fertilizer) > 0:
                        use_item(Items.Weird_Substance)
                # sm_plant_entities(ENTITIES_LIST_IDX_PUMPKIN,0,0) # かぼちゃ
            move(North) # 北に移動

# パワー充電
def charge_power(drone_type):
    wortd_size = get_world_size()
    while (num_items(Items.Power) < 10000): # パワーx1M溜まるまで
        for i in range(wortd_size):
            for j in range(wortd_size):
                # ひまわりのパワーバブで速度2倍速
                sm_plant_entities(ENTITIES_LIST_IDX_SUNFLOWER,0,0) # ひまわり
                move(North) # 北に移動
            move(East) # 東に移動
            spawn_drone(sub_proc) # サブドローンを生成

# 迷路生成
def create_maze():
    if num_items(Items.Fertilizer) > 0:
        plant(Entities.Bush)
        substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
        use_item(Items.Weird_Substance, substance)

# 迷路探索(右手法)
def maze_solver():
    # ゴールの座標
    goal_x, goal_y = measure()

    # 現在の向き（0:北, 1:東, 2:南, 3:西）
    direction = 0
    directions = [North, East, South, West]

    while True:
        # パワーがないと迷路探索が無理なので関数を抜ける
        if num_items(Items.Power) < 1000:
            break

        # 現在座標
        now_x, now_y = get_pos_x(), get_pos_y()

        # ゴール判定
        if((now_x == goal_x) and (now_y == goal_y)):
            if (Entities.Treasure == get_entity_type()):
                harvest()
            break

        # 右手法：右→前→左→後ろの順に確認
        # 右方向を確認（現在の向き+1）
        right_dir = directions[(direction + 1) % 4]
        front_dir = directions[direction]
        left_dir = directions[(direction - 1) % 4]
        back_dir = directions[(direction + 2) % 4]

        # 右に曲がれるなら右に曲がる
        if can_move(right_dir):
            move(right_dir)
            direction = (direction + 1) % 4
        # 前に進めるなら前進
        elif can_move(front_dir):
            move(front_dir)
        # 左に曲がれるなら左に曲がる
        elif can_move(left_dir):
            move(left_dir)
            direction = (direction - 1) % 4
        # どこも行けないなら後ろに（Uターン）
        elif can_move(back_dir):
            move(back_dir)
            direction = (direction + 2) % 4

# メインドーロン処理
def main_proc():
    # 農作業
    if(PROC_TYPE_PLANT == 1):
        plant_main_proc()
    # 迷路探索
    else:
        # パワーが尽きるまで探索
        if(num_items(Items.Power) > 1000):
            clear()
            create_maze() # 迷路生成
            maze_solver() # 迷路探索(右手法)
        else:
            clear()
            charge_power(MAIN_DRONE)  # パワー充電

# サブドローン処理
def sub_proc():
    wortd_size = get_world_size()
    move(West) # 西に移動
    for i in range(wortd_size):
        move(South) # 南に移動
        if can_harvest():
            harvest()
            sm_plant_entities(ENTITIES_LIST_IDX_SUNFLOWER,0,0) # ひまわり
        else:
            move(West) # 西に移動

# メインループ
while True:
    main_proc()