% Rules based on the decision tree

decide(c0) :- a5(false), !.
decide(c0) :- a5(true), a8(false), a9(false), a2(false), !.
decide(c0) :- a5(true), a8(false), a9(false), a2(true), a0(false), a4(true), !.
decide(c1) :- a5(true), a8(false), a9(false), a2(true), a0(false), a4(false), !.
decide(c1) :- a5(true), a8(false), a9(false), a2(true), a0(true), !.
decide(c1) :- a5(true), a8(false), a9(true), !.
decide(c1) :- a5(true), a8(true), a1(false), a2(false), a0(false), !.
decide(c0) :- a5(true), a8(true), a1(false), a2(false), a0(true), !.
decide(c0) :- a5(true), a8(true), a1(false), a2(true), a4(true), !.
decide(c1) :- a5(true), a8(true), a1(false), a2(true), a4(false), !.
decide(c0) :- a5(true), a8(true), a1(true), !.

% User prompts to gather input for attributes

ask_attribute(5) :- write('Enter value for a5 (true/false): '), read(Value), assert(a5(Value)).
ask_attribute(8) :- write('Enter value for a8 (true/false): '), read(Value), assert(a8(Value)).
ask_attribute(9) :- write('Enter value for a9 (true/false): '), read(Value), assert(a9(Value)).
ask_attribute(0) :- write('Enter value for a0 (true/false): '), read(Value), assert(a0(Value)).
ask_attribute(1) :- write('Enter value for a1 (true/false): '), read(Value), assert(a1(Value)).
ask_attribute(2) :- write('Enter value for a2 (true/false): '), read(Value), assert(a2(Value)).
ask_attribute(4) :- write('Enter value for a4 (true/false): '), read(Value), assert(a4(Value)).

% Main function to gather all inputs and predict

start_decision :-
    ask_attribute(5),
    ask_attribute(8),
    ask_attribute(9),
    ask_attribute(0),
    ask_attribute(1),
    ask_attribute(2),
    ask_attribute(4),
    decide(Result),
    write('The Pragyan Rover should measure parameter: '), write(Result), nl.
