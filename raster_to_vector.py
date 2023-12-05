import matplotlib.pyplot as plt
from skimage import io, color, measure
import numpy as np

# Load the raster image of the parking lot (masked_image.jpg)
image_path = 'image_1051403817.jpg'
image_array = io.imread(image_path)
image_gray = color.rgb2gray(image_array)

# Create a mask to identify the black parts (assuming black is the area to trace)
mask = (image_gray < 0.1)  # Modify the threshold as needed

# Apply the mask to the grayscale image
masked_image = np.where(mask, 1, 0)

# Invert the mask to trace the edges
inverted_mask = np.invert(mask)

# Contour detection using skimage's `find_contours` function on the inverted mask
contours = measure.find_contours(inverted_mask, 0.8)

# Find the contour with the largest area
largest_contour = max(contours, key=len)

# Function to find points with higher curvature (edge points)
def find_edge_points(contour, num_points):
    edge_indices = np.linspace(0, len(contour) - 1, num_points, dtype=int)
    return contour[edge_indices].astype(int)

# Function to find intersection points of a line with a polygon
def find_intersection_points(poly, line):
    intersections = []
    for i in range(len(poly) - 1):
        for j in range(len(line) - 1):
            x1, y1 = poly[i]
            x2, y2 = poly[i + 1]
            x3, y3 = line[j]
            x4, y4 = line[j + 1]
            denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denominator != 0:
                px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
                py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
                if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
                    intersections.append((px, py))
    return np.array(intersections)

# Create a figure and axis for plotting
fig, ax = plt.subplots()

# Display the grayscale image with inverted mask
ax.imshow(image_gray, cmap='gray')

# Extract 10 edge points from the largest contour
edge_points = find_edge_points(largest_contour, 10)

# Plot the edges of the largest contour
ax.plot(largest_contour[:, 1], largest_contour[:, 0], color='blue')

# Plot the sampled edge points (dots) only on the edge of the shape
ax.scatter(edge_points[:, 1], edge_points[:, 0], color='red', s=10)

# Create a straight line from the first to the last edge point
start_point = edge_points[0]
end_point = edge_points[-1]
straight_line = np.array([start_point, end_point])

# Find intersection points between the straight line and the contour
intersections = find_intersection_points(largest_contour, straight_line)
ax.scatter(intersections[:, 1], intersections[:, 0], color='red', s=30, marker='x')

# Print the coordinates of the intersection points
print("Coordinates of the intersection points:")
for point in intersections:
    print(point)

# Show the plot
plt.show()
