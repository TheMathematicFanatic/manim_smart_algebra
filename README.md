## Introduction

This is a ManimGL / ManimCE plugin (**still under construction**) for the automated animation of algebra. It consists of a few key components: 
- SmartExpression: These objects contain a tree structure representing algebra expressions/equations, such as `3x^2`, `5+9`, and `sin(y)=14e^x`, as well as a method for producing a corresponding Tex/MathTex mobject.
- SmartAction: These objects contain methods to convert between expressions/equations, such as adding something to both sides, or substituting a variable for a value. This conversion can be static or animated.
- SmartTimeline: These objects contain an alternating sequence of expressions and actions, and methods for automatically determining these sequences, and animating them.


## SmartExpression

There are many subclasses of SmartExpression:
```
SmartExpression
├── SmartVariable
├── SmartNumber
│   ├── SmartInteger
│   └── SmartReal
├── SmartCombiner
│   ├── SmartOperation
│   │   ├── SmartAdd
│   │   ├── SmartSub
│   │   ├── SmartMul
│   │   ├── SmartDiv
│   │   └── SmartPow
│   ├── SmartRelation
│   │   ├── SmartEquation
│   │   ├── SmartLessThan
│   │   ├── ...
│   └── SmartSequence
├── SmartFunction
└── SmartNegative
```
Every SmartExpression contains an attribute called children, which is a list. Sometimes this list is empty, such as for variables and numbers. But often this list contains other SmartExpressions, such as for operations and functions.












