class Box:
    counter = 1

    def __init__(self, box_id, original_width, original_height, original_depth, is_fragile=False):
        self.box_id = int(box_id)
        self.original_width = float(original_width)
        self.original_height = float(original_height)
        self.original_depth = float(original_depth)
        self.is_fragile = bool(int(is_fragile))
        self.x = self.y = self.z = 0
        self.width = self.original_width
        self.height = self.original_height
        self.depth = self.original_depth
        self.unique_id = Box.counter
        Box.counter += 1
        self.orientation = [
            (self.original_width, self.original_height, self.original_depth),
            (self.original_width, self.original_depth, self.original_height),
            (self.original_height, self.original_width, self.original_depth),
            (self.original_height, self.original_depth, self.original_width),
            (self.original_depth, self.original_width, self.original_height),
            (self.original_depth, self.original_height, self.original_width)
        ]

    def rotate(self, idx):
        self.width, self.height, self.depth = self.orientation[idx]

    def copy(self):
        new_box = Box(self.box_id, self.original_width, self.original_height, self.original_depth, self.is_fragile)
        new_box.x, new_box.y, new_box.z = self.x, self.y, self.z
        new_box.width, new_box.height, new_box.depth = self.width, self.height, self.depth
        new_box.unique_id = self.unique_id
        return new_box
