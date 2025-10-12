# にんじん作成
def plant_Carrot():
    if can_harvest():
        harvest() # 収穫
        till() # 土を耕す
        plant(Entities.Carrot) # 人参を埋める
        if get_water() < 1:
            use_item(Items.Water) # 水やり
    else :
        move(East)

# 茂み作成
def plant_Bush():
    move(North) # 北に移動
    if can_harvest():
        harvest() # 収穫
        plant(Entities.Bush)
    else :
        move(East)

# 茂み作成
def plant_Pumpkin():
    if can_harvest():
        harvest() # 収穫
        # till() # 土を耕す
        plant(Entities.Pumpkin)
        if get_water() < 1:
            use_item(Items.Water) # 水やり
    else :
        move(East)

# 茂み作成
while True:
    move(North) # 北に移動
    # plant_Bush()
    # plant_Carrot()
    plant_Pumpkin()

    # move(East)
    move(South)
    plant_Bush()
    # plant_Carrot()
    plant_Pumpkin()
