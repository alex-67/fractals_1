import tkinter
from math import *


def scale(points_, scalefactor):
    points = points_.copy()
    for i in range(len(points)):
        points[i] = points[i] * scalefactor
    return points


def rotate(points_, angle):
    points = points_.copy()
    for i in range(0, len(points) - 1, 2):
        p_ = points[i]
        points[i] = points[i] * cos(angle) + points[i + 1] * sin(angle)
        points[i + 1] = -p_ * sin(angle) + points[i + 1] * cos(angle)
    return points


def translate(points_, dx, dy):
    points = points_.copy()
    for i in range(0, len(points) - 1, 2):
        points[i] = points[i] + dx
        points[i + 1] = points[i + 1] + dy
    return points


def translate_to_point(points_, x, y):
    return translate(points_, x - points_[0], y - points_[1])


def get_length(points):
    return sqrt(pow(points[0] - points[len(points) - 2], 2) + pow(points[1] - points[len(points) - 1], 2))


def get_scale_factor(points1, points2):
    return get_length(points1) / get_length(points2)


def rotate_by_line(x1, x2, y1, y2, points):
    """Поворачивает фигуру с координатами points паралельно линии x1, x2, y1, y2"""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0:
        newPoints = rotate(points, -atan2(dy, dx))
    elif dy == 0:
        newPoints = rotate(points, atan2(dy, dx))
    else:
        angle = -atan(dy / dx)
        if (dx < 0 and dy < 0) or (dx < 0 and dy > 0):
            angle = -pi + angle
        newPoints = rotate(points, angle)
    return newPoints


def scale_down_generator(segment, generator):
    """Уменьшает генератор в соответствии с длиной отрезка segment"""
    generator_copy = generator.copy()
    if generator[0] == generator[len(generator) - 2] and generator[1] == generator[len(generator) - 1]:
        generator_copy.pop()
        generator_copy.pop()
    scalefactor = get_scale_factor(segment, generator_copy)
    return translate_to_point(scale(generator_copy, scalefactor), 0, 0)

def get_fractal(initiator, generator, iterations):
    """Вычисляет фрактал и выдает координаты его точек"""
    l = get_length(initiator[0:4])
    limit, fractal_part = 4, []
    condition = l > limit and l < max(can.winfo_reqwidth(), can.winfo_reqheight()) and iterations != 0
    if condition:
        for i in range(0, len(initiator), 2):
            if i < len(initiator) - 3:
                scaled_generator = scale_down_generator(initiator[i:i + 4], generator)
                rotated_generator = rotate_by_line(initiator[i], initiator[i + 2], initiator[i + 1], initiator[i + 3],
                                                   scaled_generator)
                new_initiator = translate_to_point(rotated_generator, initiator[i], initiator[i + 1])
                fractal_part.append(get_fractal(new_initiator, generator, iterations - 1))
    else:
        return initiator
    return fractal_part


a = 100
l_min = 7
dx, dy = 30, -10
triangle = [0, 0, a, 0, 0.5 * a, -a / 2 * sqrt(3), 0, 0]
triangle = translate_to_point(triangle, 20, a + 30)
square = [0, 0, a, 0, a, -a, 0, -a, 0, 0]
square = translate_to_point(square, 30, a + 20)
line_0 = [0, 0, a * 1.3, 0]
line_0 = translate_to_point(line_0, 30, 100)
Koch_snowflake = [0, 0, a, 0, 1.5 * a, a * sqrt(3) / 2, 2 * a, 0, 3 * a, 0]
Koch_snowflake = translate(Koch_snowflake, 10, 10)
Koch_curve1 = [0, 0, a, 0, a, -a, 2 * a, -a, 2 * a, 0, 3 * a, 0]
Koch_curve1 = translate(Koch_curve1, 30, a + 10)
minkowski_sausage = [0, 0, 2 / sqrt(5) * a, a / sqrt(5), 3 * a / sqrt(5), -a / sqrt(5), a * sqrt(5), 0]
minkowski_sausage = translate(minkowski_sausage, 30, a / sqrt(5) + 20)
a = 50
Koch_curve2 = [0, 0, a, 0, a, a, 2 * a, a, 2 * a, 0, 2 * a, -a, 3 * a, -a, 3 * a, 0, 4 * a, 0]
Koch_curve2 = translate(Koch_curve2, 30, a + 10)
generator, initiator = [], []


def on_button_draw(event):
    global generator
    generator_copy = generator.copy()
    if len(generator_copy) != 0:
        generator_copy = rotate(translate_to_point(generator_copy, 0, 0),
                                atan2(generator_copy[len(generator_copy) - 1] - generator_copy[1],
                                      generator_copy[len(generator_copy) - 2] - generator_copy[0]))
    if len(lb.curselection()) != 0:
        index = int(lb.curselection()[0])
        if index == 4:
            other_fractal([0, 0, 600, 0, 300.0, 550.0127018922193], 'blue', 'red', triangle_fractal)
        elif index == 5:
            other_fractal([0, 0, 0, 500, 500, 500, 500, 0], 'blue', 'red', square_fractal)
        else:
            segment = [0, 0]
            segment.append(can_generator.winfo_reqwidth())
            segment.append(0)
            figure = scale(initiator, can.winfo_reqwidth() / can_initiator.winfo_reqwidth())
            can_initiator.create_line(initiator, fill="red", width=4)
            can_generator.create_line(generator, fill="blue", width=4)
            can.create_line(get_fractal(figure, generator_copy, scale_iterations.get()), fill="blue",
                            width=scale_width.get())
    elif len(initiator)!=0:
        can_initiator.create_line(initiator, fill="red", width=4)
        can_generator.create_line(generator, fill="blue", width=4)
        figure = scale(initiator, can.winfo_reqwidth() / can_initiator.winfo_reqwidth())
        can.create_line(get_fractal(figure, generator_copy, scale_iterations.get()), fill="blue",
                        width=scale_width.get())


def on_initiator_canvas(event):
    r, x, y = 5, event.x - event.x % 10, event.y - event.y % 10
    var.set('x={0};y={1}'.format(x, y))
    initiator.append(x)
    initiator.append(y)
    draw_points(initiator, can_initiator, r)
    if len(initiator) > 2:
        can_initiator.create_line(initiator, fill="red", width=4)


def on_generator_canvas(event):
    r, x, y = 5, event.x - event.x % 10, event.y - event.y % 10
    can_generator.create_oval(x - r, y - r, x + r, y + r, fill="black")
    var.set('x={0};y={1}'.format(x, y))
    generator.append(x)
    generator.append(y)
    draw_points(generator, can_generator, r)
    if len(generator) > 2:
        can_generator.create_line(generator, fill="blue", width=4)


def draw_points(points, canvas, r):
    for i in range(0, len(points) - 1, 2):
        x, y = points[i], points[i + 1]
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")


def on_canvas_move(event):
    w = event.widget
    r, x, y = 5, event.x - event.x % 10, event.y - event.y % 10
    w.delete('all')
    if w.winfo_name() == "generator":
        p = generator
        color = 'blue'
    elif w.winfo_name() == "initiator":
        p = initiator
        color = 'red'
    if len(p) > 2:
        w.create_line(p, fill=color, width=4)
    draw_points(p, w, 5)
    var.set('x={0};y={1}'.format(event.x - event.x % 10, event.y - event.y % 10))
    w.create_oval(x - r, y - r, x + r, y + r, fill="black")


def on_button_clear(event):
    can.delete("all")
    can_generator.delete("all")
    can_initiator.delete("all")
    lb.selection_clear(0, lb.size())
    generator.clear()
    initiator.clear()


def on_select(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    #on_button_clear(evt)
    global initiator, generator
    if index == 3:
        initiator = square.copy()
        generator = minkowski_sausage.copy()
    elif index == 1:
        initiator = line_0.copy()
        generator = Koch_curve1.copy()
    elif index == 2:
        initiator = line_0.copy()
        generator = Koch_curve2.copy()
    elif index == 0:
        initiator = triangle.copy()
        generator = Koch_snowflake.copy()
    if len(generator) != 0:
        can_initiator.delete('all')
        can_generator.delete('all')
        can_initiator.create_line(initiator, fill="red", width=4)
        can_generator.create_line(generator, fill="blue", width=4)
        draw_points(generator, can_generator, 5)
        draw_points(initiator, can_initiator, 5)


def new_coordinat(triangle, i, j, k):
    """Для построения треугольника Серпинского"""
    return triangle[i] + (triangle[j] - triangle[k]) / 2


def triangle_fractal(triangle, fractal):
    """Для построения треугольника Серпинского"""
    l = get_length(triangle)
    if l > l_min:
        triangel_c = [new_coordinat(triangle, 0, 2, 0), new_coordinat(triangle, 1, 3, 1),
                      new_coordinat(triangle, 2, 4, 2), new_coordinat(triangle, 3, 5, 3),
                      new_coordinat(triangle, 0, 4, 0), new_coordinat(triangle, 1, 5, 1)]
        p_n1x = triangle[0] + (triangle[2] - triangle[0]) / 2
        p_n1y = triangle[1] + (triangle[3] - triangle[1]) / 2
        p_n2x = triangle[2] + (triangle[4] - triangle[2]) / 2
        p_n2y = triangle[3] + (triangle[5] - triangle[3]) / 2
        p_n3x = triangle[0] + (triangle[4] - triangle[0]) / 2
        p_n3y = triangle[1] + (triangle[5] - triangle[1]) / 2
        triangle1 = [triangle[0], triangle[1], p_n1x, p_n1y, p_n3x, p_n3y]
        triangle2 = [p_n1x, p_n1y, triangle[2], triangle[3], p_n2x, p_n2y]
        triangle3 = [p_n3x, p_n3y, p_n2x, p_n2y, triangle[4], triangle[5]]
        fractal.append(triangel_c)
        triangle_fractal(triangle1, fractal)
        triangle_fractal(triangle2, fractal)
        triangle_fractal(triangle3, fractal)


def new_square(x, y, l):
    """Для построения ковра Серпинского"""
    return [[x, y, x, y + l / 3, x + l / 3, y + l / 3, x + l / 3, y]]


def square_fractal(square, fractal):
    """Для построения ковра Серпинского"""
    l = get_length(square[0:4])
    if l > l_min:
        p1, squares = square[0:2], []
        square_central = [p1[0] + l / 3, p1[1] + l / 3, p1[0] + l / 3, p1[1] + 2 * l / 3, p1[0] + 2 * l / 3,
                          p1[1] + 2 * l / 3, p1[0] + 2 * l / 3, p1[1] + l / 3]
        squares += new_square(p1[0], p1[1], l) + new_square(p1[0], p1[1] + l / 3, l) + new_square(p1[0],
                                                                                                  p1[1] + 2 * l / 3,
                                                                                                  l) + new_square(
            p1[0] + l / 3, p1[1] + 2 * l / 3, l) + new_square(p1[0] + 2 * l / 3, p1[1] + 2 * l / 3, l) + new_square(
            p1[0] + 2 * l / 3, p1[1] + l / 3, l) + new_square(p1[0] + l / 3, p1[1], l) + new_square(p1[0] + 2 * l / 3,
                                                                                                    p1[1], l)
        fractal.append(square_central)
        for square_ in squares:
            square_fractal(square_, fractal)


def other_fractal(figure, color1, color2, f):
    """Рисование figure"""
    can.create_polygon(figure, fill=color1)
    fractal = []
    f(figure, fractal)
    for item in fractal:
        can.create_polygon(item, fill=color2)


root = tkinter.Tk()
root.geometry('1200x700+0+0')
can = tkinter.Canvas(root, width=800, height=700, bd=10, bg="white")
can.pack(side=tkinter.LEFT)
root.update()
frame1 = tkinter.Frame(root, width=200, height=700)
frame2 = tkinter.Frame(frame1, width=frame1.winfo_reqwidth())
lb = tkinter.Listbox(frame1, name='lb', height=6)
lb.insert(tkinter.END, 'Снежинка Коха')
lb.insert(tkinter.END, 'Кривая Коха 1')
lb.insert(tkinter.END, 'Кривая Коха 2')
lb.insert(tkinter.END, 'Фрактал Минковского')
lb.insert(tkinter.END, 'Треугольник Серпинского')
lb.insert(tkinter.END, 'Ковёр Серпинского')
lb.pack(fill='x')
lb.bind('<<ListboxSelect>>', on_select)
label_iterations = tkinter.Label(frame1, text='Количество итераций')
label_generator = tkinter.Label(frame1, text='Укажите генератор')
label_initiator = tkinter.Label(frame1, text='Укажите инициатор')
scale_iterations = tkinter.Scale(frame1, orient=tkinter.HORIZONTAL, length=200, from_=1, to=20, resolution=1)
label_thickness = tkinter.Label(frame1, text='Толщина линии')
scale_width = tkinter.Scale(frame1, orient=tkinter.HORIZONTAL, length=200, from_=1, to=20, resolution=1)
btn = tkinter.Button(frame1, text='Построить')
btn_clear = tkinter.Button(frame1, text='Очистить')
drawGenerator = tkinter.IntVar()
var = tkinter.StringVar()
label = tkinter.Label(frame1, textvariable=var)
label_iterations.pack(fill='x')
scale_iterations.pack(fill='x')
label_initiator.pack(fill='x')
can_initiator = tkinter.Canvas(frame1, name='initiator', width=frame1.winfo_reqwidth(), height=150, bg="white")
can_initiator.pack(fill='x')
label_generator.pack(fill='x')
can_generator = tkinter.Canvas(frame1, name='generator', width=frame1.winfo_reqwidth(), height=150, bg="white")
can_generator.pack(fill='x')
frame2.pack(fill='x')
label.pack(fill='x')
label_thickness.pack(fill='x')
scale_width.pack(fill='x')
btn.pack(fill='x')
btn_clear.pack(fill='x')
frame1.pack(side='top', fill='x')
btn.bind('<Button-1>', on_button_draw)
can_initiator.bind('<Button-1>', on_initiator_canvas)
can_generator.bind('<Button-1>', on_generator_canvas)
can_generator.bind('<Motion>', on_canvas_move)
can_initiator.bind('<Motion>', on_canvas_move)
btn_clear.bind('<Button-1>', on_button_clear)
drawGenerator.set(0)
tkinter.mainloop()






