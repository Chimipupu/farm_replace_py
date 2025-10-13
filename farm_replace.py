# -----------------------------------------------------------------------------
# @file farm_replace.py
# @author Chimipupu (https://github.com/Chimipupu)
# @brief 「農家はReplace()されました」の迷路探索までのアプリ
# @version 0.1
# @date 2025-10-13
# @copyright Copyright (c) 2025 Chimipupu (https://github.com/Chimipupu)
# -----------------------------------------------------------------------------

# 定数
ENTITIES_LIST_IDX_GRASS     = 0
ENTITIES_LIST_IDX_BUSH      = 1
ENTITIES_LIST_IDX_TREE      = 2
ENTITIES_LIST_IDX_CARROT    = 3
ENTITIES_LIST_IDX_PUMPKIN   = 4
ENTITIES_LIST_IDX_SUNFLOWER = 5

MAZE_SOLVEING               = 0
MAZE_GOAL                   = 1

# グローバル変数
g_entities_list = [
    Entities.Grass,     # 草
    Entities.Bush,      # 茂み
    Entities.Tree,      # 木
    Entities.Carrot,    # にんじん
    Entities.Pumpkin,   # かぼちゃ
    Entities.Sunflower  # ひまわり
]

g_directions = [North, East, South, West]

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
            harvest()
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
            harvest()
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
            harvest()
            till()

        petals_cnt = measure()
        # ひまわりの最大の花びら(=15)のときに刈り取る
        # if ((petals_cnt == None) or ((petals_cnt == 15) and can_harvest())):
        if ((petals_cnt == None) or can_harvest()):
            harvest()
            plant(g_entities_list[list_idx])
            farm_SpeedUp()

    # 草
    if (list_idx == ENTITIES_LIST_IDX_GRASS):
        if can_harvest():
            harvest()

# 農作業
def plant_proc():
    wortd_size = get_world_size()

    for i in range(wortd_size):
        move(Eest) # 東に移動
        for j in range(wortd_size):
            if(i < 2): # ひまわり
                # ひまわりのパワーバブで速度2倍速
                sm_plant_entities(ENTITIES_LIST_IDX_SUNFLOWER,0,0) # ひまわり
            elif (i <= 3) and (i >= 9):
                sm_plant_entities(ENTITIES_LIST_IDX_TREE,i,j)    # 木
            elif (i <= 10) and (i >= 20): # 迷路生成
                sm_plant_entities(ENTITIES_LIST_IDX_BUSH,0,0)    # 茂み
                if num_items(Items.Fertilizer) > 0:
                    use_item(Items.Fertilizer)  # 肥料
            elif (i <= 20) and (i >= 26):
                sm_plant_entities(ENTITIES_LIST_IDX_CARROT,0,0)  # にんじん
            elif (i <= 27) and (i >= 32):
                sm_plant_entities(ENTITIES_LIST_IDX_PUMPKIN,0,0) # かぼちゃ

            move(North) # 北に移動

# 迷路生成
def create_maze():
    if num_items(Items.Fertilizer) > 0:
        plant(Entities.Bush)
        substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
        use_item(Items.Weird_Substance, substance)

# 迷路探索(右手法)
def maze_solver():
    # 現在の向き（0:北, 1:東, 2:南, 3:西）
    direction = 0
    directions = [North, East, South, West]

    while True:
        # パワーがないと迷路探索が無理なので関数を抜ける
        if num_items(Items.Power) < 1000:
            break

        # ゴール判定
        if Entities.Treasure == get_entity_type():
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

def main_proc():
    if(num_items(Items.Power) > 0):
        clear()
        create_maze() # 迷路生成
        maze_solver() # 迷路探索
    else:
        clear()
        plant_proc()  # 農作業

# メインループ
while True:
    # spawn_drone(main_proc)

    if(num_items(Items.Power) > 0):
        clear()
        create_maze() # 迷路生成
        maze_solver() # 迷路探索
    else:
        clear()
        plant_proc()  # 農作業