from robot import Robot
from fleet_app import app
from robot_fleet_manager import RobotFleetManager

if __name__ == "__main__":
    fleet_manager = RobotFleetManager()
    app.run(debug=True)

    # robots set internally in fleet manager



