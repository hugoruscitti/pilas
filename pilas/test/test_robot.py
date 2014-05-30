import unittest
import pilas

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
        self.assertEqual(self.actor.lapiz_bajo, False)

    def test_down_pen(self):
        self.robot.subelapiz()
        self.robot.bajalapiz()
        self.assertEqual(self.actor.lapiz_bajo, True)

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
    pilas.terminar()
