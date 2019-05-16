#!/usr/bin/env python3

import math
import re

import cairo
from gi.repository import GObject
from gi.repository import Gtk, Gdk
from gi.repository import Pango
from gi.repository import PangoCairo

import config


class KaraokeLyric(Gtk.Window, object):

    def __init__(self):
        super(KaraokeLyric, self).__init__()

        # 加载配置
        self.config = {}
        self.config['locked'] = False
        self.config['stroke_outline'] = True
        self.config['double_line'] = False
        self.config['karaoke'] = True
        self.config['font'] = ('WenQuanYi Micro Hei,Normal 28')
        self.config['font-color'] = [0.8, 0.3, 0.1, 1.0]
        self.config['played-color'] = [0.2, 0.5, 0.9, 1.0]
        self.config['outline_color'] = [0.7, 0.2, 0.1, 1.0]
        self.config['lrc-encoding'] = 'gb18030'
        self.config['interval'] = 250
        self.config['x-padding'] = 20
        self.config['y-padding'] = 20
        self.config['size'] = [800, 80]
        self.config['min-size'] = [400, 80]
        # 歌词窗口总在最前
        self.set_keep_above(True)
        # 不需要窗口装饰器
        self.set_decorated(False)
        # 直接在窗口内绘图
        self.set_app_paintable(True)
        # 窗口透明
        #self.set_opacity(0.0)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual is not None and screen.is_composited():
            self.set_visual(visual)
        self.resize(*self.config['size'])

        # 悬浮按钮栏图标
        self.toolbar = self.init_toolbar()
        # 连接信号
        # 添加鼠标移动事件监听
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        # 添加鼠标点击/释放，进入/离开窗口事件监听
        self.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect('button-press-event', self.on_button_press)
        self.connect('button-release-event', self.on_button_release)
        self.connect('motion-notify-event', self.on_poniter_motion)
        self.connect('enter-notify-event', self.on_pointer_enter)
        self.connect('leave-notify-event', self.on_pointer_leave)
        self.connect("destroy", Gtk.main_quit)
        self.connect("draw", self.on_draw)

        # 初始化状态信息
        self.lrc_obj = None
        self.status = {}
        self.status['time'] = 0
        #self.status['text1'] = 250
        self.status['play-status'] = 'stop'
        self.status['move-resize'] = ''
        self.status['show-bg'] = False
        #self.status['old-root-x'] = 0
        #self.status['old-root-y'] = 0
        #self.status['old-x'] = 0
        #self.status['old-y'] = 0

        self.set_position(Gtk.WindowPosition.CENTER)
        # test code
        if True:
            self.txt = ''
            self.txt = "天王盖地虎，小鸡炖蘑菇\t宝塔镇河妖，蘑菇放辣椒"
            self.pos = [0.0, 0.2, 0.5, 0.9, 1.0]
            self.pos2 = [0.0, 0.2, 0.5, 0.9, 1.0]
            self.pos3 = [0.0, 0.8, 0.3, 0.1, 1.0]
            self.pos4 = [1.0, 0.8, 0.3, 0.1, 1.0]

        self.show_all()

    def parse_lrc(self, lrc_text):
        lrc_obj = {}
        lrc_obj['offset'] = 0
        lrc_obj['ti'] = ''
        lrc_obj['ar'] = ''
        lrc_obj['al'] = ''
        lrc_obj['content'] = []

        lbl_reg = re.compile('\[(offset|ti|ar|al):(.+?)\]')
        time_reg = re.compile('\[(\d{1,3}):(\d{2})([.:]\d{1,3})?\]')
        for line in lrc_text.splitlines():
            match = lbl_reg.match(line)
            if match is not None:
                lbl_name, lbl_content = match.groups()
                if lbl_name == 'ti':  # title
                    lrc_obj['ti'] = lbl_content
                elif lbl_name == 'ar':  # artist
                    lrc_obj['ar'] = lbl_content
                elif lbl_name == 'al':  # album
                    lrc_obj['al'] = lbl_content
                elif lbl_name == 'offset':
                    lrc_obj['offset'] = int(lbl_content)
                continue
            match = time_reg.match(line)
            time_tags = []
            while match:
                match_offset = match.end()
                m, s, ms = match.groups()
                if ms is None:
                    ms = 0
                else:
                    # 毫秒可以为小数？
                    ms = float(ms[1:])
                content_time = int(m) * 60 + int(s)
                content_time = content_time * 1000 + ms
                time_tags.append(content_time)
                match = time_reg.match(line, match_offset)

            if len(time_tags) > 0:
                content = line[match_offset:].strip()
                for tag in time_tags:
                    lrc_obj['content'].append((tag, content))
            lrc_obj['content'].sort()
        return lrc_obj

    def load_lrc_buf(self, buf):
        self.lrc_obj = self.parse_lrc(f.read())

    def load_lrc_file(self, filename, encoding=config.configs['lrc-encoding']):
        with open(filename, encoding=encoding) as f:
            self.lrc_obj = self.parse_lrc(f.read())

    def pop_menu(self, widget):
        print('Popup menu not implemented yet')
        pass

    def init_toolbar(self):
        toolbar = Gtk.Window(Gtk.WindowType.POPUP)
        toolbar.set_size_request(120, 30)
        # toolbar.set_app_paintable(True)
        #toolbar.set_opacity(0.3)

        hbx = Gtk.HBox(spacing=2)
        # 添加按钮到hbox
        toolbar.window_frame.pack_start(hbox)
        toolbar.add(hbox)

        #toolbar.connect('draw', self.draw_toolbar)
        return toolbar

    def draw_toolbar(self, widget, cr):
        x, y = self.toolbar.get_position()
        w, h = self.toolbar.get_size()
        cr.set_source_rgba(0.5, 0.5, 0.5, 0.3)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.rectangle(x, y, w, h)
        cr.fill()

        return True

    def show_toolbar(self):
        x, y = self.get_position()
        w, h = self.get_size()
        l_w, l_h = self.toolbar.get_size()
        m_x = x + w/2 - l_w/2
        m_y = y - l_h

        self.toolbar.move(m_x, m_y)
        self.toolbar.show_all()

    def hide_toolbar(self):
        self.toolbar.hide()

    def play(self):
        # 卡拉ok歌词定时器
        if self.lrc_obj is None:
            return
        self.txt = ''
        #self.txt = "天王盖地虎，小鸡炖蘑菇\t宝塔镇河妖，蘑菇放辣椒"
        self.pos = [0.0, 0.2, 0.5, 0.9, 1.0]
        self.pos2 = [0.0, 0.2, 0.5, 0.9, 1.0]
        self.pos3 = [0.0, 0.8, 0.3, 0.1, 1.0]
        self.pos4 = [1.0, 0.8, 0.3, 0.1, 1.0]
        GObject.timeout_add(100, self.on_animation)

    def pause(self):
        pass

    def stop(self):
        pass

    def on_animation(self):
        self.pos2[0] += 0.005
        self.pos3[0] += 0.005
        self.queue_draw()

        return True

    def on_button_press(self, widget, event):
        rect = widget.get_allocation()
        if event.button == 1:  # 鼠标左键
            self.status['old-root-x'] = event.x_root
            self.status['old-root-y'] = event.y_root
            self.status['old-x'], self.status['old-y'] = widget.get_position()
            if event.x < self.config['x-padding']:
                self.status['move-resize'] = 'resize-left'
            elif event.x > rect.width - self.config['x-padding']:
                self.status['move-resize'] = 'resize-right'
            else:
                self.status['move-resize'] = 'move'

        return True

    def on_button_release(self, widget, event):
        if event.button == 1:  # 鼠标左键
            self.status['move-resize'] = ''
        elif event.button == 3: # 鼠标右键
            # 弹出右键菜单
            self.pop_menu(widget)

        return True

    def on_poniter_motion(self, widget, event):
        '''移动桌面歌词窗口事件响应函数'''
        # 拖动歌词窗口/改变窗口宽度
        rect = widget.get_allocation()
        if event.x < self.config['x-padding'] and self.status['move-resize'] == '':
            # 设置拖动左边框的鼠标指针
            widget.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.LEFT_SIDE))
        elif event.x > rect.width - self.config['x-padding'] and \
                self.status['move-resize'] == '':
            # 设置拖动右边框的鼠标指针
            widget.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.RIGHT_SIDE))
        else:
            widget.get_window().set_cursor(None)

        if self.status['move-resize'] == 'move':
            x = self.status['old-x'] + event.x_root - self.status['old-root-x']
            y = self.status['old-y'] + event.y_root - self.status['old-root-y']
            widget.move(x, y)
        elif self.status['move-resize'] == 'resize-left':
            x_size = self.config['size'][0] + self.status['old-root-x'] - event.x_root
            x_size = max(x_size, self.config['min-size'][0])
            x_move = self.status['old-x'] + self.config['size'][0] - x_size
            widget.resize(x_size, self.config['size'][1])
            widget.move(x_move, self.status['old-y'])
            # 更改窗口配置及状态信息
            self.config['size'][0] = x_size
            self.status['old-x'] = x_move
            self.status['old-root-x'] = event.x_root
        elif self.status['move-resize'] == 'resize-right':
            x_size = self.config['size'][0] + event.x_root - self.status['old-root-x']
            x_size = max(x_size, self.config['min-size'][0])
            widget.resize(x_size, self.config['size'][1])

            # 更改窗口配置及状态信息
            self.config['size'][0] = x_size
            self.status['old-root-x'] = event.x_root

        return True

    def on_pointer_enter(self, widget, event):
        # 如果从左/右边进入窗口，则可进行拖动改变窗口大小
        if self.config['locked'] == False:
            self.status['show-bg'] = True
            self.queue_draw()
            self.show_toolbar()

        return True

    def on_pointer_leave(self, widget, event):
        # 离开窗口
        self.status['show-bg'] = False
        self.hide_toolbar()
        self.queue_draw()

        return True

    def on_draw(self, widget, cr):
        # 清空窗口上的内容。
        cr.set_operator(cairo.OPERATOR_CLEAR)
        # 浅色背景，未锁定鼠标移动到歌词窗口上时显示
        if self.status['show-bg'] == True:
            cr.set_source_rgba(0.5, 0.5, 0.5, 0.5)
        else:
            cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)

        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        if self.txt == '':
            return

        # 创建字体布局
        layout = PangoCairo.create_layout(cr)
        #ctx = layout.get_context()
        #ctx.set_base_gravity(Pango.Gravity.EAST)
        fd = Pango.FontDescription(self.config['font'])
        layout.set_font_description(fd)
        layout.set_markup(self.txt, -1)

        logic_ext, ink_ext = layout.get_pixel_extents()
        #widget.resize(logic_ext.x + logic_ext.width, logic_ext.y + logic_ext.height)
        w = logic_ext.x + logic_ext.width
        h = logic_ext.y + logic_ext.height

        cr.move_to(self.config['x-padding'], self.config['y-padding'])
        # 布局转路径
        PangoCairo.layout_path(cr, layout)

        if (self.config['stroke_outline']):
            cr.set_operator(cairo.OPERATOR_OVER)
            #cr.set_source_rgba(0.7, 0.2, 0.1, 1.0)
            cr.set_source_rgba(*self.config['outline_color'])
            # 路径描边
            cr.set_line_width(1)
            cr.stroke_preserve()

        # 路径渐变填充
        #cr.set_source_rgba(0.1, 0.2, 0.7, 1.0)
        pattern = cairo.LinearGradient(0, 0, w, h)
        pattern.add_color_stop_rgba(*self.pos)
        pattern.add_color_stop_rgba(*self.pos2)
        pattern.add_color_stop_rgba(*self.pos3)
        pattern.add_color_stop_rgba(*self.pos4)
        cr.set_source(pattern)
        cr.fill()

        return True

if __name__ == "__main__":
    import sys

    lrc = KaraokeLyric()
    if len(sys.argv) > 1:
        print(sys.argv[1])
        with open(sys.argv[1], encoding=config.configs['lrc-encoding']) as f:
            lrc.load_lrc_file(sys.argv[1])
            print('play')
            lrc.play()

    Gtk.main()
