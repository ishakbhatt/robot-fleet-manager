"""
`Robot Fleet Manager` class
* starts the webpage
* add robots
* remove robots
* update info about individual robots
"""
from fleet_app import app
from robot import Robot
from flask import Flask, jsonify, request

# development environment
# selected port 5000 for one fleet
# multiple ports for multiple fleets
api_url = "localhost:5000"

class RobotFleetManager:
    
    def __init__(self):
        # Initialize fleet with some robots
        self.robots = {f"robot_{i+1}": Robot(f"robot_{i+1}") for i in range(5)}
        self.register_routes()

    def register_routes(self):
        @app.route("/")
        def home():
            return "Robot Fleet Manager is running."

        # Get a single robot's details
        @app.route("/robots/<robot_name>", methods=["GET"])
        def get_robot(robot_name):
            robot = self.robots.get(robot_name) # wont throw an error 
            if robot:  # Robot found
                return jsonify(robot._to_dict())
            return jsonify({"error": "Robot not found"}), 404

        # Get all robots in the fleet
        @app.route("/robots", methods=["GET"])
        def get_fleet():
            return jsonify([robot._to_dict() for robot in self.robots.values()])

        # Update robot's pose
        @app.route("/robots/<robot_name>/pose", methods=["PATCH"])
        def update_pose(robot_name, pose):
            robot = self.robots.get(robot_name)
            if robot:
                robot.position = pose[0] # position
                robot.orientation = pose[1] # orientation
                return jsonify(robot._to_dict())
            return jsonify({"error": "Robot not found"}), 404

        # Update robot's PTP time
        @app.route("/robots/<robot_name>/time", methods=["PATCH"])
        def update_time(robot_name, ptp_time):
            robot = self.robots.get(robot_name) # get the robot
            if robot:
                robot.grandmaster_time = ptp_time
                return jsonify(robot._to_dict())
            return jsonify({"error": "Robot not found"}), 404

        # Update robot's name
        @app.route("/robots/<robot_name>/name", methods=["PATCH"])
        def update_name(robot_name, new_name):
            robot = self.robots.get(robot_name)
            if robot:
                if new_name:
                    robot.robot_name = new_name
                    return jsonify(robot._to_dict())
                return jsonify({"error": "New name is required"}), 400
            return jsonify({"error": "Robot not found"}), 404

        # Update robot's status
        @app.route("/robots/<robot_name>/status", methods=["PATCH"])
        def update_status(robot_name, status):
            robot = self.robots.get(robot_name)
            if robot:
                robot.status = status
                return jsonify(robot._to_dict())
            return jsonify({"error": "Robot not found"}), 404

        # Update robot's battery
        @app.route("/robots/<robot_name>/battery", methods=["PATCH"])
        def update_battery(robot_name, battery_val):
            robot = self.robots.get(robot_name)
            if robot:
                robot.battery = battery_val
                return jsonify(robot._to_dict())
            return jsonify({"error": "Robot not found"}), 404

        # Add a new robot to the fleet
        @app.route("/robots", methods=["PUT"])
        def add_robot(new_robot_name):
            if new_robot_name:
                new_robot = Robot(new_robot_name)
                self.robots[new_robot_name] = new_robot
                return jsonify(new_robot._to_dict()), 201
            return jsonify({"error": "Name is required"}), 400

        # Take a robot offline (remove from fleet)
        @app.route("/robots/<robot_name>", methods=["DELETE"])
        def take_robot_offline(robot_name):
            robot = self.robots.pop(robot_name, None) # None if not found
            if robot:
                return jsonify({"message": f"{robot_name} is now offline."})
            return jsonify({"error": "Robot not found"}), 404