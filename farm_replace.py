# にんじん作成
def plant_Carrot():
    if can_harvest():
        harvest() # 収穫
        till() # 土を耕す
        plant(Entities.Carrot) # 人参を埋める
        if get_water() < 1:
            use_item(Items.Water) # 水やり
        else :
            use_item(Items.Fertilizer)

# かぼちゃ作成
def plant_Pumpkin():
    if can_harvest():
        harvest() # 収穫
        till() # 土を耕す
        plant(Entities.Pumpkin)
        if get_water() < 1:
            use_item(Items.Water) # 水やり
        else :
            use_item(Items.Fertilizer)
    else :
        till() # 土を耕す

# 茂み作成
def plant_Bush():
    if can_harvest():
        harvest() # 収穫
        plant(Entities.Bush)
    else :
        till()

# 木作成
def plant_Tree():
    if can_harvest():
        harvest() # 収穫
        till() # 土を耕す
        plant(Entities.Tree)
        if get_water() < 1:
            use_item(Items.Water) # 水やり
        else :
            use_item(Items.Fertilizer)

while True:
    i = 0
    for i in range(7):
        move(North) # 北に移動
        # plant_Bush()
        plant_Tree()
        # plant_Carrot()
        # plant_Pumpkin()

    move(East)