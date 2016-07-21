from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    # for rule in rules:
        # print rule.antecedent()
        # print rule.consequent()
    if not rules:
        return hypothesis
    return simplify(rule_match_goal_tree(rules, hypothesis))

def rule_match_goal_tree(rules, hypothesis):
    # matches = filter(lambda rule: rule_has_match(rule, hypothesis), rules)
    # return OR([antecedents_goal_tree(item, rules, match(item.consequent()[0], hypothesis)) for item in matches])
    subtrees = []
    for rule in rules:
        binding = match(rule.consequent()[0], hypothesis)
        if binding is not None:
            subtrees.append(antecedents_goal_tree(rule, rules, binding))
        else:
            subtrees.append(hypothesis)
    return OR(subtrees)

def antecedents_goal_tree(rule, rules, binding):
    ant = rule.antecedent()
    new_hypothesis = populate(ant, binding)
    if not (isinstance(ant, AND) or isinstance(ant, OR)):
        return rule_match_goal_tree(rules, new_hypothesis)
    subtrees = [rule_match_goal_tree(rules, item) for item in new_hypothesis]
    if isinstance(ant, AND):
        return AND(subtrees)
    else: 
        return OR(subtrees)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
