import random
import streamlit as st

# Lab Report 2: Genetic Algorithm
# Parameters specified in the lab sheet
POPULATION_SIZE = 300
CHROMOSOME_LENGTH = 80
TARGET_ONES = 50
GENERATIONS = 50
MUTATION_RATE = 0.01


def create_individual():
    """Create one chromosome containing 80 binary genes."""
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]


def fitness(individual):
    """
    Maximum fitness is 80 when the chromosome contains exactly 50 ones.
    Fitness = 80 - absolute difference between actual and target number of ones.
    """
    number_of_ones = sum(individual)
    return CHROMOSOME_LENGTH - abs(number_of_ones - TARGET_ONES)


def select_parent(population):
    """Fitness-proportionate selection (roulette-wheel style)."""
    weights = [fitness(individual) for individual in population]
    return random.choices(population, weights=weights, k=1)[0][:]


def crossover(parent1, parent2):
    """One-point crossover creates a child from two parents."""
    point = random.randint(1, CHROMOSOME_LENGTH - 1)
    child = parent1[:point] + parent2[point:]
    return child


def mutate(individual):
    """Flip each bit with a small probability."""
    child = individual[:]
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            child[i] = 1 - child[i]
    return child


def run_genetic_algorithm(seed=None):
    """Run the GA and return the best chromosome and generation history."""
    if seed is not None:
        random.seed(seed)

    population = [create_individual() for _ in range(POPULATION_SIZE)]
    history = []

    for generation in range(GENERATIONS + 1):
        best = max(population, key=fitness)
        history.append({
            "Generation": generation,
            "Best fitness": fitness(best),
            "Number of ones": sum(best)
        })

        if generation == GENERATIONS:
            break

        new_population = [best[:]]  # Elitism: preserve the best chromosome
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = mutate(crossover(parent1, parent2))
            new_population.append(child)
        population = new_population

    best = max(population, key=fitness)
    return best, history


st.set_page_config(page_title="Genetic Algorithm: 80-bit Pattern", page_icon="🧬")
st.title("Genetic Algorithm: 80-bit Pattern")
st.write(
    "This app demonstrates a genetic algorithm using the parameters in Lab Report 2: "
    "population = 300, chromosome length = 80, and 50 generations."
)

st.subheader("Fitness function")
st.latex(r"f(x) = 80 - \left|\sum_{i=1}^{80} x_i - 50\right|")
st.write(
    "Each chromosome is an 80-bit string. The fitness reaches its maximum value of 80 "
    "when the chromosome contains exactly 50 ones."
)

seed_value = st.number_input(
    "Random seed (optional; use the same value to reproduce a run)",
    min_value=0, max_value=1000000, value=42, step=1
)

if st.button("Run Genetic Algorithm", type="primary"):
    best, history = run_genetic_algorithm(seed=int(seed_value))
    ones = sum(best)
    st.success("Genetic algorithm completed.")
    st.metric("Best fitness", fitness(best))
    st.metric("Number of ones", ones)
    st.metric("Number of zeros", CHROMOSOME_LENGTH - ones)
    st.write("Best 80-bit chromosome:")
    st.code("".join(map(str, best)), language="text")

    st.subheader("Fitness progress")
    st.line_chart(
        [{"Generation": row["Generation"], "Best fitness": row["Best fitness"]}
         for row in history],
        x="Generation", y="Best fitness"
    )
    st.subheader("Generation history")
    st.dataframe(history, use_container_width=True)

st.divider()
st.subheader("How the algorithm works")

st.markdown("""
1. **Initialisation:** Generate 300 random chromosomes, each containing 80 bits.
2. **Fitness assignment:** Score each chromosome using the fitness function above.
3. **Selection:** Choose parents with higher fitness more likely to be selected.
4. **Crossover:** Combine two parents at a randomly selected point.
5. **Mutation:** Randomly flip bits at a rate of 1%.
6. **Replacement:** Preserve the best chromosome and form the next population.
7. **Termination:** Stop after 50 generations.
""")
