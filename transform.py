import math

import moderngl
import numpy
import numpy.matlib
import glfw
import mat

width = 600
height = 600


# 当窗口大小改变，调用这个函数
def resize_callback(window, w, h):
    global width
    global height
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
    ctx = moderngl.create_context(require=410)

    # 顶点数组
    vertices = numpy.array([
        0, 0, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ], dtype='f4')

    # 建立vbo
    vbo = ctx.buffer(vertices.tobytes())

    # 顶点index
    indice = numpy.array([
        0, 1, 2
    ], dtype='u4')
    ebo = ctx.buffer(indice.tobytes())

    # 读取shader
    f = open('shaders/transform.vert')
    vert = f.read()
    f.close()

    f = open('shaders/orange.frag')
    frag = f.read()
    f.close()

    # 编译shader
    program = ctx.program(vertex_shader=vert, fragment_shader=frag)

    angle = 0

    # 建立vao
    vao = ctx.simple_vertex_array(program, vbo, 'aPos', index_buffer=ebo)

    # 主循环
    while not glfw.window_should_close(window):
        process_input(window)

        ctx.viewport = (0, 0, width, height)  # 这个就是glViewport()，设置opengl的窗口大小，不设置其实也无所谓
        ctx.clear(0.2, 0.3, 0.3, 1.0)

        angle += math.pi / 180

        trans = mat.rotate(angle, 0, 0, 1)
        program['transform'].write(trans.tobytes())

        vao.render()

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
