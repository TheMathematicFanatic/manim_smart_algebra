## Introduction

This is a ManimGL / ManimCE plugin (**still under construction**) for the automated animation of algebra. It consists of a few key components: 
- Expression: These objects contain a tree structure representing algebra expressions/equations, such as `3x^2`, `5+9`, and `sin(y)=14e^x`, as well as a method for producing a corresponding Tex/MathTex mobject.
- Action: These objects contain methods to convert between expressions/equations, such as adding something to both sides, or substituting a variable for a value. This conversion can be static or animated.
- Timeline: These objects contain an alternating sequence of expressions and actions, and methods for automatically determining these sequences, and animating them.


## Expression

There are many subclasses of Expression:
```
Expression
├── Variable
├── Number
│   ├── Integer
│   └── Real
├── Combiner
│   ├── Operation
│   │   ├── Add
│   │   ├── Sub
│   │   ├── Mul
│   │   ├── Div
│   │   └── Pow
│   ├── Relation
│   │   ├── Equation
│   │   ├── LessThan
│   │   ├── ...
│   └── Sequence
├── Function
└── Negative
```
Every Expression contains an attribute called children, which is a list. Sometimes this list is empty, such as for variables and numbers. But often this list contains other Expressions, such as for operations and functions.












