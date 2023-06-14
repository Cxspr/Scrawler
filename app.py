import sys
from threading import Thread

"""
TODO
* eventually add support for removing colors by clicking them in the color showcase
"""


from pynput import keyboard

from custom_gui_widgets import *
from Scrawler import *

from PyQt6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QTimer)
from PyQt6.QtGui import (QFont, QIcon, QPixmap)
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QSlider, QSpacerItem, QToolButton,
                               QVBoxLayout, QWidget, QGridLayout)


class Ui_scrawler_gui(object):
    def setupUi(self, scrawler_gui):
        if not scrawler_gui.objectName():
            scrawler_gui.setObjectName(u"scrawler_gui")
        scrawler_gui.setEnabled(True)
        scrawler_gui.resize(800, 600)
        font = QFont()
        font.setPointSize(12)
        scrawler_gui.setFont(font)
        scrawler_gui.setAutoFillBackground(True)
        self.parent = scrawler_gui
        self.centralwidget = QWidget(scrawler_gui)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.main_menu = QVBoxLayout()
        self.main_menu.setSpacing(4)
        self.main_menu.setObjectName(u"main_menu")
        self.main_menu.setContentsMargins(12, 8, 12, 12)
        self.game_label = QLabel(self.centralwidget)
        self.game_label.setObjectName(u"game_label")

        self.main_menu.addWidget(self.game_label)

        self.game_select = QComboBox(self.centralwidget)
        self.game_select.setObjectName(u"game_select")
        self.game_select.addItems(Scrawler.game_definitions.keys())
        self.game_select.addItem('Custom') # TODO implement custom games
        self.game_select.setCurrentIndex(-1)


        self.main_menu.addWidget(self.game_select)

        self.brush_size_label = QLabel(self.centralwidget)
        self.brush_size_label.setObjectName(u"brush_size_label")

        self.main_menu.addWidget(self.brush_size_label)

        self.brush_size_slider = QSlider(self.centralwidget)
        self.brush_size_slider.setObjectName(u"brush_size_slider")
        self.brush_size_slider.setEnabled(True)
        self.brush_size_slider.setMinimum(1)
        self.brush_size_slider.setMaximum(7)
        self.brush_size_slider.setSingleStep(2)
        self.brush_size_slider.setValue(3)
        self.brush_size_slider.setOrientation(Qt.Orientation.Horizontal)
        self.brush_size_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.brush_size_slider.setTickInterval(2)

        self.main_menu.addWidget(self.brush_size_slider)

        self.draw_speed_label = QLabel(self.centralwidget)
        self.draw_speed_label.setObjectName(u"draw_speed_label")

        self.main_menu.addWidget(self.draw_speed_label)

        self.draw_speed_slider = QSlider(self.centralwidget)
        self.draw_speed_slider.setObjectName(u"draw_speed_slider")
        self.draw_speed_slider.setMinimum(0)
        self.draw_speed_slider.setMaximum(8)
        self.draw_speed_slider.setSingleStep(1)
        self.draw_speed_slider.setValue(4)
        self.draw_speed_slider.setOrientation(Qt.Orientation.Horizontal)
        self.draw_speed_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.draw_speed_slider.setTickInterval(1)

        self.main_menu.addWidget(self.draw_speed_slider)

        self.color_selection_label = QLabel(self.centralwidget)
        self.color_selection_label.setObjectName(u"color_selection_label")
        self.color_selection_label.setVisible(False)

        self.main_menu.addWidget(self.color_selection_label)

        self.color_selection = QComboBox(self.centralwidget)
        self.color_selection.setObjectName(u"color_selection")
        self.color_selection_types = {
            'Color Grid' : ColorSelection.COLOR_GRID,
            'Submenu' : ColorSelection.SUBMENU,
            'Limited' : ColorSelection.LIMITED
        }
        self.color_selection.addItems(self.color_selection_types.keys())
        self.color_selection.setVisible(False)

        self.main_menu.addWidget(self.color_selection)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_menu.addItem(self.verticalSpacer)
        
        self.calibration_instructions = QLabel(self.centralwidget)
        self.calibration_instructions.setObjectName(u"calibration_instructions")
        self.calibration_instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.calibration_instructions.setWordWrap(True)
        self.calibration_instructions.setVisible(False)

        self.main_menu.addWidget(self.calibration_instructions)

        self.color_showcase = QGridLayout()
        self.color_showcase.setObjectName(u"color_showcase")
        self.color_showcase.layout
        
        self.main_menu.addLayout(self.color_showcase)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pick_colors = QPushButton(self.centralwidget)
        self.pick_colors.setObjectName(u"pick_colors")
        self.pick_colors.setEnabled(False)
        font1 = QFont()
        font1.setPointSize(14)
        self.pick_colors.setFont(font1)
        self.pick_colors.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_3.addWidget(self.pick_colors)
        
        self.pick_canvas = QPushButton(self.centralwidget)
        self.pick_canvas.setObjectName(u"pick_canvas")
        self.pick_canvas.setEnabled(False)
        font1 = QFont()
        font1.setPointSize(14)
        self.pick_canvas.setFont(font1)
        self.pick_canvas.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_3.addWidget(self.pick_canvas)

        self.small_draw = QPushButton(self.centralwidget)
        self.small_draw.setObjectName(u"small_draw")
        self.small_draw.setFont(font1)
        icon = QIcon()
        icon.addFile(u"icons/draw.png",
                     QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.small_draw.setIcon(icon)
        self.small_draw.setIconSize(QSize(24, 24))
        self.small_draw.setVisible(False)

        self.horizontalLayout_3.addWidget(self.small_draw)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 4)
        self.horizontalLayout_3.setStretch(2, 2)
        

        self.main_menu.addLayout(self.horizontalLayout_3)

        self.horizontalLayout.addLayout(self.main_menu)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setEnabled(True)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout.addWidget(self.line)

        self.gfx_menu = QVBoxLayout()
        self.gfx_menu.setObjectName(u"gfx_menu")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.collapse = QToolButton(self.centralwidget)
        self.collapse.setObjectName(u"collapse")
        icon1 = QIcon()
        icon1.addFile(u"icons/panel_close.png",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.collapse.setIcon(icon1)
        self.collapse.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.collapse)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.toggle_vis = QToolButton(self.centralwidget)
        self.toggle_vis.setObjectName(u"toggle_vis")
        icon2 = QIcon()
        icon2.addFile(u"icons/toggle_vis_on.png",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toggle_vis.setIcon(icon2)
        self.toggle_vis.setIconSize(QSize(24, 24))
        self.toggle_vis.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.toggle_vis)

        self.undo = QToolButton(self.centralwidget)
        self.undo.setObjectName(u"undo")
        icon3 = QIcon()
        icon3.addFile(u"icons/undo.png",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.undo.setIcon(icon3)
        self.undo.setIconSize(QSize(24, 24))
        self.undo.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.undo)

        self.close = QToolButton(self.centralwidget)
        self.close.setObjectName(u"close")
        icon4 = QIcon()
        icon4.addFile(u"icons/x_close.png",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close.setIcon(icon4)
        self.close.setIconSize(QSize(24, 24))
        self.close.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.close)

        self.gfx_menu.addLayout(self.horizontalLayout_4)
        
        self.collapse_spacer = QSpacerItem(
            self.collapse.width(), 550, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)

        self.gfx_bucket = GraphicsBucket('gfx_bucket',self)
        self.gfx_bucket.setObjectName(u"gfx_bucket")
        self.gfx_bucket.setPixmap(
            QPixmap(u"icons/download.png"))
        self.gfx_bucket.setScaledContents(False)
        self.gfx_bucket.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gfx_menu.addWidget(self.gfx_bucket)
        
        self.gfx_instructions = QLabel()
        self.gfx_instructions.setObjectName(u"gfx_instructions")
        self.gfx_instructions.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.gfx_menu.addWidget(self.gfx_instructions)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(12, -1, 12, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dither = QCheckBox(self.centralwidget)
        self.dither.setObjectName(u"dither")
        self.dither.setFont(font1)

        self.verticalLayout.addWidget(self.dither)

        self.filter_noise = QCheckBox(self.centralwidget)
        self.filter_noise.setObjectName(u"filter_noise")
        self.filter_noise.setFont(font1)

        self.verticalLayout.addWidget(self.filter_noise)

        self.horizontalLayout_5.addLayout(self.verticalLayout)

        self.generate = QPushButton(self.centralwidget)
        self.generate.setObjectName(u"generate")
        self.generate.setFont(font1)
        self.generate.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.generate)

        self.draw = QPushButton(self.centralwidget)
        self.draw.setObjectName(u"draw")
        self.draw.setFont(font1)
        self.draw.setEnabled(False)
        self.small_draw.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.draw)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_5.setStretch(2, 3)
        

        self.gfx_menu.addLayout(self.horizontalLayout_5)

        self.gfx_menu.setStretch(0, 1)
        self.gfx_menu.setStretch(1, 10)
        self.gfx_menu.setStretch(2, 1)
        self.gfx_menu.setStretch(3, 2)

        self.horizontalLayout.addLayout(self.gfx_menu)

        self.horizontalLayout.setStretch(0, 30)
        self.horizontalLayout.setStretch(2, 70)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        scrawler_gui.setCentralWidget(self.centralwidget)

        self.retranslateUi(scrawler_gui)

        QMetaObject.connectSlotsByName(scrawler_gui)
        
        # custom vals
        self.scrawler = Scrawler()
        self.game = GameDef(None)
        self.game_speed = 0.01
        self.brush_size = 3
        self.colors = []
        self.calibration_goal = 3
        self.calibration_timer = None
        self.draw_thread = None
        self.keyboard = None
        self.custom_game = GameDef(
            color_selection=ColorSelection.COLOR_GRID,
            brush_sizes=list(range(1,25)),
            speed=0.01)
        self.using_custom = False
        self.panel_collapsed = False
        
        # setup signals
        self.game_select.currentIndexChanged.connect(self.game_change)
        self.brush_size_slider.valueChanged.connect(self.brush_size_change)
        self.draw_speed_slider.valueChanged.connect(self.draw_speed_change)
        self.color_selection.currentIndexChanged.connect(self.color_selection_change)
        
        self.pick_colors.clicked.connect(self.color_pick_event)
        self.pick_canvas.clicked.connect(self.canvas_pick_event)
        
        self.generate.clicked.connect(self.generate_event)
        self.close.clicked.connect(self.close_event) 
        self.undo.clicked.connect(self.undo_event)
        self.toggle_vis.clicked.connect(self.toggle_vis_event)
        self.draw.clicked.connect(self.draw_event)
        
        self.collapse.clicked.connect(self.collapse_event)
        
    # UI callbacks
    def game_change(self, value):
        if value == -1:
            return
        else:
            game = self.game_select.currentText()
            if game == 'Custom':
                self.scrawler.set_game(game=self.custom_game)
                self.brush_size_slider.setMinimum(1)
                self.brush_size_slider.setMaximum(25)
                self.brush_size_slider.setSingleStep(1)
                self.brush_size_slider.setTickInterval(1)
                self.color_selection.setVisible(True)
                self.pick_colors.setEnabled(True)
                self.pick_canvas.setEnabled(True)
                self.using_custom = True
            elif game in self.scrawler.game_definitions.keys():
                self.scrawler.set_game(game)
                self.brush_size_slider.setMinimum(self.scrawler.game.brush_sizes[0])
                self.brush_size_slider.setMaximum(self.scrawler.game.brush_sizes[len(self.scrawler.game.brush_sizes) - 1])
                self.brush_size_slider.setSingleStep(2)
                self.brush_size_slider.setTickInterval(2)
                self.pick_colors.setEnabled(True)
                self.pick_canvas.setEnabled(True)
                self.color_selection.setVisible(False)
                self.using_custom = False
                
    def brush_size_change(self, value):
        self.brush_size = value
        # self.gfx_bucket.clear_alt_image()
        
    def draw_speed_change(self, speed):
        speed_options = [0.1,
                         0.075,
                         0.05,
                         0.025,
                         0.01,
                         0.0075,
                         0.005,
                         0.0025,
                         0.001]
        self.game_speed = speed_options[speed]
        if self.using_custom:
            self.custom_game.speed = self.game_speed
        self.scrawler.game.speed = self.game_speed
        # self.gfx_bucket.clear_alt_image()
        
    def color_selection_change(self, value):
        self.custom_game.color_selection = self.color_selection_types[self.color_selection.currentText()]
        self.scrawler.game.color_selection = self.color_selection_types[self.color_selection.currentText()]
        
    def gfx_button_callback(self, has_img):
        cal_done = self.scrawler.game is not None and self.scrawler.check_calibration_params()
        self.generate.setEnabled(cal_done)
        self.close.setEnabled(True)
        self.scrawler.load_img(self.gfx_bucket.original_image)
        self.draw.setEnabled(False)
        self.small_draw.setEnabled(False)
        self.gfx_instructions.setVisible(False)
        
    def close_event(self):
        self.gfx_bucket.setPixmap(
            QPixmap(u"icons/download.png"))
        self.gfx_bucket.original_image = None
        self.gfx_bucket.alt_image = None
        self.generate.setEnabled(False)
        self.draw.setEnabled(False)
        self.small_draw.setEnabled(False)
        self.close.setEnabled(False)
        self.undo.setEnabled(False)
        self.toggle_vis.setEnabled(False)
        self.gfx_instructions.setVisible(True)
        
    def generate_event(self):
        #brush_size passed to kmeans, -1 done since base kmeans is 0
        self.scrawler.gen_img(self.dither.isChecked(), brush_size=self.brush_size - 1)
        alt = self.scrawler.im_mod.copy()
        self.gfx_bucket.load_alt_image(alt)
        self.draw.setEnabled(True)
        self.small_draw.setEnabled(True)
        self.undo.setEnabled(True)
        self.toggle_vis.setEnabled(True)
    
    def undo_event(self):
        self.gfx_bucket.clear_alt_image()
        self.draw.setEnabled(False)
        self.small_draw.setEnabled(False)
        self.toggle_vis.setEnabled(False)
        self.undo.setEnabled(False)
    
    def toggle_vis_event(self):
        self.gfx_bucket.swap_images()
        
    def draw_event(self):
        self.calibration_instructions.setVisible(True)
        self.calibration_instructions.setText("Press enter when you're ready to start the Scrawler. Press escape at anytime to force stop.")
        
        self.keyboard = keyboard.Listener(on_release=self.key_release)
        self.keyboard.start()
        
        self.draw_thread = Thread(target=self.scrawler.draw, args=(self.brush_size, self.filter_noise.isChecked(), self.game_speed, True))
        self.draw_thread.start()
        
        print('scrawler thread started')
        # # TODO add an idle spinner overlay to the draw button
        # # self.scrawler.draw(self.brush_size, self.filter_noise.isChecked())
        
        self.draw_timeout_counter = 0
        self.draw_timer = QTimer()
        self.draw_timer.timeout.connect(self.check_draw_thread)
        self.draw_timer.start(2000)
        if self.using_custom:
            print('custom parameters',
                  'brush size', self.brush_size,
                  'draw speed', self.game_speed)
        
    def key_release(self, key): # TODO maybe change the keys later
        if key == keyboard.Key.esc:
            print('Stopping Scrawler')
            self.scrawler.scrawler_stopped = True
            self.keyboard.stop()
        if key == keyboard.Key.enter:
            print('Starting Scrawler')    
            self.scrawler.scrawler_stopped = False  
    
    def check_draw_thread(self):
        running = self.draw_thread.is_alive()
        # print('thread is alive?', running)
        if not running:
            self.draw_timer.stop()
            self.calibration_instructions.setText(
                "Scrawler has finished!"
            )
            self.scrawler.scrawler_stopped = True
            self.keyboard.stop()
            
        if self.scrawler.scrawler_stopped:
            self.draw_timeout_counter += 2000
            if self.draw_timeout_counter >= 20000:
                self.calibration_instructions.setText(
                    "Drawing thread timed out, please try again"
                )
        else:
            self.draw_timeout_counter = 0
            return
        
        
    def color_pick_event(self):
        self.calibration_goal = 2
        self.gfx_bucket.clear_alt_image() # since params are changing
        self.calibration_instructions.setVisible(True)
        self.calibration_instructions.setText("Click each color you want to use, then press escape. They will show up below as added.")
        for i in reversed(range(self.color_showcase.count())):
            self.color_showcase.itemAt(i).widget().setParent(None)
        self.colors = []
        self.scrawler.run_calibration(blocking=False, start_stage=1, goal_stage=self.calibration_goal)
        if self.calibration_timer == None:
            self.calibration_timer = QTimer()
            self.calibration_timer.timeout.connect(self.calibration_update)
        self.calibration_timer.start(500)
        
    def canvas_pick_event(self):
        self.calibration_goal = 3
        self.gfx_bucket.clear_alt_image() # since params are changing
        self.generate.setEnabled(False)
        self.calibration_instructions.setVisible(True)
        self.calibration_instructions.setText("Click the upper left and lower right corners of your drawing space.")
        self.scrawler.run_calibration(blocking=False, start_stage=2, goal_stage=self.calibration_goal)
        if self.calibration_timer == None:
            self.calibration_timer = QTimer()
            self.calibration_timer.timeout.connect(self.calibration_update)
        self.calibration_timer.start(500)
        
        
    def calibration_update(self):
        # stage update detector
        if self.calibration_goal == 2:
            self.scrawler.check_color_params()
            # check for new colors
            if len(self.scrawler.colors) > len(self.colors): # then we need to update our colors
                diff = len(self.scrawler.colors) - len(self.colors) // 3
                for i in range(((len(self.colors)) // 3), (len(self.scrawler.colors) // 3)):
                    base = i*3
                    r, g, b = self.scrawler.colors[base:base+3]
                    color = Color((r, g, b))
                    color.setFixedSize(QSize(20, 20))
                    num_colors = len(self.colors) // 3
                    col = num_colors % 5
                    row = num_colors // 5
                    self.color_showcase.addWidget(color, row, col, 1, 1)
                    self.colors.append(r)
                    self.colors.append(g)
                    self.colors.append(b)
        
        if self.scrawler.game.cal.stage == self.calibration_goal:
            self.calibration_timer.stop() 
            self.calibration_instructions.setVisible(False)   
        # check if all calibrations are finished
        # if as the above checks if the current calibration is finished
            if self.scrawler.check_canvas_params() and self.scrawler.check_color_params():
                # TODO this might need to be changed as it may enable the buttons before color calibration done
                self.generate.setEnabled(self.gfx_bucket.original_image is not None)
                
    def collapse_event(self):
        if self.panel_collapsed:
            self.toggle_vis.setVisible(True)
            self.undo.setVisible(True)
            self.close.setVisible(True)
            
            self.gfx_bucket.setVisible(True)
            self.gfx_instructions.setVisible(True)
        
            self.dither.setVisible(True)
            self.filter_noise.setVisible(True)
            self.generate.setVisible(True)
            self.draw.setVisible(True)
            
            self.small_draw.setVisible(False)
            self.gfx_menu.removeItem(self.collapse_spacer)
            
            self.parent.resize(800, 600)
            icon1.addFile(u"icons/panel_close.png",
                        QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.collapse.setIcon(icon1)
            
        else:
            self.toggle_vis.setVisible(False)
            self.undo.setVisible(False)
            self.close.setVisible(False)
            
            self.gfx_bucket.setVisible(False)
            self.gfx_instructions.setVisible(False)
        
            self.dither.setVisible(False)
            self.filter_noise.setVisible(False)
            self.generate.setVisible(False)
            self.draw.setVisible(False)
            
            self.small_draw.setVisible(True)
            self.small_draw.setEnabled(self.draw.isEnabled())
            self.gfx_menu.addItem(self.collapse_spacer)
            
            #resize window
            self.parent.resize(230, 600)
            icon1 = QIcon()
            icon1.addFile(u"icons/panel_open.png",
                        QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.collapse.setIcon(icon1)
            
            
        self.panel_collapsed = not self.panel_collapsed
        
    # setupUi

    def retranslateUi(self, scrawler_gui):
        scrawler_gui.setWindowTitle(QCoreApplication.translate(
            "scrawler_gui", u"Scrawler", None))
        self.game_label.setText(QCoreApplication.translate(
            "scrawler_gui", u"Select a game/program", None))
        self.brush_size_label.setText(QCoreApplication.translate(
            "scrawler_gui", u"Brush Size", None))
        self.draw_speed_label.setText(QCoreApplication.translate(
            "scrawler_gui", u"Drawing Speed", None))
        self.color_selection_label.setText(QCoreApplication.translate(
            "scrawler_gui", u"Color Selection Type", None))
        self.calibration_instructions.setText(QCoreApplication.translate(
            "scrawler_gui", u"Click each color you want to use, then press enter. They will show up below as added.", None))
        self.color_selection_label.setText(QCoreApplication.translate(
            "scrawler_gui", u"Color Selection Type", None))
        self.pick_colors.setText(QCoreApplication.translate(
            "scrawler_gui", u"Set Colors", None))
        self.pick_canvas.setText(QCoreApplication.translate(
            "scrawler_gui", u"Set Canvas", None))
        self.small_draw.setText("")
        self.collapse.setText(QCoreApplication.translate(
            "scrawler_gui", u"...", None))
        self.toggle_vis.setText(
            QCoreApplication.translate("scrawler_gui", u"...", None))
        self.undo.setText(QCoreApplication.translate(
            "scrawler_gui", u"...", None))
        self.close.setText(QCoreApplication.translate(
            "scrawler_gui", u"...", None))
        self.gfx_bucket.setText("")
        self.gfx_instructions.setText(QCoreApplication.translate(
            "scrawler_gui", u"Drag and drop an image into the bucket above."))
        self.dither.setText(QCoreApplication.translate(
            "scrawler_gui", u"Dithering", None))
        self.filter_noise.setText(QCoreApplication.translate(
            "scrawler_gui", u"Filter Noise", None))
        self.generate.setText(QCoreApplication.translate(
            "scrawler_gui", u"Generate", None))
        self.draw.setText(QCoreApplication.translate(
            "scrawler_gui", u"Draw", None))
    # retranslateUi


class ScrawlerGUI(QMainWindow):
    def __init__(self):
        super(ScrawlerGUI, self).__init__()
        self.setWindowTitle('Scrawler')
        self.setWindowIcon(QIcon('icons/scrawler_temp.png'))
        self.setGeometry(0, 0, 800, 600)
        self.ui = Ui_scrawler_gui()
        self.ui.setupUi(self)
        
        # define the primary menu


def main():
    app = QApplication(sys.argv)
    window = ScrawlerGUI()
    window.show()
    app.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ScrawlerGUI()
    gui.show()
    sys.exit(app.exec())
