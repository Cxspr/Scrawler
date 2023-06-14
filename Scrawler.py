from PIL import Image, ImageGrab
from pynput import mouse, keyboard
from pynput.mouse import Controller, Button
import time
from enum import Enum

class Calibration():
    def __init__(self) -> None:
        """
        calibration stages
        0 :: not started
        1 :: color picking
        2 :: canvas defs
        3 :: prepped/done
        """
        self.stage = 0 
        self.colors = {}
        self.canvas_bounds = []
        self.mouse = None
        self.keyboard = None # define for class-wide access to listeners'
        
        # The remaining variables relate to variants in color options and selection types
        self.menu_coords = None
        self.ignore_click = False
        self.color_pick_event = self.color_grab # default to the most prominant type
        # self.threshold = None # related to greyscale mode // may remove
        # self.color_count = 2 # related to greyscale mode, may not be needed
        self.goal_stage = 3
        
    def is_calibrate(self) -> bool:
        return self.stage == self.goal_stage

    def key_release(self, key):
        if key == keyboard.Key.esc:
            if self.goal_stage == 2:
                self.mouse.stop()
                self.stage = 2
                self.keyboard.stop()
                return
            self.stage = 2 # keyboard listener only needed for progression from stage 1
            print('Select the top left and bottom right bounds of your drawing area.')
            self.keyboard.stop()

    def mouse_on_click(self, x, y, button, pressed):
        if not pressed and button == Button.left:
            # mouse click release event
            if self.stage == 1:
                self.color_pick_event(x, y)
            elif self.stage == 2:
                self.canvas_bounds.append((x, y))
                if len(self.canvas_bounds) == 2:
                    self.stage = 3
                    print('Calibration finished')
                    self.mouse.stop() # end mouse listener // calibration done
    
    """
    color_grab is the default call to grab colors and coordinates dynamically. it's meant to be used
    with apps that have the colors laid out in a gridlike fashion i.e. paint, gartic, etc.
    """
    def color_grab(self, x, y):
        im = ImageGrab.grab(bbox=(x, y, x + 1, y + 1), all_screens=True)
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((0, 0))
        self.colors[(r, g, b)] = (x, y) # create or modify dict entry to associate coordinates

    """
    submenu_color_grab expands upon the default color_grab method by adding support for apps with their
    color palettes contained within a pop-up menu accessed by clicking a button to open the menu. 
    the functionality differs by initially recording the first click to open the menu as well as the
    following color selection, after this the calibration loop ignores every other mouse click as it
    assumes those clicks are to open the menu. this method may be expanded upon later if an app is found
    with a non-autoclosing menu for color selection.
    this category includes games like champed up.
    """
    def submenu_color_grab(self, x, y): # variant of color grab call for autoclosing submenus
        if self.menu_coords != None:
            if not self.ignore_click:
                self.color_grab(x, y)
            self.ignore_click = not self.ignore_click # toggle to ignore next menu click
        else:
            self.menu_coords = (x, y)
    
    
    # TODO re-evalutate the need for the limited_color_grab method
    """
    limited_color_grab differs significantly from the others as it is designed around supporting games like
    drawful in which very few options are given for colors (only 1 or 2 in addition to the white background).
    games like these should be treated differently and coordinates of color options will be tracked however,
    the colors will instead be just black, white, and grey depending on the number available
    """
    def limited_color_grab(self, x, y):
        # TODO this more than likely will need to be reworked however this mode is low on my priorities
        im = ImageGrab.grab(bbox=(x, y, x + 1, y + 1), all_screens=True)
        grey_im = im.convert('L') # convert color sample to greyscale
        color = grey_im.getpixel((0, 0))
        # key still 3 value tuple to avoid having to create new code in the Scrawler
        self.colors[(color, color, color)] = (x, y) 
        
        
    """
    The calibrate method essentially controls all the functionalty of this class can support a few arguments.
    
    The variant argument relates to the color options and selection type for an application.
    Valid variants and the type they correspond to:
        0 :: there is no submenu and colors are all laid out (like paint or gartic)
        1 :: there is a submenu that closes once a color is selected (like champed up)
        2 :: very limited palette, will ensure the white background is utilized (like drawful)
    """
    def calibrate(self, variant=0, blocking=True, start_stage=1, goal_stage=3):
        # variants = [
        #     self.color_grab,
        #     self.submenu_color_grab,
        #     self.color_grab] 
        variants = {
            ColorSelection.COLOR_GRID: self.color_grab,
            ColorSelection.SUBMENU: self.submenu_color_grab,
            ColorSelection.LIMITED: self.color_grab
        }
        try:
            self.color_pick_event = variants[variant]
        except:
            print('Invalid color selection/options type given')
            return False
     
        
        # start by clearing any previous calibration
        if start_stage == 1:
            self.colors = {}
            self.menu_coords = None
            self.ignore_click = False
        if goal_stage == 3:
            self.canvas_bounds = []
        self.stage = start_stage
        self.goal_stage = goal_stage
        
        # handle variant unique settings
        if variant == 2: # limited mode mode
            self.colors[(255,255,255)] = None #pre add white without coords as it's just the background
        
        self.keyboard = keyboard.Listener(
            on_release = self.key_release
        )
        self.mouse = mouse.Listener(
            on_click = self.mouse_on_click
        )
        
        # start listeners
        if self.stage == 1:
            self.keyboard.start()
            print('Click the locations of colors you want to use and press "Esc" when you\'re finished.')
        self.mouse.start()
        # wait for calibration to finish
        if blocking:
            while self.stage != self.goal_stage:
                time.sleep(.1) # safety limit for calibration waiting
            
        return True

# Enum for easier creation of new game defs
class ColorSelection(Enum):
    COLOR_GRID = 0
    SUBMENU = 1
    LIMITED = 2

"""
Class related to the implementation of specific games. Instances of this type should define things unique to
that game such as brush size options, color selection type and options, etc.

The GameDef class is also intended to act as an interface between the Scrawler process and the calibration
instance
"""
class GameDef():
    def __init__(\
        self,
        color_selection,
        brush_sizes=[1, 3, 5],
        speed=0.01,
        pick_delay=0.15,
        skip_white=False
        
    ) -> None:
        self.cal = Calibration()
        self.color_selection = color_selection
        self.brush_sizes = brush_sizes
        self.speed = speed
        self.skip_white = skip_white
        self.pick_delay = pick_delay
        
        # added for easy access by the Scrawler
        # self.palette = None
        pass
    
    def calibrate(self, blocking=True, start_stage=1, goal_stage=3):
        if (self.cal.calibrate(variant=self.color_selection, blocking=blocking, start_stage=start_stage, goal_stage=goal_stage) is not True):
            print('Something went wrong during calibration')
            return None, []
        
        # Get function critical stuff so the parent Scrawler object can access them more easily
        palette = Image.new("P", (16, 16))
        colors = list(sum(list(self.cal.colors.keys()), ()))
        if self.color_selection == ColorSelection.LIMITED:
            palette.putpalette(colors * 64)
        else:
            palette.putpalette(colors)
        
        return palette, colors, self.cal.canvas_bounds #, width, height # these will be returned to the calling Scrawler
        
    def get_color_params(self):
        palette = Image.new("P", (16, 16))
        colors = list(sum(list(self.cal.colors.keys()), ()))
        if self.color_selection == ColorSelection.LIMITED:
            palette.putpalette(colors * 64)
        else:
            palette.putpalette(colors)
        
        return palette, colors
    
    def get_canvas_params(self):
        return self.cal.canvas_bounds
        
    def get_calibration_params(self):
        palette = Image.new("P", (16, 16))
        # colors = list(sum(list(self.cal.colors.keys()), ()))
        colors = list(self.cal.colors.keys())
        color_data = ( # following code ensures palette is always 768 in length with only desired colors
            sum( [list(x) for x in colors], []) #flattens nested array
            + list(colors[-1] * (256 - len(colors))) #fill rest of color_space with a preexisting value as a dummy
        )[:256*3] # trim if needed
        palette.putdata(color_data)
        
        return palette, list(sum(colors)), self.cal.canvas_bounds 

    def is_calibrated(self) -> bool:
        return self.cal.stage == 3
    
    # mouse should be a mouse controller and color should be the proper dict key for the coordinate dictionary    
    def change_color(self, mouse: Controller, color) -> bool:
        try:
            coords = self.cal.colors[color]
            # if here then a color was found and coords were pulled and we can now select it
            
            # first account for opening the color menu if applicable
            if self.color_selection == ColorSelection.SUBMENU:
                mouse.position = self.cal.menu_coords
                time.sleep(self.pick_delay)
                mouse.click(Button.left)
                time.sleep(self.pick_delay)
                
            mouse.position = coords
            time.sleep(self.pick_delay) # time buffers ensure app being interacted with can register the color change
            mouse.click(Button.left)
            time.sleep(self.pick_delay)
            return True
        except KeyError:
            print('The requested color could not be found!')
            return False


class Scrawler():
    
    game_definitions = {
        'Paint': GameDef(
            color_selection=ColorSelection.COLOR_GRID,
            brush_sizes=[1, 3, 5, 8],
            speed=0.01,
            pick_delay=0.15
        ),
        'Gartic Phone': GameDef(
            color_selection=ColorSelection.COLOR_GRID,
            brush_sizes=[2, 3, 5, 8, 11], # TODO figure out the actual brush sizes
            speed=0.01,
            pick_delay=0.15
        ),
        'Champ\'d Up': GameDef(
            color_selection=ColorSelection.SUBMENU,
            brush_sizes=[2, 3, 5, 8, 11, 25], # TODO needs calibration
            speed=0.01,
            pick_delay=0.15
        )
    }
    
    def __init__(self):
        self.game : GameDef = None
        self.palette : Image.Image = None
        self.canvas = []
        self.colors = None
        
        self.im_src : Image.Image = None
        self.im_mod : Image.Image = None
        
        self.mouse = Controller()
        self.keyboard = None
        self.scrawler_stopped = True
        
    ### game selection and calibration ###     
    
    def set_game(self, game_name: str="", game=None):
        if isinstance(game, GameDef):
            self.game = game
        elif game_name not in Scrawler.game_definitions.keys():
            print(game_name, 'was not found among the defined games.') 
            self.game = None # reset to avoid conflicts with what was selected
        else:
            self.game = Scrawler.game_definitions[game_name]
            self.im_mod = None # clear any mod image
            
    def game_check(self, check_calibration=False) -> bool:
        if self.game is None:
            print('No game selected')
            return False
        if check_calibration and not self.game.is_calibrated(): 
            print('The game has not been calibrated yet')
            return False
        return True
            
    def run_calibration(self, blocking=True, start_stage=1, goal_stage=3) -> bool:
        if not self.game_check():
            return False
        
        palette, colors, canvas = self.game.calibrate(blocking=blocking,
                                                      start_stage=start_stage,
                                                      goal_stage=goal_stage)
        if start_stage == 1:
            self.palette = palette
            self.colors = colors
        if goal_stage == 3:
            self.canvas = canvas
        if self.palette is None or len(self.canvas) != 2:
            return False
        
        # update image dimensions to reflect the max size with this canvas
        if self.im_src is not None:
            self.resize_img() # only resize if the image was loaded before calibration was done
            self.im_mod = None # get rid of any previous generation since src image changed
        
        return True
    
    def check_color_params(self) -> bool:
        self.palette, self.colors = self.game.get_color_params()
        if self.palette is None:
            return False
        return True
        
    def check_canvas_params(self):
        self.canvas = self.game.get_canvas_params()
        if len(self.canvas) != 2:
            return False
        if self.im_src is not None:
            self.resize_img() # only resize if the image was loaded before calibration was done
        return True
        
    
    def check_calibration_params(self) -> bool:
        self.palette, self.colors, self.canvas = self.game.get_calibration_params()
        if self.palette is None or len(self.canvas) != 2:
            return False
        
        # update image dimensions to reflect the max size with this canvas
        if self.im_src is not None:
            self.resize_img() # only resize if the image was loaded before calibration was done
            # self.im_mod = None # get rid of any previous generation since src image changed
        
        return True
    
    ### image related methods ###
    
    def load_img(self, img : Image.Image) -> bool:
        self.im_src = img
        self.im_mod = None # clear any previously generated image
        # resize image if game selected and calibration was already done
        if self.game_check(True):
            self.resize_img()
        
    
    def resize_img(self) -> bool:
        if not self.game_check(): # verify
            return False
        if self.im_src is None:
            print('No image loaded')
            return False
        try:
            w, h = self.im_src.size
            w_bounds = self.canvas[1][0] - self.canvas[0][0]
            h_bounds = self.canvas[1][1] - self.canvas[0][1]
            
            if w > w_bounds or h > h_bounds:
                # size reduction of image
                self.im_src.thumbnail((int(w_bounds * 0.9), int(h_bounds * 0.9)))
            # find percent to increase dimensions
            w_percent = w_bounds/float(w)
            h_percent = h_bounds/float(h)
            if w_percent < h_percent:
                percent = w_percent * 0.9 # reduce a little bit to give margins to drawing space
            else:
                percent = h_percent * 0.9
            nw = int(w * percent)
            nh = int(h * percent)
            self.im_src = self.im_src.resize((nw, nh))
        except:
            print('Something went wrong while resizing the image.')
            return False
        return True
        
    def gen_img(self, dither=False, brush_size=0) -> bool:
        if not self.game_check(): # verify
            return False
        if self.im_src is None:
            print('No image loaded')
            return False
        self.im_mod = self.im_src.copy().convert("RGB").quantize(palette=self.palette, dither=dither, method=2, kmeans=brush_size)
        # self.im_mod = self.im_src.copy().convert("RGB")
        # self.im_mod = self.im_mod.convert("P", 0, palette=self.palette, colors=len(self.colors)//3)
        
        # self.im_mod.show()
        
    ### draw related methods ###
    def extract_lines(self, brush_size=3, filter_noise=True):
        vert_lines, vert_count = self.scan_lines(vert_scan=True, brush_size=brush_size, filter_noise=filter_noise)
        hori_lines, hori_count = self.scan_lines(vert_scan=False, brush_size=brush_size, filter_noise=filter_noise)
        if hori_count <= vert_count:
            return hori_lines
        return vert_lines
    
    def scan_lines(self, vert_scan, brush_size=3, filter_noise=True):
        if not vert_scan:
            bound1 = self.im_mod.height
            bound2 = self.im_mod.width
        else: # horizontal scan
            bound1 = self.im_mod.width
            bound2 = self.im_mod.height
        lines = {}
        line_count = 0
        for i in range(0, bound1, brush_size):
            line_color = None
            for j in range(0, bound2, brush_size):
                if not vert_scan:
                    color_id = self.im_mod.getpixel((j, i))
                    base = color_id*3
                    r, g, b = self.colors[base:base+3]
                    current_position = (j + self.canvas[0][0], i + self.canvas[0][1])
                else:
                    color_id = self.im_mod.getpixel((i, j))
                    base = color_id*3
                    r, g, b = self.colors[base:base+3]
                    current_position = (i + self.canvas[0][0], j + self.canvas[0][1])
                if line_color is None: # start of new line
                    line_color = (r, g, b)
                    line_start = current_position
                elif line_color != (r, g, b): # end of line, finalize and add it to color's list
                    if line_color not in lines:
                        lines[line_color] = []
                    if (filter_noise and line_start != line_end) or not filter_noise:
                        lines[line_color].append([line_start, line_end])
                    if line_color == (255,255,255) and self.game.color_selection == ColorSelection.LIMITED:
                        line_count -= 1 # dont count white on this mode
                    line_count += 1
                    line_color = (r, g, b)
                    line_start = current_position
                line_end = current_position
            if line_color not in lines:
                lines[line_color] = []
            if (filter_noise and line_start != line_end) or not filter_noise:
                lines[line_color].append([line_start, line_end])
            if line_color == (255,255,255) and self.game.color_selection == ColorSelection.LIMITED:
                line_count -= 1 # dont count white on this mode
            line_count += 1
            line_color = None # reset detected color
        return [lines, line_count]
                  
    def draw(self, brush_size=3, filter_noise=True, draw_speed=.01, gui_linked=False):
        # add error/safety catches
        if brush_size not in self.game.brush_sizes:
            print('Invalid brush size given')
            return
        self.game.speed = draw_speed
    
        lines = self.extract_lines(brush_size=brush_size, filter_noise=filter_noise)
        # self.mouse.move(self.canvas[0][0], self.canvas[0][1])
        # self.mouse.click(Button.left)
        if gui_linked:
            self.keyboard = keyboard.Listener(on_release=self.key_release)
            self.keyboard.start()
            print('Scrawler ready to draw, press enter to start.')
        wait_time = 0
        while self.scrawler_stopped:
            time.sleep(.1) # lazy wait for user to press enter to start
            wait_time += .1
            if wait_time >= 20:
                return
        
        for key, value in lines.items():
            color = (key[0], key[1], key[2])
            if color == (255, 255, 255) and self.game.color_selection == ColorSelection.LIMITED:
                continue # skip over white in this case
            self.game.change_color(self.mouse,  color)
            for line in value:
                self.draw_line(line)
                if self.scrawler_stopped:
                    return # emergency stop system
            time.sleep(0.1) # delay added between colors
        if gui_linked:
            self.keyboard.stop()
        print("Scrawler is done")
    
    def draw_line(self, coords):
        self.mouse.position = coords[0]
        self.mouse.press(Button.left)
        self.mouse.move(abs(coords[1][0] - coords[0][0]), abs(coords[1][1] - coords[0][1]))
        if (abs(coords[1][0] - coords[0][0]) > 0 or abs(coords[1][1] - coords[0][1]) > 0):
            time.sleep(self.game.speed)
        else:
            time.sleep(self.game.speed)
        self.mouse.release(Button.left)
                
    def key_release(self, key): # TODO maybe change the keys later
        if key == keyboard.Key.esc:
            print('Stopping Scrawler')
            self.scrawler_stopped = True
            self.keyboard.stop()
        if key == keyboard.Key.enter:
            print('Starting Scrawler')    
            self.scrawler_stopped = False   
        
def main():
    scrawler = Scrawler()
    scrawler.set_game('Gartic Phone')
    scrawler.run_calibration()
    scrawler.load_img(Image.open('Virgin.png'))
    scrawler.gen_img(False)
    scrawler.draw(brush_size=2, filter_noise=True)
    
if __name__ == '__main__':
     main()