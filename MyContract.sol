// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;
contract MyContract{
    string name;
    struct User{
        uint score;
    }
    User[] users;
    event Trade(string str,uint amount);
    enum STATE{ACTIVE,INACTIVE}
    STATE state;
    mapping(address=>uint) balances;
    function setToactive() external{
        state=STATE.ACTIVE;
    }
    function balance() external view returns(uint){
        return(address(this).balance);
    }
    function set()external view returns(uint){
        User storage uses=users[0];
        // uses.score=10;
        return(uses.score);
    }
    function initialise(string calldata _name)external{
        name=_name;
    }
    function setvalue(uint _val)external{
        User storage uses=users[0];
        uses.score=10;
        uses.score=_val;
    }
    function pay() payable external{
        balances[msg.sender]+=msg.value;
        
    }
    function emission() external{
        emit Trade('Harsh',250);
    }
    function send(address payable recipient)external{
        recipient.transfer(100 wei);
    }

}