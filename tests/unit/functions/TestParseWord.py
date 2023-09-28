import unittest
from pipeline.functions.ParseWord import create_doc_object, chunk_dict, headers


class TestParseWord(unittest.TestCase):
    def test_create_doc_object(self):
        text = "test"
        first_object = create_doc_object(text, headers.H1)
        self.assertEqual(first_object, {
                         headers.HEADER: text, headers.HEADER_TYPE: headers.H1, headers.CONTENT: [], headers.TEXT: ""})

    def test_basic_chunk_dict(self):
        example_dict = [
            {
                headers.HEADER: "Untitled",
                headers.HEADER_TYPE: headers.H1,
                headers.TEXT: "1",
                headers.CONTENT: [
                    {
                                headers.HEADER: "title2",
                                headers.HEADER_TYPE: headers.H2,
                                headers.TEXT: "2",
                                headers.CONTENT: []
                    }
                ]
            }
        ]
        results = chunk_dict(example_dict)
        expected_results = ['Header: Untitled\nText: 1',
                            'Header: Untitled\nTitle: title2\nText: 2']
        self.assertEqual(results, expected_results)

    def test_complex_chunk_dict(self):
        example_dict = [
            {
                headers.HEADER: "Untitled",
                headers.HEADER_TYPE: headers.H1,
                headers.TEXT: "1",
                headers.CONTENT: [
                    {
                                headers.HEADER: "title2",
                                headers.HEADER_TYPE: headers.H2,
                                headers.TEXT: "2",
                                headers.CONTENT: [
                                    create_doc_object("title4", headers.H4),
                                    create_doc_object("title3", headers.H3)
                                ]
                    },
                    create_doc_object("TEST", headers.H2)
                ]
            }
        ]
        results = chunk_dict(example_dict)
        expected_results = ['Header: Untitled\nText: 1',
                            'Header: Untitled\nTitle: title2\nText: 2',
                            'Header: Untitled\nTitle: title2\nSubtitle: title4\nText: ',
                            'Header: Untitled\nTitle: title2\nSubtitle: title3\nText: ',
                            'Header: Untitled\nTitle: TEST\nText: ']
        self.assertEqual(results, expected_results)


if __name__ == '__main__':
    unittest.main()
