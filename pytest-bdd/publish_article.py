from pytest_bdd import steps


@step2("I'm an author user")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    assert 1 == 2


@step2("I have an article")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    pass


@step2("I go to the article page")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    pass


@step2("I press the publish button")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    pass


@step2("I should not see the error message")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    pass


@step2("the article should be published  # Note: will query the database")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    pass