def farm_SpeedUp():
    if get_water() < 1:
        use_item(Items.Water) # 水やり
    else :
        use_item(Items.Fertilizer)

# にんじん作成
def plant_Carrot():
    if can_harvest():
        harvest() # 収穫
        till() # 土を耕す
        plant(Entities.Carrot) # 人参を埋める
        farm_SpeedUp()

# かぼちゃ作成
# NOTE: かぼちゃは20%の確率で枯れるので対策でtill()
def plant_Pumpkin():
    if can_harvest():
        harvest() # 収穫
        till() # 土を耕す
    else :
        plant(Entities.Pumpkin)
        farm_SpeedUp()

# 茂み作成
def plant_Bush():
    if can_harvest():
        harvest() # 収穫
        plant(Entities.Bush)

# 木作成
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
    # clear()

    i = 0
    for i in range(8):
        # plant_Hay()         # 草
        # plant_Bush()        # 茂
        # plant_Tree()        # 木
        plant_Carrot()      # 人参
        # plant_Pumpkin()     # かぼちゃ
        move(North) # 北に移動

    move(East)