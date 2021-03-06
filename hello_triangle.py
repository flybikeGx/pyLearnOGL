import glfw
import moderngl as mg
from OpenGL.GL import *
import numpy

width = 800
height = 600


def resize_callback(window, w, h):
    global width
    global height
    width = w
    height = h


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    window = glfw.create_window(width, height, "Hello Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize_callback)
    ctx = mg.create_context(require=410)

    print(glGetIntegerv(GL_MAX_VERTEX_ATTRIBS))

    # 顶点数组
    vertices = numpy.array([
        0.5, 0.5, 0.0,
        0.5, -0.5, 0.0,
        - 0.5, -0.5, 0.0,
        - 0.5, 0.5, 0.0
    ], dtype='f4')

    # 建立vbo
    vbo = ctx.buffer(vertices.tobytes())

    # 顶点index
    indice = numpy.array([
        0, 1, 3,
        1, 2, 3
    ], dtype='u4')
    ebo = ctx.buffer(indice.tobytes())

    # 这是shader
    vert = '''
#version 410 core

layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
}
'''

    frag = '''
#version 410 core
out vec4 color;

void main()
{
    color = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
'''
    # 编译shader
    program = ctx.program(vertex_shader=vert, fragment_shader=frag)

    # 建立vao
    vao = ctx.simple_vertex_array(program, vbo, 'position', index_buffer=ebo)

    while not glfw.window_should_close(window):
        process_input(window)

        ctx.viewport = (0, 0, width, height)
        ctx.clear(0.2, 0.3, 0.3, 1.0)

        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # 渲染
        vao.render()

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
