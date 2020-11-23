import bpy

class DisjointSet():
    def __init__(self, size):
        self.data = [-1] * size

    def find_set(self, idx):
        elem = self.data[idx]
        if elem < 0:
            return idx
        parent_idx = self.find_set(elem)
        self.data[idx] = parent_idx
        return parent_idx
    
    def union(self, a_idx, b_idx):
        a_root = self.find_set(a_idx)
        b_root = self.find_set(b_idx)
        if (size(a_root) > size(b_root)):
            self.data[b_root] = a_root
        else:
            self.data[a_root] = b_root
        
    def size(set_id):
        root_idx = self.find_set(set_id)
        return self.data[root_idx] * -1

def get_image_from_plane(obj):
    return obj.active_material.node_tree.nodes['Image Texture'].image

def to_idx(img, x, y):
    width = img.size[0]
    height = img.size[1]
    return (y * width + x) * 4

def valid_neighbors(img, x, y):
    return [coord for coord in all_neighbors(x, y) if valid_coord(img, (x, y))]

def all_neighbors(x, y):
    return [ (x+x_off, y+y_off) for x_off in [-1, 0, 1] for y_off in [-1, 0 ,1] if not (x_off == y_off and x_off == 0)]

def valid_coord(img, coord):
    return coord[0] > 0 and coord[0] < img.size[0] and coord[1] > 0 and coord[1] < img.size[1]

def is_black(img, x, y):
    pix = pix_at(img, x, y)
    threshold = 5 / 256
    return pix[0] < threshold and pix[1] < threshold and pix[2] < threshold

def pix_at(img, x, y):
    index = to_idx(img, x, y)
    return (img.pixels[index], img.pixels[index + 1], img.pixels[index + 2], img.pixels[index + 3])

def mesh_from_points(points):
    ob_name = "output"
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)
    me.from_pydata( [(p[0], p[1], 0.0) for p in points] , [], [])
    ob.show_name = True
    me.update()
    print("updated mesh")
    return ob

def main():
    img = get_image_from_plane(bpy.context.active_object)
#    set = DisjointSet(img.size[0] * img.size[1])
    boundary = []
    full_neighbor_count = 8
    for x in range(0, img.size[0]-1):
        for y in range (0, img.size[1]-1):
            if not is_black(img, x, y):
                continue
            black_neighbors = [coord for coord in valid_neighbors(img, x, y) if is_black(img, *coord)]
            if len(black_neighbors) < full_neighbor_count:
                boundary.append((x, y))
                print("found boundary!!")
        print("done with column", x)
    print("building mesh")
    ob = mesh_from_points(boundary)
    bpy.context.collection.objects.link(ob)
    
main()

