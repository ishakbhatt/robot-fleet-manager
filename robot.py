"""
`Robot` class
* contains information about an individual robot
* all robots have the same sensors
* update info about individual robots
* future development - 
    * get sensing info via sensor SDKs, mcap api, and sensor web pages
    * grandmaster clock time and sensor times - important for debugging!
"""

class Robot:
    def __init__(self, name):
        self.robot_name = name  # name can also have id
        self.position = (0, 0)
        self.orientation = 0
        self.grandmaster_time = 0
        self.status = "IDLE"
        self.battery = 100

        # making the assumption they all have the same sensors
        self.sensors = [
            {"type": "lidar", "subscribed_topic": "/ouster/points", "status": "active", "time_protocol": "PTP", "synchronized": "true"},
            {"type": "imu", "subscribed_topic": "/camera/camera/imu", "status": "active", "time_protocol": "PTP", "synchronized": "true"},
            {"type": "camera", "subscribed_topic": "/camera/camera/image_raw", "status": "active", "time_protocol": "PTP", "synchronized": "true"}
        ]

    def _to_dict(self):
        return {
            "name": self.robot_name,
            "position": self.position,
            "orientation": self.orientation,
            "status": self.status,
            "battery": self.battery,
            "sensors": self.sensors,
            "time": self.grandmaster_time
        }
