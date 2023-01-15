// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.6;

contract Ticket {
    // Ticket State - RESERVED afeter a ticket is reserved by airlines, CONFIRMED after customer makes payment, CANCELLED after cancellation, etc 
    enum TicketState {RESERVED, CONFIRMED, CANCELLED, CLAIMED}
    enum FlightState {ONTIME, DELAYED, CANCELLED, SCHEDULED}
    
    struct TicketData {
        address payable airline; // Address of the airline
        address payable customer; // Address of the customer
        string flight_number; // Number of the flight
        uint datetime; // Date and Time of the flight
        uint8 seat_number; // Seat number of the flight
        uint flight_price; // Price of the flight
        TicketState state; // Ticket State
        FlightState flightStatus; //Flight Status
        uint delay; // Delay in the fligh departure
        uint refund; // Refund made to the customer(if any)
        uint payment; // Payment made to the airline for service (if any)  
        string comment; // Comment specifying last action executed on the Ticket
    }
    
    TicketData _ticketData;
    TicketServer _parent;
    
    // Airline creates a ticket for the customer along with the flight details
    constructor(address payable _airline, address payable _customer, string memory _flight_number, uint _datetime, uint8 _seat_number, TicketServer parent) {
        _ticketData = TicketData({
                                    airline: _airline,
                                    customer: _customer,
                                    flight_number: _flight_number, 
                                    datetime: _datetime,
                                    seat_number: _seat_number,
                                    flight_price: 100, 
                                    state: TicketState.RESERVED,
                                    flightStatus: FlightState.SCHEDULED,
                                    delay: 0,
                                    refund: 0, 
                                    payment: 0,                                    
                                    comment: 'Ticket is reserved'
                            });
        _parent = parent;
    }
    
    // Customer's account is checked for sufficient balance and booking is confirmed
    function confirm(address payable _initiator, uint value)  public payable returns (bool) {
        require(_ticketData.state == TicketState.RESERVED, "Confirmation not allowed, invalid state");
        require(_ticketData.customer == _initiator, "Confirmation not allowed, invalid initiator");
        require(value >= _ticketData.flight_price, "Insufficient balance");
        _ticketData.state = TicketState.CONFIRMED;
        _ticketData.comment = 'Ticket is now confirmed';
        return true;
    }
    
    // Customer initiated cancel is checked and necessary penalties applied
    // Airline initiated cancel is checked and refunds applied 
    function cancel(address payable _initiator) public returns (bool) {
        bool cancellationEligibility = false;
        if (_ticketData.customer == _initiator) {
            cancellationEligibility= __customer_cancel();
        } else if (_ticketData.airline == _initiator) {
            cancellationEligibility = __airline_cancel(_initiator);
        } else {
            cancellationEligibility = false;
        }        
                 
        return cancellationEligibility;
    }  

    // Customer initiated cancel is checked and necessary penalties applied
    function __customer_cancel() private ValidateCustomerCancellationEligibility() returns (bool) {
        uint8 refund;   
        _ticketData.comment = 'Ticket is cancelled by the customer';
        //Proces refund to customer - % cancellation penalty
        refund = __refund_get();
        _ticketData.refund = _ticketData.flight_price*refund/100;
        _ticketData.payment = _ticketData.flight_price - _ticketData.refund;
        _parent.transfer(_ticketData.customer, _ticketData.refund);
        _parent.transfer(_ticketData.airline, _ticketData.payment);
        _ticketData.state = TicketState.CANCELLED;
        return true;
    }  

    // Get the refund in percentage
    function __refund_get() view private returns (uint8) {
        uint8 refund;
        uint tlfd; // time left for departure

        // refund percentage varies between 10 - 100 depending on the time left for departure.    
        tlfd = _ticketData.datetime - block.timestamp;
        if ( tlfd > 96 hours) {
            refund = 100;
        } else if (tlfd > 48 hours) {
            refund = 50;
        } else if (tlfd > 24 hours) {
            refund = 25;
        } else {
            refund = 10;
        }
        return refund;
    }  

    modifier ValidateCustomerCancellationEligibility() {
        //Customer can cancel 2hrs prior to departure
        require((_ticketData.state == TicketState.CONFIRMED), "Customer cancellation not allowed, invalid state");
        require((_ticketData.datetime  >= (2*60*60 + block.timestamp) ), "Customer cancellation allowed only till 2hrs of departure");
        _;
    }

    // Airline initiated cancel is checked and refunds applied 
    function __airline_cancel(address payable _initiator) private ValidateFlightStatusUpdate(_initiator) returns (bool) {
        _ticketData.comment = 'Flight is cancelled';
        _ticketData.flightStatus = FlightState.CANCELLED;   
        return true;
    }  

    // Airline initiated delay is checked and necessary actions executed
    function delay(address payable _initiator, uint time) public  ValidateFlightStatusUpdate(_initiator)  returns (bool) {
        _ticketData.comment = 'Flight is delayed';
        _ticketData.flightStatus = FlightState.DELAYED;
        _ticketData.delay = time;    
        return true;
    }

    // Airline initiated delay is checked and necessary actions executed
    function ontime(address payable _initiator) public  ValidateFlightStatusUpdate(_initiator) returns (bool) {
        _ticketData.comment = 'Flight is ontime';
        _ticketData.flightStatus = FlightState.ONTIME;
        return true;
    }

    modifier ValidateFlightStatusUpdate(address payable _initiator) {
        //Airline can update status till 24hrs of departure
        require((_ticketData.airline == _initiator), "Airline alone can execute this operation");
        require((block.timestamp <= (_ticketData.datetime + 24*60*60)), "Airline status update allowed only till 24hrs of departure");
        _;
    }

    // Customer initiated claim is checked and necessary actions executed
    function claim(address payable _initiator) public ValidateCustomerClaim(_initiator) returns (bool) {
        uint8 payment;

        _ticketData.comment = 'Ticket claimed by customer';
        _ticketData.state = TicketState.CLAIMED;

        //Rule 1: If airline has already cancelled get complete refund
        if (_ticketData.flightStatus == FlightState.CANCELLED) {
            //Proces complete refund to customer
            _ticketData.refund = _ticketData.flight_price;
            _parent.transfer(_ticketData.customer, _ticketData.refund);
        }

        //Rule 2: If there was a delay % refund
        if (_ticketData.flightStatus == FlightState.DELAYED) {
            payment = __payment_get();
            _ticketData.payment = _ticketData.flight_price*payment/100;
            _ticketData.refund = _ticketData.flight_price - _ticketData.payment;
            _parent.transfer(_ticketData.customer, _ticketData.refund);
            _parent.transfer(_ticketData.airline, _ticketData.payment);
        }

        //Rule 3: If airline has not updated status, complete refund
        if (_ticketData.flightStatus == FlightState.SCHEDULED) {
             //Proces complete refund to customer
            _ticketData.refund = _ticketData.flight_price;
            _parent.transfer(_ticketData.customer, _ticketData.refund);
        }


        //Rule 4: If airline was on time, complete payment
        if (_ticketData.flightStatus == FlightState.ONTIME) {
             //Proces complete payment to airline
            _ticketData.payment = _ticketData.flight_price;
            _parent.transfer(_ticketData.airline, _ticketData.payment);
        }

        return true;
    }

    modifier ValidateCustomerClaim(address payable _initiator) {
        //Customer can cancel 24hrs after departure
        require((_ticketData.customer == _initiator), "Customer alone can execute this operation");
        require((_ticketData.state == TicketState.CONFIRMED), "Customer cliam not allowed, invalid state");
        // For testing purpose, the below line is comment out.
        //require((block.timestamp > (24*60*60 + _ticketData.datetime)), "Customer claim allowed only after 24hrs of departure");
        _;
    }   
    
    // Get the payment in percentage
    function __payment_get() view private returns (uint8) {
        uint8 payment;
        uint _delay;

        _delay = _ticketData.delay;

        // payment percentage varies between 10 - 100 depending on the flight delay    
        if (_delay  > 12 hours) {
            payment = 10;
        } else if (_delay > 6 hours) {
            payment = 25;
        } else if (_delay > 3 hours) {
            payment = 50;
        } else {
            payment = 100;
        }
        return payment;
    }  

    // Returns the Ticket Details
    function getTicketDetails() public view returns (address payable , address payable, TicketState, FlightState, uint, uint, uint, string memory) {
        return (_ticketData.airline, _ticketData.customer, _ticketData.state, _ticketData.flightStatus, _ticketData.flight_price, _ticketData.refund, _ticketData.payment, _ticketData.comment);
    } 

    // Returns the Ticket
    function getTicket() public view returns (string memory, uint, uint8) {
        return (_ticketData.flight_number, _ticketData.datetime, _ticketData.seat_number);
    } 
}


contract TicketServer {
    // Mapping from (flightNum, datetime) to booked seats
    mapping(bytes32 => uint8[]) _bookedSeatList;

    // Mapping from (flightNum, datetime, seatnum) to a ticket instance
    mapping(bytes32 => Ticket) _ticketList;

    modifier validateAddress(address payable _customer) {
        require(_customer != address(0), "Customer Address cannot be empty");
        require(msg.sender != _customer, "Customer Addresss cannot be same as airline/initiator");
        _;
    }
    
    modifier validateTicket(string memory _flightNum, uint _dateTime) {
        require((_dateTime > block.timestamp), "Flight is not available");
        _;
    }  

    // Airline creates a reservation for the customer along with the ticket details
    // Before creating the input parameters are validated
    // _customer = is non zero and not same as airline address(msg.sender)
    // _flighNum = is one of valide flights 
    // _dateTime = is not less than current date and time 
    // On success, returns the flight Details is returned
    function reserve(address payable _customer, string memory _flightNum, uint _dateTime) public validateAddress(_customer) validateTicket(_flightNum, _dateTime) returns (string memory, uint, uint8) {
        uint8 seatNum = __getNextSeatNum(_flightNum, _dateTime);
        require((seatNum > 0), "No seats are available");
        Ticket ticket = new Ticket(payable(msg.sender), _customer, _flightNum, _dateTime, seatNum, this);
        bytes32 reservation_id = keccak256(abi.encodePacked(_flightNum, _dateTime, seatNum));
        _ticketList[reservation_id] = ticket;
        __bookSeatNum(_flightNum, _dateTime, seatNum);
        return (_flightNum, _dateTime, seatNum);
    }

    function __getNextSeatNum(string memory _flightNum, uint _dateTime) private view returns (uint8){
        bytes32 flight_id = keccak256(abi.encodePacked(_flightNum, _dateTime));
        uint8[] memory array = new uint8[](51);
        uint8 seatNum = 0;

        for (uint8 i = 0; i < _bookedSeatList[flight_id].length; i++) {
            uint8 j = _bookedSeatList[flight_id][i];
            array[j] = 1;
        }

        for (uint8 i = 1; i < array.length; i++) {
            if (array[i] == 0) {
                seatNum = i;
                break;
            }
        }
        return seatNum;
    }

    function __bookSeatNum(string memory _flightNum, uint _dateTime, uint8 _seatNum) private{
        bytes32 flight_id = keccak256(abi.encodePacked(_flightNum, _dateTime));
        _bookedSeatList[flight_id].push(_seatNum);
    }

    function __cancelSeatNum(string memory _flightNum, uint _dateTime, uint8 _seatNum) private{
        bytes32 flight_id = keccak256(abi.encodePacked(_flightNum, _dateTime));
        uint8 pos = 0;

        for (uint8 i = 0; i < _bookedSeatList[flight_id].length; i++) {
            if (_bookedSeatList[flight_id][i] == _seatNum) {
                pos = i;
                break;
            }
        }

        for (uint8 i = pos; i < _bookedSeatList[flight_id].length - 1; i++) {
            _bookedSeatList[flight_id][pos] = _bookedSeatList[flight_id][pos+1];
        }
        
        _bookedSeatList[flight_id].pop();
    }

    // Customer updates the created Ticket to Confirmed
    // Before updating the input parameter are validated
    // On success, the reservationId, true is returned
    function confirm(string memory _flightNum, uint _dateTime, uint8 seatNum) public payable returns (bytes32, bool){
        bytes32 reservation_id = keccak256(abi.encodePacked(_flightNum, _dateTime, seatNum));
        Ticket ticket = _ticketList[reservation_id];
        bool ret = ticket.confirm(payable(msg.sender), msg.value);
        return (reservation_id, ret);
    }

    // Customer/Airline updates the Ticket status to Cancelled
    // Before updating the input parameters are validated
    // On success, 0 is returned.
    // Otherwise, 1 is returned.
    function cancel(bytes32 _reservationId) public returns (bool){
        Ticket ticket = _ticketList[_reservationId];
        bool val = ticket.cancel(payable(msg.sender));
        if (val) {
            string memory flightNum;
            uint datetime;
            uint8 seatNum;
            (flightNum, datetime, seatNum) = ticket.getTicket();
            __cancelSeatNum(flightNum, datetime, seatNum);
        }
        return val;
    }

    // Airline updates the Ticket status to Delayed
    // Before updating the input parameters are validated
    // On success, 0 is returned.
    // Otherwise, 1 is returned.
    function delay(bytes32 _reservationId, uint _delay) public returns (bool){
        Ticket ticket = _ticketList[_reservationId];
        return ticket.delay(payable(msg.sender), _delay);
    }

    // Airline updates the Ticket status to OnTime
    // Before updating the input parameters are validated
    // On success, 0 is returned.
    // Otherwise, 1 is returned.
    function ontime(bytes32 _reservationId) public returns (bool){
        Ticket ticket = _ticketList[_reservationId];
        return ticket.ontime(payable(msg.sender));
    }

    // Customer updates the Ticket status to Claimed
    // Before updating the input parameters are validated
    // On success, 0 is returned.
    // Otherwise, 1 is returned.
    function claim(bytes32 _reservationId) public returns (bool){
        Ticket ticket = _ticketList[_reservationId];
        return ticket.claim(payable(msg.sender));
    }   

    function transfer(address payable _to, uint value) public {
        _to.transfer(value);
    }    

    function getTicketDetails(bytes32 _reservationId) view public returns (address payable, address payable, Ticket.TicketState, Ticket.FlightState, uint, uint, uint, string memory){
        Ticket ticket = _ticketList[_reservationId];
        return ticket.getTicketDetails();
    }   

    function getTicket(bytes32 _reservationId) view public returns (string memory, uint , uint8){
        Ticket ticket = _ticketList[_reservationId];
        return ticket.getTicket();
    }   
}