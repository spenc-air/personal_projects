import numpy as np
import hexsudoku as hex

def test_unique_vals():
    assert hex.unique_vals(np.array([1, 2, 3, 4])) == True
    assert hex.unique_vals(np.array([1, None, 3, 4])) == True
    assert hex.unique_vals(np.array([1, None, 3, None])) == True
    assert hex.unique_vals(np.array([1, 2, 2, 4])) == False
    assert hex.unique_vals(np.array([3, None, 3, 4])) == False

def test_valid_hexudoku():
    M = np.array([[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]])
    S = np.array([[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]])
    P = np.array([[0,1,2,7,4,7,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]])
    H = np.array([[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,8,5,6],[8,1,2,3,4,5,6],[0,1,2,3,4,5,6]])
    R = np.array([[0,1,7,3,4,5,6],[0,1,2,3,4,5,7],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]])
    L = np.array([[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,9,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,9,5,6]])
    assert hex.valid_hexudoku(M) == True, "returned false when the hexudoku was valid"
    assert hex.valid_hexudoku(S) == False, "didn't catch invalid shape"
    assert hex.valid_hexudoku(P) == False, "didn't catch duplicate within group"
    assert hex.valid_hexudoku(H) == False, "didn't catch horizontal axis duplicate"
    assert hex.valid_hexudoku(R) == False, "didn't catch up-right axis duplicate"
    assert hex.valid_hexudoku(L) == False, "didn't catch up-left axis duplicate"
    assert hex.valid_hexudoku(hex.just_middle()) == True, "returned false for just_middle"

def test_possible_vals():
    M = hex.just_middle()
    assert hex.possible_vals(M, 2, 5) == {0, 1, 5, 6}
    assert hex.possible_vals(M, 6, 1) == {0, 1, 3}
    assert hex.possible_vals(M, 0, 1) == {1, 3, 4, 5, 6}