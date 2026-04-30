class Camera:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.viewport_width = 1
        self.viewport_height = 1

    def set_to_center(
        self,
        render_grid_width: int,
        render_grid_height: int,
        x_scale: int,
        y_scale: int,
    ) -> None:
        viewport_render_width = max(self.viewport_width // x_scale, 1)
        viewport_render_height = max(self.viewport_height // y_scale, 1)

        self.x = max((render_grid_width - viewport_render_width) // 2, 0)
        self.y = max((render_grid_height - viewport_render_height) // 2, 0)

    def move_up(self, step: int = 1) -> None:
        self.y = max(self.y - step, 0)

    def move_down(self, step: int = 1) -> None:
        self.y += step

    def move_left(self, step: int = 1) -> None:
        self.x = max(self.x - step, 0)

    def move_right(self, step: int = 1) -> None:
        self.x += step
