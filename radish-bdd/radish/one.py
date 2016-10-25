from radish import given, when, then


@given("I have the numbers {number1:g} and {number2:g}")
def have_numbers(step, number1, number2):
	step.context.number1 = number1
	step.context.number2 = number2


@when("I sum them")
def sum_numbers(step):
	step.context.result = step.context.number1 + \
	                      step.context.number2


@then("I expect the result to be {result:g}")
def expect_result(step, result):
	assert step.context.result == result
