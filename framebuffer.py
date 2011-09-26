from pyglet.gl import *
import ctypes
import glsl

class Framebuffer(object):
    """
    """
    def __init__(self, width, height):
        self.bound = False
        self.id = GLuint()
        self.width = width
        self.height = height
        self.tex = pyglet.image.Texture.create(width, height, GL_RGBA)
        
        # create a new FBO
        glGenFramebuffersEXT(1, byref(self.id))        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.id.value)
        
        # create depth renderbuffer
        # glGenRenderbuffersEXT(1, byref(self.depthbuffer_id))
        # glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, self.depthbuffer_id.value)
        # glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_DEPTH_COMPONENT, 512, 512)

        # attach renderbufers to fbo
        # glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT, GL_DEPTH_ATTACHMENT_EXT, GL_RENDERBUFFER_EXT, self.depthbuffer_id.value)
        # glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, GL_RENDERBUFFER_EXT, self.colorbuffer_id.value)
        
        # create texture renderbuffer
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, self.tex.target, self.tex.id, 0)
        # glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, self.tex_b.target, self.tex_b.id, 0)
        # attach texture
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
        
        # check if ok
        assert glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT) == GL_FRAMEBUFFER_COMPLETE_EXT
        
        glBindTexture(self.tex.target, self.tex.id)
        glTexParameteri(self.tex.target, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(self.tex.target, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glBindTexture(self.tex.target, 0)
                                    
    def bind(self):        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.id.value)
        glPushAttrib(GL_VIEWPORT_BIT)
        glViewport(0,0, self.width, self.height)
        self.bound = True
        
    def unbind(self):
        """
        Don't forget to unbind!
        """
        glPopAttrib()
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
        self.bound = False

    def delete(self):
        glDeleteFramebuffersEXT(1, byref(self.id));
        
    def clear(self):
        if not self.bound: 
            self.bind()
            glClear(GL_COLOR_BUFFER_BIT)
            self.unbind()
        else:
            glClear(GL_COLOR_BUFFER_BIT)
            
    def __enter__(self):
        self.bind()
        return self
        
    def __exit__(self, type, value, traceback):
        self.unbind()
                
    def draw(self, fb=None, shader=None):        
        if fb: fb.bind()
        if shader: shader.bind()
        
        # draw a fullscreen quad with the fb texture
        pyglet.gl.glBindTexture(self.tex.target, self.tex.id)        
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, 
            ('v2f', [0,0,0,self.height,self.width,self.height,self.width,0]), 
            ('t2f', [0,0,0,1,1,1,1,0])
        )
        pyglet.gl.glBindTexture(self.tex.target, 0)
        
        if shader: shader.unbind()            
        if fb: fb.unbind()