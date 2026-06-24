def get_triangle_3d_offsets():
    return [
        (0, 0, 0),      # leader
        (-2, -2, 0),    # follower 1
        (-2, 2, 0),     # follower 2
    ]


def get_tetrahedron_offsets():
    return [
        (0, 0, 0),       # leader / top
        (-2, -2, -2),    # follower 1
        (-2, 2, -2),     # follower 2
        (-4, 0, 1),      # follower 3
    ]