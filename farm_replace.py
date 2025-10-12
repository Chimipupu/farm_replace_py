def farm_SpeedUp():
    if get_water() < 1:
        if num_items(Items.Water) > 0:
            use_item(Items.Water) # 水やり
    else :
        if num_items(Items.Fertilizer) > 0:
            use_item(Items.Fertilizer)  # 肥料

# にんじん作成
def plant_Carrot():
    if get_ground_type() != Grounds.Soil:
        till() # 土を耕す
    else :
        if can_harvest():
            harvest() # 収穫
            plant(Entities.Carrot) # 人参を埋める
            farm_SpeedUp()

# かぼちゃ作成
def plant_Pumpkin():
    if get_ground_type() != Grounds.Soil:
        till() # 土を耕す
    else :
        if can_harvest():
            harvest() # 収穫
            plant(Entities.Pumpkin) # かぼちゃを植える
            farm_SpeedUp()

# 茂み作成
def plant_Bush():
    if can_harvest():
        harvest() # 収穫
        plant(Entities.Bush)

# 木作成
# NOTE: 木は四方に木で囲うと成長側が1/16になる
def plant_Tree():
    if can_harvest():
        harvest() # 収穫
        plant(Entities.Tree)

# 草作成
def plant_Hay():
    if can_harvest():
        harvest() # 収穫
    else :
        till() # 土を耕す

while True:
    clear()

    i = 0
    for i in range(12): # 農地面積 12x12
        # plant_Hay()         # 草
        # plant_Bush()        # 茂

        # NOTE: 木は四方に木で囲うと成長側が1/16になる
        if(i % 2 == 0):
            plant_Tree()        # 木

        # plant_Carrot()      # 人参
        # plant_Pumpkin()     # かぼちゃ
        move(North) # 北に移動

    move(East)