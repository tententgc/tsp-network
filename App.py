import math


def tsp_nn(points):
    # Start at a random point
    current_point = points[0]
    unvisited_points = set(points)
    unvisited_points.remove(current_point)
    tour = [current_point]

    while unvisited_points:
        next_point = None
        next_point_distance = math.inf
        for point in unvisited_points:
            distance = math.sqrt(
                (current_point[0] - point[0]) ** 2 + (current_point[1] - point[1]) ** 2)
            if distance < next_point_distance:
                next_point = point
                next_point_distance = distance
        current_point = next_point
        unvisited_points.remove(current_point)
        tour.append(current_point)

    return tour


points = [(1,3), (1, 1), (2, 2), (3, 3), (4, 4)]
print(tsp_nn(points))
