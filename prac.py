from dataclasses import dataclass

#def add(x: int, y: int) -> int:
#def __init__(self) -> None:
# arrow denotes the return type

class EndOfStream(Exception):
    pass

class TokenError(Exception):
    pass

# class Hero:
#     def __init__(self) -> None:
#         print("SuperHero")

# class Alover:
#     def __init__(self) -> None:
#         print("love >3")

# class Rover:
#     def __init__(self,x,y) -> None:
#         print(y,x)

@dataclass
        
#Iterate over the string
class Stream:
    # def __init__(self,source:str,pos:int=0) -> None:
    #     self.source:str=source
    #     self.pos:int=pos
    source:str
    pos:int
    def from_string(s):
        return Stream(s,0)
    
    def next_char(self):
        if self.pos < len(self.source):
            char=self.source[self.pos]
            self.pos=self.pos+1
            return char
        else:
            raise EndOfStream()
    def unget(self):
        assert self.pos>0
        self.pos-=1 
# @dataclass   
# class Hello:
#     def __init__(self) -> None:
#         self.hero=Hero
#         self.alover=Alover
#         self.posit=int
#         self.rov=Rover
#         self.stream=Stream
#     # hero:Hero
#     # alover:Alover
#     # posit:int
#     # rov:Rover
#     # stream:Stream
    
#     def func(self):
#         return (self.hero(), self.alover(), self.posit(13), self.rov(y=11,x=9), self.stream("allWell",1).next_char())

# print(Hello().func())
# f=Stream.from_string("brceus")
# f.pos=len(f.source)-1
# print(f.next_char())
# print(f.next_char())
# f.unget()
# print(f.next_char())


#define the tokens

@dataclass
class Integer:
    value:int

@dataclass
class Float:
    value:int

@dataclass
class Bool:
    value:bool

@dataclass    
class String:
    value:str

@dataclass
class KeyWord:
    value:str

@dataclass
class ListWord:
    value:list

@dataclass
class Identifier:
    value:str

@dataclass
class Operator:
    value:str
    
class EndOfTokens():
    pass

Token=Integer | Float |String| Bool| ListWord | KeyWord | Identifier | Operator | EndOfTokens |None

#Identifiers: defined name for particular function
#keywords-> special resevation for the value for particular functionality
keywords="str int bool lst is in let letAnd get assign end if else then do done while for printing put len defFun funCall isEmpty".split()
symbolic_operators="= > < & | ^ ( ) - + { } [ ] % / * ; , : !".split()
word_operators="and or not flor cil log".split()
whitespace=" \t\n"

def word_to_token(value):
    print("value ",value, " type ",type(value))
    # if type(value)==list:
    #     return ListWord(value)
    # if type(value)==str:
    #     return String(value)
    if value in keywords:
        print("word1")
        return KeyWord(value)
    if value in word_operators:
        print("word2")
        return Operator(value)
    if value == "True":
        print("word3")
        return Bool(True)
    if value =="False":
        print("word4")
        return Bool(False)
    print("word5")
    return Identifier(value)



@dataclass
class Lexer:
    stream: Stream
    save: Token = None
    # an instance variable, named save of type Token with a default value of None.
    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        # returns the next token in the input stream
        try:
            match self.stream.next_char():
                case c if c in symbolic_operators:
                    if c =='-':
                        d=self.stream.next_char()
                        if d.isdigit():
                            n = int(d)
                            flag=0
                            while True:
                                try:
                                    d = self.stream.next_char()
                                    if d=='.':
                                        flag=1
                                        d = self.stream.next_char()
                                        count=0  
                                    if d.isdigit() and flag==0:
                                        n = n*10 + int(d)
                                    elif d.isdigit() and flag==1:
                                        flag=1
                                        count+=1
                                        n = n*(10**count) + int(d)
                                        n=n/(10**count)

                                    elif flag==0:
                                        self.stream.unget()
                                        return Integer(-n)
                                    elif flag==1:
                                        self.stream.unget()
                                        return Float(-n)
                                except EndOfStream:
                                    if flag==1:
                                        self.stream.unget()
                                        return Float(-n)
                                    else:
                                        self.stream.unget()
                                        return Integer(-n)
                
                        else:
                            self.stream.unget()
                            return Operator(c)
                    
                    return Operator(c)
                case '"':
                    s=""
                    try:
                        c=self.stream.next_char()
                        while c!='"':
                            s+=c
                            c=self.stream.next_char()
                        return String(s)
                    except EndOfStream:
                        raise TokenError()
                case c if c.isdigit():
                    n = int(c)
                    flag=0
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c=='.':
                                flag=1
                                c = self.stream.next_char()
                                count=0  
                            if c.isdigit() and flag==0:
                                n = n*10 + int(c)
                            elif c.isdigit() and flag==1:
                                flag=1
                                count+=1
                                n = n*(10**count) + int(c)
                                n=n/(10**count)

                            elif flag==0:
                                self.stream.unget()
                                return Integer(n)
                            elif flag==1:
                                self.stream.unget()
                                return Float(n)
                        except EndOfStream:
                            if flag==1:
                              return Float(n)
                            else:
                                return Integer(n)
                case c if c.isalpha():
                    s = c
                    while True:
                        # print("s ",s)
                        try:
                            c = self.stream.next_char()
                            if c.isalpha():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)
                case c if c in whitespace:
                    return self.next_token()
        except EndOfStream:
            # raise EndOfTokens
            return EndOfTokens()

    def peek_token(self) -> Token:

# to look ahead in the stream to see the next token without 
# actually consuming it. 
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def advance(self):
        #  This method advances the stream to the next token.
        assert self.save is not None
        self.save = None

    def match(self, expected):
        # matches the current token with the expected token. 
        # If the current token matches the expected token,
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    def __iter__(self):
        #makes the Lexer class iterable
        # so you can use a for loop to iterate over the tokens.
        return self

    def __next__(self):
        # It calls next_token to get the next token
        return self.next_token()
        # try:
        #     return self.next_token()
        # # except EndOfTokens:
        #     raise StopIteration
     
            

    










        