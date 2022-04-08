import numpy as np
import matplotlib.image
import time


IMAGESIZE = 512


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
    # print(value)

    return value


def bresenham(vertex1: list, vertex2: list):
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


def shade_triangle(img: list, verts2d: list, vcolors: list, shade_t: str):
    """
    :param img: the image that contains M x N pixels each one of it has 3 colors. It probably contains
                pre-existing triangles.
    :param verts2d: a 3 x 2 list.Each row contains the 2-d coordinates of the triangle's vertices
    :param vcolors: a 3 x 3 list.Each row contains the colors RGB for one of the vertices of the triangle.
    :param shade_t: a string that defines which filling algorithm will be implemented
    :return: Y, a list M x N x 3 that contains for all the triangle's points, their calculated colors(Ri, Gi, Bi)
    """

    # Call 3 times the bresenham algorithm to shape the triangle
    side1 = bresenham(verts2d[0], verts2d[1])
    side2 = bresenham(verts2d[1], verts2d[2])
    side3 = bresenham(verts2d[2], verts2d[0])

    # Bresenham returns a list of points [row, col] for all the points that shape one side
    # Sort each side according to row, from the lower value to the biggest
    # The sort is done in order to know the start and the end of the scanline
    side1 = sorted(side1, key=lambda row: row[0])
    side2 = sorted(side2, key=lambda row: row[0])
    side3 = sorted(side3, key=lambda row: row[0])

    # The average color in case flat shading needs to be done
    average_color = [0, 0, 0]
    # If the given shade_t argument is "flat" each pixel in the triangle will obtain a unique color,
    # which will be the average color of the triangle's vertices.
    if shade_t == "flat":
        # Find average R of the vertices
        average_color[0] = (vcolors[0][0] + vcolors[1][0] + vcolors[2][0]) / 3
        # Find average G of the vertices
        average_color[1] = (vcolors[0][1] + vcolors[1][1] + vcolors[2][1]) / 3
        # Find average B of the vertices
        average_color[2] = (vcolors[0][2] + vcolors[1][2] + vcolors[2][2]) / 3

        # Color each point on the triangle's sides
        for pixel in side1:
            img[pixel[1]][pixel[0]] = list(average_color)
        for pixel in side2:
            img[pixel[1]][pixel[0]] = list(average_color)
        for pixel in side3:
            img[pixel[1]][pixel[0]] = list(average_color)

    elif shade_t == "gouraud":
        # for each point in side 1, calculate its color
        for pixel in side1:
            # If the point is not a vertex, calculate its color by interpolate function
            if pixel not in verts2d:
                # If gradient > 1 reverse rows with cols
                if abs(verts2d[0][0] - verts2d[1][0]) > abs(verts2d[0][1] - verts2d[1][1]):
                    img[pixel[1]][pixel[0]] = interpolate_color(verts2d[0][0], verts2d[1][0], pixel[0], vcolors[0],
                                                                vcolors[1])
                # Else don't change them
                else:
                    img[pixel[1]][pixel[0]] = interpolate_color(verts2d[0][1], verts2d[1][1], pixel[1], vcolors[0],
                                                                vcolors[1])
            # Else if the point is a vertex its color is known from vcolors list
            else:
                # Find in verts2d array the index that contains the same coordinates as pixel
                index = verts2d.index(pixel)
                # The vcolors[index] contains the color of the vertex
                img[pixel[1]][pixel[0]] = vcolors[index]

        # Repeat the same work for the side2 as well
        for pixel in side2:
            if pixel not in verts2d:
                if abs(verts2d[1][0] - verts2d[2][0]) > abs(verts2d[1][1] - verts2d[2][1]):
                    # If gradient > 1
                    img[pixel[1]][pixel[0]] = interpolate_color(verts2d[1][0], verts2d[2][0], pixel[0], vcolors[1],
                                                                vcolors[2])
                else:
                    img[pixel[1]][pixel[0]] = interpolate_color(verts2d[1][1], verts2d[2][1], pixel[1], vcolors[1],
                                                                vcolors[2])
            else:
                index = verts2d.index(pixel)
                img[pixel[1]][pixel[0]] = vcolors[index]

        # Repeat the same work for side3 as well
        for pixel in side3:
            if pixel not in verts2d:
                if abs(verts2d[2][0] - verts2d[0][0]) > abs(verts2d[2][1] - verts2d[0][1]):
                    # If gradient > 1
                    img[pixel[1]][pixel[0]] = interpolate_color(verts2d[2][0], verts2d[0][0], pixel[0], vcolors[2],
                                                                vcolors[0])
                else:
                    img[pixel[1]][pixel[0]] = interpolate_color(verts2d[2][1], verts2d[0][1], pixel[1], vcolors[2],
                                                                vcolors[0])
            else:
                index = verts2d.index(pixel)
                img[pixel[1]][pixel[0]] = vcolors[index]
    else:
        print("I don't know this shading algorithm\n")

    # The smallest value of sides' cols is the start of scanline
    scan_start = min(side1[0][0], side2[0][0], side3[0][0])
    # The last elements(index=-1) have the biggest row values and the maximum of them is needed
    # to find where the scanline ends
    scan_end = max(side1[-1][0], side2[-1][0], side3[-1][0])

    # Find the active points(the colored)
    for scan in range(scan_start, scan_end + 1):
        # In each iteration this list will be initialized again and hold the active points per scanline
        active_points = []
        for pixel in side1:
            if pixel[0] == scan:
                active_points.append(pixel)
        for pixel in side2:
            if pixel[0] == scan:
                active_points.append(pixel)
        for pixel in side3:
            if pixel[0] == scan:
                active_points.append(pixel)

        # If a vertex is found continue to the next loop
        if len(active_points) == 1:
            continue
        else:
            # Find the minimum value of column in active points list
            min_col_active = np.array(active_points).min(axis=0)[1]

            # Find the maximum value of column in active points list
            max_col_active = np.array(active_points).max(axis=0)[1]

            # For the points between minimum and the maximum column, find the colored one and continue else shade them
            for i in range(min_col_active + 1, max_col_active):
                if [i, scan] in active_points:
                    continue
                else:
                    if shade_t == "flat":
                        img[i][scan] = list(average_color)
                    elif shade_t == "gouraud":
                        img[i][scan] = interpolate_color(min_col_active, max_col_active, i,
                                                         img[min_col_active][scan], img[max_col_active][scan])


def render(verts2d: list, faces: list, vcolors: list, depth: list, shade_t: str):
    """
    :param verts2d: The list with the triangles' vertices
    :param faces:   The list with the K-colored triangles' vertices
    :param vcolors:  The L x 3 list with the vertices' colors
    :param depth:    The L x 1 list with each vertex's depth
    :param shade_t:  string that defines the shading method
    :return:
    """

    # Initialize the image
    image = [[[1.0 for i in range(3)] for j in range(512)] for k in range(512)]

    triangle_colors = []
    depths_of_triangles = []
    for triangle in faces:
        # Search in faces which index has the triangle
        index = faces.index(triangle)
        # Store in faces the coordinates of each triangle's vertices
        faces[index] = [verts2d[triangle[0]], verts2d[triangle[1]], verts2d[triangle[2]]]

        # Calculate the depth of the triangle that is shaped by the current vertices
        new_depth = (depth[triangle[0]] + depth[triangle[1]] + depth[triangle[2]]) / 3
        triangle_colors.append([vcolors[triangle[0]], vcolors[triangle[1]], vcolors[triangle[2]]])
        depths_of_triangles.append(new_depth)

    # Sort the depths from smaller to bigger to smaller
    depths_of_triangles, faces, triangle_colors = zip(
        *sorted(zip(depths_of_triangles, faces, triangle_colors), key=lambda x: -x[0]))

    for triangle in faces:
        shade_triangle(image, triangle, triangle_colors[faces.index(triangle)], shade_t)

    return image
