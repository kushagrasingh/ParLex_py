# -*- coding: utf-8 -*-

import re
## lexer starts here
## specifying pattern to match in the text.
token_pattern = r"""
(?P<TK_REAL_LIT>[0-9]+\.[0-9]+)
|(?P<TK_INTLIT>[0-9]+)
|(?P<TK_INT>int)
|(?P<TK_FLOAT>float)
|(?P<TK_STRING>string)
|(?P<TK_PLUS>[+])
|(?P<TK_STAR>[*])
|(?P<newline>\n)
|(?P<TK_STRINGLIT>".*?")
|(?P<TK_ASSIGN>[=])
|(?P<slash>[/])
|(?P<TK_Semicolon>[;])
|(?P<TK_Comma>[,])
|(?P<TK_LFBK>[(])
|(?P<TK_RTBK>[)])
|(?P<TK_LFBR>[{])
|(?P<TK_RTBR>[}])
|(?P<TK_ID>[a-zA-Z_][a-zA-Z0-9_]*)


"""


token_re = re.compile(token_pattern, re.VERBOSE)

class TokenizerException(Exception): pass
line_number = 1
res = []
count = -1
id = 0
def tokenize(text):
    global id
    id = 1
    pos = 0
    ptr = 0
    global res
    global line_number
    while True:
        if pos<len(text) and text[pos]=="\n":
            line_number = line_number + 1
        if pos<len(text) and text[pos] != '\n' and text[pos] != '\t' and text[pos] != " " and text[pos] != "\r":
            m = token_re.match(text, pos)
            if not m: break
            pos = m.end()
            tokname = m.lastgroup
            tokvalue = m.group(tokname)
            res.append((id,line_number,tokname, tokvalue))
            id = id + 1

        else:
            pos = pos + 1
            if pos > len(text):
                return
    if pos <= len(text):
        raise TokenizerException('tokenizer stopped at pos %r of %r at line number %r' % (
            pos, len(text),line_number))

f = open("spl.txt")
stuff = f.read().rstrip()
tokenize(stuff)


resCount = -1

def assignScope():
    i = 0
    scope = 0

    while i < len(res):
        
        if res[i][2] == "TK_ID":
            if res[i+1][2] == "TK_LFBK":
                if res[i-1][2] != "TK_ASSIGN":
                    scope = res[i][3]
            else:
                cur = res[i]
                new_cur = cur[0:] + (scope,)
                res[i] = new_cur
                #print res[i]
        if res[i][2]== "TK_RTBR":
            if res[i+1][2] == "TK_Comma":
                scope = "main"
        i = i + 1


assignScope()

def getNextToken():
     """

     """
     global resCount
     resCount = resCount + 1
     if resCount >= id-1:
         print "Done with the parsing.No Errors reported...Thank you very much!!"
         exit()
     else:
         return res[resCount][2] , res[resCount][1]


## parser starts here
nonterminals = ["<program>","<functions>","<function>","<funsignature>","<type>","<params>","<functionbody>","<declarations>","<statements>","<statements'>","<idstatements>","<expr1>","<expr2>","<expr'>","<T>","<T'>","<F>","<F'>","<funcall>","<args>","<expr3>"]
nonTermIndex = {}
nonTerminalCount = -1
for nonterm in nonterminals:
    nonTermIndex[nonterm] = nonTerminalCount + 1
    nonTerminalCount = nonTerminalCount + 1

#print nonTermIndex["<functions>"]

terminals = ["TK_ID","TK_PLUS","TK_Semicolon", "TK_Comma", "TK_LFBK","TK_RTBK",
             "TK_LFBR","TK_RTBR","TK_ASSIGN","TK_STAR","TK_INTLIT","TK_REAL_LIT","TK_STRINGLIT","TK_INT","TK_FLOAT","TK_STRING","eps"]

termIndex = {}
terminalCount = -1
for terminal in terminals:
    termIndex[terminal] = terminalCount + 1
    terminalCount = terminalCount + 1


f = open("grammar-2.txt","r+");
grammar= {}
count  = 1
while 1:
    line = f.readline();
    line = line[:len(line)-1]
    #print line
    if not line:
        break
    #print line
    grammar[count] = line
    count = count + 1

ins = open( "parseTable.txt", "r" )
parseTable = []
for line in ins:
    row = line.split(',')
    parseTable.append(map(int,line.split(',')))



# stack implementation using lists
class Stack:
    def __init__(self):
        self.items = []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        self.items.pop()

    def isEmpty(self):
        return self.items == []
    def print_stack(self):
        print self.items
    def top_elem(self):
        return self.items[len(self.items) -1]


s = Stack()

s.push('$')
s.push("<program>")

y = getNextToken()
lnumber = y[1]
a = y[0]

while(s.top_elem() != '$'):
    x = s.top_elem()

    if(x in terminals and a in terminals and x==a):

        s.pop()
        y = getNextToken()
        lnumber = y[1]
        a = y[0]
        #print "from lexer", a
    else:
        if(x in terminals and x!=a):
            print
            print "Syntax Error!!" ,"Expected", x , "got" , a , "in line number" , lnumber
            print
            exit()
        else:
            #print x
            m = nonTermIndex[x]
            n = termIndex[a]

            if parseTable[m][n] == 0:
                #print "Error again!!"
                #print x,a
                #print m,n
                print "Error on line number", lnumber, "grammar does not support this"
                print "For this non Terminal",x ,"the set of allowable tokens are :"
                for i in range(0,terminalCount):
                    if parseTable[m][i] != 0:
                        #print m,i
                        print terminals[i]
                exit()

            else:
                #print m , n
                y =  grammar[parseTable[m][n]]
                s.pop()
                tokens = y.split()
                #print tokens
                for idx in range(len(tokens)-1, 0 , -1):
                    if(tokens[idx] != "eps"):
                        s.push(tokens[idx])
                print y



## parsing ends






