import numpy as np
import matplotlib.image

import image_manipulation as rndr


if __name__ == '__main__':
    data = np.load('hw1.npy', allow_pickle=True)

    verts2d = data[()]['verts2d'].astype(int).tolist()
    vcolors = data[()]['vcolors'].tolist()
    faces = data[()]['faces'].tolist()
    depth = data[()]['depth'].tolist()

    img = rndr.render(verts2d, faces, vcolors, depth, "flat")

    matplotlib.image.imsave('flat.png', np.array(img), origin='upper')
