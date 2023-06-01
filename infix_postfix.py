"""
Construct a function that, when given a string containing an expression in infix notation, will return an identical expression in postfix notation.

The operators used will be +, -, *, /, and ^ with left-associativity of all operators but ^.

The precedence of the operators (most important to least) are : 1) parentheses, 2) exponentiation, 3) times/divide, 4) plus/minus.

The operands will be single-digit integers between 0 and 9, inclusive.

Parentheses may be included in the input, and are guaranteed to be in correct pairs.

to_postfix("2+7*5") # Should return "275*+"
to_postfix("3*3/(7+1)") # Should return "33*71+/"
to_postfix("5+(6-2)*9+3^(7-1)") # Should return "562-9*+371-^+"
to_postfix("1^2^3") # Should return "123^^"
"""

tests = {
    "2+7*5": "275*+",
    "3*3/(7+1)": "33*71+/",
    "5+(6-2)*9+3^(7-1)": "562-9*+371-^+",
    "1^2^3": "123^^",
    "(5-4-1)+9/5/2-7/1/7": "54-1-95/2/+71/7/-",
    "(8-(5-(3+3)))": "8533+--",
    "(((((((1/3)/2)*9)/(6^((8*3)/4)))/2)*(((((2*3)/((4/(((4+(1^((((((2+((((((((((7+(((4+1)-(8^1))+0))+5)/((((((5*0)-(8^(0^3)))/(8^3))-1)-3)^7))/5)-7)+9)+3)-2)-5)/(6^5)))-7)/3)*5)*0)-0)))+7)+1))-0))-5)-2)^2))/(2^0))": "13/2/9*683*4/^/2/23*4412741+81^-0++5+50*803^^-83^/1-3-7^/5/7-9+3+2-5-65^/+7-3/5*0*0-^+7+1+/0-/5-2-2^*20^/"
}

levels = {
    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
    "^": 4,
    "(": 1,
    ")": 1,
}


def to_postfix(infix):
    """Convert infix to postfix"""
    operation_buffer = []
    result = ""
    for temp in infix:
        if temp == "(":
            operation_buffer.append(temp)
        elif temp == ")":
            while operation_buffer and operation_buffer[-1] != "(":
                result += operation_buffer.pop()
            operation_buffer.pop()
        elif temp.isdigit():
            result += temp
        elif not operation_buffer or levels[temp] > levels[operation_buffer[-1]]:
            operation_buffer.append(temp)
        elif levels[temp] == levels[operation_buffer[-1]] and levels[operation_buffer[-1]] > 3:
            operation_buffer.append(temp)
        else:
            while operation_buffer and levels[operation_buffer[-1]] >= levels[temp]:
                print(operation_buffer)
                result += operation_buffer.pop()
            operation_buffer.append(temp)
    result += "".join(reversed(operation_buffer))
    return result


if __name__ == "__main__":
    for key, value in tests.items():
        result = to_postfix(key)
        print(f"Infix - {key}\nPostfix - {value}\nResult - {result}\nDone - {result == value}\n\n")



"""
Best practice 


LEFT  = lambda a,b: a>=b
RIGHT = lambda a,b: a>b
PREC  = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4, '(': 1, ')': 1}

OP_ASSOCIATION = {'+': LEFT, '-': LEFT, '*': LEFT, '/': LEFT, '^': RIGHT}


def to_postfix (infix):
    stack, output = [], []
    for c in infix:
        prec = PREC.get(c)
        
        if prec is None: output.append(c)
        elif c == '(':   stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append( stack.pop() )
            stack.pop()
        else:
            while stack and OP_ASSOCIATION[c](PREC[stack[-1]], prec):
                output.append( stack.pop() )
            stack.append(c)
            
    return ''.join(output + stack[::-1])
"""