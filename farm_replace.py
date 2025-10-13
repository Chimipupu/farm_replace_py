# __builtins__ import *

# 定数
ENTITIES_LIST_IDX_GRASS     = 0
ENTITIES_LIST_IDX_BUSH      = 1
ENTITIES_LIST_IDX_TREE      = 2
ENTITIES_LIST_IDX_CARROT    = 3
ENTITIES_LIST_IDX_PUMPKIN   = 4
ENTITIES_LIST_IDX_SUNFLOWER = 5

# グローバル変数
g_entities_list = [
    Entities.Grass,     # 草
    Entities.Bush,      # 茂み
    Entities.Tree,      # 木
    Entities.Carrot,    # にんじん
    Entities.Pumpkin,   # かぼちゃ
    Entities.Sunflower  # ひまわり
]

# 水と肥料の散布関数
def farm_SpeedUp():
    if get_water() < 1:
        if num_items(Items.Water) > 0:
            use_item(Items.Water) # 水やり
    else :
        if num_items(Items.Fertilizer) > 0:
            use_item(Items.Fertilizer)  # 肥料

# 農作物作成ステートマシーン
def sm_plant_entities(list_idx, i, j):
    if (list_idx > ENTITIES_LIST_IDX_SUNFLOWER):
        return

    # にんじん or かぼちゃ
    if ((list_idx == ENTITIES_LIST_IDX_CARROT) or (list_idx == ENTITIES_LIST_IDX_PUMPKIN)):
        if get_ground_type() != Grounds.Soil:
            till()

        if can_harvest():
            harvest()

        plant(g_entities_list[list_idx])
        farm_SpeedUp()

    # 茂み
    if (list_idx == ENTITIES_LIST_IDX_BUSH):
        if can_harvest():
            harvest()
            plant(g_entities_list[list_idx])

    # 木
    if (list_idx == ENTITIES_LIST_IDX_TREE):
        if get_ground_type() == Grounds.Soil:
            till()

        if((i % 2 == 0) and (j % 2 == 0)) or ((i % 2 == 1) and (j % 2 == 1)) :
            if can_harvest():
                harvest()
                plant(g_entities_list[list_idx])
            else:
                harvest() # 空き地の草刈り

    # ひまわり
    if (list_idx == ENTITIES_LIST_IDX_SUNFLOWER):
        if get_ground_type() != Grounds.Soil:
            till()

        if can_harvest():
            harvest()
            plant(g_entities_list[list_idx])
            farm_SpeedUp()

    # 草
    if (list_idx == ENTITIES_LIST_IDX_GRASS):
        if can_harvest():
            harvest()

# メインループ
while True:
    # clear()

    wortd_size = get_world_size()# 農地面積
    for i in range(wortd_size):
        move(East) # 東に移動
        for j in range(wortd_size):
            # sm_plant_entities(ENTITIES_LIST_IDX_GRASS,0,0)   # 草
            # sm_plant_entities(ENTITIES_LIST_IDX_BUSH,0,0)    # 茂み
            # sm_plant_entities(ENTITIES_LIST_IDX_TREE,i,j)    # 木
            # sm_plant_entities(ENTITIES_LIST_IDX_CARROT,0,0)  # にんじん
            sm_plant_entities(ENTITIES_LIST_IDX_PUMPKIN,0,0) # かぼちゃ
            move(North) # 北に移動