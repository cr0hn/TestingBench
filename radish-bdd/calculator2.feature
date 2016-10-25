Feature: The calculator should be able to sum numbers
  In order to make sure the calculator
  sums numbers correctly I have the following
  test scenarios:

  Scenario: Test my calculator
    Given I have the numbers 5 and 6
    When I sum them
    Then I expect the result to be 11
