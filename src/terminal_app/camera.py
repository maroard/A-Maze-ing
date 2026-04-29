class camera():
    def __init__(self, viewport_width: int, viewport_height: int):
        self.x: int
        self.y: int
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def set_to_center(
        self,
        viewport_width: int,
        viewport_height: int,
    ) -> None:

        render_grid_width = 2 * self.maze.width + 1
        render_grid_height = 2 * self.maze.height + 1

        viewport_width_render = max(viewport_width
                                    // self.renderer.x_scale, 1)
        viewport_height_render = max(viewport_height
                                     // self.renderer.y_scale, 1)

        self.x = max(
            (render_grid_width - viewport_width_render) // 2,
            0,
        )
        self.y = max(
            (render_grid_height - viewport_height_render) // 2,
            0,
        )

    def move_top(self):
        pass

    def move_left(self):
        pass

    def move_bottom(self):
        pass

    def move_right(self):
        pass
