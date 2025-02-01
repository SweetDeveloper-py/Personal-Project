function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    return "Division by zero!";
  }
  return a / b;
}

function greet(name) {
  return "Hello, " + name + "!";
}

function power(base, exponent) {
  return Math.pow(base, exponent);
}

function squareRoot(number) {
  if (number < 0) {
    return "Cannot calculate square root of a negative number";
  }
  return Math.sqrt(number);
}

function countZerosInMatrix(matrix) {
  let count = 0;
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      if (matrix[i][j] === 0) {
        count++;
      }
    }
  }
  return count;


function sumArray(arr) {
  if (!Array.isArray(arr)) {
    return "Input is not an array";
  }
  return arr.reduce((sum, num) => sum + num, 0);
}

function advancedMathOperations(num1, num2) {
    const sum = num1 + num2;
    const difference = num1 - num2;
    const product = num1 * num2;
    const quotient = num2 === 0 ? "Division by zero!" : num1 / num2;
    const power = Math.pow(num1, num2);
    const sqrtNum1 = num1 < 0 ? "Cannot calculate square root of a negative number" : Math.sqrt(num1);
    const sqrtNum2 = num2 < 0 ? "Cannot calculate square root of a negative number" : Math.sqrt(num2);
    return {
        sum,
        difference,
        product,
        quotient,
        power,
        sqrtNum1,
        sqrtNum2,
    };
}

}

