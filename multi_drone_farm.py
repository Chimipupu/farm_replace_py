# -----------------------------------------------------------------------------
# @file multi_drone_farm.py
# @author Chimipupu (https://github.com/Chimipupu)
# @brief 「農家はReplace()されました」のドローンが32機使える時の並列処理専用Python
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

# 農作物作成ステートマシーン
def sm_plant_entities(arg_entities, i):
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

        if(i % 2 == 0) or (i % 2 == 1) :
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
        if get_ground_type() == Grounds.Soil:
            till()
        if can_harvest():
            harvest()

# メインドーロン処理
def main_proc():
    wortd_size = get_world_size() # 32x32面 = 1024面
    for i in range(wortd_size): # 横32面
        spawn_drone(sub_proc) # サブドローンを生成
        move(West) # 西に移動

# サブドローン処理
def sub_proc():
    wortd_size = get_world_size()
    for i in range(32):
        # ひまわりのパワーバブで速度2倍速
        if(i < 3):
            sm_plant_entities(ENTITIES_LIST_IDX_SUNFLOWER, 0) # ひまわり
        else:
            if(num_items(Items.Hay) < 100000):
                sm_plant_entities(ENTITIES_LIST_IDX_GRASS, 0)   # 草
            elif(num_items(Items.Wood) < 100000):
                sm_plant_entities(ENTITIES_LIST_IDX_TREE, i)    # 木
            elif(num_items(Items.Carrot) < 100000):
                sm_plant_entities(ENTITIES_LIST_IDX_CARROT, 0)  # にんじん
            else:
                sm_plant_entities(ENTITIES_LIST_IDX_PUMPKIN, 0) # かぼちゃ

        move(North) # 北に移動

# メインループ
while True:
    main_proc()