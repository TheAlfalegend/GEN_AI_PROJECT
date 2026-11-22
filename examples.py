"""Built-in sample explanations for an offline UI demo (not live AI output)."""

from explainer import ExplainerError, LEVELS, clean_topic

EXAMPLES = {
    "Gravity": (
        "Gravity pulls things toward the ground. Toss a ball up and it comes back down. Earth is pulling on you, too. That's why, after you jump, your feet land back on the floor.",
        "Gravity is the attraction between objects that have mass. Near Earth's surface, it accelerates falling objects downward at about 9.8 metres per second squared if air resistance is small. Gravity also keeps the Moon in orbit: the Moon is always falling toward Earth, but it is moving sideways fast enough to keep missing it.",
        "In Newtonian gravity, two point masses attract with force magnitude F = G m₁m₂/r², where r is their separation. The inverse-square law also applies outside a spherically symmetric mass distribution. General relativity instead describes freely falling bodies as following geodesics in curved spacetime. Newton's model is a good approximation for weak fields and speeds much lower than the speed of light.",
    ),
    "Photosynthesis": (
        "A leaf is like a tiny kitchen powered by sunlight. A plant uses that light, some water, and a gas from the air to make sugar. The sugar helps it grow. It also lets oxygen out into the air.",
        "Photosynthesis uses energy from sunlight to make sugars from water and carbon dioxide. Chlorophyll in chloroplasts absorbs light, and oxygen is released as a by-product. A sunflower uses some of the sugar for energy and can use the rest to build new leaves or store it as starch.",
        "In oxygenic photosynthesis, photosystem II oxidizes water, releasing oxygen and supplying electrons to the photosynthetic electron transport chain. Light reactions produce ATP and NADPH. The Calvin cycle consumes them to fix CO₂ and produce triose phosphates, which can be used to make sucrose or starch. The released oxygen comes from water, not from CO₂.",
    ),
    "Inflation": (
        "Imagine your pocket money stays the same, but snacks, bus rides and notebooks all get more expensive. You can buy less than before. When prices go up across lots of things, we call it inflation.",
        "Inflation is a rise in the general price level over time. A common way to measure it is to compare the cost of a basket of goods and services with its cost a year earlier. If a representative basket costs ₹1,000 one year and ₹1,050 the next, that is 5% inflation for the basket.",
        "Consumer price inflation is commonly expressed as the percentage change in a weighted price index: 100 × (CPI now / CPI before − 1). Demand pressures, supply shocks and changing expectations can all affect it. A rise in one price is not necessarily inflation, and a national CPI may differ from the price changes a particular household experiences.",
    ),
    "Recursion": (
        "Picture a stack of boxes. Each time you open one, you find a smaller one inside. You keep doing the same thing until you reach the last box. Recursion uses the same idea: solve a smaller version of the problem until you reach the easy one.",
        "Recursion happens when a function calls itself to solve a smaller case. It needs a base case that can be answered immediately. For example, factorial(4) returns 4 × factorial(3), and the calls continue until factorial(0), which returns 1. Without that stopping rule, the calls would keep going.",
        "A recursive definition specifies base cases and reduces other inputs according to a well-founded measure. In a straightforward factorial implementation, each call decrements a nonnegative integer until n = 0, establishing termination. Counting calls alone, that version uses Θ(n) calls and Θ(n) stack depth without tail-call elimination. Python does not eliminate tail calls, so an iterative solution avoids the recursion-depth limit.",
    ),
    "Black holes": (
        "Think of a place in space with a point of no return. Outside that boundary, light can still travel away. Once light crosses it, it cannot get back out. That is why we call it a black hole.",
        "A black hole is a region in space from which light cannot escape once it crosses the boundary called the event horizon. Some black holes form when massive stars collapse. We can detect them by watching nearby stars move or by observing hot material around them, even though light cannot escape from inside the horizon.",
        "In general relativity, an event horizon is the boundary of the region from which no future-directed causal signal reaches distant infinity. For an isolated, nonrotating, electrically neutral black hole, the Schwarzschild horizon has areal radius rₛ = 2GM/c². The horizon is not a material surface, and crossing it need not produce an immediate local signal for an infalling observer.",
    ),
}


def explain_demo(topic):
    normalized = clean_topic(topic).casefold()
    for name, answers in EXAMPLES.items():
        if name.casefold() == normalized:
            return dict(zip(LEVELS, answers))
    raise ExplainerError("Demo mode has five built-in topics. Choose one listed below or switch to Live AI.")
