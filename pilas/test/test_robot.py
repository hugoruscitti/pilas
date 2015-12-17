# -*- coding: utf-8 -*-
import unittest
import pilas
import math

def rotar_actor_respecto_otro(referencia, actor, angulo):
    radianes = math.radians(360 - angulo)
    actor.x = math.cos(radianes) * 200 + referencia.x
    actor.y = math.sin(radianes) * 200 + referencia.y

class TestRobot(unittest.TestCase):
    INITIAL_ROTATION = 270
    def setUp(self):
        self.board = pilas.actores.Board()
        self.robot = pilas.actores.Robot(self.board, 1)
        self.actor = self.robot.actor

    def tearDown(self):
        pilas.mundo.reiniciar()

    def test_initial_position(self):
        self.assertEqual(self.actor.x, 0)
        self.assertEqual(self.actor.y, 0)
        self.assertEqual(self.actor.rotacion,
                         TestRobot.INITIAL_ROTATION)

    def test_destruction(self):
        actors = len(pilas.escena_actual().actores)
        del self.robot
        self.assertEqual(len(pilas.escena_actual().actores), actors - 1)

    def test_forward_with_time(self):
        self.robot.forward(100, 1)
        self.assertGreater(self.actor.y, 0)

    def test_backward_with_time(self):
        self.robot.backward(100, 1)
        self.assertLess(self.actor.y, 0)

    def test_turn_left_with_time(self):
        self.robot.turnLeft(100, 1)
        self.assertLess(self.actor.rotacion, TestRobot.INITIAL_ROTATION)

    def test_turn_right_with_time(self):
        self.robot.turnRight(100, 1)
        self.assertGreater(self.actor.rotacion, TestRobot.INITIAL_ROTATION)
        
    def test_up_pen(self):
        self.robot.bajalapiz()
        self.robot.subelapiz()
        self.assertFalse(self.actor.lapiz_bajo)

    def test_down_pen(self):
        self.robot.subelapiz()
        self.robot.bajalapiz()
        self.assertTrue(self.actor.lapiz_bajo)
    
    def test_ping_obstacle_present(self):
        m = pilas.actores.Mono()
        for ang in range(0, 360, 20):
            rotar_actor_respecto_otro(self.actor, m, ang)
            self.actor.rotacion = ang
            self.assertGreater(600, self.robot.ping(),
                "Robot y obstaculo rotados a {} grados"
                .format(ang))
    
    def test_ping_obstacle_absent(self):
        m = pilas.actores.Mono()
        for ang in range(0, 360, 20):
            rotar_actor_respecto_otro(self.actor, m, ang)
            self.actor.rotacion = ang + 180
            self.assertEqual(601, self.robot.ping(),
                "Robot y obstaculo rotados a {} grados"
                .format(ang))
    
    def test_behind_the_robot(self):
        m = pilas.actores.Mono()
        ang = 20
        rotar_actor_respecto_otro(self.actor, m, 180 + ang)
        self.actor.rotacion = ang
        self.assertEqual(601, self.robot.ping())
        
    def test_ahead_of_the_robot(self):
        m = pilas.actores.Mono()
        m.y = 150
        self.assertGreater(600, self.robot.ping())
        
    # FIXME: Testear precisión
    # self.assertAlmostEqual(200, self.robot.ping(), delta=1.5)
            

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
    pilas.terminar()
