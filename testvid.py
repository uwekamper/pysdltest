import os
import sys
import sdl2
import sdl2.ext
import ctypes
import time

from sdl2.sdlttf import TTF_OpenFont
from sdl2.sdlttf import TTF_RenderText_Shaded
from sdl2.sdlttf import TTF_GetError
from sdl2.sdlttf import TTF_Init
from sdl2.sdlttf import TTF_Quit
#from moviepy.editor import VideoFileClip

import av


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
    global button_alpha
    sdl2.ext.init()
    #container = av.open(RESOURCES.get_path("darknet.mp4"))
    container = av.open(RESOURCES.get_path("BOKK (loop)-162670765.mp4"))
    video = next(s for s in container.streams)
    W = video.format.width
    H = video.format.height
    window = sdl2.ext.Window("Hello World!", size=(W, H))
    window.show()

    print("Using hardware acceleration")
    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    
    
    sprite = factory.from_color(sdl2.ext.Color(r=255, g=255, b=255, a=255), size=(W,H))
    uifactory = sdl2.ext.UIFactory(factory)
    
    button = uifactory.from_image(sdl2.ext.BUTTON, RESOURCES.get_path("button.png"))
    button.position = 200, 160
    
    processor = sdl2.ext.TestEventProcessor()
    button.click += onclick
    
    
    spriterenderer = factory.create_sprite_render_system(window)
    
    uiprocessor = sdl2.ext.UIProcessor()
    sdl2.render.SDL_SetTextureAlphaMod(button.texture, 255)
    font_mgr = sdl2.ext.FontManager(RESOURCES.get_path("Arial Bold.ttf"), size = 160, color=RED)
    
    print(dir(renderer))
    

    #texture = sdl2.render.SDL_CreateTexture(renderer.renderer, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_STREAMING, W, H)
    
    running = True
    # while running:
    for packet in container.demux(video):
        fps = packet.duration // 10
        dec = packet.decode()
        for frame in dec:
            sdl2.render.SDL_SetRenderDrawColor(renderer.renderer, 255, 128, 128, 255)
            sdl2.render.SDL_RenderClear(renderer.renderer)
            # frame = clip.get_frame(t)
            pixels = frame.to_rgb().to_nd_array().ctypes.data_as(ctypes.c_void_p)
            surface = sdl2.surface.SDL_CreateRGBSurfaceFrom(pixels, W, H, 8*3 ,3*W, 0x0000FF, 0x00FF00, 0x00FF00, 1)
            tex = sdl2.render.SDL_CreateTextureFromSurface(renderer.renderer, surface)

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
            text_sprite.position = 10, 10
            sprite.texture = tex
            sdl2.render.SDL_SetTextureAlphaMod(sprite.texture, button_alpha)
            
            spriterenderer.render((sprite, button, text_sprite))
            sdl2.surface.SDL_FreeSurface(surface)
            sdl2.render.SDL_DestroyTexture(tex)
        
        
            sdl2.SDL_Delay(10)
    sdl2.ext.quit()
    return 0



if __name__ == "__main__":
    sys.exit(run())
