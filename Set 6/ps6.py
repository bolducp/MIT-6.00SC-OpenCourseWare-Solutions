# Problem Set 6: Simulating robots

import math
import random
import ps6_visualize
import pylab


# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        tiles = []
        for x_tile in range(width):
            for y_tile in range(height):
                tiles.append((x_tile, y_tile))

        tiles_dict = {}
        for tile in tiles:
            tiles_dict[tile] = "dirty"
        self.tiles = tiles_dict

    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = int(pos.x)
        y = int(pos.y)

        self.tiles[x, y] = "clean"


    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[m, n] == "clean"


    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.tiles.keys())


    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        clean_count = 0
        for tile in self.tiles.keys():
            if self.tiles[tile] == "clean":
                clean_count += 1
        return clean_count


    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.randrange(self.width) + round(random.random(), 2)
        y = random.randrange(self.height) + round(random.random(), 2)

        return Position(x, y)


    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.x >= 0 and pos.x <= self.width and pos.y >= 0 and pos.y <= self.height


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = self.room.getRandomPosition()
        self.direction = random.randint(0, 360)

        self.room.cleanTileAtPosition(self.position)



    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position


    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction


    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position


    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction


    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        if self.direction > 337.5 or self.direction <= 22.5:
            position = Position(self.position.x, self.position.y + 1)

        elif self.direction > 22.5 and self.direction <= 67.5:
            position = Position(self.position.x + 1, self.position.y + 1)

        elif self.direction > 67.5 and self.direction <= 112.5:
            position = Position(self.position.x + 1, self.position.y)

        elif self.direction > 112.5 and self.direction <= 157.5:
            position = Position(self.position.x + 1, self.position.y - 1)

        elif self.direction > 157.5 and self.direction <= 202.5:
            position = Position(self.position.x, self.position.y - 1)

        elif self.direction > 202.5 and self.direction <= 247.5:
            position = Position(self.position.x - 1, self.position.y - 1)

        elif self.direction > 247.5 and self.direction <= 292.5:
            position = Position(self.position.x - 1, self.position.y)

        elif self.direction > 292.5 and self.direction <= 337.5:
            position = Position(self.position.x - 1, self.position.y + 1)

        self.setRobotPosition(position)
        self.room.cleanTileAtPosition(position)


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        potential_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(potential_position):
            self.setRobotPosition(potential_position)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.randint(0, 360)


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    time_steps_needed = []

    for trial in range(num_trials):
        # anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        time_steps = 0
        room = RectangularRoom(width, height)

        total_robots = []
        for robot in range(num_robots):
            total_robots.append(robot_type(room, speed))

        while (room.getNumCleanedTiles() / float(room.getNumTiles())) < min_coverage:
            # anim.update(room, total_robots)
            for robot in total_robots:
                robot.updatePositionAndClean()
            time_steps += 1
        time_steps_needed.append(time_steps)
        # anim.done()
    print time_steps_needed

    return sum(time_steps_needed) / float(len(time_steps_needed))


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?


# print runSimulation(1, 1, 10, 10, .75, 1000, StandardRobot)
# print runSimulation(1, 1, 20, 20, .8, 100, StandardRobot)


def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    simulation_results = []
    robots = []

    for num_robots in range(1, 11):
        robots.append(num_robots)
        result = runSimulation(num_robots, 1, 20, 20, .8, 35, StandardRobot)
        simulation_results.append(result)

    pylab.plot(robots, simulation_results)
    pylab.xlabel("Number of robots")
    pylab.ylabel("Cleaning Time")
    pylab.title("Relationship between cleaning time and number of robots")
    pylab.show()


def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    dimensions = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    simulation_results = []
    ratio_width_to_height = []

    for dimension in dimensions:
        result = runSimulation(2, 1, dimension[0], dimension[1], .8, 100, StandardRobot)
        simulation_results.append(result)
        ratio = dimension[0] / float(dimension[1])
        ratio_width_to_height.append(ratio)

    pylab.plot(ratio_width_to_height, simulation_results)
    pylab.xlabel("Room width to height ratio")
    pylab.ylabel("Cleaning Time")
    pylab.title("Relationship between room width to height ratio and cleaning time")
    pylab.show()


# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):

        self.direction = random.randint(0, 360)
        potential_position = self.position.getNewPosition(self.direction, self.speed)

        if self.room.isPositionInRoom(potential_position):
            self.setRobotPosition(potential_position)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.randint(0, 360)


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.

def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    standard_simulation_results = []
    random_simulation_results = []
    robots = []

    for num_robots in range(1, 11):
        robots.append(num_robots)
        standard_result = runSimulation(num_robots, 1, 20, 20, .8, 30, StandardRobot)
        standard_simulation_results.append(standard_result)

        random_result = runSimulation(num_robots, 1, 20, 20, .8, 30, RandomWalkRobot)
        random_simulation_results.append(random_result)

    pylab.gca().set_color_cycle(["blue", "yellow"])
    pylab.plot(robots, standard_simulation_results)
    pylab.plot(robots, random_simulation_results)
    pylab.legend(["Standard Robots", "Random Walk Robots"], loc="upper right")


    pylab.xlabel("Number of robots")
    pylab.ylabel("Cleaning Time")
    pylab.title("Relationship between cleaning time and number of robots and type of robot")
    pylab.show()
