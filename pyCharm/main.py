import numpy as np
import matplotlib.image

IMAGESIZE = 10


def interpolate_color(x1, x2, x, C1: list, C2: list):
    """
    :param x1: horizontal coordinate of an intersection point between one side of the triangle and the line of the gouraud
    :param x2: the second horizontal coordinate of an intersection point
    :param x: the horizontal coordinate of the point between x1 and x2, which interpolate-color is required
    :param C1: a list that contains the R,G,B colors of the first given point
    :param C2: a list that contains the R,G,B colors of the second given point
    :return: the value is a list that contains interpolate-colors

    The algorithm of Gouraud shading is being used in order to fill the triangle.
    According to Gouraud shading algorithm each point's color is calculated through the following type:
    C = m * C1 + (1 - m) * C2, m = (x2 - x)/(x2 - x1)
    """
    m = (x2 - x) / (x2 - x1)
    value = m * np.array(C1) + (1 - m) * np.array(C2)
    print(value)

    return value


def bresenham(vertex1: list, vertex2 :list):
    x0 = vertex1[0]
    y0 = vertex1[1]
    x1 = vertex2[0]
    y1 = vertex2[1]

    inverted = False
    x, y = x0, y0
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    if dy > dx:
        dx, dy = dy, dx
        x, y = y, x
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        inverted = True

    f = 2 * dy - dx

    coordinates = []

    if inverted:
        coordinates.append([y, x])
    else:
        coordinates.append([x, y])

    for k in range(dx):
        if f > 0:
            if y < y1:
                y = y + 1
            else:
                y = y - 1
            f = f + 2 * (dy - dx)
        else:
            f = f + 2 * dy

        if x < x1:
            x = x + 1
        else:
            x = x - 1

        if inverted:
            coordinates.append([y, x])
        else:
            coordinates.append([x, y])

    return coordinates


def shade_triangle(img: list, verts2d: list, vcolors: list, shade_t: str, average_color:list):
    """
    :param img: the image that contains M x N pixels each one of it has 3 colors. It probably contains
                pre-existing triangles.
    :param verts2d: a 3 x 2 list.Each row contains the 2-d coordinates of the triangle's vertices
    :param vcolors: a 3 x 3 list.Each row contains the colors RGB for one of the vertices of the triangle.
    :param shade_t: a string that defines which filling algorithm will be implemented
    :return: Y, a list M x N x 3 that contains for all the triangle's points, their calculated colors(Ri, Gi, Bi)
    """

    side1 = bresenham(verts2d[0], verts2d[1])
    side2 = bresenham(verts2d[1], verts2d[2])
    side3 = bresenham(verts2d[2], verts2d[0])

    # if the given shade_t argument is "flat" each pixel in the triangle will obtain a unique color,
    # which will be the average color of the triangle's vertices.
    if shade_t == "flat":
        # find average R of the vertices
        average_color[0] = (vcolors[0][0] + vcolors[1][0] + vcolors[2][0]) / 3
        # find average G of the vertices
        average_color[1] = (vcolors[0][1] + vcolors[1][1] + vcolors[2][1]) / 3
        # find average B of the vertices
        average_color[2] = (vcolors[0][2] + vcolors[1][2] + vcolors[2][2]) / 3

        for pixel in side1:
            img[pixel[0]][pixel[1]] = list(average_color)
        for pixel in side2:
            img[pixel[0]][pixel[1]] = list(average_color)
        for pixel in side3:
            img[pixel[0]][pixel[1]] = list(average_color)

    elif shade_t == "gouraud":
        for pixel in side1:
            img[pixel[0]][pixel[1]] = interpolate_color(verts2d[0][0], verts2d[1][0], pixel[0], vcolors[0], vcolors[1])
        for pixel in side2:
            img[pixel[0]][pixel[1]] = list(average_color)
        for pixel in side3:
            img[pixel[0]][pixel[1]] = list(average_color)
    else:
        print("I don't know this guy\n")


def findActivePoints(side1: list, side2: list, side3: list):
    """
    :param side1: The 1st side of the triangle calculated by bresenham
    :param side2: The 2nd side
    :param side3: The 3rd side
    :return:
    """
    # -----------FOR Ys-------------------------
    # Find the maximum y coordinate of each side
    max1 = np.array(side1).max(axis=0)[1]
    max2 = np.array(side2).max(axis=0)[1]
    max3 = np.array(side3).max(axis=0)[1]

    # Find minimum y coordinate of each side
    min1 = np.array(side1).min(axis=0)[1]
    min2 = np.array(side2).min(axis=0)[1]
    min3 = np.array(side3).min(axis=0)[1]

    # --------------FOR X-s---------------------
    # Find the maximum x coordinate of each side
    max1 = np.max(side1, axis=0)[0]
    max2 = np.max(side2, axis=0)[0]
    max3 = np.max(side3, axis=0)[0]

    # Find minimum y coordinate of each side
    min1 = np.min(side1, axis=0)[0]
    min2 = np.min(side2, axis=0)[0]
    min3 = np.min(side3, axis=0)[0]
    min_y = min(min1, min2, min3)
    max_y = max(max1, max2, max3)

    side1 = sorted(side1, key=lambda y: y[0])
    side2 = sorted(side2, key=lambda y: y[0])
    side3 = sorted(side3, key=lambda y: y[0])
    print(side1, "\n", side2, "\n", side3)

    for scan in range(min_y, max_y + 1):




    print(max1, max2, max3)
    print(min1, min2, min3)


if __name__ == '__main__':
    image = [[[1.0 for i in range(3)] for j in range(10)] for k in range(10)]

    side1 = bresenham(1, 2, 5, 1)
    side2 = bresenham(1, 2, 3, 6)
    side3 = bresenham(5, 1, 3, 6)
    print("The 1st side: ", side1)
    print("The 2nd side: ", side2)
    print("The 3rd side: ", side3)

    findActivePoints(side1, side2, side3)

    # findActivePoints(side1, side2, side3)

    for pixel1 in side1:
        image[pixel1[0]][pixel1[1]] = [0, 0, 0]
    for pixel2 in side2:
        image[pixel2[0]][pixel2[1]] = [0, 0, 0]
    for pixel3 in side3:
        image[pixel3[0]][pixel3[1]] = [0, 0, 0]
    c1 = [0.1, 0.2, 0.9]
    c2 = [0.1, 0.3, 0.8]
    interpolate_color(5, 7, 6, c1, c2)
    matplotlib.image.imsave('image.png', np.array(image), origin='lower')
