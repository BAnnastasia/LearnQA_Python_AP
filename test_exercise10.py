class TestExercise10:
    def test_check(self):
        phrase = input("Set a phrase: ")
        print(phrase)
        len_st = len(phrase)
        assert len_st <= 15

