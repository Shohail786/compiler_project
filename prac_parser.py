from prac import KeyWord, Lexer,Identifier,Integer,Float,Bool,String,\
Operator
from typing import Optional
from typing import List
from prac_enviroment import Environment
from prac import Stream,symbolic_operators,word_operators
from dataclasses import dataclass

@dataclass
class intType:
    pass

@dataclass
class stringType:
    pass

@dataclass
class boolType:
    pass

@dataclass
class floatType:
    pass

@dataclass
class listType:
    pass


SimType=intType| stringType | boolType | floatType | listType

@dataclass
class int_literal:
    value:int
    type:SimType=intType()
    

@dataclass
class string_literal:
    value:str
    type:SimType=stringType()

@dataclass
class bool_literal:
    value:bool
    type:SimType=boolType()

@dataclass
class float_literal:
    value:float
    type:SimType=floatType()

@dataclass
class bin_op:
    operator:str
    left:'AST'
    right:'AST'
    type:Optional[SimType]=None

@dataclass
class un_op:
    op:str
    value:'AST'
    type:Optional[SimType]=None

@dataclass
class variable:
    value:str
    type:Optional[SimType]=None

@dataclass
class let:
    expr1:'AST'
    expr2:'AST'
    type:Optional[SimType]=None

@dataclass
class defFun:
    funcName:'AST'
    expr1:'AST'
    body:'AST'
    type:Optional[SimType]=None

@dataclass
class funObj:
    expr1:'AST'
    body:'AST'
    type:Optional[SimType]=None

@dataclass
class funCall:
    funcName:str
    expr2:'AST'
    type:Optional[SimType]=None


@dataclass
class if_else:
    cond:'AST'
    expr1:'AST'
    expr2:'AST'
    type:Optional[SimType]=None
    
@dataclass
class while_loop:
    cond:'AST'
    body:'AST'
    type:Optional[SimType]=None

@dataclass
class for_loop:
    expr1:'AST'
    cond:'AST'
    expr2:'AST'
    body:'AST'
    type:Optional[SimType]=None

@dataclass
class printing:
    expr:'AST'
    type:Optional[SimType]=None

@dataclass
class get:
    var:'AST'
    type:Optional[SimType]=None

@dataclass
class put:
    expr:'AST'
    type:Optional[SimType]=None

@dataclass
class lst:
    expr:List['AST']
    type:SimType=listType()

@dataclass
class isEmpty:
    expr:List['AST']
    type:SimType=boolType()

# class Slice:
#     def __init__(self,val1:str,val2:int,val3:int):
#         self.val1:str=val1
#         self.val2:int=val2
#         self.val3:int=val3

AST=int_literal | string_literal | bool_literal | float_literal | bin_op | un_op |variable| let |if_else | while_loop| \
for_loop | printing | get | put | lst | isEmpty \
# | Slice

@dataclass
class Parser:
    lexer:Lexer

    def from_lexer(lexer):
        return Parser(lexer)
    
    def parse_equal(self):
        left=self.parse_expr()
        match self.lexer.peek_token():
            case KeyWord("is"):
                self.lexer.advance()
                right=self.parse_expr()
                return bin_op("is",left,right)
        return left

    def parse_expr(self):
        match self.lexer.peek_token():
            case KeyWord("if"):
                return self.parse_if()
            case KeyWord("for"):
                return self.parse_for()
            case KeyWord("while"):
                return self.parse_while()
            case KeyWord("printing"):
                return self.parse_print()
            case KeyWord("get"):
                return self.parse_get()
            case KeyWord("put"):
                return self.parse_put()
            case KeyWord("let"):
                print("leting ")
                return self.parse_let()
            case KeyWord("defFun"):
                return self.parse_defFun()
            # case KeyWord("funCall"):
                # return self.parse_funCall()
            case KeyWord("lst"):
                return self.parse_list()
            case KeyWord("bool"):
                return self.parse_bool()
            case KeyWord("isEmpty"):
                return self.parse_isEmpty()
            # case c if c==KeyWord("slice"):
            #     return self.parse_slice()
            # case c if c==KeyWord("seq"):
            #     return self.parse_seq()
            case _:
                return self.parse_simple()


    def parse_simple(self):
        return self.parse_and()
    
    
    def parse_and(self):
        left=self.parse_or()
        match self.lexer.peek_token():
            case Operator("and"):
                self.lexer.advance()
                right=self.parse_or()
                return bin_op("and",left,right)
        return left
    
    def parse_or(self):
        left=self.parse_not()
        match self.lexer.peek_token():
            case Operator("or"):
                self.lexer.advance()
                right=self.parse_not()
                return bin_op("or",left,right)
        return left
    
    def parse_not(self):
        match self.lexer.peek_token():
            case Operator("not"):
                self.lexer.advance()
                right=self.parse_equal()
                return un_op("not",right) 
            case _:
                return self.parse_compr()

    def parse_compr(self):
        left=self.parse_add()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in '<>=!':
                    self.lexer.advance()
                    right=self.parse_equal()
                    return bin_op(op,left,right)
                case _:
                    break
        return left
    
    def parse_add(self):
        left=self.parse_mult()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in '-+':
                    self.lexer.advance()
                    right=self.parse_add()
                    # print("plus1 ",left)
                    # print("plus2 ",right)
                    return bin_op(op,left,right)
                case _:
                    break
        return left
    
    def parse_mult(self):
        left=self.parse_expo()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in '*/%':
                    self.lexer.advance()
                    right=self.parse_expo()
                    return bin_op(op,left,right)
                case _:
                    break
            
        return left
        
    
    def parse_expo(self):
        left=self.parse_funCall()
        match self.lexer.peek_token():
            case Operator('^'):
                self.lexer.advance()
                right=self.parse_funCall()
                return bin_op('^',left,right)
            case _:
                return left
        
    def parse_funCall(self):
        match self.lexer.peek_token():
            case KeyWord("funCall"):
                self.lexer.match(KeyWord("funCall"))
                funcName=self.parse_equal()
                self.lexer.match(Operator('('))
                expr2=[]
                while True:
                    match self.lexer.peek_token():
                        case Operator(')'):
                            self.lexer.advance()
                            break
                        case _:
                            while True:
                                expr2.append(self.parse_equal())
                                print("funCall_expr2 ",expr2)
                                match self.lexer.peek_token():
                                    case Operator(','):
                                        self.lexer.advance()
                                        continue
                                    case _:
                                        break
                left= funCall(funcName,expr2)
                match self.lexer.peek_token():
                    case op if ((op in word_operators) or (op in symbolic_operators)):
                        self.lexer.advance()
                        right=self.parse_equal()
                        return bin_op(op,left,right)
                    case _:
                        return left
            
            case _:
                return self.parse_atom()
                
    def parse_atom(self):
        match self.lexer.peek_token():
            case Identifier(value):
                self.lexer.advance()
                return variable(value)
            case KeyWord(value):
                self.lexer.advance()
                return variable(value)
            case Integer(value):
                self.lexer.advance()
                return int_literal(value)
            case Float(value):
                self.lexer.advance()
                return float_literal(value)
            case Bool(value):
                self.lexer.advance()
                return bool_literal(value)
            case String(value):
                self.lexer.advance()
                return string_literal(value)
    
    def parse_if(self):
        self.lexer.match(KeyWord("if"))
        cond=self.parse_equal()
        self.lexer.match(KeyWord("then"))
        expr1=self.parse_equal()
        self.lexer.match(KeyWord("else"))
        expr2=self.parse_equal()
        self.lexer.match(KeyWord("end"))
        return if_else(cond,expr1,expr2)

    def parse_for(self):
        self.lexer.match(KeyWord("for"))
        expr1=self.parse_equal()
        self.lexer.match(Operator(';'))
        cond=self.parse_equal()
        self.lexer.match(Operator(';'))
        expr2=self.parse_equal()
        self.lexer.match(Operator(':'))
        body=self.parse_equal()
        return for_loop(expr1,cond,expr2,body)
    
    def parse_while(self):
        self.lexer.match(KeyWord("while"))
        cond=self.parse_equal()
        self.lexer.match(Operator(':'))
        body=self.parse_equal()
        return while_loop(cond,body)
    
    def parse_print(self):
        self.lexer.match(KeyWord("printing"))
        expr=self.parse_equal()
        self.lexer.match(KeyWord("end"))
        return printing(expr)
    
    def parse_get(self):
        self.lexer.match(KeyWord("get"))
        var=self.parse_equal()
        return get(var)
    
    def parse_put(self):
        self.lexer.match(KeyWord("put"))
        expr=self.parse_equal()
        return put(expr)
    
    def parse_let(self):
        self.lexer.match(KeyWord("let"))
        expr1=self.parse_equal()
        self.lexer.match(KeyWord("in"))
        expr2=self.parse_equal()
        self.lexer.match(KeyWord("end"))
        return let(expr1,expr2)
    
    def parse_defFun(self):
        self.lexer.match(KeyWord("defFun"))
        funcName=self.parse_equal()
        self.lexer.match(Operator("("))
        expr1=[]
        while True:
            match self.lexer.peek_token():
                case Operator(")"):
                    self.lexer.advance()
                    break
                case _:
                    while True:
                        expr1.append(self.parse_equal())
                        match self.lexer.peek_token():
                            case Operator(','):
                                self.lexer.advance()
                                continue
                            case _:
                                break
        self.lexer.match(Operator(':'))    
        body=self.parse_equal()
        return defFun(funcName,expr1,body)

    # def parse_funCall(self):
    #     self.lexer.match(KeyWord("funCall"))
    #     funcName=self.parse_equal()
    #     self.lexer.match(Operator('('))
    #     expr2=[]
    #     while True:
    #         match self.lexer.peek_token():
    #             case Operator(')'):
    #                 self.lexer.advance()
    #                 break
    #             case _:
    #                 while True:
    #                     expr2.append(self.parse_equal())
    #                     print("funCall_expr2 ",expr2)
    #                     match self.lexer.peek_token():
    #                         case Operator(','):
    #                             self.lexer.advance()
    #                             continue
    #                         case _:
    #                             break

    #     return funCall(funcName,expr2)
    
    def parse_list(self):
        self.lexer.match(KeyWord("lst"))
        self.lexer.match(Operator("["))
        a=[]
        while True:
            match self.lexer.peek_token():
                case Operator("]"):
                    self.lexer.advance()
                    break
                case _:
                    while True:
                        a.append(self.parse_equal())
                        match self.lexer.peek_token():
                            case Operator(','):
                                self.lexer.advance()
                                continue
                            case _:
                                break
                        

        return lst(a)


    def parse_bool(self):
        self.lexer.match(KeyWord('bool'))
        a=self.parse_equal()
        return bool_literal(a)

    def parse_isEmpty(self):
        self.lexer.match(KeyWord('isEmpty'))
        self.lexer.match(KeyWord('('))
        b=self.parse_equal()
        self.lexer.match(KeyWord(')'))
        return isEmpty(b)

    # def parse_slice(self):
    #     self.lexer.match(KeyWord("slice"))
    #     s=self.lexer.prevToken
    #     self.lexer.match(Operator("("))
    #     a=self.parse_expr()
    #     self.lexer.match(Operator(","))
    #     b=self.parse_expr()
    #     self.lexer.match(Operator(")"))
    #     return Slice(s,a,b)


Value= int |float|bool|str

class TypeError(Exception):
    pass

class InvalidProgram(Exception):
    pass


def eval(program:AST,environment:Environment=None)->Value:
    
    if environment is None:
        environment=Environment()

    def eval_(program):
        return eval(program,environment)
    
    match program:
        case int_literal(value):
            return value
        case string_literal(value):
            return value
        case bool_literal(value):
            return value
        case float_literal(value):
            return value
        case variable(value):
            if environment.check(value):
                return environment.get(value)
            else:
                return value
            
        
        case bin_op('+',left,right):
            
            return eval_(left)+eval_(right)
        
        case bin_op('-',left,right):
            return eval_(left)-eval_(right)
        
        case bin_op('*',left,right):
            return eval_(left)*eval_(right)
        
        case bin_op('^',left,right):
            return eval_(left)**eval_(right)
        
        case bin_op('/',left,right):
            return eval_(left)/eval_(right)
        
        case bin_op('%',left,right):
            return eval_(left)%eval_(right)
        
        case bin_op('>',left,right):
            return eval_(left)>eval_(right)
        
        case bin_op('<',left,right):
            return eval_(left)<eval_(right)
        
        case bin_op('=',left,right):
            return eval_(left)==eval_(right)
        
        case bin_op('|',left,right):
            return eval_(left) | eval_(right)
        
        case bin_op('&',left,right):
            return eval_(left) & eval_(right)
        
        case bin_op('is',left,right):
            print("  ")
            print("left1 ",left)
            print("right1 ",right)
            if left.type==listType() and right.type==listType():
                expr_left=left.expr
                expr_right=right.expr
                res_right=[]
                for i in range(len(expr_left)):
                    expr_left[i].type=expr_right[i].type
                    res_right.append(eval_(expr_right[i]))
                environment.enter_scope()
                for i in range(len(expr_left)):
                    # res_left=eval_(expr_left[i])
                    environment.add(expr_left[i].value,res_right[i])
                print("environ ",environment.env)
                return expr_right

            else:
                c=left.value
                d=eval_(right)
                print("c ",c, " d ",d)
                print("yes ",left.type)
                left.type=right.type
                print("yes1 ",left.type)
                environment.enter_scope()
                environment.add(c,d)
                print("environ ",environment.env)
                return 
        
        case bin_op('and',left,right):
            return eval_(left) and eval_(right)
        
        case bin_op('or',left,right):
            return eval_(left) or eval_(right)
        
        case un_op('not',expr):
            return not eval_(expr)
        
        case let(expr1,expr2):
            environment.enter_scope()
            v1=eval_(expr1)
            v2=eval_(expr2)
            environment.exit_scope()
            return v2

        case defFun(funcName,expr1,body):
            environment.enter_scope()
            print("funcName ",funcName.value)
            print("funcObj ",funObj(expr1,body))
            environment.add(funcName.value,funObj(expr1,body))
            # environment.exit_scope()
            return 

        case funCall(funcName,expr2):
            print("    ")
            print("env3 ",environment.env)
            print("fun", funcName.value)
            eye=environment.get(funcName.value)
            print("   ")
            print("eye ",eye)
            sol1=lst(eye.expr1)
            print("sol1 ",sol1)
            sol2=lst(expr2)
            print("sol2 ",sol2)
            print("   ")
            
            val=eval_(bin_op('is',sol1,sol2))
            v1=eye.body
            # environment.enter_scope()
            print("   ")
            print("v2 ",val)
            v2=eval_(v1)
            environment.exit_scope()
            # print("env4 ",environment.env)
            return v2
        
        case if_else(cond,expr1,expr2):
            c=eval_(cond)
            if c==True:
                return eval_(expr1)
            else:
                return eval_(expr2)
            
        case while_loop(cond,body):
            environment.enter_scope()
            c=eval_(cond)
            while c==True:
                eval_(body)
                c=eval_(cond)
            environment.exit_scope()
            return None
        
        case for_loop(expr1,cond,expr2,body):
            environment.enter_scope()
            e1=eval_(expr1)
            c=eval_(cond)
            while c==True:
                b=eval_(body)
                eval_(expr2)
                c=eval_(cond)
            environment.exit_scope()
            return b

        case lst(elements):
            v1=[]
            for item in elements:
                v1.append(eval_(item))
            return v1
        
        case put(name,value):
            environment.update(name,value)

        case get(name):
            environment.get(name)

        case printing(expr):
            c=eval_(expr)
            print(c)
            return c

        case isEmpty(variable(value)):
            c=environment.get(value)
            assert c.type is listType()
            print(len(c)==0)


        # case Slice(s,start,end):
        #     return s[start:end]
        
    
    raise InvalidProgram()


import sys

class test_parse:
    def parse(string):
        return Parser.parse_equal(Parser.from_lexer(Lexer.from_stream(Stream.from_string(string))))
    
#     file=open(sys.argv[1],'r')
#     x=file.read()
#     result = []
#     parens = 0
#     buff = ""
#     for c in x:
#         if c == "{":
#             parens += 1
#         if parens > 0:
#             if c == "{":
#                 pass
#             elif c == "}":
#                 pass
#             else:
#                 buff += c
#         if c == "}":
#             parens -= 1
#         if not parens and buff:
#             result.append(buff)
#             buff = ""
#     for i, r in enumerate(result):
#         print(i,r)
#         y=parse(r)
#         print("y-> ",y)
#         print("ans-> ",eval(y))

# test_parse()

##debugging
y=test_parse.parse
def test_for(): 
    z=y('for i is 2 ; i<10; i is i+1 : lst[printing i*i end, i is i+2] ')
    print(z)
    print("Test ",eval(z))      

def test_list(): 
    z=y('lst[a,b] is lst[2,3]')
    print(z)
    print("Test ",eval(z)) 

def test_let():
    z=y('let a is -6.2 in lst[a*a, if a=-6 then "hello" else "hi" end, let a is -2.7 in a - 6.2 end,let a is 24.7 in a - 1000.2 end]end')
    print(z)
    print("Test ",eval(z))

def test_func(): 
    z=y('lst[defFun fun (a,b) : a+b , funCall fun (1,2)]')
    print(z)
    print("Test ",eval(z)) 

def test_fact():
    z=y('lst[defFun fun (a,b) : if a<2 then 1 else printing funCall fun(a - 1, b - 1)+ a +b +a   end end , funCall fun (4,5) ]')
    print(z)
    print("Test ",eval(z)) 

def test_sumFun():
    z=y('lst[defFun fun (a) : if a<2 then printing 1 end else funCall fun(a - 1) + funCall fun(a - 1) + funCall fun(a - 1) end, funCall fun (4) ]')
    print(z)
    print("Test ",eval(z))


test_for()
# test_list()
# test_let()
# test_func()
# test_fact()
# test_sumFun()

#Examples
#for i is 2 ; i<10; i is i+1 : lst[printing i*i end,i is i+2]
    