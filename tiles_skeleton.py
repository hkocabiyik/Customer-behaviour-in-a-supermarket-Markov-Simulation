import numpy as np
import cv2


TILE_SIZE = 32

MARKET = """
##################
##..............##
##..##..m#..#a..##
##..##..m#..#a..##
##..##..m#..#b..##
##..g#..##..#b..##
##..g#..##..#b..##
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)
        elif char == "b":
            return self.extract_tile(0, 4)
        elif char == "a":
            return self.extract_tile(1, 11)
        elif char == "m":
            return self.extract_tile(4, 13)
        elif char == "g":
            return self.extract_tile(6, 13)
        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


class Customer:

   def __init__(self, supermarket, avatar, row, col):
      """
      supermarket: A SuperMarketMap object
      avatar : a numpy array containing a 32x32 tile image
      row: the starting row
      col: the starting column
      """

      self.supermarket = supermarket
      self.avatar = avatar
      self.row = row
      self.col = col

   def draw(self, frame):
      x = self.col * TILE_SIZE
      y = self.row * TILE_SIZE
      frame[y:y+self.avatar.shape[0], x:x+self.avatar.shape[1]] = self.avatar


   def move(self, direction):
        new_row = self.row
        new_col = self.col

        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1

        if self.supermarket.contents[new_row][new_col] == '.':
            self.col = new_col
            self.row = new_row
if __name__ == "__main__":

    background = np.zeros((500, 700, 3), np.uint8)
    tiles = cv2.imread("images/tiles.png")
    pac = tiles[96:128, 0:32, :]
    market = SupermarketMap(MARKET, tiles)
    c = Customer(market,pac,10,14)
    while True:
        frame = background.copy()
        market.draw(frame)
        c.draw(frame)
        cv2.imshow('frame', frame)
        # https://www.ascii-code.com/
        key = cv2.waitKey(1)
       
        # 119 is w
        if key == 119:
            c.move('up')
        # 115 is s
        if key == 115:
            c.move('down')

         # 97 is a
        if key == 97:
            c.move('left')
        
         # 100 is d
        if key == 100:
            c.move('right')

        if key == 113: # 'q' key
            break
    
        cv2.imshow("frame", frame)


    cv2.destroyAllWindows()

    market.write_image("images/supermarket.png")
