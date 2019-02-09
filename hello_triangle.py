import glfw
import moderngl as mg
import numpy

width = 800
height = 600

def resize_callback(window, w, h):
    global width
    global height
    width = w
    height = h
    
def input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def main():

    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, "Hello Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize_callback)
    ctx = mg.create_context(require=430)

    # 顶点数组
    vertices = numpy.array([
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0,  0.5, 0.0],
        dtype = 'f4')

    # 建立vbo
    vbo = ctx.buffer(vertices)

    # 这是shader
    vert = '''
#version 430 core

layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
}
'''

    frag = '''
#version 430 core
out vec4 color;

void main()
{
    color = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
'''
    # 编译shader
    program = ctx.program(vertex_shader=vert, fragment_shader=frag)
    
    # 建立vao
    vao = ctx.simple_vertex_array(program, vbo, 'position')

    while not glfw.window_should_close(window):
        input(window)

        ctx.viewport = (0,0,width,height)
        ctx.clear(0.2, 0.3, 0.3, 1.0)

        # 渲染
        vao.render()

        glfw.poll_events()

        glfw.swap_buffers(window)


    glfw.terminate()


if __name__ == '__main__':
    main()