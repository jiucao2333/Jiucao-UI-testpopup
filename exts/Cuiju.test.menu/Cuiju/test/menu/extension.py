import omni.ext
import omni.ui as ui
from omni.ui import color as cl
from omni.kit.viewport.utility import get_active_viewport_window
from functools import partial

# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[Cuiju.test.self.menu] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class CuijuTestmenuExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):

        window = get_active_viewport_window()
        self.frame = window.get_frame(ext_id)
        
        with self.frame:
            
            with ui.HStack():
                
                ui.Spacer()
                with ui.VStack():
                    ui.Spacer()
                    ui.Button("Cuiju Test self.menu", mouse_pressed_fn=self.show_menu, width = 100, height = 30)
                    ui.Spacer()
                ui.Spacer()

                
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
