#coding=utf-8
import random

class Polygon:
    def __init__(self, width, height, edge = 5):
        self.edge = edge
        self.points = []
        x, y = random.randint(0, int(width)), random.randint(0, int(height))
        #for i in range(edge):
        #    self.points.append((random.randint(0, int(width)), random.randint(0, int(height))))
        for i in range(edge):
            self.points.append((x + random.randint(0, int(width/4)), y + random.randint(0, int(height/4))))
        
        # rgba
        self.color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        self.width = width
        self.height = height
        
        
    def variation(self, scale = 1.0):
        variation_type = ['point', 'color', 'change']
        variation_weight = [60, 40, 10]
        
        # 选一种变异方式
        var = random.choices(variation_type, weights = variation_weight, cum_weights=None, k=1)[0]
        
        point_change_range = 50 * scale
        color_change_range = 50 * scale
        
        if var == 'point':
            i = random.sample(range(self.edge),1)[0]
            self.points[i] = (
                random.randint(-point_change_range,point_change_range)+self.points[i][0],
                random.randint(-point_change_range,point_change_range)+self.points[i][1]
            )
        elif var == 'color':
            self.color = tuple(random.randint(-color_change_range, color_change_range) + c for c in self.color)
            # rgba 不得超过255，不得小于0
            self.color = tuple(min(max(c, 0), 255) for c in self.color)
        elif var == 'change':
            new_polygon = Polygon(self.width, self.height, self.edge)
            self.points = new_polygon.points
            self.color = new_polygon.color