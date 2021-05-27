#coding=utf-8
from PIL import Image, ImageDraw
from imgcompare import image_diff
from polygon import Polygon
import random


class drawByPil:
    def __init__(self, polygon_num, target_img, max_polygon_num = 100, edge = 3):
        self.max_polygon_num = max_polygon_num
        # 记录当前多边形数量
        self.polygon_quantity = polygon_num
        self.img_width, self.img_height = target_img.size
        self.edge = edge
        # 多边形的数组
        self.polygons = [Polygon(self.img_width, self.img_height, edge) for p in range(polygon_num)]
        # 背景颜色
        self.background = (0,0,0,255)
        self.target_img = target_img
        # 适应度
        self.fitness = None
    
    
    
    def draw(self) -> Image:
        # 创建背景布， 默认是纯黑色画布
        canvas = Image.new('RGBA', (self.img_width, self.img_height))
        bg = ImageDraw.Draw(canvas)
        bg.polygon([(0,0), (0, self.img_height), (self.img_width, self.img_height), (self.img_width, 0)], fill = self.background)
        
        # 将半透明多边形画到背景布上
        for p in self.polygons:
            new_canvas = Image.new('RGBA', (self.img_width, self.img_height))
            new_bg = ImageDraw.Draw(new_canvas)
            new_bg.polygon(p.points, fill = p.color)
            
            # 关键的一步 半透明图像相互叠加 PIL 中有方法可以直接画
            canvas = Image.alpha_composite(canvas, new_canvas)
            
        return canvas
            
            
    # 交叉
    @staticmethod
    def mating(dad, mom):
        if not dad.polygon_quantity == mom.polygon_quantity:
            raise Exception("父类间多边形数量不一致")
            
        child = drawByPil(0, dad.target_img, dad.max_polygon_num, dad.edge)
        
        # zip()压缩对象为元组 在for循环内解包返回原数据
        for dad_polygon, mom_polygon in zip(dad.polygons, mom.polygons):
            if random.random() > 0.5:
                child.polygons.append(dad_polygon)
            else:
                child.polygons.append(mom_polygon)
                
        child.polygon_quantity = dad.polygon_quantity
        return child
        
        
    # 变异
    def variation(self, rate = 0.05, scale = 1.0):
        total_variation = int(rate*self.polygon_quantity)
        random_indices = list(range(self.polygon_quantity))
        random.shuffle(random_indices)
        # 随机变异
        for i in range(total_variation):
            index = random_indices[i]
            self.polygons[index].variation(scale=scale)
            
            
    # 适应度函数 通过image_diff函数 量化比较图片差异
    def fit(self) -> float:
        if self.polygon_quantity < 1:
            return None
        self.img = self.draw()
        self.fitness = image_diff(self.img, self.target_img)
        return self.fitness
        
        
        
    # 新增多边形数量  如果要交叉则需要保持基因数量一致，不要用这个方法
    def grow(self, new_polynum_num):
        if self.polygon_quantity >= self.max_polygon_num:
            return False
            
        if self.polygon_quantity + new_polynum_num > self.max_polygon_num:
            new_polynum_num = self.max_polygon_num - self.polygon_quantity
            self.polygon_quantity = self.max_polygon_num
        else:
            self.polygon_quantity += new_polynum_num
            
        new_polygons = [Polygon(self.img_width, self.img_height, edge) for p in range(new_polynum_num)]
        self.polygons += new_polygons