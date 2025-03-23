// Author : K.L.M 
// Difficulty : Easy

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
/*
 __  __           _   _           _                             _ 
 |  \/  |         | | (_)         | |     /\                    | |
 | \  / |_   _ ___| |_ _  ___ __ _| |    /  \   _ __   __ _  ___| |
 | |\/| | | | / __| __| |/ __/ _` | |   / /\ \ | '_ \ / _` |/ _ \ |
 | |  | | |_| \__ \ |_| | (_| (_| | |  / ____ \| | | | (_| |  __/ |
 |_|  |_|\__, |___/\__|_|\___\__,_|_| /_/    \_\_| |_|\__, |\___|_|
          __/ |                                        __/ |       
         |___/                                        |___/        

       .-""-.                     .-""-.
     .'_.-.  |                   |  .-._'.
    /    _/ /       _______       \ \_    \
   /.--.' | |      `=======`      | | '.--.\
  /   .-`-| |       ,ooooo,       | |-`-.   \
 ;.--':   | |     .d88888/8b.     | |   :'--.;
|    _\.'-| |    d8888888/888b    | |-'./_    |
;_.-'/:   | |   d8888P"`  'Y88b   | |   :\'-._;
|   | _:-'\  \.d88(` ^ _ ^  )88b./  /'-:_ |   |
;  .:` '._ \.d88888\   _   /88888b / _.' `:.  ;
|-` '-.;_ .d88888888b.___.d8888888b.` _;.-' `-|
; / .'\ | 888888888P'    'Y888888888b'| /'. \ ;
| .' / `'.8888888P' `"---"` 'Y88888888'` \ '. |
;/  /\_/-`Y888888|           |8888888P-\_/\  \;
 |.' .| `; Y88888| |       | |888888P;` |. '.|
 |  / \.'\_/Y8888| :--"""--: |8888P`_/'./ \  |
  \| ; | ; |/8888| |       | |8888\| : | ; |/
   \ | ; | /d8888\.'-.....-'./8888b\ | ; | /
    `\ | |`d8888P' / ;|: | \ 'Y88888`| | /`
     .-:_/ Y8;=' .' / ' . : '. '888P`\_:'
     |  \```      .'  ;     \    `:
      \  \                   '     `'.
   .--'\  |  '         '       .      `-._
  /`;--' /_.'          .                  `-.
  |  `--`        /               \           \
   \       .'   '                 '-.        |
    \   '               '          __\       |
     '.      .                 _.-'  `)     /
       '-._                _.-' `| .-`   _.'
           `'--....____.--'|     (`  _.-'
                    /  | |  \     `"`
                    \__/ \__/
As a traveler, you came across a mystical angel who can bless you. Try to get 10 blessings from the angel to ascend to the heavens.
*/

contract Challenge {

    bool public solved = false;
    uint256 private seed;

    mapping(address => uint256) public blessings;

    event Blessed(address indexed sender);
    event Ascended(address indexed sender);

    constructor() payable{
        require(msg.value == 2 ether, "Insufficient funds");
        seed = block.timestamp;
    }

    function Blessing() public payable {
        require(msg.value == 1 ether, "You must pay the right to get your blessing");
        uint256 randomNumber = uint256(keccak256(abi.encodePacked(seed, msg.sender, block.prevrandao, block.timestamp)));
        uint256 AngelNumber = randomNumber % 2;

        if (AngelNumber == 1) {
            (bool sent, ) = msg.sender.call{value: 1 ether}("");
            require(sent, "Failed to send Ether");
            blessings[msg.sender] += 1;
        }

        if (AngelNumber == 0) {
            (bool sent, ) = msg.sender.call{value: 0 ether}("");
            require(sent, "Failed to send Ether");
            blessings[msg.sender] = 0;
        }
    }

    function ascend() public payable {
        require(blessings[msg.sender] >= 10,"You have not proved your worthiness :((");
        solved = true;
    }

    function isSolved() public view returns (bool) {
        return solved;
    }

}