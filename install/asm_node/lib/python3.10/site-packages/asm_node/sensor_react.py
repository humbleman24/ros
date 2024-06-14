import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random

class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        self.publisher_ = self.create_publisher(Twist, '/vehicle_blue/cmd_vel', 10)
        self.subscriber_ = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.count = 0
        self.flag = 1
    def scan_callback(self, msg):
        self.count += 1
        if self.count > 800:
            self.count = 0
            r = random.uniform(-1,1)
            if r < -8:
                self.flag = 0
            else:
                self.flag = 1
        else:
            if self.flag:
                r = 0.8
            else:
                r = -0.8
        lidar_range = msg.ranges
        detect_wall = False
        for dist in lidar_range:
            if dist < 1:
                detect_wall = True
                break

        cmd_vel_value = Twist()
        if detect_wall:
            cmd_vel_value.linear.x = 0.0
            cmd_vel_value.angular.z = 0.7
        else:
            cmd_vel_value.linear.x = 1.5
            cmd_vel_value.angular.z = 0.0
        self.publisher_.publish(cmd_vel_value)

        


def main(args=None):
    rclpy.init(args=args)
    velocity_publisher = VelocityPublisher()
    rclpy.spin(velocity_publisher)
    velocity_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()