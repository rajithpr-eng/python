// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.6;

contract RPSGame {
    // GameState - INITIATED after inital game setup, RESPONDED after responder adds hash choice, WIN or DRAW after final scoring
    enum RPSGameState {INITIATED, RESPONDED, WIN, DRAW}
    
    // PlayerState - PENDING until they add hashed choice, PLAYED after adding hash choice, CHOICE_STORED once raw choice and random string are stored
    enum PlayerState {PENDING, PLAYED, CHOICE_STORED}
    
    // 0 before choices are stored, 1 for Rock, 2 for Paper, 3 for Scissors. Strings are stored only to generate comment with choice names
    string[4] choiceMap = ['None', 'Rock', 'Paper', 'Scissors'];
    
    struct RPSGameData {
        address initiator; // Address of the initiator
        PlayerState initiator_state; // State of the initiator
        bytes32 initiator_hash; // Hashed choice of the initiator
        uint8 initiator_choice; // Raw number of initiator's choice - 1 for Rock, 2 for Paper, 3 for Scissors
        string initiator_random_str; // Random string chosen by the initiator
        
	    address responder; // Address of the responder
        PlayerState responder_state; // State of the responder
        bytes32 responder_hash; // Hashed choice of the responder
        uint8 responder_choice; // Raw number of responder's choice - 1 for Rock, 2 for Paper, 3 for Scissors
        string responder_random_str; // Random string chosen by the responder
                
        RPSGameState state; // Game State
        address winner; // Address of winner after completion. addresss(0) in case of draw
        string comment; // Comment specifying what happened in the game after completion
    }
    
    RPSGameData _gameData;
    
    // Initiator sets up the game and stores its hashed choice in the creation itself. Game and player states are adjusted accordingly
    constructor(address _initiator, address _responder, bytes32 _initiator_hash) {
        _gameData = RPSGameData({
                                    initiator: _initiator,
                                    initiator_state: PlayerState.PLAYED,
                                    initiator_hash: _initiator_hash, 
                                    initiator_choice: 0,
                                    initiator_random_str: '',
                                    responder: _responder, 
                                    responder_state: PlayerState.PENDING,
                                    responder_hash: 0, 
                                    responder_choice: 0,
                                    responder_random_str: '',
                                    state: RPSGameState.INITIATED,
                                    winner: address(0),
                                    comment: ''
                            });
    }
    
    // Responder stores their hashed choice. Game and player states are adjusted accordingly.
    function addResponse(bytes32 _responder_hash) public {
        require(_gameData.state == RPSGameState.INITIATED, "addResponse not allowed");
        _gameData.responder_hash = _responder_hash;
        _gameData.state = RPSGameState.RESPONDED;
        _gameData.responder_state = PlayerState.PLAYED;
    }
    
    // Initiator adds raw choice number and random string. If responder has already done the same, the game should process the completion execution
    function addInitiatorChoice(uint8 _choice, string memory _randomStr) public returns (bool) {
        require((_gameData.state == RPSGameState.INITIATED) || (_gameData.state == RPSGameState.RESPONDED), "addInitiatorChoice not allowed");   
        _gameData.initiator_choice = _choice;
        _gameData.initiator_random_str = _randomStr;
        _gameData.initiator_state = PlayerState.CHOICE_STORED;
        if (_gameData.responder_state == PlayerState.CHOICE_STORED) {
            __validateAndExecute();
        }
        return true;
    }

    // Responder adds raw choice number and random string. If initiator has already done the same, the game should process the completion execution
    function addResponderChoice(uint8 _choice, string memory _randomStr) public returns (bool) {
        require(_gameData.state == RPSGameState.RESPONDED, "addResponderChoice not allowed");
        _gameData.responder_choice = _choice;
        _gameData.responder_random_str = _randomStr;
        _gameData.responder_state = PlayerState.CHOICE_STORED;
        if (_gameData.initiator_state == PlayerState.CHOICE_STORED) {
            __validateAndExecute();
        }
        return true;
    }
    
    // function to set the game results
    function __setResult(RPSGameState state, address winner, string memory comment) private {
        _gameData.state = state;
        _gameData.winner = winner;
        _gameData.comment = comment;
    }

    // funciton to execute the game logic.
    function __Execute() private {
        if ((_gameData.initiator_choice == 1) && (_gameData.responder_choice == 1)) {
            __setResult(RPSGameState.DRAW, address(0), "Rock draws Rock");
        } else if ((_gameData.initiator_choice == 1) && (_gameData.responder_choice == 2)) {
            __setResult(RPSGameState.WIN, _gameData.responder, "Paper beats Rock");
        } else if ((_gameData.initiator_choice == 1) && (_gameData.responder_choice == 3)) {
            __setResult(RPSGameState.WIN, _gameData.initiator, "Rock beats Scissor");
        } else if ((_gameData.initiator_choice == 2) && (_gameData.responder_choice == 1)) {
            __setResult(RPSGameState.WIN, _gameData.initiator, "Paper beats Rock");
        } else if ((_gameData.initiator_choice == 2) && (_gameData.responder_choice == 2)) {
            __setResult(RPSGameState.DRAW, address(0), "Paper draws Paper");
        } else if ((_gameData.initiator_choice == 2) && (_gameData.responder_choice == 3)) {
            __setResult(RPSGameState.WIN, _gameData.responder, "Scissor beats Paper");
        } else if ((_gameData.initiator_choice == 3) && (_gameData.responder_choice == 1)) {
            __setResult(RPSGameState.WIN, _gameData.responder, "Rock beats Scissor");
        } else if ((_gameData.initiator_choice == 3) && (_gameData.responder_choice == 2)) {
            __setResult(RPSGameState.WIN, _gameData.responder, "Paper beats Scissor");
        } else if ((_gameData.initiator_choice == 3) && (_gameData.responder_choice == 3)) {
            __setResult(RPSGameState.DRAW, address(0), "Scissor draws Scissor");
        } 
    }

    // Core game logic to check raw choices against stored hashes, and then the actual choice comparison
    // Can be split into multiple functions internally
    function __validateAndExecute() private {
        bytes32 initiatorCalcHash = sha256(abi.encodePacked(choiceMap[_gameData.initiator_choice], '-', _gameData.initiator_random_str));
        bytes32 responderCalcHash = sha256(abi.encodePacked(choiceMap[_gameData.responder_choice], '-', _gameData.responder_random_str));
        bool initiatorAttempt = false;
        bool responderAttempt = false;
        
        if (initiatorCalcHash == _gameData.initiator_hash) {
            initiatorAttempt = true;
        }
        
        if (responderCalcHash == _gameData.responder_hash) {
            responderAttempt = true;
        }
        
        // Logic to complete the game first based on attempt validation states.
        if ((initiatorAttempt == false) && (responderAttempt == false)) {
            __setResult(RPSGameState.DRAW, address(0), "Initiator and Reponder attempt invalid");
        } else if ((initiatorAttempt == false) && (responderAttempt == true)) {
            __setResult(RPSGameState.WIN, _gameData.responder, "Initiator attempt invalid");
        } else if ((initiatorAttempt == true) && (responderAttempt == false)) {
            __setResult(RPSGameState.WIN, _gameData.initiator, "Responder attempt invalid");            
        } else {
            // Both attempts are valid, execute the game logic.
            __Execute();   
        }
    }

    // Returns the address of the winner, GameState (2 for WIN, 3 for DRAW), and the comment
    function getResult() public view returns (address, RPSGameState, string memory) {
        require((_gameData.state == RPSGameState.WIN) || (_gameData.state == RPSGameState.DRAW), "getResults not allowed");
        return (_gameData.winner, _gameData.state, _gameData.comment);
    } 
    
}


contract RPSServer {
    // Mapping for each game instance with the first address being the initiator and internal key aaddress being the responder
    mapping(address => mapping(address => RPSGame)) _gameList;

    modifier validateAddress(address _opponent) {
        require(_opponent != address(0), "Address cannot be empty");
        require(msg.sender != _opponent, "Addresss cannot be same as sender");
        _;
    }
    
    modifier validateChoice(uint8 _choice) {
        if ((_choice > 0) && (_choice < 4)) {
            _;
        } else {
            revert("You have entered a choice other than - 1(Rock), 2(Paper), 3(Scissor)");
        }
    }

    // Initiator sets up the game and stores its hashed choice in the creation itself. New game created and appropriate function called    
    function initiateGame(address _responder, bytes32 _initiator_hash) public validateAddress(_responder) {
        RPSGame game = new RPSGame(msg.sender, _responder, _initiator_hash);
        _gameList[msg.sender][_responder] = game;
    }

    // Responder stores their hashed choice. Appropriate RPSGame function called   
    function respond(address _initiator, bytes32 _responder_hash) public validateAddress(_initiator) {
        RPSGame game = _gameList[_initiator][msg.sender];
        game.addResponse(_responder_hash);
    }

    // Initiator adds raw choice number and random string. Appropriate RPSGame function called  
    function addInitiatorChoice(address _responder, uint8 _choice, string memory _randomStr) public validateAddress(_responder) validateChoice(_choice) returns (bool) {
        RPSGame game = _gameList[msg.sender][_responder];
        return game.addInitiatorChoice(_choice, _randomStr);
    }

    // Responder adds raw choice number and random string. Appropriate RPSGame function called
    function addResponderChoice(address _initiator, uint8 _choice, string memory _randomStr) public validateAddress(_initiator) validateChoice(_choice) returns (bool) {
        RPSGame game = _gameList[_initiator][msg.sender];
        return game.addResponderChoice(_choice, _randomStr);
    }
    
    // Result details request by the initiator
    function getInitiatorResult(address _responder) public validateAddress(_responder) view returns (address, RPSGame.RPSGameState, string memory) {
        RPSGame game = _gameList[msg.sender][_responder];
        return game.getResult();
    }

    // Result details request by the responder
    function getResponderResult(address _initiator) public validateAddress(_initiator) view returns (address, RPSGame.RPSGameState, string memory) {
        RPSGame game = _gameList[_initiator][msg.sender];
        return game.getResult();
    }
}
