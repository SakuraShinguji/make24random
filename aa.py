import itertools
import random
import math

def evaluate(expression):
    #checks and returns the result.
    try:
        result = eval(expression)
        if result == float('inf') or result == float('-inf') or math.isnan(result):
            return None
        return result
    except (ZeroDivisionError, SyntaxError):
        return None


def combine_numbers(numbers):
    #exclude 0 from combinations
    numbers = [n for n in numbers if n != 0]
    #pad the list with 0 if it has fewer than four elements
    numbers += [0] * (4 - len(numbers))
    #generate all possible combinations of rolled numbers
    number_combinations = itertools.chain.from_iterable(
        itertools.combinations(numbers, r) for r in range(1, len(numbers) + 1))
    #generate all possible ways of combining the numbers by concatenation
    for number_combination in number_combinations:
        #generate all possible ways of splitting the combination into two sublists
        for i in range(1, len(number_combination)):
            for j in range(i, len(number_combination)):
                a = ''.join(map(str, number_combination[:i]))
                b = ''.join(map(str, number_combination[i:j]))
                c = ''.join(map(str, number_combination[j:]))
                yield [a, b, c]

def generate_operations(numbers):
    #generate all possible arithmetical operations for the given numbers.
    numbers += [0] * (4 - len(numbers))
    #generate all possible ways of combining the numbers with single arithmetic operator
    a, b, c, d = numbers

    # addition
    yield ['{}+{}'.format(a, b), '{}+{}'.format(c, d)]
    yield ['{}+{}'.format(a, c), '{}+{}'.format(b, d)]
    yield ['{}+{}'.format(a, d), '{}+{}'.format(b, c)]

    # subtraction
    yield ['{}-{}'.format(a, b), '{}-{}'.format(c, d)]
    yield ['{}-{}'.format(a, c), '{}-{}'.format(b, d)]
    yield ['{}-{}'.format(a, d), '{}-{}'.format(b, c)]

    # multiplication
    yield ['{}*{}'.format(a, b), '{}*{}'.format(c, d)]
    yield ['{}*{}'.format(a, c), '{}*{}'.format(b, d)]
    yield ['{}*{}'.format(a, d), '{}*{}'.format(b, c)]

    # division
    if b != 0 and d != 0:
        try:
            yield ['{}/{}'.format(a, b), '{}/{}'.format(c, d)]
        except ZeroDivisionError:
            yield None
    if c != 0 and d != 0:
        try:
            yield ['{}/{}'.format(a, c), '{}/{}'.format(b, d)]
        except ZeroDivisionError:
            yield None

    #generate expressions with 1 arithmetic operator
    for i in range(10):
        # randomly choose 1 arithmetic operator
        ops = random.choices(['+', '-', '*', '/'], k=1)
        #randomly choose 4 numbers to use in the expression
        nums = random.sample(numbers, k=4)
        expression = '{}{}{}{}{}{}{}'.format(nums[0], ops[0],nums[1], ops[0], nums[2], ops[0], numbers[-1])
        try:
            if evaluate(expression) == 24:
                yield expression
        except ZeroDivisionError:
            yield None

def find_24(numbers): # find a way for expression to make a 24
    for number_combination in combine_numbers(numbers):
        for operation in generate_operations(number_combination):
            try:
                #join the elements of the list into a single string expression
                expression = ''.join(operation)
                #try evaluating the expression
                if evaluate(expression) == 24:
                    return expression
            except ZeroDivisionError:
                # ignore division by zero errors
                pass
    return None


def main():
    #generate a list of 4 random numbers between 1 and 9
    numbers = [random.randint(0, 9) for _ in range(4)]
    #find a way to combine the numbers to get 24
    solution = find_24(numbers)
    #print the solution
    if solution is not None:
        print('{} = 24'.format(solution))
    else:
        print('No solution found for {}'.format(numbers))


if __name__ == '__main__':
    main()
