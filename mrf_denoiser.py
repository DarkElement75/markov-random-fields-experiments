import sys
import numpy as np

def denoise(src, class_n):
    """
    Given a src image, looks though and executes MRFs on this image,
        returning the dst image.
    """
    h, w = src.shape
    dst = np.zeros_like(src)

    costs = np.zeros((class_n))
    while(SNR(src,dst)>10):
        for i in range(h):
            sys.stdout.write("\rDenoising Image... %i%%"%(int(float(i)/h*100)))
            sys.stdout.flush()
            for j in range(w):

                """
                Get indices of neighbors
                """
                neighbors=get_neighbors(i,j,h,w)
                
                """
                Get cost of each class for this pixel in our src img
                """
                for class_i in range(class_n):
                    costs[class_i] = cost(class_i,src[i,j],src,neighbors)

                """
                Assign dst pixel to class with highest cost.
                """
                dst[i,j] = np.argmax(costs)
        #src=dst
        break
    return dst

def SNR(A,B):
        """
        Given two matrices of same size, 
        This returns the mean of the absolute value difference between a and b.
            So it's a way of measuring how different they are on the large scale.
        You could also do the squared difference, if you wished.
        """
        #return np.mean(np.abs(A-B))
        return np.sum(np.square(A-B))

def kronecker_delta(a,b):
        """
        The Kronecker Delta function is really useful, but there isn't an actual method in many libraries.
        Fortunately, it's pretty much just ~(a-b), since we want the following behavior:
            kronecker_delta(a,b) = 1 if a == b
            kronecker_delta(a,b) = 0 if a != b
        So we do this, then return the integer representation of our logical op.
        Since I use numpy it holds for scalars and also vectors/matrices.
        """
        return np.logical_not(a-b).astype(int)

def get_neighbors(i,j,h,w):
    """
    Get all adjacent neighbors, vertically, diagonally, and horizontally.
    We handle our edge cases by getting all 8 of these neighbors, then looping backwards through the list
        and removing those that aren't inside the bounds of our image.
    """
    neighbors=[(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
    for neighbor_i in range(len(neighbors)-1, -1, -1):#Iterate from len-1 to 0
        sample_i, sample_j = neighbors[neighbor_i]
        if sample_i < 0 or sample_i > h-1 or sample_j < 0 or sample_j > w-1:
            del neighbors[neighbor_i]
    return neighbors

def cost(dst_val,src_val,src,neighbors):
    """
    Our cost parameters
        Apparently when A = 10*B, dst == src
    """
    alpha=1
    beta=10

    """
    The values of the neighbor indices of our src pixel. We get these as a vector to speed up the cost computation.
    """
    neighbor_vals = np.array([src[neighbor] for neighbor in neighbors])

    """
    Compute our cost function as follows, using our neighbor value vector to compute the neighbor kronecker deltas simultaneously.
    """
    return (alpha * kronecker_delta(dst_val,src_val) + beta * np.sum(kronecker_delta(dst_val,neighbor_vals)))

#main()
