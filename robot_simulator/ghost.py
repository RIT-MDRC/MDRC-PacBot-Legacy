from grid import *
from bot_math import Pose
from Position import Position
import math

UP = 3*math.pi/2
RIGHT = 0
DOWN = math.pi/2
LEFT = math.pi


class Ghost():

    pos: Position
    color: str

    def get_move_based_on_target(self, target: Position) -> Position:
        pass

    def get_next_scatter_move(self) -> Position:
        pass

    # This is awful. Look online to find out blue is supposed to move, and let's just work under the
    # assumption that this function returns that sort of move.
    def blue_next_target(self, pacbot_pose: Pose, red_pos: Position) -> Position:
        pacbot_target = Position(0, 0)

        if pacbot_pose.angle == UP:
            pacbot_target = Position(pacbot_pose.pos.x - 2, pacbot_pose.pos.y + 2)
        elif pacbot_pose.angle == DOWN:
            pacbot_target = Position(pacbot_pose.pos.x, pacbot_pose.pos.y - 2)
        elif pacbot_pose.angle == LEFT:
            pacbot_target = Position(pacbot_pose.pos.x - 2, pacbot_pose.pos.y)
        elif pacbot_pose.angle == RIGHT:
            pacbot_target = Position(pacbot_pose.pos.x + 2, pacbot_pose.pos.y)

        target_x = pacbot_target[0] + (pacbot_target[0] - red_pos.x)
        target_y = pacbot_target[1] + (pacbot_target[1] - red_pos.y)

        return self.get_move_based_on_target(Position(target_x, target_y))

    # Return the move closest to the space 4 tiles ahead of Pacman in the direction
    # Pacman is currently facing. If Pacman is facing up, then we replicate a bug in
    # the original game and return the move closest to the space 4 tiles above and
    # 4 tiles to the left of Pacman.
    def pink_next_target(self, pacbot_pose: Pose) -> Position:
        target = Position(0, 0)

        if pacbot_pose.angle == UP:
            target.x = pacbot_pose.pos.x - 4
            target.y = pacbot_pose.pos.y + 4
        elif pacbot_pose.angle == DOWN:
            target.x = pacbot_pose.pos.x
            target.y = pacbot_pose.pos.y - 4
        elif pacbot_pose.angle == LEFT:
            target.x = pacbot_pose.pos.x - 4
            target.y = pacbot_pose.pos.y
        elif pacbot_pose.angle == RIGHT:
            target.x = pacbot_pose.pos.x + 4
            target.y = pacbot_pose.pos.y

        return self.get_move_based_on_target(target)

    # Returns the move that will bring the ghost closest to Pacman
    def red_next_target(self, pacbot_pose: Pose) -> Position:
        return self.get_move_based_on_target(pacbot_pose.pos)

    # If the ghost is close to Pacman, return the move that will bring the ghost closest
    # to its scatter position (bottom left corner). If the ghost is far from Pacman,
    # return the move that will bring the ghost closest to Pacman.
    def orange_next_target(self, pacbot_pose: Pose) -> Position:
        if self.pos.dist(pacbot_pose.pos) < 8:
            return self.get_next_scatter_move()
        return self.get_move_based_on_target(pacbot_pose.pos)
