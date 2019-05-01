import cv2
import numpy as np

# Assignment code
def gradient_x(image):

    # Should the x and y just be 1 and 0?
    gradient = cv2.Sobel(image, -1, 1, 0, scale=1.0/8, ksize=3)
    return gradient


def gradient_y(image):

    gradient = cv2.Sobel(image, -1, 0, 1, scale=1.0/8, ksize=3)
    return gradient

def optic_flow_lk(img_a, img_b, k_size, k_type, sigma=1):

    gxa = gradient_x(img_a)
    gya = gradient_y(img_a)
    gxb = gradient_x(img_b)
    gyb = gradient_y(img_b)

    #So we don't use gxb or gyb?
    Ix = gxa
    Iy = gya
    It = img_b - img_a

    #This next part assumes this matrix:
    #[ A  B ]
    #[ C  D ]
    #and we will find the inverse as 1/(ad-bc) times:
    #[ D -C ]
    #[-B  A ]
    if k_type is 'gaussian':
        kernel = cv2.getGaussianKernel(k_size, sigma).transpose() * cv2.getGaussianKernel(k_size, sigma)
        # kernel = cv2.getGaussianKernel(k_size, sigma)
    else:
        kernel = np.ones((k_size,k_size))/float(k_size*k_size)
    a = cv2.filter2D(Ix * Ix, -1, kernel)
    bc = cv2.filter2D(Ix * Iy, -1, kernel)
    d = cv2.filter2D(Iy * Iy, -1, kernel)
    rightUpper = -1 * cv2.filter2D(Ix * It, -1, kernel)
    rightLower = -1 * cv2.filter2D(Iy * It, -1, kernel)

    det = a*d - bc*bc
    det[det < .001] = .001
    # det[det < .0000001] = .0000001

    u = (d*rightUpper - bc*rightLower)/det
    v = (-1 * bc*rightUpper + a*rightLower)/det

    # u = np.nan_to_num(u)
    # v = np.nan_to_num(v)
    # return u*255, v*255

    u[u == np.inf] = 0
    v[v == -np.inf] = 0
    u[u == -np.inf] = 0
    v[v == np.inf] = 0
    np.nan_to_num(u, False)
    np.nan_to_num(v, False)
    # threshold = 100
    # u[(u < threshold) & (u > -threshold)] = 0
    # v[(v < threshold) & (v > -threshold)] = 0
    return u,v



def hierarchical_lk(img_a, img_b, levels, k_size, k_type, sigma, interpolation,
                    border_mode):

    gausA = gaussian_pyramid(img_a, levels)
    gausB = gaussian_pyramid(img_b, levels)

    u = np.zeros(gausA[-1].shape)
    v = np.zeros(gausB[-1].shape)
    for i in range(levels, 0, -1):
        if (i < levels):
            u = expand_image(u)*2.0
            v = expand_image(v)*2.0

            #u width check
            if not u.shape[1] == gausA[i-1].shape[1]:
                u = u[:, int((u.shape[1]-gausA[i-1].shape[1])/2) : int((u.shape[1]+gausA[i-1].shape[1])/2)]

            #u height check
            if not u.shape[0] == gausA[i-1].shape[0]:
                u = u[int((u.shape[0]-gausA[i-1].shape[0])/2) : int((u.shape[0]+gausA[i-1].shape[0])/2), :]

            # v width check
            if not v.shape[1] == gausA[i-1].shape[1]:
                v = v[:, int((v.shape[1] - gausA[i-1].shape[1]) / 2): int((v.shape[1] + gausA[i-1].shape[1]) / 2)]

            # v height check
            if not v.shape[0] == gausA[i-1].shape[0]:
                v = v[int((v.shape[0]-gausA[i-1].shape[0])/2) : int((v.shape[0]+gausA[i-1].shape[0])/2), :]

        warped = warp(gausB[i - 1], u, v, interpolation, border_mode)

        #du and dv make this seem like calculus.
        du, dv = optic_flow_lk(gausA[i-1], warped, k_size, k_type, sigma)
        u = u + du
        v = v + dv

    # threshold = 100
    # u[(u < threshold) & (u > -threshold)] = 0
    # v[(v < threshold) & (v > -threshold)] = 0
    return u, v



def expand_image(image):

    kernel = np.array([[1,4,6,4,1]])/8.0
    kernel = np.dot(kernel.transpose(),kernel)

    newImg = np.zeros((np.shape(image)[0]*2, np.shape(image)[1]*2))
    newImg[::2, ::2] = image

    exp = cv2.filter2D(newImg, -1, kernel)

    return exp


def laplacian_pyramid(g_pyr):

    lplPyramid = []
    expandedGuassians = []
    for i in range(len(g_pyr)-1):
        expandedGuassians.append(expand_image(g_pyr[i+1]))
    for i in range(len(expandedGuassians)):
        expandedGuassians[i] = expandedGuassians[i][0:g_pyr[i].shape[0],0:g_pyr[i].shape[1]]
        lplPyramid.append(g_pyr[i] - expandedGuassians[i])
    lplPyramid.append(g_pyr[-1])

    return lplPyramid




def warp(image, U, V, interpolation, border_mode):


    mapX, mapY = np.meshgrid(range(np.shape(image)[1]), range(np.shape(image)[0]))
    mapX = np.asarray(U + mapX).astype(np.float32)
    mapY = np.asarray(V + mapY).astype(np.float32)

    warped  = cv2.remap(image, mapX, mapY, interpolation, None, border_mode)
    return warped



def gaussian_pyramid(image, levels):

    images = [image]
    for level in range(levels-1):
        image = images[-1]
        newImage = reduce_image(image)
        images.append(newImage)
    return images



def reduce_image(image):

    imgShape = image.shape
    newShape = (np.ceil(imgShape[0]/2), np.ceil(imgShape[1]/2))
    # newImage = np.zeros(newShape)

    kernel = np.array([[1, 4, 6, 4, 1]]) / 16.0
    kernel = kernel.transpose() * kernel
    blurred = cv2.filter2D(image, -1, kernel)

    newImage = blurred[::2,::2]
    return newImage
