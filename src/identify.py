def identify(node, observations):
    if node.plant is not None:
        return node.plant

    answer = ask_question(node.question)

    if answer == "yes":
        return identify(node.yes, observations)
    else:
        return identify(node.no, observations)