import os
import sys
import sdl2
import sdl2.ext

from sdl2.sdlttf import TTF_OpenFont
from sdl2.sdlttf import TTF_RenderText_Shaded
from sdl2.sdlttf import TTF_GetError
from sdl2.sdlttf import TTF_Init
from sdl2.sdlttf import TTF_Quit

RESOURCES = sdl2.ext.Resources(__file__, "resources")
RED = sdl2.ext.Color(86, 141, 153)
text = "NOPE"
button_alpha = 255

# A callback for the Button.click event.
def onclick(button, event):
    global button_alpha
    global text
    if button_alpha < 128:
        button_alpha = 255
        text = "NOPE"
    else:
        button_alpha = 127
        text = "YEP!"
    sdl2.render.SDL_SetTextureAlphaMod(button.texture, button_alpha)
    print("Button was clicked! {}".format(button_alpha))

def run():
    sdl2.ext.init()

    window = sdl2.ext.Window("Hello World!", size=(547, 624))
    window.show()

    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    
    
    sprite = factory.from_image(RESOURCES.get_path("background.png"))
    uifactory = sdl2.ext.UIFactory(factory)
    
    button = uifactory.from_image(sdl2.ext.BUTTON, RESOURCES.get_path("button.png"))
    button.position = 120, 60
    
    processor = sdl2.ext.TestEventProcessor()
    button.click += onclick
    
    
    spriterenderer = factory.create_sprite_render_system(window)
    
    uiprocessor = sdl2.ext.UIProcessor()
    sdl2.render.SDL_SetTextureAlphaMod(button.texture, 255)
    font_mgr = sdl2.ext.FontManager(RESOURCES.get_path("Arial Bold.ttf"), size = 160, color=RED)
    
    
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
                # Pass the SDL2 events to the UIProcessor, which takes care of
                # the user interface logic.
            uiprocessor.dispatch([button,], event)

        # Render all user interface elements on the window.
        text_sprite = factory.from_text(text,fontmanager=font_mgr) # Creating TextureSprite from Text
        text_sprite.position = 45, 440
        spriterenderer.render((sprite, button, text_sprite))
        
        
        sdl2.SDL_Delay(10)
    sdl2.ext.quit()
    return 0



if __name__ == "__main__":
    sys.exit(run())