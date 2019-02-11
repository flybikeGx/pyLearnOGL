import glfw
import moderngl as mg
import numpy

width = 800
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
    ctx = mg.create_context(require=410)

    # 主循环
    while not glfw.window_should_close(window):
        process_input(window)

        ctx.viewport = (0, 0, width, height)  # 这个就是glViewport()，设置opengl的窗口大小，不设置其实也无所谓
        ctx.clear(0.2, 0.3, 0.3, 1.0)
        glfw.poll_events()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
