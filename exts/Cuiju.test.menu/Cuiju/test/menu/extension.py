import omni.ext
import omni.kit.actions
import omni.kit.actions.core
import omni.kit.renderer_capture
import omni.kit.viewport.actions
import omni.kit.viewport.actions.hotkeys
import omni.kit.viewport.legacy_gizmos
import omni.kit.viewport.menubar
import omni.kit.viewport.menubar.render
import omni.kit.viewport.menubar.render.renderer_menu_container
import omni.kit.viewport.menubar.settings
import omni.kit.viewport.registry
import omni.kit.viewport.window
import omni.ui as ui
import omni.kit.viewport
import omni
import carb
from omni.ui import color as cl
from omni.kit.viewport.utility import get_active_viewport_window
from functools import partial

import pprint
import carb.events
import omni.kit.app
import omni.kit.viewport.utility as view_util
from pxr import Sdf




# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class CuijuTestmenuExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def __init__(self):
        super().__init__()
        mouse = omni.appwindow.get_default_app_window().get_mouse()
        self.vp_api = view_util.get_active_viewport()
        
        stage = omni.usd.get_context().get_stage()
        self.vp_api = view_util.get_active_viewport()
        path = self.vp_api.camera_path
        
        self.cam = stage.GetPrimAtPath(path).GetPrim()        
        # pprint.pprint(dir(carb.input), indent= 4)
        print('///////////////////////////////')
        # pprint.pprint(dir(carb.input.MouseEvent), indent= 4)
        # pprint.pprint((carb.input.MouseEvent.modifiers.getter), indent= 4)
        # pprint.pprint((carb.input.MouseEvent.mouse.getter), indent= 4)
        
    def on_update(self, e: carb.events.IEvent):
        
        #!这里是实现轮询的地方
        down = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_DOWN)
        up = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_UP)
        val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MIDDLE_BUTTON)
        if val or up or down: 
            print(f"MIDDLE_BUTTON : {val}")
            self.cam.GetAttribute('omni:kit:cameraLock').Set(True)
        else: 
            print(f"MIDDLE_BUTTON : {val}")
            self.cam.GetAttribute('omni:kit:cameraLock').Set(False)
        
        # state = self.cam.GetAttribute('omni:kit:cameraLock').Get()
        # print(f'Camera Lock State : {state}')
        # val = input.get_mouse_value(mouse, carb.input.MouseInput.MIDDLE_BUTTON)
        # if val: print(f"MIDDLE_BUTTON : {val}")
        # print(f"Update: {e.payload['dt']}, mouse {val}")

    def freeze_camera():
        
        pass
    
    
    
    def on_startup(self, ext_id):
        
        ###!这里是告诉app每当input轮询到有新的输入时就打印，不需要以来on_update的轮询
        self.input = carb.input.acquire_input_interface()
        self.mouse = omni.appwindow.get_default_app_window().get_mouse()           
        # val = input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_DOWN)
        # if val: print(f"SCROLL_DOWN : {val}")     
        ###!
        update_stream = omni.kit.app.get_app().get_update_event_stream()

        self.sub = update_stream.create_subscription_to_pop(self.on_update, name="My Subscription Name")
        window = get_active_viewport_window()
        self.frame = window.get_frame(ext_id)
        self.text = f'({0}, {0})'
        # pprint.pprint(omni.kit.viewport.actions.hotkeys._DEFAULT_HOTKEY_MAP)
        
        # update_stream = omni.kit.app.get_app().get_update_event_stream()
        # sub = update_stream.create_subscription_to_pop(self.on_update, name="My Subscription Name")
        
        def teet():
            # self.text = f'{overlay.scroll_x}, {overlay.scroll_y})'
            print(self.text)
            
        with self.frame:
            
            # overlay = ui.ScrollingFrame(width = window.width, height = window.height-20, horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            #             vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,)
            # overlay.style = {'background_color': cl.transparent}
            
            # self.text = f'{overlay.scroll_x}, {overlay.scroll_y})'            
            # with overlay:
            with ui.HStack():
                
                ui.Spacer()
                with ui.VStack():
                    ui.Spacer()
                    ui.Button(width = 200, height = 50, clicked_fn = self.getcam, )
                    ui.Spacer(width = 30)
                    ui.Button(self.text, mouse_pressed_fn=self.show_menu, width = 100, height = 30)
                    ui.Spacer()
                    ui.Button('kill update', mouse_pressed_fn=self.kill, width = 100, height = 30)
                ui.Spacer()
        
        self.frame.scroll_only_window_hovered = True
        
    def kill(self, *args):
        
        self.sub = None
        print(self.sub)
        
    def getcam(self):
        
        update_stream = omni.kit.app.get_app().get_update_event_stream()
        self.sub = update_stream.create_subscription_to_pop(self.on_update, name="My Subscription Name")
        
        stage = omni.usd.get_context().get_stage()
        self.vp_api = view_util.get_active_viewport()
        path = self.vp_api.camera_path
        
        self.cam = stage.GetPrimAtPath(path).GetPrim()
        lock_check = self.cam.GetAttribute('omni:kit:cameraLock')
        
        if not lock_check:
            self.cam.CreateAttribute('omni:kit:cameraLock', Sdf.ValueTypeNames.Bool).Set(False)
            
        
                
    def show_menu(self, x, y, button, modifers):
        
        self.menu = ui.Menu("Reticle", width=200, height=100)
        self.menu.clear()
        
        print(x, y)
        
        with self.menu:
            with ui.Frame(width = 425 , height = 425):
                with ui.ScrollingFrame(
                        height=425,
                        width = 425,
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                    ):
                        with ui.VGrid(column_width=100, row_height=100):
                            for i in range(100):
                                with ui.ZStack():
                                    ui.Button(
                                        text= str(i),
                                        clicked_fn = partial(self.click_image, i),
                                        style={
                                            "border_color": cl.black,
                                            "background_color": cl.gray,
                                            "border_width": 1,
                                            "margin": 0,
                                        }
                                    )
                                # ui.Label(f"{i}", style={"margin": 5})
            



                
        self.menu.show_at(x- (self.menu.width) * 2 - 40, y - self.menu.height)

    def click_image(self, index):
        
        print(f'clicked image index = {index}')

    def on_shutdown(self):
        print("[Cuiju.test.self.menu] Cuiju test self.menu shutdown")

