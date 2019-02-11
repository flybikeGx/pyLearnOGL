import math

import glfw
import moderngl as mg
import numpy

width = 800
height = 600


# 当窗口大小改变，调用这个函数
def resize_callback(window, w, h):
    width = w
    height = h


# 处理输入
def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main():
    # 以下初始化glfw和窗口
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    # 新建窗口
    window = glfw.create_window(width, height, "Hello Window", None, None)
    if not window:
        glfw.terminate()
        return

    # 设置context
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize_callback)
    ctx = mg.create_context(require=410)

    # 顶点数组
    vertices = numpy.array([
        0.5, -0.5, 0.0,
        -0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ], dtype='f4')

    # 建立vbo
    vbo = ctx.buffer(vertices.tobytes())

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

uniform vec4 ourColor;

void main()
{
    color = ourColor;
}
'''
    # 编译shader
    program = ctx.program(vertex_shader=vert, fragment_shader=frag)

    # 建立vao
    vao = ctx.simple_vertex_array(program, vbo, 'position')

    while not glfw.window_should_close(window):
        process_input(window)

        ctx.viewport = (0, 0, width, height)
        ctx.clear(0.2, 0.3, 0.3, 1.0)

        time = glfw.get_time()
        green = math.sin(time) / 2.0 + 0.5

        program['ourColor'].write(numpy.array([0.0, green, 0.0, 1.0], dtype='f4').tobytes())

        vao.render()

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
