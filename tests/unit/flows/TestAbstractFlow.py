import unittest
from pipeline.flows.abstract.generic_flow import AbstractFlow
from pipeline.config.config import config


class TestAbstractFlow(unittest.TestCase):
    def test_gen_abstract_flow_raise_input_expection(self):
        generic_flow = AbstractFlow(config)
        with self.assertRaises(TypeError):
            generic_flow.run(100)
            generic_flow.run(0.0)
            generic_flow.run([])

if __name__ == '__main__':
    unittest.main()
