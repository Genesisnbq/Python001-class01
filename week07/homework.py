# 动物园类
# 动物园类要求有“名字”的属性和“添加动物”的方法，
# “添加动物”方法要实现同一个动物实例不能被重复添加。
class Zoo(object):
    def __init__(self, name):
        self.animal = {}
        self.zoo_name = name
    # z.add_amimal(cat1)
    def add_amimal(self, obj_animal):
        if obj_animal in self.animal:
            print('该动物已存在')
            return self.animal[obj_animal]
        else:
            self.animal[obj_animal] = obj_animal
            print('添加成功')
            return True

# 动物类
# 定义“体型”（大、中、小）、“类型”（肉、草、杂）、“性格”（凶、顺）、“是否属于凶猛动物”四个属性，
# 是否属于凶猛动物的标准是：
# “体型>=中等”并且是“食肉类型”同时“性格凶猛”；
class Animal(object):
    size_dict = {
        '小型':1,
        '中型':2,
        '大型':3,
    }
    like_meat_type = {
        '食肉':True,
        '食草':False,
        '杂食':False,
    }
    is_fierce_type = {
        '凶猛':True,
        '温顺':False,        
    }
    def __init__(self, like_meat, size, is_fierce):
        super().__init__()
        self.size = Animal.size_dict[size]
        self.like_meat = Animal.like_meat_type[like_meat]
        self.is_fierce = Animal.is_fierce_type[is_fierce]
        if self.size>=2 and self.like_meat==True and self.is_fierce==True:
            self.is_fierce_animal = True
        else:
            self.is_fierce_animal = False

# 猫类
# 猫类要求定义“叫声”、“是否合适作为宠物”以及“名字”三个属性，
# 其中“叫声”作为类属性，猫类继承自动物类；
class Cat(Animal):
    cry = '喵喵喵'
    def __init__(self, name, size, like_meat, is_fierce, for_pet=False):
        super().__init__(size, like_meat, is_fierce)
        self.name = name
        self.for_pet = for_pet

if __name__ == "__main__":
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化猫cat1
    cat1 = Cat('大花猫1', '食肉', '小型', '温顺')
    # 增加cat1到动物园
    z.add_amimal(z.cat1)
    # 判断动物园是否有猫这种动物
    getattr(z, 'Cat')