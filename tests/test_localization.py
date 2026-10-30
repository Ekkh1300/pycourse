import unittest

import app


class LocalizationApiTests(unittest.TestCase):
    def test_curriculum_uses_requested_language_without_leaking_global_state(self):
        app.paths.set_language("fa")
        en_cur = app.api_curriculum({"lang": ["en"]})
        self.assertTrue(en_cur["lessons"][0]["title"].startswith("Lesson"))
        self.assertEqual(app.paths.get_language(), "fa")

        fa_cur = app.api_curriculum({"lang": ["fa"]})
        self.assertTrue(fa_cur["lessons"][0]["title"].startswith("درس"))

    def test_diagnosis_uses_request_language(self):
        en = app.api_run({"code": "print(missing_name)", "lang": "en"})
        fa = app.api_run({"code": "print(missing_name)", "lang": "fa"})
        self.assertEqual(en["diagnosis"]["title"], "Undefined variable")
        self.assertEqual(fa["diagnosis"]["title"], "متغیر تعریف نشده")

    def test_quiz_questions_route_has_one_canonical_path(self):
        result = app.api_quiz_questions({})
        self.assertEqual(result["total"], len(app.QUESTIONS))
        self.assertEqual(len(result["questions"]), len(app.QUESTIONS))
        self.assertNotIn("error", result)

    def test_quiz_count_matches_question_bank(self):
        count = len(app.QUESTIONS)
        self.assertEqual(app.api_curriculum({"lang": ["en"]})["quiz_count"], count)
        self.assertEqual(app.api_curriculum({"lang": ["fa"]})["quiz_count"], count)


if __name__ == "__main__":
    unittest.main()
