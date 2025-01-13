from django.shortcuts import render
from django.http import JsonResponse
from .forms import ExpressionForm
import re

def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []
    tokens = re.findall(r'\d+|\+|\-|\*|\/|\(|\)', expression)

    for token in tokens:
        if token.isdigit():
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence.get(token, 0) <= precedence.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(token)
    while stack:
        postfix.append(stack.pop())
    return ' '.join(postfix)

def evaluate_postfix(expression):
    stack = []
    tokens = expression.split()
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
    return stack.pop()

def calculate(request):
    if request.method == 'POST':
        form = ExpressionForm(request.POST)
        if form.is_valid():
            infix = form.cleaned_data['expression']
            postfix = infix_to_postfix(infix)
            result = evaluate_postfix(postfix)
            return JsonResponse({'result': result})
    return render(request, 'calculator/calculate.html', {'form': ExpressionForm()})
