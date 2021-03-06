#!/usr/bin/env python

import unittest
import numpy as np
import rospy
import rostest

from moveit_ros_planning_interface._moveit_move_group_interface import MoveGroup


class PythonMoveGroupTest(unittest.TestCase):
    PLANNING_GROUP = "manipulator"

    @classmethod
    def setUpClass(self):
        self.group = MoveGroup(self.PLANNING_GROUP, "robot_description")

    @classmethod
    def tearDown(self):
        pass

    def check_target_setting(self, expect, *args):
        if len(args) == 0:
            args = [expect]
        self.group.set_joint_value_target(*args)
        res = self.group.get_joint_value_target()
        self.assertTrue(np.all(np.asarray(res) == np.asarray(expect)),
                        "Setting failed for %s, values: %s" % (type(args[0]), res))

    def test_target_setting(self):
        n = self.group.get_variable_count()
        self.check_target_setting([0.1] * n)
        self.check_target_setting((0.2,) * n)
        self.check_target_setting(np.zeros(n))
        self.check_target_setting([0.3] * n, {name: 0.3 for name in self.group.get_active_joints()})
        self.check_target_setting([0.5] + [0.3]*(n-1), "joint_1", 0.5)


if __name__ == '__main__':
    PKGNAME = 'moveit_ros_planning_interface'
    NODENAME = 'moveit_test_python_move_group'
    rospy.init_node(NODENAME)
    rostest.rosrun(PKGNAME, NODENAME, PythonMoveGroupTest)
