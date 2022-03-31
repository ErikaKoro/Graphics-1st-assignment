import numpy as np


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


def shade_triangle(img: list, verts2d: list, vcolors: list, shade_t: str, average_color:list):
    """
    :param img: the image that contains M x N pixels each one of it has 3 colors. It probably contains
                pre-existing triangles.
    :param verts2d: a 2 x 3 list.Each row contains the 2-d coordinates of the triangle's vertices
    :param vcolors: a 3 x 3 list.Each row contains the colors RGB for one of the vertices of the triangle.
    :param shade_t: a string that defines which filling algorithm will be implemented
    :return: Y, a list M x N x 3 that contains for all the triangle's points, their calculated colors(Ri, Gi, Bi)
    """

    # if the given shade_t argument is "flat" each triangle will obtain a unique color, which will be the average color of the triangle's vertices.
    if shade_t == "flat":
        # find average R of the vertices
        average_color[0] = (vcolors[0][0] + vcolors[1][0] + vcolors[2][0]) / 3
        #find average G of the vertices
        average_color[1] = (vcolors[0][1] + vcolors[1][1] + vcolors[2][1]) / 3
        #find average B of the vertices
        average_color[2] = (vcolors[0][2] + vcolors[1][2] + vcolors[2][2]) / 3
        return average_color
    elif shade_t == "gouraud":


if __name__ == '__main__':
    c1 = [0.1, 0.2, 0.9]
    c2 = [0.1, 0.3, 0.8]
    interpolate_color(5, 7, 6, c1, c2)
