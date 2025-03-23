// Author : K.L.M 
// Difficulty : Easy

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Challenge {
    bool public solved;
    uint8[9][9] public initialGrid;
    
    constructor() {
        solved = false;
        initialGrid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ];
    }

    function submitSolution(uint8[9][9] memory solution) public {

        if (isValidSolution(solution)) {
            solved = true;
        }
    }

    function isValidSolution(uint8[9][9] memory solution) internal view returns (bool) {
        for (uint8 i = 0; i < 9; i++) {
            for (uint8 j = 0; j < 9; j++) {
                if (initialGrid[i][j] != 0 && solution[i][j] != initialGrid[i][j]) {
                    return false;
                }
            }
        }

        for (uint8 i = 0; i < 9; i++) {
            if (!isUnique(solution[i])) return false;
            if (!isUnique(getColumn(solution, i))) return false;
        }

        for (uint8 i = 0; i < 3; i++) {
            for (uint8 j = 0; j < 3; j++) {
                if (!isUnique(getSubgrid(solution, i * 3, j * 3))) return false; 
            }
        }

        return true;
    }

    function isUnique(uint8[9] memory arr) internal pure returns (bool) {
        bool[10] memory seen;
        for (uint8 i = 0; i < 9; i++) {
            if (arr[i] < 1 || arr[i] > 9 || seen[arr[i]]) {
                return false;
            }
            seen[arr[i]] = true;
        }
        return true;
    }

    function getColumn(uint8[9][9] memory grid, uint8 col) internal pure returns (uint8[9] memory) {
        uint8[9] memory column;
        for (uint8 i = 0; i < 9; i++) {
            column[i] = grid[i][col];
        }
        return column;
    }

    function getSubgrid(uint8[9][9] memory grid, uint8 row, uint8 col) internal pure returns (uint8[9] memory) {
        uint8[9] memory subgrid;
        uint8 index = 0;
        for (uint8 i = 0; i < 3; i++) {
            for (uint8 j = 0; j < 3; j++) {
                subgrid[index++] = grid[row + i][col + j];
            }
        }
        return subgrid;
    }

    function isSolved() public view returns(bool){
        return solved;
    }
}