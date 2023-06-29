ops = [["^"], ["*", "/"], ["+", "-"]]
all_ops = []
for o in ops:
    all_ops.extend(o)

class expression:
    def __init__(self, num1 : int, num2 : int, operator : str) -> None:
        self.n1 = num1
        self.n2 = num2
        self.o = operator
    def execute(self):
        #Recursive execution to eventally solve all elements of the expression
        if isinstance(self.n1, expression): self.n1 = self.n1.execute()
        if isinstance(self.n2, expression): self.n2 = self.n2.execute()

        if self.o=="+":
            return self.n1+self.n2
        elif self.o=="-":
            return self.n1-self.n2
        elif self.o=="*":
            return self.n1*self.n2
        elif self.o=="/":
            if int(self.n2)==0:
                print("Error: division by 0")
                return
            return self.n1/self.n2
        elif self.o=="^":
            return self.n1**self.n2
        else:
            print(f"Error: invalid operator '{self.o}'")
            return

#Organize nested expressions
def get_exps(str_to_solve : str, *, use_ops : int = 2, look_in_parentheses : bool = False):
    #print("Checking", str_to_solve, "for", ops[use_ops])

    def inside_parentheses(e : str, i : int):
        lp = e.find("(")
        rp = e.find(")")
        if lp<0 or rp<0: return False

        return i>lp and i<rp
    def split_outside_parentheses(e : str, o : str):
        str_list = []
        last_split = -1
        for i, char in enumerate(e):
            if char==o and not inside_parentheses(e, i):
                str_list.append(e[last_split+1:i])
                last_split = i
        str_list.append(e[last_split+1:])
        return str_list
    def find_outside_parentheses(e : str, o : str) -> int:
        for i, char in enumerate(e):
            if char==o and not inside_parentheses(e, i):
                return i
        return -1

    #No operators left to check
    if use_ops<0:
        if look_in_parentheses:
            print("Error: no operators found.")
        else:
            look_in_parentheses = True
            use_ops = 2
        
    o = ops[use_ops]

    #Which operator appears first?
    closest_index = len(str_to_solve)
    closest_operator = o[0]
    for fo in o:
        if look_in_parentheses: index = str_to_solve.find(fo)
        else: index = find_outside_parentheses(str_to_solve, fo)
        if index<closest_index and index>0:
            closest_index = index
            closest_operator = fo

    if look_in_parentheses: exp_list = str_to_solve.split(closest_operator)
    else: exp_list = split_outside_parentheses(str_to_solve, closest_operator)

    #No operators in expression, try other set
    if len(exp_list)==1:
        exp = get_exps(str_to_solve, use_ops=use_ops-1, look_in_parentheses=look_in_parentheses)


    elif len(exp_list)==2: 
        exp = expression(exp_list[0], exp_list[1], closest_operator)

    else:
        num2 = ""
        for i in range(1, len(exp_list), 2):
            num2+=exp_list[i]+closest_operator+exp_list[i+1]
        exp = expression(exp_list[0], num2, closest_operator)

    #Remove parentheses if needed
    if look_in_parentheses:
        if str(exp.n1)[0]=="(": exp.n1 = str(exp.n1)[1:]
        if str(exp.n2)[-1]==")": exp.n2 = str(exp.n2)[:-1]

    try:
        exp.n1 = float(exp.n1)
    except:
        exp.n1 = get_exps(exp.n1, look_in_parentheses=look_in_parentheses).execute()

    try:
        exp.n2 = float(exp.n2)
    except:
        exp.n2 = get_exps(exp.n2, look_in_parentheses=look_in_parentheses).execute()

    return exp

def main():
    exit = ""
    while not exit.lower()=="n":
        my_expression = input("Please type your awesome math expression here: ")

        indexes = 0
        for o in all_ops:
            indexes+=my_expression.find(o)+1

        if indexes>0:
            exp = get_exps(my_expression)

            print("Answer:", exp.execute())
        else:
            try:
                print("Answer:", float(my_expression))
            except:
                print("Invalid expression :(")

        exit = input("Do you want to continue? y or n\n>>")

main()